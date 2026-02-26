# Standard library
import flask
import requests
import math
import datetime
from urllib.parse import urlparse, urlunparse, unquote
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from cachetools import TTLCache, cached
import re


def json_asset_query(file_name):
    """
    A JSON endpoint to request JSON assets from the asset manager
    """
    try:
        response = requests.get(
            url=f"https://assets.ubuntu.com/v1/{file_name}",
        )
        json = response.json()
    except requests.HTTPError:
        flask.current_app.extensions["sentry"].captureException()
        return flask.jsonify({"error": "Asset not found"}), 404

    return flask.jsonify(json)


# Case studies
def build_case_study_index(engage_docs):
    def case_study_index():
        page = flask.request.args.get("page", default=1, type=int)
        preview = flask.request.args.get("preview")
        language = flask.request.args.get("language", default=None, type=str)
        tag = flask.request.args.get("tag", default=None, type=str)
        limit = 21
        offset = (page - 1) * limit

        if tag or language:
            (
                metadata,
                count,
                active_count,
                current_total,
            ) = engage_docs.get_index(
                limit,
                offset,
                tag_value=tag,
                key="type",
                value="case study",
                second_key="language",
                second_value=language,
            )
        else:
            (
                metadata,
                count,
                active_count,
                current_total,
            ) = engage_docs.get_index(
                limit, offset, key="type", value="case study"
            )
        total_pages = math.ceil(current_total / limit)

        for case_study in metadata:
            path = case_study["path"]
            if path.startswith("/engage"):
                case_study["path"] = "https://ubuntu.com" + path

        tags = engage_docs.get_engage_pages_tags()
        # strip whitespace, remove dupes and order alphabetically
        processed_tags = sorted({tag.strip() for tag in tags if tag.strip()})

        return flask.render_template(
            "case-study/index.html",
            forum_url=engage_docs.api.base_url,
            metadata=metadata,
            page=page,
            preview=preview,
            language=language,
            posts_per_page=limit,
            total_pages=total_pages,
            current_page=page,
            tags=processed_tags,
        )

    return case_study_index


# Events
# Cache geocoding results for 24 hours (86400 seconds)
geocode_cache = TTLCache(maxsize=1000, ttl=86400)


@cached(cache=geocode_cache)
def geocode_location(location_name, timeout=3):
    """Geocode a location and cache the result"""
    try:
        geolocator = Nominatim(user_agent="canonical-events")
        result = geolocator.geocode(location_name, timeout=timeout)
        return result
    except Exception:
        return None


def build_events_index(engage_docs):
    def events_index():
        limit = 50
        search_query = flask.request.args.get("q", default=None, type=str)

        (
            metadata,
            count,
            active_count,
            current_total,
        ) = engage_docs.get_index(
            limit, offset=None, tag_value=None, key="type", value="event"
        )
        # Filter out events without topic_name
        metadata = [event for event in metadata if event.get("topic_name")]
        total_pages = math.ceil(current_total / limit)
        is_location_search = False
        clean_search = search_query.strip() if search_query else None

        # Search by location or keyword
        if clean_search:
            # Geolocation search
            try:
                search_location = geocode_location(search_query)
                if search_location:
                    is_location_search = True
                    search_coords = (
                        search_location.latitude,
                        search_location.longitude,
                    )

                    # Get coordinates of all event_locations if available
                    for event in metadata:
                        location = event.get("event_location")
                        if location:
                            try:
                                event_location = geocode_location(location)
                                if event_location:
                                    event_coords = (
                                        event_location.latitude,
                                        event_location.longitude,
                                    )
                                    distance = geodesic(
                                        search_coords, event_coords
                                    ).km
                                    event["distance"] = round(distance, 2)
                            except Exception:
                                pass

                    # Filter and sort events by distance
                    metadata = [
                        event for event in metadata if "distance" in event
                    ]
                    metadata.sort(
                        key=lambda x: x.get("distance", float("inf"))
                    )
            except Exception:
                is_location_search = False

            # Keyword search
            if not is_location_search:
                search_lower = search_query.lower()
                metadata = [
                    event
                    for event in metadata
                    if (
                        search_lower in event.get("topic_name", "").lower()
                        or search_lower
                        in event.get("event_location", "").lower()
                    )
                ]

            # Convert to DD Month YYYY format
            today = datetime.datetime.now().date()
            valid_events = []
            for events in metadata:
                date = events.get("event_date", None)
                if date:
                    try:
                        event_date = datetime.datetime.strptime(
                            date, "%d/%m/%Y"
                        ).date()
                        # Filter past events
                        if event_date >= today:
                            formatted_date = event_date.strftime("%d %B %Y")
                            events["event_date"] = formatted_date
                            valid_events.append(events)
                    except ValueError:
                        pass
            metadata = valid_events

        # Default events
        else:
            today = datetime.datetime.now().date()
            valid_events = []
            for events in metadata:
                # Prefix all engage paths with full URL
                path = events.get("path", "")
                if path.startswith("/engage"):
                    events["path"] = "https://ubuntu.com" + path

                # Convert date to DD Month YYYY format
                date = events.get("event_date", None)
                if date:
                    try:
                        event_date = datetime.datetime.strptime(
                            date, "%d/%m/%Y"
                        ).date()
                        # Filter past events
                        if event_date >= today:
                            formatted_date = event_date.strftime("%d %B %Y")
                            events["event_date"] = formatted_date
                            valid_events.append(events)
                    except ValueError:
                        pass
            metadata = valid_events

            # Sort by latest event
            metadata.sort(
                key=lambda x: datetime.datetime.strptime(
                    x.get("event_date", "31 December 1999"), "%d %B %Y"
                ),
                reverse=True,
            )

        return flask.render_template(
            "events/index.html",
            forum_url=engage_docs.api.base_url,
            metadata=metadata,
            posts_per_page=limit,
            total_pages=total_pages,
            query=search_query,
        )

    return events_index


def build_canonical_days_index(engage_docs):
    def canonical_days_index():
        limit = 50
        (
            metadata,
            count,
            active_count,
            current_total,
        ) = engage_docs.get_index(
            limit, offset=None, tag_value="roadshow", key="type", value="event"
        )
        total_pages = math.ceil(current_total / limit)

        for events in metadata:
            # Prefix all engage paths with full URL
            path = events.get("path", "")
            if path.startswith("/engage"):
                events["path"] = "https://ubuntu.com" + path

            # Convert date to DD Month YYYY format
            date = events.get("event_date")
            if date:
                formatted_date = datetime.datetime.strptime(
                    date, "%d/%m/%Y"
                ).strftime("%d %B %Y")
                events["event_date"] = formatted_date

        # Only show events with event metadata
        valid_events = []
        for events in metadata:
            if (
                events.get("event_location")
                and events.get("event_region")
                and events.get("event_date")
            ):
                # Check if event_date is in the future then append
                event_date = datetime.datetime.strptime(
                    events["event_date"], "%d %B %Y"
                ).date()
                today = datetime.datetime.now().date()
                if event_date >= today:
                    valid_events.append(events)
        metadata = valid_events

        # Sort by latest event
        metadata.sort(
            key=lambda x: datetime.datetime.strptime(
                x.get("event_date", "31 December 1999"), "%d %B %Y"
            ),
            reverse=True,
        )

        return flask.render_template(
            "events/canonical-days.html",
            forum_url=engage_docs.api.base_url,
            metadata=metadata,
            posts_per_page=limit,
            total_pages=total_pages,
        )

    return canonical_days_index


def append_utms_cookie_to_ubuntu_links(response):
    """
    Append utms cookie parameter to all ubuntu.com links in HTML responses
    """
    if response.mimetype == "text/html" and response.is_sequence:
        cookie_value = flask.request.cookies.get("utms")

        if cookie_value:
            # Decode the URI encoded cookie value
            cookie_value = unquote(cookie_value)
            data = response.get_data(as_text=True)

            # Find all href attributes pointing to ubuntu.com
            pattern = r'href=["\']([^"\']*ubuntu\.com[^"\']*)["\']'

            def add_cookie_to_url(match):
                url = match.group(1)
                # Parse URL to properly handle fragments (hash)
                parsed = urlparse(url)

                # Determine separator: use & if query params exist, otherwise ?
                separator = "&" if parsed.query else "?"

                # Build new query string with cookie value
                new_query = (
                    f"{parsed.query}{separator}{cookie_value}"
                    if parsed.query
                    else cookie_value
                )

                # Reconstruct URL with updated query string
                new_url = urlunparse(
                    (
                        parsed.scheme,
                        parsed.netloc,
                        parsed.path,
                        parsed.params,
                        new_query,
                        parsed.fragment,
                    )
                )

                return f'href="{new_url}"'

            data = re.sub(pattern, add_cookie_to_url, data)
            response.set_data(data)

    return response
