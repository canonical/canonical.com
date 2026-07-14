import unittest
import talisker.requests
from requests import Session
from pathlib import Path

from webapp.marketo import MarketoAPI
from canonicalwebteam.flask_base.env import get_flask_env

# Fields that are allowed in a Marketo form payload.
# Add to this set when intentionally introducing a new hidden field.
ALLOWED_HIDDEN_FIELDS = frozenset(
    {
        "firstname",
        "lastname",
        "email",
        "company",
        "title",
        "country",
        "state",
        "phone",
        "comments_from_lead__c",
        "facebook_click_id__c",
        "gclid__c",
        "utm_content",
        "utm_term",
        "utm_medium",
        "utm_source",
        "utm_campaign",
        "formid",
        "returnurl",
        "thankyoumessage",
        "productcontext",
        "preferredlanguage",
        "consent_to_processing__c",
        "canonicalupdatesoptin",
        # JS-injected fields added at runtime by forms.js
        "user_id",
        "consent_info",
        "utms",
    }
)


def get_marketo_template_files():
    """
    Return template files that contain Marketo form submissions.
    """
    result = []
    for ext in ("*.html", "*.jinja"):
        for f in Path("templates").rglob(ext):
            if "templates/tests" in str(f):
                continue
            if "marketo/submit" in f.read_text():
                result.append(f)
    return result


class MarketoFormTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SET_FIELDS = ALLOWED_HIDDEN_FIELDS

        marketo_session = Session()
        talisker.requests.configure(marketo_session)
        cls.marketo_api = MarketoAPI(
            get_flask_env("MARKETO_API_URL"),
            get_flask_env("MARKETO_API_CLIENT"),
            get_flask_env("MARKETO_API_SECRET"),
            marketo_session,
        )
        cls.marketo_api._authenticate()

    def _process_form_fields(self, check_form, field_id, fields):
        """
        Helper function to process form fields for checking.
        """
        field_id = field_id.lower()

        if check_form == "marketo":
            if field_id == "utm_content":
                field_id = "utmcontent"

            marketo_field_ids = [f.get("id", "").lower() for f in fields]
            return field_id, marketo_field_ids

        elif check_form == "form-data":
            if field_id not in self.SET_FIELDS:
                form_field_ids = [f.get("id", "").lower() for f in fields]
                return field_id, form_field_ids
            # Skip checking fields that are in SET_FIELDS
            else:
                return None, None
        else:
            self.fail(f"Unknown check_form: {check_form}")

    def _get_marketo_fields(self, form_id):
        """
        Helper function to get Marketo fields for a form ID.
        """
        marketo_response = self.marketo_api.get_form_fields(form_id)
        self.assertEqual(marketo_response.status_code, 200)
        self.assertIsNotNone(
            marketo_response,
            f"Marketo response should not be None for form ID {form_id}",
        )
        return marketo_response.json().get("result", [])

    def _get_form_gen_files(self):
        """
        Helper function to get form generator files.
        """
        return [
            f
            for f in Path("templates").rglob("form-data.json")
            if "templates/tests" not in str(f)
        ]
