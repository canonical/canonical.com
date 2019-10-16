from canonicalwebteam.http import CachedSession

from random import sample

api_session = CachedSession(
    fallback_cache_duration=300, file_cache_directory=".webcache", timeout=6
)

base_url = "https://partners.ubuntu.com/partners.json"


def get(endpoint):
    return api_session.get(f"{base_url}?{endpoint}")


def get_cloud():
    return get("programme__name=Certified%20Public%20Cloud&featured=true")


def get_silicon():
    return get("service_offered__name=Hardware%20manufacturer&featured=true")


def get_server():
    return get("service_offered__name=Hardware%20manufacturer&featured=true")


def get_devices():
    return get("programme__name=Internet%20of%20Things&featured=true")


def get_system_integrators():
    return get("programme__name=Channel&featured=true")


def get_charms():
    return get("programme__name=Charm%20Partner%20Programme&featured=true")


def get_apps_and_snaps():
    return get(
        "service_offered__name=Software/content%20publisher&featured=true"
    )


def random_ten(req):
    if len(req) >= 10:
        new_req = sample(req, 10)
    else:
        new_req = sample(req, len(req))
    print(len(new_req))
    return new_req


def get_partner_groups():
    partner_groups = {
        "Cloud": random_ten(get_cloud().json()),
        "Silicon": random_ten(get_silicon().json()),
        "Server": random_ten(get_server().json()),
        "Devices": random_ten(get_devices().json()),
        "System Integrators": random_ten(get_system_integrators().json()),
        "Charms": random_ten(get_charms().json()),
        "Apps and snaps": random_ten(get_apps_and_snaps().json()),
    }
    return partner_groups


def get_partner_list():
    return api_session.get(base_url).json()
