import logging

import requests
import secrets
import sentry_sdk

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
        "www.tfaforms.com",
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


def init_handlers(app):

    @app.route(CSP_REPORT_PATH, methods=["POST"])
    def csp_report():
        """
        Browsers POST violations here for both the enforced CSP and the
        Content-Security-Policy-Report-Only header (report bodies include
        a "disposition" field of "enforce" or "report" to tell them apart).
        """
        report = flask.request.get_json(silent=True, force=True) or {}
        violation = report.get("csp-report", {})
        logger.warning("CSP violation report: %s", report)

        if violation:
            with sentry_sdk.new_scope() as scope:
                scope.set_extra("csp-report", violation)
                scope.fingerprint = [
                    "csp-violation",
                    violation.get("violated-directive", "unknown"),
                    violation.get("blocked-uri", "unknown"),
                ]
                sentry_sdk.capture_message(
                    "CSP violation ({}): {} blocked {}".format(
                        violation.get("disposition", "enforce"),
                        violation.get("violated-directive", "unknown"),
                        violation.get("blocked-uri", "unknown"),
                    ),
                    level="warning",
                )
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
