import copy
import yaml
from flask import Flask, render_template_string, Markup

# Read secondary-navigation.yaml
with open("secondary-navigation.yaml") as navigation_file:
    secondary_navigation_data = yaml.load(navigation_file.read(), Loader=yaml.FullLoader)


# Read meganav.yaml
with open("navigation.yaml") as meganav_file:
    meganav_data = yaml.load(meganav_file.read(), Loader=yaml.FullLoader)

print(meganav_data)

def get_current_page_bubble(path):
    """
    Create the "page_bubble" dictionary containing information
    about the current page and its child pages from
    secondary-navigation.yaml (if it exists). This dictionary is
    made globally available to all templates.
    """
    current_page_bubble = {}

    page_bubbles = copy.deepcopy(secondary_navigation_data)

    for page_bubble_name, page_bubble in page_bubbles.items():
        if path.startswith(page_bubble["path"]):
            current_page_bubble = page_bubble
            for page in page_bubble["children"]:
                if page["path"] == path:
                    page["active"] = True

    return {"page_bubble": current_page_bubble}


def build_navigation(id, title):
    meganav_section = meganav_data[id]
    html_string =  render_template_string('{% include "navigation/_dropdown.html" %}', id=id, title=title, section=meganav_section)
    return Markup(html_string)