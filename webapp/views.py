import flask
import requests


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
