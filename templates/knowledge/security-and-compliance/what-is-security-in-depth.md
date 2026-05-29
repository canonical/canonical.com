---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Security and compliance"
  tag: "Security"
  title: "What is security in depth?"
  breadcrumb: "What is security in depth?"
  description: "Security in depth is a layered cybersecurity approach that reduces risk by combining independent controls like multi-factor authentication, segmentation, monitoring, and encryption."
  copydoc: "https://docs.google.com/document/d/1lFW0x-emo_zC_qByxKgvaDtBOYqx_I_6eGMKCY8yOUo"
  hero_title: "What is security in depth?"
  cta:
    description: "Implement comprehensive security for your Ubuntu deployments."
    buttons:
      - text: "Get started with Ubuntu Pro"
        url: "https://ubuntu.com/pro"
        type: "button"
        variant: "positive"
      - text: "Get in touch"
        url: "https://ubuntu.com/contact-us/form?product=pro"
        type: "button"
      - text: "Read about layered security and Ubuntu protections ›"
        url: "https://ubuntu.com/engage/security-in-depth"
  blog:
    title: "Latest from our blog"
    id: 1364
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}

Security in depth is a cybersecurity strategy that deploys multiple, independent layers of protection across every level of a system. Learn how security in depth works to protect the system on a layer by layer basis, using robust protections that stop threats even when one layer of defense is bypassed.

## Security in depth: an overview

Security in depth is a cybersecurity strategy that deploys multiple, independent layers of protection across every level of a system. Instead of relying on a single security control, each layer, whether it's network monitoring, access controls, encryption, or hardware isolation, acts as an additional barrier to delay, detect, or stop attackers. The core principle is straightforward: if one defense is bypassed, the next layer is ready to contain the threat.

### What kinds of threats does security in depth help to prevent?

Security in depth targets a wide range of attacker profiles and threat levels, thanks to its individualized, layer-by-layer approach to security. Each layer in a security-in-depth model is designed around a specific attacker profile and capability level. At the base layer, defenses address opportunistic attackers using known exploits and automated tools. Further up, controls target adversaries who can exploit cryptographic implementation flaws, probe for misconfigurations, or wield zero-day vulnerabilities. At the highest level, protections guard against attackers who have compromised the host environment itself. By mapping defenses to threat levels, organizations ensure that security investment is deliberate, proportionate, and effective.

The kinds of attackers and threats that security in depth can help to prevent includes:

{{ text_list_kh(
  type="bullet",
  items=[
  "Opportunistic attackers exploiting publicly known vulnerabilities with automated tools and widely available exploit kits.",
  "Sophisticated attackers targeting weaknesses in cryptographic implementations rather than the algorithms themselves.",
  "Resourceful attackers who probe for configuration weaknesses, default settings, and human errors in system setup.",
  "Sophisticated attackers wielding zero-day exploits to compromise application-level code and attempt lateral movement.",
  "Attackers targeting firmware and early boot stages to establish persistent, pre-OS access that evades conventional security tools.",
  "Nation-state-level adversaries or malicious insiders with full control of the host environment, including hypervisor and firmware access."
]) }}

### What is security in depth based on?

The concept draws from the reality of computational security. Perfect, unbreakable security is theoretically possible, the one-time pad, for example, offers mathematically proven secrecy, but it's impractical to implement at scale. Modern cybersecurity instead focuses on making attacks so computationally expensive and operationally complex that they become infeasible. Consider AES-256 encryption: it isn't unbreakable in an absolute sense, but brute-forcing the key would take millions of years with current technology. Security in depth applies this same thinking across an entire system, stacking defenses so that an attacker must overcome not just one hard problem, but many independent difficult problems in a row in order to successfully attack a system.

## What is security in depth vs defense in depth?

The terms "security in depth" and "defense in depth" are often used interchangeably, and in many contexts they refer to the same general principle of layered protection. Generally speaking, however, defense in depth refers to a broad strategic framework of layering defenses, while security in depth refers to the cybersecurity practice of mapping security layers to a specific threat capability.

### What is defense in depth?

Defense in depth is the broader strategic framework. Originating from military doctrine, it describes the practice of arranging multiple lines of defense so that an adversary must breach several barriers rather than just one. In IT, defense in depth typically refers to layering controls across the network, host, application, and data levels of an environment, firewalls, access controls, encryption, monitoring, and so on.

### How is security in depth different from defense in depth?

Security in depth extends the strategy of broad defense in depth by explicitly mapping each security layer to a specific attacker capability. This threat-model-driven approach ensures that each control is calibrated to a particular risk, from script kiddies running automated exploit kits to nation-state actors with access to the host infrastructure.

In practice, security in depth can be understood as defense in depth with an explicit attacker capability model that ensures each layer is deliberately chosen to address a specific, well-understood threat.

## What are the best practices to apply security in depth?

A robust security-in-depth strategy combines controls across multiple domains, such as identity, network, endpoints, and data. The following are essential layers that organizations should consider when building a multi-layered defense:

{{ text_list_kh(
  type="bullet",
  items=[
  "Multi-factor authentication",
  "Intrusion detection and prevention systems",
  "Endpoint detection and response",
  "Network segmentation",
  "Encryption",
  "Data loss prevention",
  "Virtual private networks"
]) }}

### Multi-factor authentication (MFA)

Multi-factor authentication requires users to verify their identity through two or more independent factors: something they know (a password), something they have (a hardware key or mobile device), or something they are (a biometric). MFA is one of the most effective defenses against credential-based attacks, which remain among the most common initial access vectors. Even if passwords are compromised through phishing, brute force, or credential stuffing, MFA introduces an additional barrier that an attacker must overcome to gain access. Common implementations include hardware security keys (such as YubiKey), time-based one-time password (TOTP) apps, and biometric verification.

### Intrusion detection and prevention systems (IDS/IPS)

Intrusion detection systems (IDS) and intrusion prevention systems (IPS) monitor network traffic and system activity for known attack signatures, anomalous patterns, and policy violations. An IDS provides visibility by alerting security teams to suspicious activity, while an IPS adds active enforcement by automatically blocking or quarantining malicious traffic before it reaches its target. Together, they form a critical layer of network-level monitoring that can catch attacks in progress, from port scanning and brute-force attempts to more sophisticated lateral movement.

### Endpoint detection and response (EDR)

Endpoint detection and response extends security monitoring to individual hosts, servers, workstations, containers, and virtual machines. EDR solutions continuously collect telemetry from endpoints, analyzing process behavior, file system changes, and network connections for indicators of compromise. When threats are detected, EDR tools can isolate affected endpoints, kill malicious processes, and provide forensic data for incident response. This layer is essential because attackers who successfully bypass network-level defenses must still operate on endpoints, where EDR can detect and contain their activity.

### Network segmentation

Network segmentation divides an environment into isolated zones, restricting the flow of traffic between them. By separating critical workloads, databases, and management interfaces from general-purpose traffic, segmentation limits an attacker's ability to move laterally after gaining an initial foothold. Microsegmentation takes this further by applying per-workload security policies, ensuring that even within a network zone, each service can only communicate with the specific resources it requires. The practical effect is a dramatically reduced blast radius: a breach in one segment does not expose the entire environment.

### Encryption

Encryption protects data across three states: at rest, in transit, and in use. Data at rest is protected through full disk encryption and database-level encryption, ensuring that physical access to storage media does not expose sensitive information. Data in transit is secured via protocols like TLS, preventing interception and tampering during network communication. Data in use is the newest frontier; [confidential computing](https://ubuntu.com/confidential-computing) technologies use hardware-level memory encryption to protect data even while it is being processed, defending against attackers who have compromised the host operating system or hypervisor. Together, these three layers ensure that data remains unintelligible to unauthorized parties regardless of where it exists in the system.

### Data loss prevention (DLP)

Data loss prevention encompasses the policies, processes, and tools that monitor, detect, and block the unauthorized transfer of sensitive data outside an organization's boundaries. DLP controls can operate at the network level (inspecting outbound traffic), at the endpoint level (monitoring file copies to USB devices or cloud storage), and at the application level (restricting sharing and download capabilities). DLP is particularly important for organizations in regulated industries that handle personally identifiable information (PII), financial records, health data, or classified material, where data exfiltration can carry significant legal and reputational consequences.

### Virtual private networks (VPNs)

Virtual private networks encrypt all traffic between a user's device and the corporate network, creating a secure tunnel over untrusted networks such as public Wi-Fi or the open internet. VPNs are a foundational technology for enabling secure remote access, particularly for distributed and hybrid workforces. While VPNs provide strong transport-level encryption, modern security architectures often complement them with zero-trust network access (ZTNA) approaches, which verify user identity and device posture on a per-session basis rather than granting broad network-level access.

## How do you apply security in depth on Ubuntu?

You can easily apply the principles of security in depth on Ubuntu by making use of its security features and services that are designed to defeat specific attacker capabilities at each layer of your security strategy. This can include:

{{ text_list_kh(
  type="bullet",
  items=[
  "Patching known vulnerabilities with Expanded Security Maintenance (ESM) via Ubuntu Pro for long-term CVE coverage across Main and Universe packages",
  "Using FIPS-validated cryptographic modules (Kernel Crypto API, OpenSSL, OpenSSH and more) to reduce risk from crypto implementation flaws",
  "Applying automated hardening with the Ubuntu Security Guide (USG) to reduce misconfigurations and generate audit-ready reports",
  "Containing zero-day impact with AppArmor mandatory access control profiles that confine applications to least privilege",
  "Securing boot and storage with Secure Boot and Full Disk Encryption (LUKS/LVM) to prevent pre-OS tampering and protect data at rest",
  "Protecting workloads even from a compromised host with confidential computing (e.g., AMD SEV-SNP, Intel TDX) using Ubuntu Confidential VMs"
]) }}

[Learn more about Ubuntu platform security primitives ›](https://ubuntu.com/security/platform-security)

### How do you defend against publicly known vulnerabilities?

At the most fundamental level, cybersecurity begins with patching known vulnerabilities. Once a CVE is publicly disclosed, attackers worldwide have the same information, and exploits often follow within days or hours. Most known vulnerabilities can be patched by applying fixes manually or automatically from third-party trusted vendors. For example, most major vulnerabilities in Ubuntu are patched by Canonical, its publisher, through its comprehensive subscription for security, support, and compliance, Ubuntu Pro.

With an Ubuntu Pro subscription, each LTS release receives up to 15 years of security updates. The Ubuntu security team ingests vulnerability reports daily from sources including MITRE and NVD, and frequently publishes fixes. This patching covers tens of thousands of packages for the most popular open source software across the Ubuntu Main and Universe repositories, together forming a single trusted source for open source software.

### How do you defend against attackers targeting weaknesses in cryptographic implementations?

More advanced adversaries may not attempt to brute-force encryption directly but instead target flaws in how cryptographic algorithms are implemented. Techniques such as padding oracle attacks on improperly configured encryption schemes, or timing side-channel attacks that infer key material by measuring how long operations take, can compromise data without breaking the underlying mathematics. Ubuntu helps address this threat with FIPS (Federal Information Processing Standards) certified cryptographic modules that meet the strict standards set by the National Institute of Standards and Technology (NIST). The validated components include the Linux Kernel Crypto API, OpenSSL, OpenSSH, libgcrypt, and strongSwan, ensuring that cryptographic operations across the system are robust against both theoretical and practical implementation attacks.

### How do you defend against attackers who target configuration weaknesses, default settings, and human errors in system setup?

Even a fully patched system with strong cryptography can be undermined by a single misconfiguration – a default password left unchanged, an unnecessary service left running, or file permissions set too broadly. These weaknesses can be addressed by applying configurations that align with robust industry benchmarks, such as the CIS and DISA. Typical hardening steps include disabling unused USB ports to prevent physical attacks, configuring full disk encryption, removing unnecessary packages, tightening directory permissions to enforce least privilege, and configuring remote logging with file integrity monitoring so that attackers cannot cover their tracks.

In Ubuntu, you can apply these hardening profiles and benchmarks through The Ubuntu Security Guide (USG), which automates system hardening based on industry benchmarks from CIS and DISA. USG can apply hundreds of configuration changes in a single procedure and generate audit reports detailing which rules have been applied. USG profiles are available for both CIS benchmarks and DISA STIGs, making it applicable across a wide range of regulated industries.

### How do you defend against zero-day exploits in application-level code?

When an attacker possesses a zero-day vulnerability, no patch exists to defend against it, and no patching regime will help until the flaw is disclosed. In order to address this security flaw, you need to reduce the extent of potential attacks by strictly confining, isolating, or limiting the abilities of attackers to execute code across networks or systems. In Ubuntu, this is achieved through AppArmor, Ubuntu's Mandatory Access Control (MAC) framework. AppArmor confines applications to only the system resources they legitimately require, and enforces security profiles that define strict boundaries on file access, network capabilities, and process execution. Even if an application is compromised through an unknown vulnerability, AppArmor prevents the attacker from escalating privileges, accessing sensitive data outside the application's scope, or moving laterally within the system. Ubuntu ships with pre-installed AppArmor profiles for common applications. For custom workloads, administrators can generate new profiles by running the application in Complain mode to capture its legitimate behaviours, then switching to Enforce mode to lock down access.

### How do you defend against attackers targeting firmware and early boot stages?

Some attackers target systems before the operating system has even loaded, inserting malware into firmware or early boot components to establish a persistent foothold that survives reboots and evades OS-level security tools. In order to defend against these attacks, you need to secure and verify your firmware and boot stages. Ubuntu helps guard against these threats with two complementary protections. Secure Boot enforces a chain of trust during the boot process, ensuring that only signed, verified code is executed. In Ubuntu's implementation, all pre-built boot binaries, except the initial ramdisk, are signed with Canonical's UEFI certificate, embedded within the shim loader signed by Microsoft. Full Disk Encryption (FDE), enabled through the Logical Volume Manager (LVM) and Linux Unified Key Setup (LUKS) during installation, ensures that all data on disk is inaccessible without the correct encryption key. Together, Secure Boot and FDE prevent unauthorized code from running at boot time and protect data against physical access and offline attacks.

### How do you defend against malicious actors with full control of the host environment?

The most capable adversaries can compromise the entire host environment, hypervisor, host operating system, firmware, and may have the backing of malicious insiders with administrative access. Historically, this level of access would expose all workload data, because the hypervisor and host OS were implicitly trusted to manage virtual machine resources. Confidential computing fundamentally changes this model by decoupling resource management from data access. Through CPU security extensions such as AMD SEV-SNP and Intel TDX, Ubuntu Confidential Virtual Machines (CVMs) create a hardware-rooted execution environment that isolates workloads from the host. Memory is encrypted using an AES engine within the CPU's memory controller on every read and write operation, and new hardware-based access controls allow auditing of memory management to detect unauthorized modifications and replay attacks. Even a compromised hypervisor or a malicious administrator cannot access data within a CVM. Ubuntu CVMs are available on all major public cloud providers and can also be deployed in private cloud environments using Ubuntu on both host and guest.
