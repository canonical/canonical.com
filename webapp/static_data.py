class FeaturedProduct:
    def __init__(
        self,
        link,
        image,
        alt,
        content,
        footer,
    ):
        self.link = link
        self.image = image
        self.alt = alt
        self.content = content
        self.footer = footer


base_url = "https://assets.ubuntu.com"
homepage_featured_products = [
    FeaturedProduct(
        link="https://ubuntu.com",
        image=f"{base_url}/v1/25be0ace-products-ubuntu-wht-aubergine.svg",
        alt="Ubuntu",
        content=(
            "The new standard secure enterprise Linux for servers, desktops,"
            " cloud, developers and things"
        ),
        footer="ubuntu.com",
    ),
    FeaturedProduct(
        link="https://ubuntu.com/security",
        image=f"{base_url}/v1/c47655d3-products-security-wht-aubergine4.svg",
        alt="Security and support",
        content=(
            "Extended Security Maintenance, Kernel Livepatch, FIPS, enterprise"
            " support and certification"
        ),
        footer="ubuntu.com/security",
    ),
    FeaturedProduct(
        link="https://landscape.canonical.com",
        image=f"{base_url}/v1/7f8d7403-products-landscape-wht.svg",
        alt="Landscape",
        content=(
            "Updates, package management, repositories, security, and"
            " regulatory compliance for Ubuntu"
        ),
        footer="landscape.canonical.com",
    ),
    FeaturedProduct(
        link="https://maas.io",
        image=f"{base_url}/v1/3c26ff14-products-maas-wht-aubergine2.svg",
        alt="MAAS",
        content=(
            "Dynamic server provisioning and IPAM gives you on-demand bare"
            " metal, a physical cloud"
        ),
        footer="maas.io",
    ),
    FeaturedProduct(
        link="https://ubuntu.com/lxd",
        image=f"{base_url}/v1/a737970a-products-lxd-wht-aubergine4.svg",
        alt="LXD",
        content=(
            "The pure-container hypervisor. Run legacy apps in secure"
            " containers for speed and density"
        ),
        footer="ubuntu.com/lxd",
    ),
    FeaturedProduct(
        link="https://canonical.com/juju",
        image=f"{base_url}/v1/1dee5076-products-juju-wht-aubergine2.svg",
        alt="Juju",
        content=(
            "Model-driven cloud-native apps on public and private"
            " infrastructure and CAAS"
        ),
        footer="canonical.com/juju",
    ),
    FeaturedProduct(
        link="https://ubuntu.com/openstack",
        image=f"{base_url}/v1/0694ab7a-openstack_lrg.svg",
        alt="OpenStack",
        content=(
            "Upgrades, maintenance, support, and fully managed options for"
            " long-term low-cost infrastructure"
        ),
        footer="ubuntu.com/openstack",
    ),
    FeaturedProduct(
        link="https://ubuntu.com/kubernetes",
        image=f"{base_url}/v1/32ef9123-kubernetes_lrg.svg",
        alt="Kubernetes",
        content=(
            "App portability for K8s on VMware, Amazon, Azure, Google, Oracle,"
            " IBM and bare metal"
        ),
        footer="ubuntu.com/kubernetes",
    ),
    FeaturedProduct(
        link="https://snapcraft.io",
        image=f"{base_url}/v1/11776603-snapcraft_lrg.svg",
        alt="Snapcraft",
        content=(
            "The app store with secure packages and ultra-reliable updates for"
            " multiple Linux distros"
        ),
        footer="snapcraft.io",
    ),
]
