"""
Tests for the per-request CSP nonce wiring in webapp/handlers.py.

These guard against the most common regressions when iterating on CSP:
- nonce missing from script-src / script-src-elem
- nonce reused across requests (would defeat the security model)
- nonce leaked into directives that shouldn't have it
"""

import re
import unittest

from webapp.app import app
from webapp.handlers import NONCED_DIRECTIVES


# Matches `'nonce-<base64url>'` as it appears in the CSP header.
NONCE_RE = re.compile(r"'nonce-([A-Za-z0-9_-]+)'")


def _directives(csp_header):
    """Parse `key val1 val2; key2 valA; ...` into a dict."""
    out = {}
    for chunk in csp_header.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        key, _, rest = chunk.partition(" ")
        out[key] = rest.split()
    return out


class CSPNonceTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_nonce_present_in_nonced_directives(self):
        resp = self.client.get("/robots.txt")
        directives = _directives(resp.headers["Content-Security-Policy"])
        for d in NONCED_DIRECTIVES:
            self.assertIn(d, directives, f"directive {d!r} missing")
            nonces = [v for v in directives[d] if v.startswith("'nonce-")]
            self.assertEqual(
                len(nonces),
                1,
                f"expected exactly one nonce token in {d}, " f"got {nonces!r}",
            )

    def test_nonce_changes_between_requests(self):
        r1 = self.client.get("/robots.txt")
        r2 = self.client.get("/robots.txt")
        n1 = NONCE_RE.search(r1.headers["Content-Security-Policy"])
        n2 = NONCE_RE.search(r2.headers["Content-Security-Policy"])
        self.assertIsNotNone(n1)
        self.assertIsNotNone(n2)
        self.assertNotEqual(
            n1.group(1),
            n2.group(1),
            "nonce must be regenerated per request",
        )

    def test_nonce_not_leaked_into_other_directives(self):
        resp = self.client.get("/robots.txt")
        directives = _directives(resp.headers["Content-Security-Policy"])
        for d, values in directives.items():
            if d in NONCED_DIRECTIVES:
                continue
            self.assertFalse(
                any(v.startswith("'nonce-") for v in values),
                f"unexpected nonce in directive {d}: {values!r}",
            )

    def test_unsafe_inline_removed_from_script_src_elem(self):
        """
        Every inline <script> in our templates now carries a nonce, so
        script-src-elem should NOT permit 'unsafe-inline' anymore — the
        nonce alone is what authorizes inline script execution.
        """
        resp = self.client.get("/robots.txt")
        directives = _directives(resp.headers["Content-Security-Policy"])
        self.assertNotIn(
            "'unsafe-inline'",
            directives.get("script-src-elem", []),
            "script-src-elem must not include 'unsafe-inline' — nonces "
            "are the only inline-script authorization now",
        )

    def test_script_src_has_no_unsafe_inline_or_unsafe_hashes(self):
        """
        Inline event-handler attributes (onclick=, onsubmit=, etc.)
        have all been refactored to delegated listeners in
        static/js/csp-handlers.js. script-src should therefore NOT
        permit 'unsafe-inline' or 'unsafe-hashes' — re-introducing
        either is a regression.
        """
        resp = self.client.get("/robots.txt")
        directives = _directives(resp.headers["Content-Security-Policy"])
        script_src = directives.get("script-src", [])
        self.assertNotIn(
            "'unsafe-inline'",
            script_src,
            "script-src must not include 'unsafe-inline'",
        )
        self.assertNotIn(
            "'unsafe-hashes'",
            script_src,
            "script-src must not include 'unsafe-hashes'",
        )

    def test_script_src_has_no_unsafe_eval(self):
        """
        Our Lottie JSON files don't use AE expressions and the three
        lottie-web imports point at the `lottie_light` entry-point,
        which omits the `new Function()` evaluator. Re-introducing
        'unsafe-eval' is a regression — either a dependency now needs
        it (re-evaluate the alternative), or a Lottie file gained an
        expression (re-export from After Effects without expressions).
        """
        resp = self.client.get("/robots.txt")
        directives = _directives(resp.headers["Content-Security-Policy"])
        self.assertNotIn(
            "'unsafe-eval'",
            directives.get("script-src", []),
            "script-src must not include 'unsafe-eval'",
        )

    def test_style_src_has_no_unsafe_inline(self):
        """
        Every inline <style> block now carries a per-request nonce
        (see NONCED_DIRECTIVES), and every inline style="" attribute
        has been migrated to a class defined in
        static/sass/_inline-styles-migration.scss. style-src must
        therefore NOT permit 'unsafe-inline' anymore.
        """
        resp = self.client.get("/robots.txt")
        directives = _directives(resp.headers["Content-Security-Policy"])
        self.assertNotIn(
            "'unsafe-inline'",
            directives.get("style-src", []),
            "style-src must not include 'unsafe-inline'",
        )

    def test_style_src_has_nonce(self):
        """style-src must include the per-request nonce so the 12
        inline <style> blocks (e.g. partners/request-login) are
        permitted."""
        resp = self.client.get("/robots.txt")
        directives = _directives(resp.headers["Content-Security-Policy"])
        style_src = directives.get("style-src", [])
        nonces = [v for v in style_src if v.startswith("'nonce-")]
        self.assertEqual(
            len(nonces),
            1,
            f"expected exactly one nonce token in style-src, got {nonces!r}",
        )


if __name__ == "__main__":
    unittest.main()
