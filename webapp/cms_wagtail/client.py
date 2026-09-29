"""Read pages from the Wagtail content API."""

import re

from webapp.cms_wagtail.sections import prepare_sections

PAGE_ID = re.compile(r"/pages/(\d+)/")


class WagtailContent:
    def __init__(self, session, api_url, site_host="", timeout=10):
        self.session = session
        self.api_url = api_url.rstrip("/")
        # Wagtail picks the site from the Host header. Override it when the
        # CMS is reached by an address that is not one of its Site hostnames.
        self.headers = {"Host": site_host} if site_host else {}
        self.timeout = timeout

    def page_by_path(self, path):
        normalized = path.strip("/")
        html_path = f"/{normalized}/" if normalized else "/"
        response = self.session.get(
            f"{self.api_url}/api/v2/pages/find/",
            params={"html_path": html_path},
            headers=self.headers,
            timeout=self.timeout,
            # The Location is built from the Host header, which may not
            # resolve from here. Take the id and ask api_url instead.
            allow_redirects=False,
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        match = PAGE_ID.search(response.headers.get("Location", ""))
        if not match:
            return None
        return self._get(f"/api/v2/pages/{match.group(1)}/")

    def preview(self, content_type, token):
        return self._get(
            "/api/v2/page_preview/1/",
            params={"content_type": content_type, "token": token},
        )

    def _get(self, path, params=None):
        response = self.session.get(
            f"{self.api_url}{path}",
            params=params,
            headers=self.headers,
            timeout=self.timeout,
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return _document(response.json())


def _document(data):
    meta = data.get("meta") or {}
    return {
        "id": data.get("id"),
        "type": meta.get("type", ""),
        # Plain str, never Markup: whoever passes these into a non-autoescaping
        # .jinja macro is responsible for escaping them there.
        "title": meta.get("seo_title") or data.get("title", ""),
        "heading": data.get("title", ""),
        "meta": {
            "meta_description": data.get("meta_description")
            or meta.get("search_description", ""),
            "meta_copydoc": data.get("meta_copydoc", ""),
            "body_class": data.get("body_class", ""),
        },
        "fields": data,
        "sections": prepare_sections(data.get("body")),
    }
