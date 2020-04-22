class Partners:
    base_url = "https://partners.ubuntu.com/partners.json"

    partner_page_map = {"ihv-and-oem": "programme__name=IHV"}

    def __init__(self, session):
        self.session = session

    def _get(self, query=""):
        return self.session.get(f"{self.base_url}?{query}").json()[:10]

    def get_partner_groups(self):
        return {
            "Cloud": self._get("technology__name=Cloud/server&featured=true"),
            "Server": self._get("technology__name=Cloud/server&featured=true"),
            "Desktop": self._get("programme__name=Desktop&featured=true"),
            "Silicon": self._get("programme__name=Desktop&featured=true"),
            "OpenStack": self._get("programme__name=Desktop&featured=true"),
            "Apps & snaps": self._get("programme__name=Desktop&featured=true"),
            "Snapcraft": self._get(
                "programme__name=Internet%20of%20Things&featured=true"
            ),
            "Resellers": self._get("programme__name=Desktop&featured=true"),
            "Devices": self._get("programme__name=Desktop&featured=true"),
            "Charms": self._get(
                "programme__name=Charm%20Partner%20Programme&featured=true"
            ),
            "Hosting": self._get(
                "service__offered=Hosting%20provider&featured=true"
            ),
            "System Integrators": self._get(
                "service__offered=System%20integrator/consultant&featured=true"
            ),
            "Training": self._get("programme__name=Desktop&featured=true"),
            "Kubernetes": self._get("programme__name=Desktop&featured=true"),
            "PAAS": self._get("programme__name=Desktop&featured=true"),
            "Serverless": self._get("programme__name=Desktop&featured=true"),
        }

    def get_partner_list(self):
        return self._get()
