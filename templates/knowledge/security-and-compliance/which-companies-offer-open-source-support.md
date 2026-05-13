---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Security and compliance"
  tag: "Support"
  title: "Which companies offer open source support?"
  breadcrumb: "Which companies offer open source support?"
  description: "Learn the difference between security maintenance and support. Explore which companies offer open source support, and how they do it."
  copydoc: ""
  hero_title: "Which companies offer open source support?"
  cta:
    description: "Get enterprise support across your open source stack with Canonical."
    buttons:
      - text: "Explore support plans"
        url: "https://ubuntu.com/pricing/pro"
        type: "button"
        variant: "positive"
      - text: "Compare package coverage"
        url: "https://ubuntu.com/support"
        type: "button"
      - text: "Read how Canonical support brings real value to businesses ›"
        url: "https://canonical.com/case-study/sbi-bits"
        type: "link"
  blog:
    title: "Latest from our blog"
    id: 1374
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}

Many open source software companies, such as Canonical, Red Hat, and SUSE, offer open source software support for enterprises. In Canonical’s case, these services are offered through Ubuntu Pro, a subscription available on top of Ubuntu.  Learn the differences between security maintenance and enterprise support, and get deeper insight into the enterprise-grade open source software support landscape in this article.

## Security maintenance vs enterprise support: what's the difference?

Security maintenance proactively patches known vulnerabilities. Enterprise support reactively troubleshoots and fixes unexpected production issues like bugs, misconfigurations, and regressions.

### What is security maintenance?

Security maintenance involves the proactive and reactive steps organizations take to protect their systems, applications, and data from cyber threats. It includes regularly identifying and fixing vulnerabilities, applying security patches, enforcing strong access controls, and conducting security assessments to detect and address weaknesses.

### What is enterprise support?

Support focuses on resolving unexpected technical issues that arise in production environments. Unlike security maintenance, which aims to prevent risks, enterprise support provides expert troubleshooting, break-fix and bug-fix services, and incident mitigation to restore stability, performance, and security as quickly as possible after incidents. Enterprise support includes technical guidance, knowledge base resources, and collaboration with upstream providers when needed.

### How do security maintenance and enterprise support intersect?

Security maintenance and enterprise support serve complementary roles. Security maintenance is proactive, focusing on vulnerability management and timely patching to reduce the risk of breaches. Enterprise support is reactive, addressing real-world incidents such as outages, bugs, and unexpected production issues that still occur despite preventive measures. Production systems – especially environments operating under compliance requirements – need both: proactive protection to stay secure and compliant, and reactive resilience to quickly resolve incidents and maintain business continuity. Together, security maintenance and enterprise support ensure organizations are protected from threats and prepared to handle unforeseen problems.

[Read more about the differences between maintenance and support ›](https://ubuntu.com/blog/security-maintenance-vs-support-whats-the-difference)

### When does a security patch become a support issue?

A security patch becomes a support issue when its application – even if backported carefully – unexpectedly alters system behavior, disrupts integrations or causes regressions in your specific production environment, requiring expert diagnosis and targeted remediation beyond automated deployment.

### What happens when a vulnerability appears in a package that's no longer maintained upstream?

Unmaintained packages that contain newly discovered vulnerabilities must be patched downstream if they are not maintained upstream. This would either require users to patch that software themselves, or to consume those packages from a vendor who has patched it. For example, Canonical backports upstream security fixes into Ubuntu LTS releases and supported packages within their support lifecycle via Ubuntu Pro.

## How does support work for open source software?

Enterprise support for open source combines guaranteed response times, expert troubleshooting, and bug-fix engineering across the full stack, so that organizations can run open source software under production-grade Service Level Agreements (SLAs). Open source support typically involves either: upstream maintainers who evolve the software or OS, or third-party vendors (such as Canonical) who maintain large repositories.

### What are the components of enterprise support?

Enterprise support normally includes:

{{ text_list_kh (items=[
  "Support channels such as a portal, phone, and ticketing, instead of relying only on community forums.",
  "SLAs that define response and update times by severity level.",
  "Escalation paths from frontline support to sustaining engineering and upstream maintainers.",
  "Clearly scoped coverage for specific releases, packages and platforms."
])}}

### What does "break/fix" support actually cover in enterprise software support?

In open source software support, break/fix support addresses incidents where systems stop working as expected – service outages, instability, performance degradation, configuration issues or integration failures – and focuses on restoring normal operation quickly.

### Why is a commercial support contract necessary if the software is free?

While the software may be free, a commercial contract provides predictability and transparency with accountable experts, enterprise-grade support SLAs, guidance on complex environments and help during critical outages, which community forums are not obligated to deliver.

[Learn why you need Linux support, with real-world case studies ›](https://ubuntu.com/blog/what-is-linux-support)

### How is enterprise support different from community forums or Stack Overflow?

Enterprise support offers guaranteed response times, access to engineers who understand your specific environment, and the ability to escalate and fix bugs, whereas forums and Q&A sites rely on best-effort help from volunteers.

## How do vendors handle end-of-life (EOL) software?

When software reaches the upstream end of life, vendors offer extended maintenance to keep critical systems stable, security-maintained, and supported beyond standard lifecycles, giving enterprises time to modernize safely. Vendors extend lifecycles with security backports and limited support add-ons, securing legacy systems while customers modernise at their pace. Some vendors offer similar extended phases but often require custom images, lag upstream versioning, and limit coverage to major projects – excluding small/open source tools many enterprises rely on.

### What's the risk of using open source software packages without support?

Without support, critical open source software packages may not receive timely security patches or bug fixes, leaving production systems exposed to vulnerabilities or prolonged downtime when issues arise.

## Which companies offer enterprise open source support?

There are several vendors that offer enterprise support for open source. Examples include Canonical, SUSE, Red Hat, OpenLogic, and others. Many of these companies support a curated set of packages and offer different support tiers, from standard business-hours support to premium 24/7 support and access to dedicated expertise at higher levels.

### How do the different Linux vendors offer support?

The different enterprise Linux vendors offer similar kinds of support, which include security maintenance, incident response, and premium ticketed support. The extent and depth of this support varies depending on the tier and vendor. For example, Red Hat Enterprise Linux (RHEL) offers self-support, standard, and 24/7 premium tiers subscriptions which bundle the OS with security updates, incident response, and lifecycle management for certified deployments, focusing on a curated ecosystem of RHEL packages and integrated products like OpenShift and Ansible. As another example, SUSE offers priority and premium support options for SUSE Linux Enterprise, that combine access to tested software, security updates, and technical support for enterprise deployments. SUSE supports the SLE family and associated solutions such as SUSE Rancher and storage products, focusing on officially shipped components within its enterprise ecosystem.

## How do support models compare across vendors?

The different vendors of enterprise Linux distributions, such as Canonical, RedHat, and SUSE, offer similar styles of support, with some key differences. These differences include: Breadth of coverage for open source packages, Length of support period, Possibilities for expanded or legacy support for End of Support or End of Life software, and Cost and subscription models.

### What makes Canonical different from other enterprise support options?

Canonical's enterprise support is differentiated from other enterprise Linux companies on three broad areas: package coverage, lifecycle of support, and its pricing model. Generally, Canonical's Ubuntu Pro + Support offers a broader package coverage (all OS, Infra and application packages), longer lifecycles (up to 15 years), and a more favourable per-machine pricing model, while Red Hat/SUSE offer curated stacks with versioning lag, custom image requirements and limited support for smaller projects – creating gaps for diverse enterprise stacks.

#### Package coverage

Canonical's Ubuntu Pro + Support covers Main and Universe packages over 15 years, while other vendors concentrate on smaller, curated sets of software tied closely to their platforms. Supporting thousands of community packages requires significant engineering investment and upstream relationships, so many vendors focus only on a smaller, curated set of components. Generally, other Linux vendors (for example, RedHat and SUSE) prioritize "core" ecosystems, that exclude niche OSS tools and the wide range of packages available through vast repositories like Universe.

#### What is the difference between Main and Universe package support in Ubuntu?

Main contains the core operating system and vendor-supported components, whereas Universe includes a wide range of community-maintained applications and toolchains such as PostgreSQL, Docker, Redis, and many developer tools. Infra-only support is enough to receive break/fix assistance and bug-fix support for packages in Main and infrastructure solutions like OpenStack or Kubernetes. However, full support is required in order to receive the same level of support for packages in Universe.

#### Lifecycle

Ubuntu Pro provides up to 15 years of security maintenance and support for LTS releases, similar in length to other enterprise Linux offerings but with extended coverage to a broader package set.

#### Pricing model

Canonical uses simple per-machine pricing with options for self-support, infra-only support and full-stack support, whereas other vendors often tie pricing to subscription editions and add-ons for specific products.

### How does Canonical's support model work?

Canonical's support model uses a 'follow-the-sun' approach – seamlessly transitioning high severity tickets between global teams across time zones – to provide 24/7/365 coverage with SLA-backed initial and ongoing response times. By eliminating timezone delays, Canonical's security engineers can provide continuous service to global customers and internal Canonical teams alike. This support model is spread over a few support tiers, which scale with enterprise open source software support needs:

{{ text_list_kh (items=[
  "Self-support (included with Ubuntu Pro)",
  "Weekday Support for cost-effective business-hours coverage",
  "24/7 Support with around-the-clock Sev1 response",
  "Firefighting Support for enhanced live resolution support for critical incidents",
  "Technical Account Manager (TAM) for a single point of contact and strategic reviews",
  "Dedicated Support Engineer (DSE) – for hands-on troubleshooting and proactive guidance for custom enterprise environments"
])}}

### What is the scope of Canonical support?

Canonical's support is divided into two distinct layers, which cover either your infrastructure layer, or everything up to your application layer.

#### How Canonical covers infrastructure

Canonical provides security maintenance and support for the mission-critical core systems that run your servers and data centers. This includes:

{{ text_list_kh (items=[
  'The core Ubuntu operating system, plus "cloud-building" tools like OpenStack (private clouds), Ceph (storage), and Kubernetes (container management).',
  "Specialized tools, like LXD and MicroCloud (lightweight virtualization) and MAAS, which is used for managing physical hardware like a cloud."
])}}

#### How Canonical covers applications

Canonical can also cover actual software your team uses to build products and analyze data. This includes:

{{ text_list_kh (items=[
  "Tens of thousands of open source libraries and programs from the Ubuntu Universe repository.",
  "Software delivered via all modern formats, such as container images, snaps, deb packages, and charms.",
  "Specialized software, such as Data and AI applications used for machine learning and big data processing."
])}}

[Explore Canonical's support datasheet ›](https://assets.ubuntu.com/v1/4745b2a6-ubuntu_pro_support.pdf)

### What's the difference between Ubuntu, Ubuntu Pro, and Ubuntu Pro + Support?

Ubuntu is the base operating system with standard community support. Ubuntu Pro adds expanded, 10-year security and compliance coverage, and other features such as Landscape for fleet management. Ubuntu Pro + Support layers phone and ticket support with enterprise SLAs for break/fix and bug fix assistance on top.

### How long does Canonical support LTS releases?

Ubuntu LTS releases are supported for 5 years. With Ubuntu Pro, Canonical provides 10 years of Expanded Security Maintenance for LTS releases, followed by 5 years of Legacy support via an add-on for organizations that need more time to migrate. This expands the lifecycle of LTS releases to 15 years maximum.

### What is Expanded Security Maintenance (ESM)?

Expanded Security Maintenance is an Ubuntu Pro feature that extends critical and high security fixes for packages in Main and Universe repositories for up to 10 years, far beyond the standard 5-year LTS support window, allowing businesses to keep older environments secure while planning upgrades.

### What is Legacy support?

Legacy support is an add-on to Ubuntu Pro for LTS releases of Canonical products after the end of ESM, focused on helping customers maintain stability for 5 additional years while they prepare for migrations or larger operational changes. It offers security fixes, compliance tooling, and expert help for long-lived production systems.

### What's the difference between ESM and Legacy support?

ESM extends Ubuntu LTS security patching from 5 years of standard maintenance to a full 10 years. Legacy support builds on ESM as a seamless add-on, pushing total coverage to 15 years for long-lived production systems.

[Learn how Canonical's support engineers help you when things go wrong ›](https://ubuntu.com/blog/dedicated-linux-support)
