class Partners:
    base_url = "https://partners.ubuntu.com/partners.json"

    partner_page_map = {
        "channel-and-reseller": "programme__name=Channel%20/%20Reseller"
        "&featured=true",
        "desktop": "programme__name=Desktop&featured=true",
        "devices-and-iot": "programme__name=Internet%20of%20Things"
        "&featured=true",
        "iot-device": "programme__name=Internet%20of%20Things"
        "&featured=true",
        "ihv-and-oem": "programme__name=IHV%20%2F%20OEM&featured=true",
        "iot": "programme__name=Internet%20of%20Things&featured=true",
        "gsi": "programme__name=Global%20System%20Integrators&featured=true",
        "public-cloud": "programme__name=Public%20Cloud&featured=true",
        "silicon": "programme__name=Silicon&featured=true",
    }

    def __init__(self, session):
        self.session = session

    def _get(self, query=""):
        if query:
            return self.session.get(f"{self.base_url}?{query}", timeout=15).json()[:10]
        else:
            return self.session.get(self.base_url, timeout=15).json()

    def get_partner_list(self):
        return self._get()
