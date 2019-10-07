from canonicalwebteam.http import CachedSession


api_session = CachedSession(
    fallback_cache_duration=300, file_cache_directory=".webcache", timeout=6
)

base_url = "https://partners.ubuntu.com/partners.json"


def get(endpoint):
    return api_session.get(f"{base_url}?{endpoint}")


def get_cloud():
    return get("technology__name=Cloud/server&featured=true")


def get_server():
    return get("technology__name=Cloud/server&featured=true")


def get_desktop():
    return get("programme__name=Desktop&featured=true")


def get_silicon():
    return get("programme__name=Desktop&featured=true")


def get_openstack():
    return get("programme__name=Desktop&featured=true")


def get_apps():
    return get("programme__name=Desktop&featured=true")


def get_snapcraft():
    return get("programme__name=Internet%20of%20Things&featured=true")


def get_resellers():
    return get("programme__name=Desktop&featured=true")


def get_devices():
    return get("programme__name=Desktop&featured=true")


def get_charms():
    return get("programme__name=Charm%20Partner%20Programme&featured=true")


def get_hosting():
    return get("service__offered=Hosting%20provider&featured=true")


def get_system_integrators():
    return get("service__offered=System%20integrator/consultant&featured=true")


def get_training():
    return get("programme__name=Desktop&featured=true")


def get_kubernetes():
    return get("programme__name=Desktop&featured=true")


def get_paas():
    return get("programme__name=Desktop&featured=true")


def get_serverless():
    return get("programme__name=Desktop&featured=true")


def first_ten(req):
    new_req = req[:10]
    return new_req


def get_partner_groups():
    partner_groups = {
        "Cloud": first_ten(get_cloud().json()),
        "Server": first_ten(get_server().json()),
        "Desktop": first_ten(get_desktop().json()),
        "Silicon": first_ten(get_silicon().json()),
        "OpenStack": first_ten(get_openstack().json()),
        "Apps & snaps": first_ten(get_apps().json()),
        "Snapcraft": first_ten(get_snapcraft().json()),
        "Resellers": first_ten(get_resellers().json()),
        "Devices": first_ten(get_devices().json()),
        "Charms": first_ten(get_charms().json()),
        "Hosting": first_ten(get_hosting().json()),
        "System Integrators": first_ten(get_system_integrators().json()),
        "Training": first_ten(get_training().json()),
        "Kubernetes": first_ten(get_kubernetes().json()),
        "PAAS": first_ten(get_paas().json()),
        "Serverless": first_ten(get_serverless().json()),
    }
    return partner_groups


def get_partner_list():
    return api_session.get(base_url).json()
