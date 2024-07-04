import copy
import yaml

# Read secondary-navigation.yaml
with open("secondary-navigation.yaml") as navigation_file:
    navigation_data = yaml.load(navigation_file.read(), Loader=yaml.FullLoader)


def get_current_page_bubble(path):
    """
    Create the "page_bubble" dictionary containing information about the current page and its child pages from secondary-navigation.yaml (if it exists). This dictionary is made globally available to all templates.
    """
    current_page_bubble = {}

    page_bubbles = copy.deepcopy(navigation_data)

    for page_bubble_name, page_bubble in page_bubbles.items():
        if path.startswith(page_bubble["path"]):
            current_page_bubble = page_bubble
            for page in page_bubble["children"]:
                if page["path"] == path:
                    page["active"] = True

    return {"page_bubble": current_page_bubble}
