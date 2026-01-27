# Standard library
import flask
import requests
import math
import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from cachetools import TTLCache, cached


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
                date = events.get("event_date")
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
                path = events["path"]
                if path.startswith("/engage"):
                    events["path"] = "https://ubuntu.com" + path

                # Convert date to DD Month YYYY format
                date = events.get("event_date")
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
                )
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
            limit,
            offset=None,
            tag_value=None,
            key="type",
            value="event",
            second_key="tag",
            second_value="roadshow"
        )
        total_pages = math.ceil(current_total / limit)

        for events in metadata:
            # Prefix all engage paths with full URL
            path = events["path"]
            if path.startswith("/engage"):
                events["path"] = "https://ubuntu.com" + path

            # Convert date to DD Month YYYY format
            date = events.get("event_date")
            if date:
                formatted_date = datetime.datetime.strptime(
                    date, "%d/%m/%Y"
                ).strftime("%d %B %Y")
                events["event_date"] = formatted_date

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
