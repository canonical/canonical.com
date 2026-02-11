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
        # This is necessary for Google Tag Manager to function properly.
        "'unsafe-inline'",
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
        "'unsafe-hashes'",
        "'unsafe-inline'",
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
        "'unsafe-inline'",
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
}


def init_handlers(app):

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

        def get_csp_as_str(csp={}):
            csp_str = ""
            for key, values in csp.items():
                csp_value = " ".join(values)
                csp_str += f"{key} {csp_value}; "
            return csp_str.strip()

        response.headers["Content-Security-Policy"] = get_csp_as_str(CSP)

        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        response.headers["Cross-Origin-Opener-Policy"] = (
            "same-origin-allow-popups"
        )
        response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        return response
