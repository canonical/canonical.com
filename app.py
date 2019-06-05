from canonicalwebteam.flask_base.app import FlaskBase

app = FlaskBase(__name__, "canonical.com")


@app.route("/")
def hello():
    return "Hello World!"
