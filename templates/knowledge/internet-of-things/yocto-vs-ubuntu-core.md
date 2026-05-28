---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Internet of Things"
  publish_date: 2026-05-25
  tag: "Embedded"
  title: "What is the difference between Yocto and Ubuntu Core?"
  breadcrumb: "Difference between Yocto and Ubuntu Core"
  description: "Explore Yocto vs. Ubuntu Core for IoT and embedded systems. Compare their architecture, support, security, and compliance with regulations like the Cyber Resilience Act (CRA)."
  copydoc: "https://docs.google.com/document/d/1yPBVUfiGiB97hVD0iubPf-iXxDp2B1MTdF4Ndrv1Ec4"
  hero_title: "What is the difference between the Yocto Project and Ubuntu Core?"
  cta:
    description: "To better understand which embedded Linux platform aligns with your product lifecycle and compliance needs, explore Canonical's resources on Ubuntu Core for IoT. Learn how built-in security and long-term support simplify CRA compliance."
    buttons:
      - text: "Talk to our team"
        url: "https://ubuntu.com/core/contact-us"
        type: "button"
        variant: "positive"
      - text: "Download the datasheet"
        url: "https://assets.ubuntu.com/v1/e7f9bb41-Ubuntu%20Core%20DS%201.5.2024.pdf"
        type: "button"
      - text: "Read more about CRA compliance on Ubuntu ›"
        url: "https://ubuntu.com/engage/iot-compliance-in-the-global-market-a-guide-for-iot-device-manufacturers?_gl=1*1w6nc6w*_gcl_au*MjAyNTc4NzE0Mi4xNzc4MTQ3MDEx"
        type: "link"
  blog:
    title: "Latest from our blog"
    id: 4632
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-lite-video.jinja" import lite_video %}

The Yocto Project is a customizable framework for building bespoke Linux distributions, requiring the manufacturer to own the entire software lifecycle. In contrast, Ubuntu Core is a production-grade, security-hardened operating system that provides a maintained, long-term platform for embedded devices.

This article compares the two Linux platforms, the Yocto Project and Ubuntu Core, examining their architectural and support models, as well as how they address lifecycle security for embedded devices in light of new regulations like the EU Cyber Resilience Act (CRA). 

## The Yocto Project vs Ubuntu Core: an overview

When evaluating embedded Linux platforms, device manufacturers and development teams most often choose between two approaches: the Yocto Project, and Ubuntu Core. While both are rooted in the Linux ecosystem and share the goal of powering embedded devices, they represent different philosophies in how embedded software should be built, maintained, and deployed. The Yocto Project and Ubuntu Core differ on a few key areas, including:

{{ text_list_kh (items=[
  "Their abilities to reduce complexity",
  "The stage of the lifecycle they best suit",
  "Their architecture and security foundation",
  "How much technical expertise they require",
  "Their support and security maintenance models"
])}}

### Primary use case

Yocto is designed for custom production builds and initial hardware bring-up, whereas Ubuntu Core is optimized for standardized fleet deployment and general production environments.

### Abstraction

Where Yocto asks developers to define and own every aspect of their system, Ubuntu Core abstracts away much of that complexity, allowing teams to focus on the software and applications that differentiate their product.

### Lifecycle stage excellence

The distinction between the two platforms becomes clearer when considering the full lifecycle of an embedded device. Yocto excels in the early stages, as its flexibility and the availability of silicon vendor-provided Board Support Packages (BSPs) make it a popular choice for hardware bring-up and rapid prototyping. Ubuntu Core’s long-term support makes it the clear choice in longer lifecycles.

### Technical expertise needed

Yocto requires deep technical expertise and results in maximum flexibility, Ubuntu Core trades some of that flexibility for a dramatically reduced maintenance burden, stronger security defaults, and a more predictable path to long-term compliance.

### OS architecture

Yocto utilizes a system custom-built from source for maximum granular control, while Ubuntu Core relies on a fully containerized architecture powered by snaps.

### Security hardening

Yocto requires significant internal expertise to implement and maintain security measures, whereas Ubuntu Core includes comprehensive hardening by default.

### OTA updates

Yocto depends on third-party integrations to manage over-the-air updates, while Ubuntu Core provides native, atomic updates with built-in rollback capabilities.

### Long-term support

Yocto typically offers a support lifecycle of up to 4 years, whereas Ubuntu Core provides extended coverage for up to 15 years with an Ubuntu Pro subscription.

### Supply chain

Yocto places the responsibility for supply chain auditing on the developer, while Ubuntu Core utilizes a centralized, auditable snap store.

### Maintenance burden

Yocto carries a high maintenance overhead that requires dedicated in-house Linux distribution engineers, whereas Ubuntu Core offloads the primary maintenance burden to Canonical.

### CRA readiness

Yocto requires moderate to high internal effort to achieve Cyber Resilience Act compliance, while Ubuntu Core provides platform-level features and long-term security maintenance for streamlined CRA compliance.

[Read a detailed comparison guide for CRA compliance ›](https://ubuntu.com/engage/cra-yocto-core)

## What is the Yocto Project?

The Yocto Project is a collaborative, open source initiative operating under the Linux Foundation. Rather than being a Linux distribution in its own right, Yocto is best understood as a collection of tools, methods, and frameworks that enable developers to build a custom Linux distribution from the ground up.

The Yocto Project provides a flexible set of tools that enable embedded developers to share software stacks and configurations, allowing them to create tailored Linux images for a wide range of devices and processor architectures.

### What is the Yocto Project primarily used for?

The Yocto Project’s primary value proposition lies in the granular control it gives developers over every component of the resulting system, from the bootloader to the kernel and userspace libraries. This makes Yocto a natural fit for early-stage prototyping, proof-of-concept work, and bespoke hardware configurations where no off-the-shelf distribution is available.

### How is the Yocto Project supported?

The Yocto Project is backed by a broad community of silicon vendors, independent developers, and corporations who share the goal of simplifying embedded Linux development across a wide range of processor architectures and hardware platforms.

### What are the limitations of Yocto?

Yocto’s strengths in prototyping and early development come with some challenges, including long-term support, the level of abstraction, and the complexity of builds.

For example, the Yocto community's support window for any given release is limited to only a few months, has no integrated security maintenance pipeline, and does not have a built-in mechanism for over-the-air updates. This means that manufacturers shipping long-lived devices must either track upstream releases continuously or risk operating on unsupported, potentially vulnerable software.

Maintaining a Yocto-based system in production is therefore a substantial, ongoing commitment. For device manufacturers, this often translates into a need for skilled, full-stack Linux distribution engineers on staff for the entire operational lifetime of their product, which is a high and often underestimated cost.

## How does Yocto work?

Unlike distributions such as Debian or Ubuntu, where the steps of assembling a system are largely decoupled, Yocto integrates the end user's applications directly into the root filesystem image generated from source. A Yocto build is structured with three central metadata parameters: the distro, the machine, and the image.

{{ text_list_kh (items=[
  "<strong>The distro:</strong> captures policy decisions about how the entire system is assembled.",
  "<strong>The machine:</strong> denotes the target hardware.",
  "<strong>The image:</strong> defines the list of packages to be cross-compiled and assembled into the root filesystem.",
])}}

Together, these parameters give developers precise control over the content and configuration of their target system, and allow the same distribution configuration to be retargeted to different hardware by swapping the machine definition. Bitbake, Yocto's task executor and scheduler, reads this metadata, then downloads and cross-compiles upstream source code accordingly.

### What are the core components of Yocto?

Yocto builds bootable, full-system images from upstream source code, using a compatible toolchain for the target device, a root filesystem image, a kernel, and a bootloader. Typically, a Yocto build follows a layer-based architecture that uses recipes, layers, and Board Support Packages.

**Recipe:** a metadata file that specifies how to build a particular software package, including where to download the source code, how to configure and compile it, what its dependencies are, and how to create the resulting packaged software bundle. Recipes support multiple package formats, and combine Python, shell scripts, and a BitBake-specific language to express build logic.

**Layers:** collections of related recipes that can be shared and reused across projects, hardware targets, and organizations. This modularity is one of Yocto's most cited strengths, as it allows teams to maintain clean separations between the build core, hardware-specific configurations, and custom application logic.

**Yocto Board Support Packages:** specialized category of Yocto layers tailored to a specific embedded board or hardware platform. BSPs enable running a given OS on different hardware devices by providing kernel configuration, display support recipes, machine definition files, and other hardware-specific metadata needed to produce a functional image for a target. Silicon vendors frequently provide reference BSPs for Yocto as part of their SDK offerings, making it straightforward to bring up a new chip or board within the Yocto framework. This broad hardware support, backed by active contributions from the silicon vendor community, is a primary reason for Yocto's widespread adoption in the early stages of embedded development.

With Yocto’s design and architecture, developers have control over virtually every stage of the compilation and build process, from selecting which init and SSH daemons to use, down to which individual packages and libraries are included in the final image. This results in systems that are often lightweight and optimized for minimal memory and storage footprint, which is a great advantage in resource-constrained embedded environments.

### How do embedded devices using Yocto receive OTA updates?

For Yocto, vulnerability management is more demanding. Developers are responsible for monitoring CVEs, packaging their own fixes, and verifying patch compatibility with their specific build. There is no centralized security maintenance pipeline and no guaranteed support beyond a few months. Yocto also lacks a built-in OTA update mechanism, requiring the integration of third-party solutions such as Mender; what’s more, responsibility for the content of those updates remains with the development team. Additionally, Yocto's federated build model, which pulls source code from a wide range of upstream repositories, also introduces significant supply chain risk. External changes, such as a repository disappearing, a branch being renamed, or a vendor withdrawing support, can break builds and leave manufacturers uncertain about the exact state of their devices' software.

## What is Ubuntu Core?

Ubuntu Core is a production-grade, security-hardened variant of Ubuntu designed specifically for embedded and IoT devices. Ubuntu Core provides an immutable, embedded OS that is ready for deployment at scale. It is built and maintained by Canonical, the company behind Ubuntu, and benefits from the same ecosystem, tooling, and long-term support infrastructure that has made Ubuntu the world's most widely used Linux distribution in cloud and enterprise environments.

{{ lite_video(video_id="zf9bapbzb8o", video_title="Yocto vs Ubuntu Core for the Cyber Resilience Act") | safe }}

### How does Ubuntu Core work?

The architectural foundation of Ubuntu Core is built on the understanding that traditional Linux packaging and distribution are not well-suited to the embedded world. Intermittent connectivity, the high cost of on-site intervention, the proliferation of software publishers, and the need for strict application isolation all demand a different approach. Ubuntu Core solves these problems with snaps: a secure, containerized, dependency-free, cross-platform Linux packaging format. Ubuntu Core and its applications run within a confined and transaction-based environment, and every component of the system, from user-space applications and daemons to the kernel and device drivers, is packaged and delivered as a snap.

[Find out more about Ubuntu Core’s features ›](https://ubuntu.com/core/features)

#### What are snaps?

A snap bundles an application with all its dependencies into a single, self-contained package, ensuring the software behaves consistently across different hardware and OS versions. Each snap runs within a tightly enforced security sandbox that leverages standard Linux security mechanisms to restrict access to the filesystem, network interfaces, and system calls. Fine-grained control over permissions is expressed through a simple YAML metadata file that defines an application's security profile and its desired integrations with the rest of the system. This means that, for example, a home appliance's address book application cannot access the device's camera unless explicitly permitted. Such a level of isolation is both straightforward to configure and consistently enforced at runtime.

#### What are the benefits of snaps in Ubuntu?

Because Ubuntu Core is 100% snap-based, this security model applies uniformly across the entire software stack. The minimal OS, the kernel, and device drivers all benefit from the same confinement and update guarantees as userspace applications. The root filesystem is read-only, preventing unauthorized modifications and ensuring that the base system remains immutable and tamper-resistant. Ubuntu Core further extends this security posture by supporting secure boot, abstracting the root-of-trust implementation for both ARM and x86-certified devices, and by enabling full disk encryption to protect the confidentiality and integrity of device data in the event of physical access.

### What are the core components of Ubuntu Core?

Ubuntu Core is built from the same artefacts as the corresponding Ubuntu LTS release. The kernel, boot assets, runtime environment, applications and device enablement capabilities are all delivered as snaps that are controlled by *snapd* (the snap daemon), which is itself packaged as a snap. It is built from the following components:

**Snapd:** the system daemon that supervises all other snaps. It exposes a REST API that makes Ubuntu Core devices IP-addressable by default, supporting remote device management.

**Application snaps:** define the functionality of the device. Each is confined with all its dependencies in its own sandbox. Interfaces to other applications or to the system must be explicitly defined. 

**System snaps:** deliver services critical to system function, including network-manager, modem-manager, bluez, and console-conf. A secondary tier enables device capabilities like audio, power, storage, and container orchestration via Microk8s and LXD.

**Boot assets:** define device-specific properties, including the bootloader configuration and partition layout. It is typically issued and signed by the board OEM/ODMs.

**Base snap:** holds the runtime environment inside which applications run, and serves as the root filesystem. It includes basic Ubuntu LTS packages.

**Kernel snap:** holds the kernel image, associated modules, and an initial ramdisk. Firmware and device tree files can optionally be included. The kernel snap can be updated but cannot be swapped.

Ubuntu Core’s architecture gives developers a well-defined, reproducible image composition model rather than granular build-time control. Teams using Ubuntu Core do not need to manage toolchains, dependency trees, or custom build logic; instead, they simply declare which snaps go into their device image, and Canonical handles the rest, from kernel maintenance to security updates. This makes Ubuntu Core a strong fit for organizations that want to ship embedded Linux in production without standing up a dedicated team to maintain it.

### How does Ubuntu Core handle updates?

Ubuntu Core implements fully transactional, atomic updates. An update is applied only if it completes successfully. If anything goes wrong, whether due to a software bug, a power outage, or a network interruption, the system automatically rolls back to its last known stable state. This guarantee applies equally to application snaps and to the kernel and base OS, ensuring that no update, however critical, can render a device unresponsive.

[Learn more about Ubuntu Core updates and features ›](http://www.ubuntu.com/core)

### Why is Ubuntu Core ideal for fleets of remote devices and distributed operations?

Ubuntu Core ships with built-in, production-grade support for over-the-air updates, including delta updates that calculate only the binary difference between versions, minimizing bandwidth consumption and update times for devices with limited connectivity. Every application and system component retains its previous version, allowing developers to move software forward or backwards in its version history with confidence. In this way, what is often seen as one of the most operationally risky activities in embedded Linux, pushing an update to a fleet of remote devices, becomes a routine, low-risk operation.

### How is Ubuntu Core supported?

Ubuntu Core benefits from Canonical's long-term support commitment. Devices running Ubuntu Core receive security updates, kernel maintenance, and platform support for up to 15 years (covered by Ubuntu Pro). This means device manufacturers do not need to staff and maintain their own kernel engineering team for the lifetime of their product. Instead, they can rely on the same support infrastructure that serves the world's most widely deployed Linux distribution, and direct their own engineering resources toward the software and applications that differentiate their product in the market.

## Yocto, Ubuntu Core, and CRA compliance

The EU Cyber Resilience Act (CRA) is a regulation that establishes mandatory cybersecurity requirements for software and digital products sold within the European market. Its purpose is to standardize currently fragmented national approaches by defining baseline security expectations that apply across a product's entire lifecycle, including planning, design, development, deployment, maintenance, and end-of-life.

[Read a full breakdown of the CRA ›](https://canonical.com/blog/a-cisos-comprehensive-breakdown-of-the-cyber-resilience-act)

The CRA imposes comprehensive cybersecurity obligations on device manufacturers to ensure products entering the EU market are secure throughout their lifecycle. These requirements move beyond 'nice-to-have' features, making robust security, transparency, documentation, and maintainable update infrastructure mandatory for compliance.

These requirements include:

{{ text_list_kh (items=[
  "A secure operating environment",
  "Transparency and software composition",
  "Documentation and Conformity Assessment",
  "Vulnerability reporting and remediation",
  "Secure Over-the-Air (OTA) update mechanisms"
])}}

[Explore IoT best practices for embedded and IoT manufacturers ›](https://canonical.com/blog/what-the-cyber-resilience-act-cra-means-for-iot-manufacturers)

### How do Yocto and Ubuntu Core compare under the CRA?

The CRA requires that products are designed with security from the outset, with a minimal attack surface and protection against unauthorized access. Ubuntu Core's architecture directly reflects these principles because its read-only root filesystem, mandatory snap confinement, and uniform application of AppArmor, cgroups, and seccomp across every layer of the software stack, including the kernel, make security a property of the platform rather than an add-on.

Yocto can also produce minimal images with a reduced attack surface, and security hardening is achievable with tools such as the meta-security layer. However, realizing this potential requires deep expertise and deliberate effort. Some BSP layers explicitly disable security capabilities such as cgroup, namespace, and BPF support, and the development team is responsible for enabling, configuring, and verifying every security feature. It is important to be aware of this distinction because, under the CRA, the device manufacturer bears legal accountability for the security of its product.

Here’s a concise overview of the main areas of comparison between Yocto and Ubuntu Core under the CRA:

{{ text_list_kh (items=[
  "<strong>Securely designed operating environment:</strong> Yocto requires manual effort to achieve a secure operating environment, whereas Ubuntu Core has these protections (including Secure boot, full disk encryption, and application isolation) built-in by default.",
  "<strong>OTA updates:</strong> Yocto relies on third-party solutions like Mender for over-the-air updates, while Ubuntu Core provides native, atomic updates with integrated rollback functionality.",
  "<strong>Supply chain transparency:</strong> Yocto places the responsibility for supply chain transparency on the developer, whereas Ubuntu Core utilizes a centralized snap store for streamlined auditing.",
  "<strong>Vulnerability management:</strong> Yocto requires a \"do-it-yourself\" approach to identifying and patching vulnerabilities, while Ubuntu Core offers Canonical-managed vulnerability management for up to 15 years.",
  "<strong>Secure Boot & encryption:</strong> Yocto necessitates manual configuration for secure boot and disk encryption, whereas Ubuntu Core supports these security features out of the box.",
  "<strong>Long-term security and support:</strong> Yocto typically provides security support for only a matter of months, while Ubuntu Core offers a significantly longer lifecycle of up to 15 years.",
])}}

### Which one is more cost-effective for CRA compliance? 

The cost of complying with the EU Cyber Resilience Act (CRA) is not fixed; it is a variable that depends significantly on factors like the product's intended lifecycle, device complexity, and risk classification. Crucially, the long-term cost of compliance is heavily influenced by the choice of the underlying embedded operating system or platform. For device manufacturers, the decision between a highly flexible but maintenance-intensive approach, such as the Yocto Project, and a production-ready, professionally supported platform like Ubuntu Core can be the difference between a manageable cost of ownership and a substantial, multi-year engineering burden.

#### What is the cost of CRA compliance when using Yocto?

Yocto's short support window and lack of integrated security and update mechanisms translate into a high, ongoing cost of compliance, essentially forcing manufacturers to operate as their own Linux distribution maintainers.

#### What is the cost of CRA compliance when using Ubuntu Core?

Ubuntu Core is backed by Canonical's long-term support and professional engineering infrastructure, which handles vulnerability management and OTA updates as built-in services. This approach dramatically reduces the compliance overhead, allowing manufacturers to focus on product differentiation while providing a platform-level foundation that addresses the CRA's core obligations.
