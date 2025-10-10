import unittest
import json

from webapp.app import app
from tests.helpers import MarketoFormTestCase


class TestFormGenerator(MarketoFormTestCase):
    def setUp(self):
        """

        Set up Flask app for testing

        """
        super().setUp()
        app.testing = True
        self.client = app.test_client()
        self.form_gen_files = self._get_form_gen_files()

    def test_marketo_api(self):
        """
        Test Marketo API authentication
        """
        self.assertIsNotNone(self.marketo_api.token)

    def test_form_gen_files(self):
        """
        Test form generator files are discovered
        """
        self.assertGreater(len(self.form_gen_files), 0)

    def test_form_gen_files_with_marketo(self):
        """
        Test form generator files against Marketo fields.
        """
        for form_path in self.form_gen_files:
            with open(form_path, "r") as f:
                forms = json.load(f).get("form", {})
                self.assertIsNotNone(
                    forms,
                    f"Form data could not be loaded from {form_path}",
                )

            # form-data.json may have multiple forms
            for form_data in forms.values():
                form_id = form_data.get("formData").get("formId")

                # Check that marketo form exists
                marketo_fields = self._get_marketo_fields(form_id)

                # Check that form fields match Marketo fields
                form_fields = form_data.get("fieldsets", [])
                for field in form_fields:
                    field_id = field.get("id")

                    # Check that individual fields are all expected
                    # in the Marketo fields
                    if field.get("noCommentsFromLead"):
                        if field_id != "about-you":
                            self.assertIsNotNone(
                                field_id,
                                f"Field ID is None for marketo "
                                f"fields in {form_path}",
                            )

                            clean_field_id, marketo_field_ids = (
                                self._process_form_fields(
                                    "marketo", field_id, marketo_fields
                                )
                            )
                            print("clean_field_id", clean_field_id)
                            print("marketo_field_ids", marketo_field_ids)
                            print("form_path", form_path)
                            print("form_id", form_id)
                            print("field_id", field_id)
                            self.assertIn(
                                clean_field_id,
                                marketo_field_ids,
                                f"Field {clean_field_id} is not present in "
                                f"Marketo fields "
                                f"for form {form_path} ID {form_id}",
                            )
                        else:
                            # Check enrichment fields separately
                            contact_fields = field.get("fields", [])
                            for contact_field in contact_fields:
                                clean_field_id, marketo_field_ids = (
                                    self._process_form_fields(
                                        "marketo",
                                        contact_field.get("id"),
                                        marketo_fields,
                                    )
                                )
                                self.assertIn(
                                    clean_field_id,
                                    marketo_field_ids,
                                    f"Field {clean_field_id} is not present "
                                    f"in Marketo fields "
                                    f"for form {form_path} ID {form_id}",
                                )

                # Check that Marketo required fields are included in form
                for marketo_field in marketo_fields:
                    id = marketo_field.get("id")
                    required = marketo_field.get("required")
                    if required:
                        self.assertIsNotNone(
                            field_id,
                            f"Field ID is None for form-data.json "
                            f"fields in {form_path}",
                        )

                        clean_marketo_id, form_field_ids = (
                            self._process_form_fields(
                                "form-data", id, form_fields
                            )
                        )

                        if clean_marketo_id and form_field_ids:
                            self.assertIn(
                                clean_marketo_id,
                                form_field_ids,
                                f"Field {clean_marketo_id} is not present in "
                                f"form-data fields"
                                f" for form {form_path}",
                            )


if __name__ == "__main__":
    unittest.main()
