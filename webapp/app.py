import flask

from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder


app = FlaskBase(
    __name__,
    "canonical.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)

# List of partners
partners = [
    {
        "name": "Cloud",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/d424d305-Tesco_Logo.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/ee5d503f-rabobank-4.svg",
        ],
    },
    {
        "name": "Desktop",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Silicon",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "OpenStack",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Apps",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Snapcraft",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Resellers",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Devices",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Charms",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Hosting",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "System Integrators",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Training",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Kubernetes",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "PAAS",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
    {
        "name": "Serverless",
        "url": "#",
        "images": [
            "https://assets.ubuntu.com/v1/e765a8ed-fujitsu.svg",
            "https://assets.ubuntu.com/v1/73135672-ntt-logo.svg",
            "https://assets.ubuntu.com/v1/f9832168-AstraZeneca.png?w=144",
            "https://assets.ubuntu.com/v1/e71bd588-logo-samsung.svg",
            "https://assets.ubuntu.com/v1/2244ec17-logo-intel.png",
        ],
    },
]


def index():
    return flask.render_template("index.html", partners=partners)


template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=index)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)


@app.context_processor
def inject_today_date():
    return {"current_year": datetime.date.today().year}
