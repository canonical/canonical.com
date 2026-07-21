DEPARTMENT_LIST = {
    "engineering": {
        "name": "Engineering",
        "slug": "engineering",
        "icon": "84886ac6-Engineering.svg",
    },
    "support-engineering": {
        "name": "Support Engineering",
        "slug": "support-engineering",
        "icon": "df08c7f2-Support Engineering.svg",
    },
    "marketing": {
        "name": "Marketing",
        "slug": "marketing",
        "icon": "27b93be4-Marketing.svg",
    },
    "web-and-design": {
        "name": "Web & Design",
        "slug": "web-and-design",
        "icon": "b200e162-design.svg",
    },
    "project-management": {
        "name": "Project Management",
        "slug": "project-management",
        "icon": "0f64ee5c-Project Management.svg",
    },
    "commercial-operations": {
        "name": "Commercial Operations",
        "slug": "commercial-operations",
        "icon": "1f84f8c7-Operations.svg",
    },
    "product": {
        "name": "Product",
        "slug": "product",
        "icon": "d5341dfa-Product.svg",
    },
    "sales": {"name": "Sales", "slug": "sales", "icon": "2dc1ceb1-Sales.svg"},
    "finance": {
        "name": "Finance",
        "slug": "finance",
        "icon": "8b2110ea-finance.svg",
    },
    "people": {
        "name": "People",
        "slug": "people",
        "icon": "01ff5233-Human Resources.svg",
    },
    "administration": {
        "name": "Administration",
        "slug": "administration",
        "icon": "a42f5ab5-Admin.svg",
    },
    "legal": {"name": "Legal", "slug": "legal", "icon": "4e54c36b-Legal.svg"},
    "alliances-and-channels": {
        "name": "Alliances & Channels",
        "slug": "alliances-and-channels",
        "icon": "46a968ed-no%20bg%20hand%20&%20fingers-new.svg",
    },
}


def _group_by_department(vacancies):
    """
    Return a dictionary of departments by slug,
    where each department will have a new
    "vacancies" property of all the vacancies in
    that department
    """
    departments_by_slug = {
        key: {**department, "vacancies": []}
        for key, department in DEPARTMENT_LIST.items()
    }

    for vacancy in vacancies:
        for department in vacancy.departments:
            slug = department.slug
            if slug in departments_by_slug:
                departments_by_slug[slug]["vacancies"].append(vacancy)

    return departments_by_slug


def get_sorted_departments(greenhouse):
    departments = _group_by_department(greenhouse.get_vacancies())

    sort_order = [
        "engineering",
        "support-engineering",
        "marketing",
        "web-and-design",
        "project-management",
        "commercial-operations",
        "product",
        "sales",
        "finance",
        "people",
        "administration",
        "legal",
        "alliances-and-channels",
    ]

    sorted = {slug: departments[slug] for slug in sort_order}
    remaining_slugs = set(departments.keys()).difference(sort_order)
    remaining = {slug: departments[slug] for slug in remaining_slugs}
    sorted_departments = {**sorted, **remaining}

    return sorted_departments


def get_all_departments(greenhouse) -> tuple:
    """
    Refactor for careers search section
    """
    all_departments = _group_by_department(greenhouse.get_vacancies())

    departments_overview = []
    for department in all_departments.values():
        count = len(department["vacancies"])
        name = department["name"]
        slug = department["slug"]
        icon = department["icon"]

        departments_overview.append(
            {
                "name": name,
                "count": count,
                "slug": slug,
                "icon": icon,
            }
        )

    return all_departments, departments_overview
