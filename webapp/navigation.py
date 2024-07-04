import copy
import yaml

# Read secondary-navigation.yaml
with open("secondary-navigation.yaml") as navigation_file:
    nav_sections = yaml.load(navigation_file.read(), Loader=yaml.FullLoader)


def get_secondary_navigation(path):
    """
    Set "nav_sections" and "breadcrumbs" dictionaries
    as global template variables
    """
    page_group = {}

    sections = copy.deepcopy(nav_sections)

    for nav_section_name, nav_section in sections.items():
        if path.startswith(nav_section["path"]):
            page_group = nav_section
            for page in nav_section["children"]:
                if page["path"] == path:
                    page["active"] = True

    return {"page_group": page_group}
