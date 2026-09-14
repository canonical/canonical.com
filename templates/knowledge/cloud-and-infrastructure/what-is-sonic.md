---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Cloud and infrastructure"
  publish_date: 2026-08-28
  tag: "Networking"
  title: "What is SONiC?"
  breadcrumb: "What is SONiC?"
  description: |
    Learn what SONiC is, how its container-based architecture works, 
    and how Ubuntu can help reduce complexity in open networking.
  hero_title: "What is SONiC?"
  cta:
    description: |
      Explore Canonical’s container offerings, and find out more about how 
      Canonical’s approach to secure containers, long-term support, and defense in depth 
      helps make containers safer and more sustainable.
    buttons:
      - text: "Read Canonical's SONiC blog"
        url: "https://ubuntu.com/blog/sonic-the-open-source-network-operating-system-for-modern-data-centers"
        type: "button"
        variant: "positive"
      - text: "Learn more about Rockcraft"
        url: "https://documentation.ubuntu.com/rockcraft/"
        type: "button"
      - text: "Get in touch ›"
        url: "https://canonical.com/networking-contact-us"
  blog:
    title: "Latest from our blog"
    id: 1848
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}

Software for Open Networking in the Cloud (SONiC) is an open source network OS for data center switches. 
Built on Linux, it is designed to be hardware-portable across supported switch platforms and separates the OS 
from the underlying switch hardware for flexibility and automation.

## How does SONiC work? 

SONiC uses the Switch Abstraction Interface (SAI) to talk to different switching ASICs through a common interface. 
This helps operators run a consistent software stack across supported hardware platforms. 

Its architecture is modular, but not simple. SONiC packages major network functions into Docker containers. 
Common architecture references list nine core containers, which can be grouped by function: 

{{ text_list_kh(
  items=[
    "Routing and services: DHCP-relay, BGP, LLDP, and TeamD.",
    "System management: PMON and SNMP.",
    "State and sync: Database, SWSS, and SyncD."
]) }}

The exact container set can vary by platform, ASIC, image profile, and SONiC release. 

SONiC’s container-based architecture gives operators flexibility, but it also expands the software supply chain. 
A SONiC image can include thousands of open source and vendor-specific components across the base operating system, 
network services, Python libraries, Debian packages, platform drivers, SAI implementations, and ASIC software development kits. 
For production use, teams should treat SONiC as a full infrastructure platform and generate a software bill of materials (SBOM) 
for each target image. 

## Why does SONiC matter? 

SONiC matters because it brings the operational model of Linux and cloud 
infrastructure to the network fabric. 

For cloud, telco, AI, and enterprise operators, the main value of SONiC is choice. Because SONiC is modular, open source, and built 
around hardware abstraction through SAI, it can reduce dependency on a single network equipment vendor, support automation across 
heterogeneous environments, and align switch operations with existing Linux-based engineering practices. 

SONiC is particularly effective where infrastructure teams already operate Kubernetes, OpenStack, Ceph, and Ubuntu at scale. 
The network fabric integrates neatly into the same open infrastructure, rather than a separate proprietary domain. 

## Where is SONiC used?

Originally developed by Microsoft for Azure and open-sourced in 2016, SONiC has evolved into a production-hardened network OS trusted 
by the world's largest cloud service providers. This hyperscale heritage makes it an ideal fit for organizations operating large switch 
fleets that require standardized automation and want to align their network fabric operations with existing Linux-based infrastructure. 

Common industry use cases for SONiC include: 

{{ text_list_kh(
  items=[
    "Hyperscale cloud fabrics: where operators need consistent behavior across large switch fleets.",
    "Enterprise data centers: where teams want more hardware choice and less dependency on a single vendor network operating system.",
    "AI and GPU fabrics: where Ethernet, RoCEv2, congestion management, and telemetry are becoming operational priorities.",
    "Data fabrics: for east-west traffic between servers, storage, and accelerators.",
    "Management fabrics: where a simpler, open, and automatable switch OS can reduce operational drift.",
    "Data center interconnect: where some vendors are extending SONiC into broader routing and security use cases."
]) }}

## Why does SONiC need SAI? 

SONiC requires the Switch Abstraction Interface (SAI) in order to overcome the challenge of hardware fragmentation. Modern data center 
switches are often built on merchant silicon from vendors like Broadcom, NVIDIA, Marvell, Cisco, and others, with each ASIC using its 
own proprietary software development kit. Without an abstraction layer, a network operating system would need deep, platform-specific 
integration for every ASIC family. 

SAI solves this by providing a standardized API, allowing SONiC to maintain a consistent operational 
model across diverse hardware. 

SONiC talks to SAI, while the silicon vendor provides the SAI implementation that maps those calls to the ASIC software development kit. 
This decouples the network operating system from the hardware and enables SONiC to run across multiple vendors and ASICs. 

Note that SAI does not make all hardware identical. ASIC capabilities, buffering, telemetry, performance behavior, and feature maturity 
still vary, depending on the hardware. SAI creates a stable boundary between SONiC and the switch ASIC. SONiC can evolve above that interface, 
while silicon vendors maintain the hardware-specific implementation below it. This reduces the need to rebuild the network operating system for 
every supported platform. 

## Community SONiC and the vendor ecosystem 

### What is community SONiC? 

Community SONiC is the upstream, open source version of SONiC, maintained by the SONiC community. It provides the common architecture, containerized 
services, control plane components, and integration model that vendors and operators build on. 

For hyperscalers and advanced operators, community SONiC can be a strong foundation. These organizations often have the engineering depth 
to build images, validate switch platforms, integrate ASIC software development kits, maintain SAI implementations, automate upgrades, 
and debug issues across the full stack. 

For most organizations, community SONiC is not the same as a supported product. While community SONiC provides the raw technical foundation, 
a supported product is what makes the software “production-ready.” Production deployments need a validated image, hardware compatibility, 
firmware lifecycle management, security maintenance, upgrade testing, optics validation, management integration, and a clear support path 
when the issue crosses software, ASIC, firmware, and hardware boundaries. 

### Which OEMs and vendors support SONiC? 

The [SONiC Foundation](https://sonicfoundation.dev/) lists a broad ecosystem that includes cloud providers, silicon vendors, OEMs, and 
network equipment vendors. Their level of engagement naturally varies. Some vendors offer their own enterprise SONiC distributions, and 
some certify SONiC on specific switch platforms. Others contribute silicon or SAI enablement, and others integrate upstream SONiC into 
their management, automation, or validation tools. Premier members of the SONiC Foundation include Alibaba, Arista, Broadcom, Celestica, 
Cisco, Dell Technologies, Google, Marvell, Microsoft, Nokia, and NVIDIA. 

Here are some examples of the different ways vendors engage with SONiC: 

{{ text_list_kh(
  items=[
    "Dell Technologies: Offers Enterprise SONiC Distribution by Dell Technologies, positioned for modern data centers, cloud and AI workloads, multi-tenant fabrics, RoCEv2 configuration, dynamic load balancing, and rail-optimized AI layouts",
    "Cisco: Supports SONiC on Cisco data center platforms, contributes to the SONiC ecosystem, and has described SONiC use cases as expanding from data center fabric to data center interconnect, with focus areas including routing, chassis management, telemetry, and security",
    "Asterfusion: Provides AsterNOS and SONiC-based whitebox switches for cloud, AI, storage, enterprise data center, campus, packet broker, and gateway use cases",
    "Edgecore: Provides SONiC-based switching platforms for data center and AI infrastructure",
    "Celestica: Participates as a SONiC Foundation premier member and whitebox switching ecosystem participant",
    "Data fabrics: for east-west traffic between servers, storage, and accelerators.",
    "Management fabrics: where a simpler, open, and automatable switch OS can reduce operational drift.",
    "Data center interconnect: where some vendors are extending SONiC into broader routing and security use cases."
]) }}

The ecosystem is still uneven across platforms and features. Operators should validate the exact switch model, ASIC, SAI implementation, 
optics, platform firmware, management tools, and support model before selecting SONiC for production.

## When should you consider SONiC? 

SONiC is a good fit when your organization needs: 

{{ text_list_kh(
  items=[
    "Hardware choice across supported switch platforms",
    "A Linux-based operational model for network infrastructure",
    "Automation-friendly switch management",
    "Consistent fabric behavior across large fleets",
    "Closer alignment between network engineering and platform engineering"
  ]
)}}

SONiC requires operational maturity. Teams need skills in Linux, routing, switch hardware, automation, testing, and lifecycle management. 
It is best approached as an infrastructure platform, not as a drop-in replacement for a traditional network operating system. 

## Can you use SONiC and Ubuntu together?

Yes. As we’ve discussed, SONiC is a network OS. But a network needs a foundation. That’s the job of a host OS, in this case Ubuntu, 
to take care of the rest of the stack. Now let’s look into why they fit well together.

The primary reason to use Ubuntu is that most SONiC distributions are Debian-based, as is Ubuntu. This makes Ubuntu LTS (long-term support) 
releases a natural foundation for organizations that want enterprise maintenance, the latest kernel, and a more robust security lifecycle 
than can be found in some other distros. 

### How do you use SONiC and Ubuntu together?

Whether you’re switching from another OS to Ubuntu, or setting up SONiC for the first time, it’s important to note that SONiC is not something 
you just “set and forget.” 

This is because a production SONiC distribution is usually tied closely to the switch hardware it supports. The image needs to integrate 
the base operating system, SONiC services, platform drivers, firmware, optics support, SAI implementation, and ASIC software development kit. 
That integration work is normally executed by the hardware OEM or a specialized system integrator.

As with any OS, an Ubuntu-based image still needs to be built, validated, and supported against specific switch platforms, ASICs, firmware versions, 
and deployment profiles. 

But SONiC cannot be moved to Ubuntu as a generic operating system swap. Canonical can help OEMs and system integrators 
build that foundation. Rockcraft, Pebble, and chiseled Ubuntu container images can help produce smaller, more focused SONiC containers. 
By removing packages and files that are not needed at runtime, chiseled images can reduce image size and attack surface. In resource-constrained 
switch environments, smaller images can also reduce memory pressure, although each service should still be measured on target hardware. 

For OEMs and system integrators, this enables a cleaner path to production-ready SONiC images on whitebox network equipment. 
The goal is not just to run SONiC on Ubuntu, but to make the operating model easier to maintain, patch, audit, and support over time.