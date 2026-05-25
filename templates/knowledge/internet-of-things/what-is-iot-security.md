---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Internet of Things"
  tag: "IoT Management"
  title: "What is IoT security?"
  breadcrumb: "What is IoT security?"
  description: "IoT security protects connected devices, data, and networks from vulnerabilities through secure design, trusted updates, strong access control, and fleet management."
  copydoc: "https://docs.google.com/document/d/1dPnp32Tcg770GcQzGmUWP4BU8q-tNfilNiWMDJfBtus/edit?tab=t.gx9xrjd45b1q"
  hero_title: "What is IoT security?"
  cta:
    description: "Learn about Canonical's IoT security solutions, like Ubuntu Core, which offer strong, updatable defenses for devices throughout their entire lifecycle. Discover specific security features, certification steps, and best practices for creating secure IoT products."
    buttons:
      - text: "Contact us"
        url: "https://canonical.com/solutions/iot-and-devices#get-in-touch"
        type: "button"
        variant: "positive"
      - text: "Learn more about IoT security"
        url: "https://canonical.com/solutions/iot-and-devices"
        type: "button"
      - text: "Read our Ubuntu Core success stories ›"
        url: "https://ubuntu.com/core/stories"
  blog:
    title: "Latest from our blog"
    id: 4155
---

{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-lite-video.jinja" import lite_video %}

IoT security, or Internet of Things security, refers to the set of practices, technologies, and processes that protect connected devices from vulnerabilities, misuse, and compromise. 

This knowledge hub article defines IoT security, outlines common challenges, details key considerations, and explains how Canonical and Ubuntu Core address these needs. 

## IoT security: an overview
IoT security aims to protect IoT devices, the data they generate and collect, and the networks they interact with from cyberincidents.

IoT security is a high-stakes, high-risk discipline, because unlike traditional IT systems, IoT systems are often highly distributed, resource-constrained, and deployed in unmonitored or physically exposed environments. These factors, combined with the widespread use of IoT across thousands of data-rich and lucrative industries, makes IoT assets a valuable and sensitive target for attackers.

A securely designed operating system (OS), trusted update infrastructure, and long-term security maintenance are essential to protect IoT devices and deployments against attacks, and to meet stringent security standards. Security engineers should focus their efforts on the underlying operating system, firmware, network configuration, and update mechanisms as the most critical points of control to reduce the risk of cyberincidents.

## What are the most common IoT security challenges?
IoT and edge devices are attractive targets for attackers due to their widespread adoption, distributed nature, long lifespans, and inconsistent maintenance and development. 
The most frequent challenges in IoT security include:
{{ text_list_kh(
  type="bullet",
  items=[
    "Hardware attacks",
    "Firmware and OS vulnerabilities",
    "Weak authentication and remote access risks",
    "Network exposure and misconfiguration",
    "Lack of update and patching infrastructure",
    "Limited visibility and fleet management",
]) }}

### Hardware attacks
IoT devices are often deployed in unprotected environments, such as factory floors, shopping centres, agricultural fields and more, where attackers can gain physical access.

Common risks include USB-based attacks, such as BadUSB, RubberDucky, or PoisonTap, which can inject malicious commands the moment a device is plugged in. Likewise, JTAG or UART interfaces can be exploited to bypass authentication mechanisms, extract sensitive information, or gain low-level control over the hardware. 

In more sophisticated scenarios, attackers may even tamper with components to extract cryptographic secrets or alter the boot sequence. These risks highlight the need for physical hardening, controlled access to debugging interfaces, and robust secure-boot mechanisms that prevent unauthorized code from running on the device.

### Firmware and OS vulnerabilities
Firmware is persistent, difficult to update, and frequently neglected after shipping, which makes it highly at risk of long-term compromise and attack attempts. Insecure bootloaders that fail to verify signatures can allow unsigned firmware to run, while outdated kernels or libraries introduce dependency vulnerabilities that attackers can exploit remotely. In systems without strong confinement, untrusted applications may also access privileged resources or interact with hardware in unintended ways. Overcoming these challenges requires a secure OS architecture, comprehensive isolation between applications, and a reliable mechanism for delivering validated, tamper-proof updates throughout the device lifecycle.

### Weak authentication and remote access risks
Many IoT devices still ship with default passwords, rely on password-based SSH access, or lack proper key-based authentication. These weaknesses open the door to credential-stuffing and brute-force attacks that can compromise large numbers of devices in a matter of minutes. The Mirai botnet is one of the most widely known examples of IoT default credential attacks: in this case, attackers were able to use just a small list of default credentials to infect millions of deployed systems. 

Ensuring strong, unique authentication and disabling password-based remote access are essential steps in preventing similar attacks.

### Network exposure and misconfiguration
Devices often run unnecessary services, leave ports open by default, or retain legacy network protocols that are not required for their operational role. Unrestricted WiFi or Bluetooth services increase exposure, and unfiltered inbound traffic makes systems more easily discoverable and exploitable. Even unused capabilities like IPv6 can unnecessarily broaden the attack surface if left enabled. 

Applying strict firewall rules, controlling interface-level access, and reducing network visibility are fundamental measures for reducing risk.

### Lack of update and patching infrastructure
IoT devices are often deployed in remote, off-grid, or poorly connected locations, where it is difficult to patch devices with the secure, transactional, and verifiable over-the-air (OTA) updates needed to protect against the latest vulnerabilities. Without reliable updates, devices become insecure over time as vulnerabilities accumulate. 

This is one of the most critical areas of attention for device security, making it a key security priority required by new regulations such as the Cyber Resilience Act (CRA). Security engineers must deeply consider how their deployed devices will remain continuously updated and protected against vulnerabilities across their lifecycles.

### Limited visibility and fleet management
IoT deployments scale quickly. Without centralized tools to monitor CVEs, enforce update policies, and track compliance, large fleets easily drift out of alignment. A reliable fleet management solution is a foundational requirement for maintaining long-term device security and addressing these challenges. For example, Canonical's [Landscape](https://ubuntu.com/landscape) provides a comprehensive platform for managing Ubuntu devices at scale, offering features like remote package management, security patching, and compliance monitoring, which are crucial for maintaining the security posture of an IoT fleet.

## What are the main considerations for IoT security?
The main considerations for IoT security include:

{{ text_list_kh(
  type="bullet",
  items=[
    "Secure-by-default device configuration",
    "System integrity and trusted boot",
    "Reliable updates and long-term maintenance",
    "Strong identity and access management",
    "Fleet visibility and operational security",
    "A secure and transparent software supply chain",
]) }}

### Secure-by-default device configuration
A secure IoT deployment begins with a device that is hardened from the moment it is powered on. This means shipping systems with minimal services enabled, tightly controlled connectivity, and only the components required for the device’s intended purpose. Disabling unused interfaces, whether WiFi, Bluetooth, USB ports, or IPv6, reduces the number of potential entry points for attackers. Equally important is removing any default credentials and enforcing strong, least-privilege access policies so that users and applications only interact with the resources they truly need. Ubuntu Core starts with this security baseline configuration, setting a strong foundation for the rest of the device’s lifecycle.

### System integrity and trusted boot
Ensuring the integrity of the device’s firmware and operating system is fundamental to preventing persistent compromise. A trusted boot process verifies each layer of the system before it runs, ensuring that unauthorized or tampered components cannot be loaded. When combined with an immutable or read-only system design and strict application confinement, this approach limits an attacker’s ability to modify system behaviour even if they gain some level of access. Keeping applications isolated from one another, and from the underlying OS, helps maintain predictable and secure device operation in the field. 

Ubuntu Core architecture brings immutability and confinement to the whole system, with signed artefacts to verify authenticity and secure boot enabled by default. 

### Reliable updates and long-term maintenance
IoT devices are often deployed for years at a time, making ongoing security maintenance essential. Without reliable updates, devices gradually accumulate vulnerabilities, increasing the likelihood of exploitation. Manufacturers must implement a secure and authenticated update mechanism that delivers patches consistently and can automatically roll back changes if an error occurs. This operational capability is no longer optional; modern regulations such as the Cyber Resilience Act make timely vulnerability remediation a legal obligation. A structured process for testing, validating, and rolling out updates ensures that security fixes reach devices quickly and safely.

[Learn how to manage your IoT devices at scale ›](https://ubuntu.com/engage/secure-device-management)

### Strong identity and access management
Managing how users and services authenticate to a device is central to maintaining its security posture. Devices should rely on key-based authentication, unique identities, and strict control over privileged actions. Remote access mechanisms such as SSH must be hardened, monitored, and limited to only what is necessary for operation. Combined with proper auditing, these controls ensure accountability and significantly reduce the risk of unauthorized access over the device’s lifetime.

### Fleet visibility and operational security
As IoT deployments scale into the hundreds or thousands of devices, maintaining security becomes a fleet-level challenge. Visibility into patch status, configuration drift, and emerging vulnerabilities is essential for sustaining long-term resilience. Centralized fleet management allows organizations to monitor compliance, enforce security policies, automate update schedules, and respond quickly to potential issues. This operational layer ensures that devices remain aligned with security expectations across their entire lifecycle.

### A secure and transparent software supply chain
Modern IoT devices rely heavily on open source components, meaning manufacturers must maintain a clear and complete understanding of their software supply chain. A transparent SBOM, robust dependency management, and trusted upstream sources are essential to reducing risk. 

Manufacturers remain responsible for every component included in their product. Ensuring that all dependencies receive timely security maintenance and selecting providers who assume responsibility for long-term updates is critical to achieving lasting compliance and device integrity.

[Learn how to secure your IoT devices ›](https://ubuntu.com/engage/securing-ubuntu-devices)


{{ lite_video(video_id="dY2hGPo7vjw", video_title="Learn how to optimize IoT security") | safe }}

## How does Canonical help with IoT security?
Canonical helps enterprises and users with their IoT security by providing the foundational technologies, tooling, and long-term maintenance required to build secure, compliant, and resilient IoT devices at scale. 

By combining [Ubuntu Core](https://ubuntu.com/core) with [Ubuntu Pro](https://ubuntu.com/pro/devices), manufacturers gain a reliable and stable deployment foundation and an end-to-end security posture that spans their entire device lifecycle. Canonical’s approach focuses on securing the system by default, maintaining its integrity over time, and providing the operational capabilities needed for long-term fleet management.

{{ lite_video(video_id="zf9bapbzb8o", video_title="Get an introduction to Ubuntu Core") | safe }}

### Secure-by-default system architecture
Ubuntu Core is designed around a hardened, minimal footprint and an immutable system architecture, ensuring devices ship in a secure state from the outset. Ubuntu Core enforces a minimal trusted computing base, meaning your image starts with no network exposure, no unnecessary services, and no default user accounts to disable. It enforces strict application confinement with snaps, and removes common misconfiguration risks that plague traditional IoT systems. This secure baseline significantly reduces the attack surface and ensures devices behave predictably from first boot.

### Trusted boot, strong integrity guarantees, and application confinement
Canonical’s secure boot framework and fully signed snap-based system ensure that only verified software is allowed to run on the device. Each component, from kernel to application, is cryptographically validated, providing a robust foundation for trusted execution. With mandatory confinement and sandboxing, applications are isolated and prevented from interacting with the OS or hardware beyond their explicit permissions. Together, these mechanisms make persistent compromise far more difficult, even under physical or remote attack.

### Verified, transactional, and reliable OTA updates
One of Canonical’s strongest contributions is its transactional, tamper-proof update system, built directly into Ubuntu Core. Updates are atomic and automatically rollback if anything goes wrong, eliminating the risk of “bricked” devices. Every update is signed, authenticated, and distributed through Canonical’s infrastructure. 

### Long-term maintenance
For manufacturers that require extended coverage, [Ubuntu Pro](http://www.ubuntu.com/pro) provides up to 15 years of security maintenance for thousands of open-source packages, ensuring all dependencies that are used in your device receive timely patches. This long-term maintenance model directly supports regulatory compliance requirements such as the Cyber Resilience Act (CRA).

[Learn how to build compliant IoT deployments for the CRA ›](https://ubuntu.com/engage/cra-regulations-for-ubuntu)

### Full fleet visibility and lifecycle management
Secure operation at scale requires comprehensive fleet awareness. Through [Landscape](https://ubuntu.com/landscape), Canonical delivers tooling to monitor update status, enforce compliance, and manage devices throughout their lifecycle. Landscape supports patch delivery, remote configuration, and policy enforcement. Available with a Ubuntu Pro subscription, Landscape helps device makers secure fleet posture across hundreds or thousands of deployed devices, whether you are using Ubuntu Desktop, Server, or Core.

[Explore what Landscape can do for IoT security ›](https://ubuntu.com/landscape/features)

### A secure and transparent supply chain
Ubuntu Core helps create a transparent and verifiable software supply chain by ensuring that every component is cryptographically signed, versioned, and traceable from its source to the device. With Core, you build your own images by selecting exactly which components you consume – whether from Canonical or your own software – while each remains a trusted, signed snap with a clear origin, SBOM, and history. Combined with Ubuntu Core's immutable design and transactional updates, this creates a consistent chain of trust, allowing operators to verify exactly what software is running, where it came from, and that it has not been tampered with.

[Understand IoT device compliance across the global market ›](https://ubuntu.com/engage/iot-compliance-in-the-global-market-a-guide-for-iot-device-manufacturers)
