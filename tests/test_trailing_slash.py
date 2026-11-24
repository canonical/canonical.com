import os
import re
import tempfile
import unittest

import flask
import yaml
from canonicalwebteam.flask_base.context import clear_trailing_slash
from canonicalwebteam.yaml_responses.flask_helpers import prepare_redirects

from webapp.app import app
from webapp.trailing_slash import init_trailing_slash_redirects


class TestTrailingSlashRedirects(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_trailing_slash_is_a_permanent_redirect(self):
        # maas.io/, microk8s.io/, juju.is/, anbox-cloud.io/ and dqlite.io/
        # are sent to these URLs with a trailing slash
        for product in ["maas", "microk8s", "juju", "anbox-cloud", "dqlite"]:
            response = self.client.get(f"/{product}/")

            self.assertEqual(response.status_code, 301)
            self.assertEqual(
                response.headers["Location"], f"http://localhost/{product}"
            )

    def test_slashless_legacy_roots_are_not_redirected(self):
        for product in ["maas", "microk8s", "juju", "anbox-cloud", "dqlite"]:
            response = self.client.get(f"/{product}")

            self.assertEqual(response.status_code, 200)

    def test_query_string_is_kept(self):
        response = self.client.get("/maas/?foo=bar")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response.headers["Location"], "http://localhost/maas?foo=bar"
        )


class TestRedirectTargets(unittest.TestCase):
    # Served by infrastructure outside this app, where the slashed URL is the
    # real one; the slash-less form redirects to it.
    SLASHED_TARGETS = {"/mir/docs/tutorials/"}

    def test_internal_targets_have_no_trailing_slash(self):
        """
        A target ending in a slash costs a hop, as the app then redirects it
        to the slash-less URL. Targets on other hosts are not ours to change.
        """
        root = os.path.join(os.path.dirname(__file__), "..")
        offenders = []

        for filename in ["redirects.yaml", "permanent-redirects.yaml"]:
            path = os.path.join(root, filename)

            if not os.path.isfile(path):
                continue

            with open(path) as file:
                rules = yaml.safe_load(file) or {}

            for source, target in rules.items():
                target_path = re.split(r"[?#]", str(target))[0]

                if (
                    not re.match(r"(https?:)?//", target_path)
                    and target_path != "/"
                    and target_path.endswith("/")
                    and target_path not in self.SLASHED_TARGETS
                ):
                    offenders.append(f"{source}: {target}")

        self.assertEqual(offenders, [])


class TestIntentionalAddSlashRedirects(unittest.TestCase):
    def setUp(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)

        with open(os.path.join(root.name, "redirects.yaml"), "w") as file:
            file.write("server/docs: /server/docs/\n")

        os.mkdir(os.path.join(root.name, "webapp"))
        test_app = flask.Flask(
            __name__, root_path=os.path.join(root.name, "webapp")
        )
        test_app.before_request(clear_trailing_slash)
        test_app.before_request(
            prepare_redirects(os.path.join(root.name, "redirects.yaml"))
        )
        test_app.add_url_rule("/server/docs/", "docs", lambda: "docs")
        test_app.add_url_rule("/other", "other", lambda: "other")
        init_trailing_slash_redirects(test_app)

        self.client = test_app.test_client()

    def test_redirect_that_adds_a_slash_is_not_undone(self):
        response = self.client.get("/server/docs")
        self.assertEqual(response.headers["Location"], "/server/docs/")

        response = self.client.get("/server/docs/")
        self.assertEqual(response.status_code, 200)

    def test_other_trailing_slashes_are_still_removed(self):
        response = self.client.get("/other/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response.headers["Location"], "http://localhost/other"
        )
