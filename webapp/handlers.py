import secrets

import flask
from canonicalwebteam.flask_base.env import get_flask_env

# Directives we inject a per-request nonce into. Keeping this explicit
# (rather than nonce-ing every directive) makes it obvious which surfaces
# the nonce is meant to cover and avoids leaking the nonce into directives
# where it has no effect (img-src, font-src, etc.).
#
# Note: nonces only apply to *elements* (<script>, <style>). They do not
# cover `style=""` attributes; those must be removed (we did) or allowed
# via 'unsafe-inline'/'unsafe-hashes'.
NONCED_DIRECTIVES = ("script-src", "script-src-elem", "style-src")

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
        # Inline <script> blocks (e.g. the GTM bootstrap in base_index.html)
        # are authorized via a per-request nonce injected by
        # `get_csp_nonce()` in this module, not by 'unsafe-inline'.
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
        # No 'unsafe-*' tokens here:
        # - 'unsafe-inline'/'unsafe-hashes' removed: every inline <script>
        #   carries a per-request nonce (see get_csp_nonce() above) and
        #   every inline event handler has been refactored to a delegated
        #   listener in static/js/csp-handlers.js.
        # - 'unsafe-eval' removed: our Lottie JSON contains no AE
        #   expressions, and the three call sites import the
        #   `lottie-web/build/player/lottie_light` entry point which
        #   omits the expression evaluator.
    ],
    "connect-src": [
        "'self'",
        "www.google.com",
        "ubuntu.com",
        "analytics.google.com",
        "www.googletagmanager.com",
        "o4510662863749120.ingest.de.sentry.io",
        "www.google-analytics.com",
        "*.crazyegg.com",
        "*.g.doubleclick.net",
        "js.zi-scripts.com",
        "*.google-analytics.com",
        "px.ads.linkedin.com",
        "ws.zoominfo.com",
        "youtube.com",
        "google.com",
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
        # No 'unsafe-inline':
        # - <style> blocks (12 across the templates) each carry the
        #   per-request nonce, which is appended to this directive at
        #   request time (see NONCED_DIRECTIVES).
        # - style="" attributes have all been migrated to classes in
        #   static/sass/_inline-styles-migration.scss (see
        #   scripts/migrate_inline_styles.py).
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
}


def get_csp_nonce():
    """
    Return the CSP nonce for the current request, generating one on
    first access and caching it on `flask.g`.

    Generated lazily (rather than via `before_request`) so that the
    nonce is still available when an earlier `before_request` hook
    short-circuits the request — e.g. flask_base's `prepare_redirects`
    or static handlers that bypass our before_request.

    `secrets.token_urlsafe(16)` yields ~22 chars of base64 entropy,
    comfortably above the 128-bit minimum recommended for CSP nonces.
    """
    nonce = getattr(flask.g, "csp_nonce", None)
    if nonce is None:
        nonce = secrets.token_urlsafe(16)
        flask.g.csp_nonce = nonce
    return nonce


def init_handlers(app):

    @app.context_processor
    def inject_csp_nonce():
        # Exposed as `csp_nonce` in every template so inline scripts can
        # mark themselves trusted via `nonce="{{ csp_nonce }}"`.
        return {"csp_nonce": get_csp_nonce()}

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

        def get_csp_as_str(csp, nonce):
            # Build the header per request so we can mix in the nonce
            # without mutating the module-level CSP dict (which would race
            # across concurrent requests).
            csp_str = ""
            for key, values in csp.items():
                if nonce and key in NONCED_DIRECTIVES:
                    values = list(values) + [f"'nonce-{nonce}'"]
                csp_value = " ".join(values)
                csp_str += f"{key} {csp_value}; "
            return csp_str.strip()

        response.headers["Content-Security-Policy"] = get_csp_as_str(
            CSP, get_csp_nonce()
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
