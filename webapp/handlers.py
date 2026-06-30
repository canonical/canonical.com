import logging
import time

import requests
import secrets
import sentry_sdk
from urllib.parse import urlparse

import flask
from canonicalwebteam.flask_base.env import get_flask_env

logger = logging.getLogger(__name__)

# Used if the live fetch from Google fails at startup. Covers the regions
# we've historically seen in CSP reports.
_GOOGLE_DOMAINS_FALLBACK = [
    "www.google.com",
    # Europe
    "www.google.at",
    "www.google.be",
    "www.google.ch",
    "www.google.co.uk",
    "www.google.cz",
    "www.google.de",
    "www.google.dk",
    "www.google.es",
    "www.google.fi",
    "www.google.fr",
    "www.google.gr",
    "www.google.hu",
    "www.google.ie",
    "www.google.it",
    "www.google.nl",
    "www.google.no",
    "www.google.pl",
    "www.google.pt",
    "www.google.ro",
    "www.google.se",
    # Americas
    "www.google.ca",
    "www.google.cl",
    "www.google.co",
    "www.google.com.ar",
    "www.google.com.br",
    "www.google.com.mx",
    "www.google.com.pe",
    # Asia & Pacific
    "www.google.co.id",
    "www.google.co.in",
    "www.google.co.jp",
    "www.google.co.kr",
    "www.google.co.nz",
    "www.google.co.th",
    "www.google.com.au",
    "www.google.com.hk",
    "www.google.com.my",
    "www.google.com.ph",
    "www.google.com.sg",
    "www.google.com.tw",
    "www.google.com.vn",
]


def _fetch_google_supported_domains():
    """
    Fetch Google's published list of regional search domains so GTM can
    reach the user's local google.<tld>. Falls back to a hardcoded list
    if the request fails so CSP remains valid.
    """
    try:
        response = requests.get(
            "https://www.google.com/supported_domains", timeout=5
        )
        response.raise_for_status()
        domains = [
            "www" + line.strip()
            for line in response.text.splitlines()
            if line.strip().startswith(".google.")
        ]
        if domains:
            return domains
        logger.warning("Google supported_domains response was empty")
    except requests.RequestException as exc:
        logger.warning("Failed to fetch Google supported_domains: %s", exc)
    return _GOOGLE_DOMAINS_FALLBACK


GOOGLE_DOMAINS = _fetch_google_supported_domains()

# Same-origin endpoint registered below in init_handlers(); browsers send
# CSP violation reports here regardless of the page's own connect-src.
CSP_REPORT_PATH = "/csp-report"

CSP = {
    "default-src": ["'self'"],
    "img-src": [
        "data: blob:",
        # This is needed to allow images from
        # https://www.google.*/ads/ga-audiences to load.
        "*",
    ],
    "script-src-elem": [
        "'self'",
        "'strict-dynamic'",
        "assets.ubuntu.com",
        "www.google-analytics.com",
        "www.googletagmanager.com",
        "www.youtube.com",
        "asciinema.org",
        "player.vimeo.com",
        "script.crazyegg.com",
        "www.googleadservices.com",
        "js.zi-scripts.com",
        "*.g.doubleclick.net",
        "www.google.com",
        "www.gstatic.com",
        "www.brighttalk.com",
        "snap.licdn.com",
        "connect.facebook.net",
        "maps.googleapis.com",
        "www.redditstatic.com",
        "munchkin.marketo.net",
        "w.usabilla.com",
        "api.usabilla.com",
        "*.googlesyndication.com",
        "cdn.jsdelivr.net",
        "https://esm.sh",
        "https://cdn.jsdelivr.net",
        "buttons.github.io",
        "cdn.livechatinc.com",
        "api.livechatinc.com",
        "secure.livechatinc.com",
        "www.tfaforms.com",
    ],
    "font-src": [
        "'self'",
        "assets.ubuntu.com",
        "fonts.google.com",
        "cdn.livechatinc.com",
        "secure.livechatinc.com",
    ],
    "script-src": [
        "'self'",
        "blob:",
        "'unsafe-eval'",
    ],
    "connect-src": [
        "'self'",
        "ubuntu.com",
        "analytics.google.com",
        "www.googletagmanager.com",
        "o4510662863749120.ingest.de.sentry.io",
        "www.google-analytics.com",
        "*.crazyegg.com",
        "*.g.doubleclick.net",
        "www.googleadservices.com",
        "js.zi-scripts.com",
        "*.google-analytics.com",
        "px.ads.linkedin.com",
        "ws.zoominfo.com",
        "youtube.com",
        "google.com",
        # Regional google.<tld> domains used by GTM, sourced live from
        # https://www.google.com/supported_domains at app startup.
        *GOOGLE_DOMAINS,
        "fonts.google.com",
        "maps.googleapis.com",
        "pixel-config.reddit.com",
        "www.redditstatic.com",
        "conversions-config.reddit.com",
        "https://esm.sh",
        "https://lottie.host",
        "https://cdn.jsdelivr.net",
        "*.analytics.google.com",
        "www.facebook.com",
        "*.googlesyndication.com",
        "*.mktoresp.com",
        "assets.ubuntu.com",
        "api.github.com",
        "raw.githubusercontent.com",
        "api.livechatinc.com",
        "cdn.livechatinc.com",
        "secure.livechatinc.com",
        "web.facebook.com",
        "www.tfaforms.com",
        # Fallback WASM CDN for homepage Lottie animations, see
        # static/js/homepage/animations.js
        "unpkg.com",
    ],
    "frame-src": [
        "'self'",
        "*.doubleclick.net",
        "www.youtube.com/",
        "asciinema.org",
        "player.vimeo.com",
        "www.googletagmanager.com",
        "www.google.com",
        "www.brighttalk.com",
        "cdn.livechatinc.com",
        "secure.livechatinc.com",
        "cdn.livechat-static.com",
    ],
    "style-src": [
        "'self'",
        "cdn.jsdelivr.net",
        "www.tfaforms.com",
    ],
    "media-src": [
        "'self'",
        "res.cloudinary.com",
        "assets.ubuntu.com",
    ],
    "child-src": [
        "'self'",
        "blob:",
        "youtube.com",
        "google.com",
        "fonts.google.com",
        "api.livechatinc.com",
        "cdn.livechatinc.com",
        "secure.livechatinc.com",
    ],
    "form-action": [
        "'self'",
        "https://pages.ubuntu.com",
        "https://ubuntu.com",
        "https://www.tfaforms.com",
    ],
    "object-src": ["'none'"],
    "base-uri": ["'self'"],
    "worker-src": ["'self'"],
    "report-uri": [CSP_REPORT_PATH],
}

# These sources seem stale but since marketing tags can be
# injected at runtime via GTM, outside this repo, we can't
# be fully sure they're unused from static analysis alone.
# Put them in a report-only CSP so we can watch Sentry for violations before
# removing them from the enforced CSP above.

_CSP_REPORT_ONLY_REMOVALS = {
    "script-src-elem": [
        "script.crazyegg.com",
        "js.zi-scripts.com",
        "snap.licdn.com",
        "buttons.github.io",
    ],
    "connect-src": [
        "*.crazyegg.com",
        "js.zi-scripts.com",
        "px.ads.linkedin.com",
        "ws.zoominfo.com",
        "www.tfaforms.com",
    ],
    "style-src": ["www.tfaforms.com"],
    "script-src": ["'unsafe-eval'"],
}


def _build_csp_report_only(csp):
    stricter = {directive: list(values) for directive, values in csp.items()}
    for directive, stale_values in _CSP_REPORT_ONLY_REMOVALS.items():
        stricter[directive] = [
            value for value in stricter[directive] if value not in stale_values
        ]
    return stricter


CSP_REPORT_ONLY = _build_csp_report_only(CSP)

NONCED_DIRECTIVES = ("script-src", "script-src-elem", "style-src")


# ---------------------------------------------------------------------------
# CSP violation report throttling
# ---------------------------------------------------------------------------
# CSP violation reports arrive on nearly every page load, so forwarding them
# verbatim would flood Sentry and burn the event budget. Two layers protect us:
#   1. An ignore-list of hosts already triaged as pure noise; their reports
#      are dropped entirely (no log, no Sentry event).
#   2. Per-signature de-duplication: for everything else we forward at most one
#      event per (disposition, directive, host) per dedup window, keeping
#      visibility of each distinct violation without the volume.

# Hosts already triaged as noise; their reports are dropped outright.
CSP_REPORT_IGNORED_HOSTS = frozenset(
    {
        "w.usabilla.com",
        "api.usabilla.com",
        "script.crazyegg.com",
    }
)

# Forward at most one Sentry event per unique violation signature per window.
CSP_REPORT_DEDUP_WINDOW = 3600  # seconds (1 hour)


def _csp_blocked_host(blocked_uri):
    """
    Reduce a blocked-uri to a stable host so query strings / cache-busters
    (e.g. ".../ecdf1756070a.js?lv=1") don't explode the cardinality. Non-URL
    tokens such as "inline", "eval" or "data" are returned as-is.
    """
    if not blocked_uri:
        return ""
    host = urlparse(blocked_uri).hostname
    if host:
        return host
    # Tokens like "inline"/"eval", or bare "data:" - keep the scheme/keyword.
    return blocked_uri.split(":", 1)[0]


def _is_ignored_csp_host(host):
    """True if `host` is, or is a subdomain of, an ignored host."""
    return any(
        host == ignored or host.endswith("." + ignored)
        for ignored in CSP_REPORT_IGNORED_HOSTS
    )


class _CSPReportThrottler:
    """
    In-memory, per-worker de-duplication for CSP violation reports.

    Remembers the signature of each violation it has forwarded and suppresses
    repeats within `window` seconds. The cache is bounded to `max_entries`;
    when full it evicts stale entries first, then the oldest half as a last
    resort so the expensive sort runs rarely.
    """

    def __init__(self, window, max_entries=1000):
        self._window = window
        self._max_entries = max_entries
        # signature tuple -> monotonic timestamp it was last forwarded.
        self._seen = {}

    def should_report(self, signature):
        """Return True only the first time a signature is seen per window."""
        now = time.monotonic()
        last_sent = self._seen.get(signature)
        if last_sent is not None and now - last_sent < self._window:
            return False
        if len(self._seen) >= self._max_entries:
            self._evict(now)
        self._seen[signature] = now
        return True

    def _evict(self, now):
        """Drop entries past the window, then the oldest half if still full."""
        for signature, last_sent in list(self._seen.items()):
            if now - last_sent >= self._window:
                del self._seen[signature]
        if len(self._seen) >= self._max_entries:
            oldest = sorted(self._seen, key=self._seen.get)
            for signature in oldest[: self._max_entries // 2]:
                del self._seen[signature]

    def clear(self):
        """Forget all remembered signatures (used by tests)."""
        self._seen.clear()


_csp_throttler = _CSPReportThrottler(CSP_REPORT_DEDUP_WINDOW)


def _forward_csp_violation(violation, host, directive, disposition):
    """
    Log a concise line and send a trimmed payload to Sentry. The raw report
    is dropped on the floor - notably its huge "original-policy" field, which
    is pure noise in the trace.
    """
    blocked_uri = violation.get("blocked-uri", "")
    document_uri = violation.get("document-uri", "")
    target = host or blocked_uri or "unknown"

    logger.warning(
        "CSP [%s] %s blocked %s (%s)",
        disposition,
        directive,
        target,
        document_uri or "unknown",
    )

    with sentry_sdk.new_scope() as scope:
        scope.set_extra(
            "csp-report",
            {
                "disposition": disposition,
                "violated-directive": directive,
                "blocked-uri": blocked_uri,
                "document-uri": document_uri,
                "line-number": violation.get("line-number"),
                "column-number": violation.get("column-number"),
            },
        )
        scope.fingerprint = ["csp-violation", directive, host or "unknown"]
        sentry_sdk.capture_message(
            f"CSP violation ({disposition}): {directive} blocked {target}",
            level="warning",
        )


def init_handlers(app):

    @app.route(CSP_REPORT_PATH, methods=["POST"])
    def csp_report():
        """
        Browsers POST violations here for both the enforced CSP and the
        Content-Security-Policy-Report-Only header (report bodies include
        a "disposition" field of "enforce" or "report" to tell them apart).

        These reports arrive on nearly every request, so we drop known-noisy
        hosts outright and de-duplicate everything else before forwarding to
        Sentry. We also forward a trimmed payload - the raw report includes
        the full (huge) "original-policy" which is noise in the trace.
        """
        report = flask.request.get_json(silent=True, force=True) or {}
        violation = report.get("csp-report")
        if not violation:
            return "", 204

        host = _csp_blocked_host(violation.get("blocked-uri", ""))
        directive = violation.get("violated-directive", "unknown")
        disposition = violation.get("disposition", "enforce")
        signature = (disposition, directive, host)

        # Drop known-noisy hosts, then de-duplicate everything else.
        if _is_ignored_csp_host(host):
            return "", 204
        if not _csp_throttler.should_report(signature):
            return "", 204

        _forward_csp_violation(violation, host, directive, disposition)
        return "", 204

    @app.before_request
    def set_csp_nonce():
        flask.g.csp_nonce = secrets.token_urlsafe(16)

    @app.context_processor
    def inject_csp_nonce():
        return {"csp_nonce": getattr(flask.g, "csp_nonce", "")}

    @app.after_request
    def add_headers(response):
        """
        Generic rules for headers to add to all requests
        - Content-Security-Policy: Restrict resources (e.g., JavaScript, CSS,
        Images) and URLs
        - Referrer-Policy: Limit referrer data for security while preserving
        full referrer for same-origin requests
        - Cross-Origin-Embedder-Policy: allows embedding cross-origin
        resources
        - Cross-Origin-Opener-Policy: enable the page to open pop-ups while
        maintaining same-origin policy
        - Cross-Origin-Resource-Policy: allowing cross-origin requests to
        access the resource
        - X-Permitted-Cross-Domain-Policies: disallows cross-domain access to
        resources.
        """

        def get_csp_as_str(csp={}, nonce=None):
            csp_str = ""
            for key, values in csp.items():
                directive_values = list(values)
                if nonce and key in NONCED_DIRECTIVES:
                    directive_values.append(f"'nonce-{nonce}'")
                csp_value = " ".join(directive_values)
                csp_str += f"{key} {csp_value}; "
            return csp_str.strip()

        nonce = getattr(flask.g, "csp_nonce", None)
        response.headers["Content-Security-Policy"] = get_csp_as_str(
            CSP, nonce=nonce
        )
        response.headers["Content-Security-Policy-Report-Only"] = (
            get_csp_as_str(CSP_REPORT_ONLY, nonce=nonce)
        )

        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        response.headers["Cross-Origin-Opener-Policy"] = (
            "same-origin-allow-popups"
        )
        response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        if get_flask_env("FLASK_ENV", "production") != "production":
            response.headers["X-Robots-Tag"] = "none"
        return response
