import flask


def navigation_products():

    return flask.render_template("/partial/navigation-products.html")

def leadership_team():

    return flask.render_template("leadership-team.html")


def customer_references():

    return flask.render_template("customer-references.html")


def opensource():

    return flask.render_template("opensource.html")


def press():

    return flask.render_template("press.html")
