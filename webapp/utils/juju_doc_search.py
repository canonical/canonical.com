from urllib.parse import urlparse
import requests
import concurrent.futures
from sklearn.feature_extraction.text import TfidfVectorizer

# RTD API Endpoints
RTD_HOSTED_API = "https://readthedocs.com/api/v3/search/"
RTD_PROJECTS_HOSTED = [
    "canonical-juju",
    "canonical-terraform-provider-juju",
    "canonical-charmcraft",
    "canonical-jaas-documentation",
    "canonical-jubilant",
]

RTD_PROJECTS_IO = {
    "ops": "https://ops.readthedocs.io/_/api/v3/search/",
}

# Domain information mapping, title for chips, weight for relevance
DOMAIN_INFO = {
    "documentation.ubuntu.com/juju": {
        "title": "Juju",
        "weight": 0.6,
        "search_url": (
            "https://documentation.ubuntu.com/juju/3.6/search/?q={query}"
        ),
    },
    "documentation.ubuntu.com/jubilant": {
        "title": "Jubilant",
        "weight": 0.5,
        "search_url": (
            "https://documentation.ubuntu.com/jubilant/search/?q={query}"
        ),
    },
    "documentation.ubuntu.com/terraform-provider-juju": {
        "title": "Terraform Juju",
        "weight": 0.5,
        "search_url": (
            "https://documentation.ubuntu.com/"
            "terraform-provider-juju/latest/search/?q={query}"
        ),
    },
    "documentation.ubuntu.com/jaas": {
        "title": "JAAS",
        "weight": 0.3,
        "search_url": (
            "https://documentation.ubuntu.com/jaas/v3/search/?q={query}"
        ),
    },
    "documentation.ubuntu.com/charmcraft": {
        "title": "Charmcraft",
        "weight": 0.2,
        "search_url": (
            "https://documentation.ubuntu.com/charmcraft/stable/search/"
            "?q={query}"
        ),
    },
    "ops.readthedocs.io": {
        "title": "Ops",
        "weight": 0.1,
        "search_url": (
            "https://ops.readthedocs.io/en/stable/search.html?q={query}"
        ),
    },
}


def extract_full_domain(result):
    parsed_url = urlparse(result.get("domain", ""))
    hostname = parsed_url.hostname or ""

    # Skip path prefix for non-Canonical hosted RTD projects
    if hostname == "ops.readthedocs.io":
        return hostname

    # For Canonical docs (e.g. documentation.ubuntu.com/juju)
    path_prefix = (
        result.get("path", "").split("/")[1]
        if "/" in result.get("path", "")
        else ""
    )
    return f"{hostname}/{path_prefix}"


def fetch_search_results(api_url, query, projects=None):
    """
    Fetch search results from ReadTheDocs API.
    - If `projects` is provided, constructs a query filtering
      by multiple projects.
    - Otherwise, assumes the API requires an explicit
      `project:project-name` prefix.
    """
    if projects:
        # Query multiple projects in one request
        project_filters = " ".join(
            [f"project:{project}" for project in projects]
        )
        full_query = f"{project_filters} {query}"
    else:
        full_query = f"project:{query}"

    params = {"q": full_query, "page_size": 50}

    try:
        response = requests.get(api_url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results from {api_url}: {e}")

    return []


def search_all_docs(query):
    """
    Fetch documentation search results:
    - One request for all hosted projects (`readthedocs.com`).
    - Two separate requests for `pythonlibjuju` and `ops`.
    """
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Hosted docs (single request)
        future_hosted = executor.submit(
            fetch_search_results, RTD_HOSTED_API, query, RTD_PROJECTS_HOSTED
        )

        # Separate requests for ops
        future_io = {
            project: executor.submit(
                fetch_search_results, url, f"{project} {query}"
            )
            for project, url in RTD_PROJECTS_IO.items()
        }

        results.extend(future_hosted.result())
        for project, future in future_io.items():
            try:
                results.extend(future.result())
            except Exception as e:
                print(f"Error processing search results for {project}: {e}")

    return results


def calculate_relevance(result, query):
    """
        * This calculation is very sensitive
        and is a V1 for the Juju ecosystem docs.
        It will need modified in the future.

    Calculate relevance using TF-IDF with scaled domain weighting.
    """
    title = result.get("title", "").lower()
    content = " ".join(
        block["content"] for block in result.get("blocks", [])
    ).lower()

    full_domain = extract_full_domain(result)

    search_results = [query, title, content]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(search_results)

    query_vector = tfidf_matrix[0]
    title_vector = tfidf_matrix[1]
    content_vector = tfidf_matrix[2]

    title_score = (query_vector * title_vector.T).sum() * 1.5
    content_score = (query_vector * content_vector.T).sum()

    # Boost "How to..." articles
    how_to_boost = 0.5 if title.startswith("how to") else 0

    # Normalize domain weight
    domain_weight = DOMAIN_INFO.get(full_domain, {}).get("weight", 1)

    # Convert weight into a multiplier
    domain_multiplier = 1 + (domain_weight / 5)

    # Final score with domain multiplier
    return (title_score + content_score + how_to_boost) * domain_multiplier


def process_and_sort_results(results, query, max_length=200):
    """
    Merge, truncate, and sort search results based on relevance,
    returning all results for frontend pagination.
    """
    processed_results = []

    for result in results:
        full_domain = extract_full_domain(result)
        domain_details = DOMAIN_INFO.get(full_domain, {})
        project_name = domain_details.get("title", full_domain)
        search_url = domain_details.get(
            "search_url", f"https://{full_domain}/search/?q={query}"
        ).format(query=query)

        full_content = " ".join(
            block["content"] for block in result.get("blocks", [])
        )
        short_content = (
            full_content[:max_length] + "..."
            if len(full_content) > max_length
            else full_content
        )

        relevance_score = calculate_relevance(result, query)
        parsed_url = urlparse(result.get("domain", ""))
        url = (
            f"{parsed_url.scheme}://{parsed_url.hostname}"
            f"{result.get('path', '')}"
        )

        processed_results.append(
            {
                "title": result.get("title", "Untitled"),
                "url": url,
                "domain": full_domain,
                "project_name": project_name,
                "short_content": short_content,
                "relevance_score": relevance_score,
                "search_url": search_url,
            }
        )

    return sorted(
        processed_results, key=lambda x: x["relevance_score"], reverse=True
    )
