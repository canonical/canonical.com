---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Security and compliance"
  tag: "Security"
  title: "What is software supply chain security?"
  breadcrumb: "What is software supply chain security?"
  description: "A software supply chain is the entire ecosystem of code, tools, and processes used to build software. Learn how to secure your supply chain against attacks and manage risks."
  copydoc: "https://docs.google.com/document/d/1qWLaSoLo8z-4ra3-hw4Kfv2x2TYpckrFMkP0smNLNic"
  hero_title: "What is software supply chain security?"
  cta:
    description: "Securing your software supply chain is vital to your security posture, and mandatory for cybersecurity compliance."
    buttons:
      - text: "Explore OSS security"
        url: "/solutions/open-source-security"
        type: "button"
        variant: "positive"
      - text: "Discover Ubuntu Pro"
        url: "http://www.ubuntu.com/pro"
        type: "button"
      - text: "Read a guide to open source vulnerability management ›"
        url: "https://ubuntu.com/engage/vulnerability-management"
        type: "link"
  blog:
    title: "Latest from our blog"
    id: 1364
---

{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-lite-video.jinja" import lite_video %}

Software supply chain security is the practice of protecting the software development and delivery process against malicious attacks and vulnerabilities. Explore the theory and practical aspects of software supply chain security, from design and development to deployment and maintenance, in this knowledge hub article.

A software supply chain is the ecosystem for creating, distributing, and maintaining software. This includes open source components, third-party libraries, development tools, and deployment pipelines. Every part of the software supply chain presents a potential entry point for vulnerabilities. Mapping and understanding the entirety of your software supply chain is vital for mitigating risks and preventing cyber incidents.

## What is the goal of software supply chain security?

The primary goal of software supply chain security is to ensure the integrity, authenticity, and trustworthiness of the software delivered to the end-user.

The process of software supply chain security involves securing all stages and components that contribute to the final software product. This includes:

{{ text_list_kh (items=[
  "Source code",
  "Open source dependencies",
  "Development tools",
  "Build environments",
  "Deployment pipelines",
  "Distribution channels"
])}}

Managing a software supply chain involves tracking components and understanding their provenance, licenses, and vulnerabilities. It extends to securing development infrastructure, implementing strong access controls, and continuous threat monitoring. A maintained supply chain ensures the integrity and trustworthiness of delivered software.

## Why is software supply chain security important?

Using open source software broadens the components and options available to developers. In turn, this brings flexibility and deep customizability to software engineering – but given that all of these components come from different origins and each have their own lifecycle and potential security flaws, each should be managed responsibly to ensure a securely maintained system.

Mapping the supply chain provides organizations and engineers with visibility into dependencies and other risks associated with third-party components or software.

This holistic view is essential for robust security. If the software supply chain is not secure, it could lead to severe cyber incidents, loss of customers or revenue, reputational damage, and regulatory fines and penalties.

[Explore the greatest challenges in software supply chains ›](https://ubuntu.com/blog/open-source-enterprise-application-security-remains-a-challenge-despite-greater-patching-efforts-idc-research-reveals)

## What does software supply chain security entail?

Software supply chain security encompasses a number of steps, checks, and processes to ensure that every stage of using or implementing software is secure.

Software supply chain security includes:

{{ text_list_kh (items=[
  "Vetting the integrity of third-party vendors or sources and ensuring the integrity of their packages.",
  "Securing all components, tools, and processes involved in building and delivering software.",
  "Mitigating risks like malicious code injection, open source vulnerabilities, and third-party compromises.",
  "Understanding the security posture of all software that forms the software supply chain, including direct and transitive dependencies."
])}}

{{ lite_video(video_id="i_a8eGLB1K4") | safe }}

## What are the greatest software supply chain security challenges?

The biggest challenges in software supply chain security include:

{{ text_list_kh (items=[
  "Supply chain complexity",
  "The lack of standardized security practices",
  "Human error"
])}}

### Supply chain complexity

Modern software stacks are incredibly complex. The applications they use rely heavily on open source components (such as third-party libraries), each with its own vulnerabilities and dependencies. This intricate web makes it incredibly difficult for organizations to gain full visibility into all components, their origins, and their security posture. Attacks on the software supply chain are becoming increasingly sophisticated, targeting every stage from development to distribution. Without a comprehensive strategy for supply chain security, identifying and mitigating risks becomes a daunting task, opening up the potential for exploitation.

### Poor standardization of security practices

Different vendors, developers, and projects adhere to varying levels of security rigor, creating inconsistent levels of protection. This fragmentation makes it hard to establish a uniform security baseline and enforce consistent policies throughout the supply chain. Furthermore, the rapid pace of software development often prioritizes speed over security, leading to shortcuts that can introduce vulnerabilities. Balancing this desire for fast delivery with robust security measures remains a persistent hurdle.

### Human error

Human error is a constant source of risk for software supply chains.
Examples of human error include:

{{ text_list_kh (items=[
  "Developers introducing vulnerabilities through coding errors or insecure practices.",
  "Insider threats which compromise the integrity of the supply chain.",
  "Poorly configured, maintained, or monitored automations which introduce vulnerabilities."
])}}

[Understand vulnerabilities and how to manage them ›](https://ubuntu.com/engage/vulnerability-management)

## Software supply chain security solutions

Organizations that use software primarily use three techniques to secure their software supply chain: Software Bills of Materials (SBOMs), security scanners, and open source catalogs.

### SBOM generation

SBOMs are verifiable metadata associated with source code, container images, or binary files. They contain a comprehensive "ingredient list" of every software component and dependency a software artifact consists of.

SBOM generation aims to:

{{ text_list_kh (items=[
  "Create a verifiable record of a product's composition by documenting versioning, licensing, and other important information in standardized formats",
  "Establish provenance, the verifiable record of an asset's origin, authorship, and custody",
  "Ensure the integrity of the software throughout its lifecycle"
])}}

SBOMs are generated in various human- and machine-readable formats. Some examples of popular SBOM formats include:

{{ text_list_kh (items=[
  "SPDX by the Linux Foundation, which has a focus on software licenses",
  "CycloneDX by OWASP, which focuses on security vulnerabilities",
  "SWID by NIST, which does not have one particular emphasis"
])}}

SBOMs are ideally provided by the software vendor. They can also be generated after distribution from a software artifact using SBOM generators, but the accuracy of these results could be lower.

SBOM tools are vital for modern security because they enable rapid vulnerability mapping and ensure regulatory compliance by providing total transparency into the software supply chain.

[Learn more about SBOMs ›](https://canonical.com/blog/what-is-sbom-software-bill-of-materials-explained)

### Security scanners

Software security scanners are automated tools designed to analyze code, dependencies, and running applications to identify vulnerabilities, misconfigurations, or security weaknesses.

Security scanners typically operate in three ways:

{{ text_list_kh (items=[
  "Static analysis of source code (SAST)",
  "Dynamic analysis of active environments (DAST)",
  "Vulnerability scanners"
])}}

SAST and DAST are typically used at the software vendor level, and not by the software consumer. Software consumers would generally use vulnerability scanners instead.

Security scanning tools are essential because they provide scalable, continuous oversight that allows developers to remediate critical threats before they can be exploited in production.

Canonical [partners closely with companies like Black Duck and Tenable](https://canonical.com/blog/canonical-announces-ubuntu-security-research-alliance-program) to reduce the number of false positives in vulnerability scanners on Ubuntu and improve on-platform security for Ubuntu users through more proactive threat detection.
Canonical also publishes various vulnerability data feeds: VEX, OSV, and OVAL.

#### Ubuntu’s Vulnerability Exploitability eXchange (VEX)

VEX data is a structured, human and machine readable format describing known vulnerabilities and available security patches for all supported Ubuntu releases. Ubuntu’s VEX data currently follows the OpenVEX specification, a minimal, compliant, interoperable, embeddable and open source implementation of VEX.

[Learn more about VEX ›](https://ubuntu.com/security/vex)

#### Open Source Vulnerabilities (OSV)

OSV is a JSON schema that provides a human and machine readable data format to describe vulnerabilities in a way that precisely maps to open source package versions. This schema is developed and maintained by the Open Source Security Foundation (OSSF). OSV also consists of a reference infrastructure and tooling (OSV-Scanner).

[Learn more about OSV ›](https://ubuntu.com/security/osv)

#### OVAL

Ubuntu OVAL uses the OVAL vulnerability and patch definitions to enable auditing for Common Vulnerabilities and Exposures (CVEs) and to determine whether a particular patch, via an Ubuntu Security Notice (USN), is appropriate for the local system.

Ubuntu OVAL also allows for any third-party Security Content Automation Protocol (SCAP) compliant tools to accurately scan an Ubuntu system or an official Ubuntu cloud image for vulnerabilities.

[Learn more about OVAL ›](https://ubuntu.com/security/oval)

#### Open source catalogs

Open source catalogs are curated repositories of vetted software components, created with the intent of providing a centralized, trusted source of software for developers and enterprises. Open source catalogs function as an organized inventory that simplifies software discovery while ensuring that all included components meet specific standards for quality and licensing.

These catalogs are critical because they act as a "first line of defense" in supply chain security, filtering out malicious or unmaintained code before it can be integrated into a production environment.

With Ubuntu, Canonical offers a vast collection of software components, organized into a set of official repositories:

{{ text_list_kh(
  items=[
  "Main – Officially supported, open source software",
  "Restricted – Officially supported, closed source software",
  "Universe – Community-maintained, open source software, with maintenance through Ubuntu Pro",
  "Multiverse – Varying support, license-restricted, or patented software",
]) }}

Through Ubuntu Pro, all of the packages in Ubuntu Universe get security maintenance from Canonical as well as packages in Ubuntu Main, giving users a centralized, tiered, and cryptographically-verifiable ecosystem of software to use with confidence.

[Learn more about Ubuntu Pro ›](http://www.ubuntu.com/pro)

## Third-party risk management

Besides commonly used solutions like open source catalogs, security scanners and SBOMs, all organizations who want to ensure the integrity of their software supply chain need to perform third-party risk management.

### What is third-party risk management (TPRM)?

Third-party risk management (TPRM) is the structured, continuous process of identifying, assessing, and mitigating the risks that arise from an organization's reliance on external parties, vendors, and suppliers for goods, services, or software components. TPRM is critical to supply chain security because of the external nature of these vendors. When a third party suffers a breach, their customer might also suffer a breach, which makes TPRM a core component of overall cybersecurity and operational resilience.

### What are the most important processes in third-party risk management?

#### Risk identification and assessment

This step involves defining and assessing the risk posed by each external partner. It requires classifying suppliers based on the criticality of the service they provide and the sensitivity of the information they handle. Organizations must maintain an explicit inventory of all third parties, their dependencies, and the business impact if they fail.

#### Due diligence and contracting

TPRM requires embedding security controls directly into the legal and contractual relationship with vendors. This means defining clear security requirements for the supplier and ensuring they are contractually obligated to meet necessary standards. Organizations must verify the vendor’s compliance with internal and external regulations.

#### Monitoring and remediation

TPRM requires continuous monitoring, even after a contract is signed. This involves ongoing oversight of the vendor's security posture over time, looking beyond simple certificates to assess real-world performance. Collaboration is essential for developing rapid, coordinated remediation and incident response plans to mitigate the spread of a software supply chain attack originating from a vendor.

## Trusted sources - How Canonical and Ubuntu can help

### Trusted open source

Canonical enables you to simplify your open source software supply chain, providing oversight of software vulnerabilities and remediation, as well as compliance automation tools.

Canonical’s comprehensive security maintenance subscription, Ubuntu Pro, provides access to large repositories of security maintained open source packages, giving your team a trusted open source catalog.

[Learn more about vulnerability management in Ubuntu ›](https://ubuntu.com/security/vulnerability-management)
[See what’s included in Ubuntu Pro ›](https://ubuntu.com/pro)

### A certified and compliant OSS vendor

Canonical provides a Trust Center to support transparency and security for its users. This center offers access to Canonical's important security certifications.

Canonical continually demonstrates its security- and audit-ready status, either through achieving certification or through helping organizations meet security standards and compliance requirements.

[Visit Canonical’s trust center ›](https://trust.canonical.com/)

### Helping you comply with security standards and regulations

Canonical assists many organizations with meeting many different mandatory laws or legal requirements, including:

{{ text_list_kh(
  items=[
  "EU CRA (The EU Cyber Resilience Act)",
  "HIPAA",
  "FedRAMP (Federal Risk and Authorization Management Program)"
]) }}

Canonical also offers tooling that helps you to apply the configurations needed to meet standards such as:

{{ text_list_kh(
  items=[
  "CIS Benchmarks (Center for Internet Security Benchmarks)",
  "DISA STIG (Defense Information Systems Agency Security Technical Implementation Guide)",
  "PCI DSS (Payment Card Industry Data Security Standard)",
  "OpenSSF Principles for Package Repository Security"
]) }}

[Learn more about security standards ›](https://ubuntu.com/security/security-standards)
