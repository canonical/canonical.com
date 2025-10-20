import copy
import yaml

from flask import render_template_string, Markup

# Read secondary-navigation.yaml
with open("secondary-navigation.yaml") as navigation_file:
    secondary_navigation_data = yaml.load(
        navigation_file.read(), Loader=yaml.FullLoader
    )


# Read meganav.yaml
with open("navigation.yaml") as meganav_file:
    meganav_data = yaml.load(meganav_file.read(), Loader=yaml.FullLoader)


def get_current_page_bubble(path):
    """
    Create the "page_bubble" dictionary containing information
    about the current page and its child pages from
    secondary-navigation.yaml (if it exists). This dictionary is
    made globally available to all templates.
    """
    current_page_bubble = {}

    # Remove '/docs' from the path if it exists
    normalized_path = path.replace("/docs", "")

    page_bubbles = copy.deepcopy(secondary_navigation_data)

    # Priority order for selecting the bubble:
    # 1) Exact match on a bubble's own path
    # 2) Exact match on any child path
    # 3) fallback match on a bubble's path
    exact_bubble_match = None
    exact_child_match = None
    fallback_match = None

    for page_bubble_name, page_bubble in page_bubbles.items():
        bubble_path = page_bubble.get("path", "")

        # 1) Exact match on the bubble path
        # (e.g. /solutions/ai should match the 'ai' bubble)
        if bubble_path == normalized_path:
            exact_bubble_match = page_bubble
            break

        # 2) Exact match on any child path
        # (for cases like /data/warehouse, /data/streaming
        #    that should select the 'data-and-ai' bubble)
        for child in page_bubble.get("children", []) or []:
            child_path = child.get("path")

            if child_path == normalized_path:
                exact_child_match = page_bubble
                # We found a suitable child match;
                # no need to check more children for this bubble
                break

        # 3) Longest prefix match as a fallback
        # (keeps general behavior like /data -> 'data' bubble)
        if normalized_path.startswith(bubble_path):
            fallback_match = page_bubble

    chosen_bubble = exact_bubble_match or exact_child_match or fallback_match

    if chosen_bubble:
        current_page_bubble = chosen_bubble
        parent = chosen_bubble.get("parent", None)

        if parent:
            current_page_bubble["parent_title"] = parent[0]["title"]
            current_page_bubble["parent_path"] = parent[1]["path"]

        children = current_page_bubble.get("children", [])
        if children:
            for page in children:
                if (
                    page.get("path") == normalized_path
                    or page.get("path") == path
                ):
                    page["active"] = True

    return {"page_bubble": current_page_bubble}


def build_navigation(id, title):
    """
    Takes an id and title and returns the assosiate dropdown data.
    This function is made globally avaiable and then called from the
    jinja template 'dropdown.html'
    """
    meganav_section = meganav_data[id]
    html_string = render_template_string(
        '{% include "navigation/dropdown.html" %}',
        id=id,
        title=title,
        section=meganav_section,
    )
    return Markup(html_string)


def split_list(array, parts):
    """
    Split an array into multiple sub-arrays of approximately equal size.

    Parameters:
    array (list): The array to be split.
    parts (int): The number of parts to split the array into.

    Returns:
    list: A list of sub-arrays.
    """
    if parts <= 0:
        raise ValueError("Number of parts must be a positive integer")

    k, m = divmod(len(array), parts)
    return [
        array[i * k + min(i, m): (i + 1) * k + min(i + 1, m)]
        for i in range(parts)
    ]
