---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "System hardening"
  publish_date: 2026-11-19
  tag: "Hardening"
  title: "What is system hardening?"
  breadcrumb: "What is system hardening?"
  description: "Explains what system hardening is, and when it is relevant."
  hero_title: "What is system hardening?"
  copydoc: "https://docs.google.com/document/d/1hCCI7ejvqflPZBdVSG28FjnZ8PPoNK5UciUJ96Avaw8/edit?tab=t.x7cfqmsm1i2g"
  cta:
    title: "Find out more"
    description: "Talk to Canonical’s team of security and compliance experts to learn how Ubuntu Pro can support your security hardening journey."
    buttons:
      - text: "Contact us"
        url: "https://ubuntu.com/security/contact-us"
        type: "button"
        variant: "positive"
      - text: "Download our hardening guide"
        url: "https://ubuntu.com/engage/a-guide-to-infrastructure-hardening"
        type: "button"
      - text: "Read a blog for hardening best practices ›"
        url: "https://ubuntu.com/blog/what-is-system-hardening-definition-and-best-practices"
        type: "link"
  blog:
    title: "Latest from our blog"
    id: 1228
---
{% from "macros/_macros-lite-video.jinja" import lite_video %}

System hardening means locking down a system and reducing its attack surface by removing unnecessary software packages, securing default values to the tightest possible settings and configuring the system to only run what you explicitly require. This article explains hardening in more detail, and outlines when you might need to do this on Linux operating systems like Ubuntu.

## System hardening explained

System hardening is a foundational security practice. The definition of system hardening is the reduction of an IT system’s vulnerability by minimizing its attack surface. This is achieved by removing unnecessary components, closing unused ports, and applying strict configuration settings to hardware, operating systems, and applications. The primary goal is to ensure that only the essential services and functions required for production workloads remain active, thereby limiting potential entry points for attackers.

## When is system hardening required?

Software systems such as Ubuntu have a myriad of configuration options and are generally designed to be flexible and usable in as wide a range of applications as possible, from small devices and refrigerators, to data centers and satellites. Each of these environments has a different risk profile and handles different types of data.

Hardening is essential for any organization operating critical IT infrastructure, but is particularly vital when handling sensitive user data, including financial details or personally identifiable information (PII). In addition to severe reputational fallout from public security incidents, failure to safeguard this data can trigger substantial regulatory penalties and compliance fines.

It’s up to system architects and administrators to determine the risk profile of their IT assets and make appropriate technology choices. However, many industries and operating environments are governed by regulatory requirements, and system hardening is mandated by government standards such as NIST SP800-53/171 & FedRAMP in the US, the EU CRA, and in many industries such as PCI-DSS for financial data processors.

## The system hardening process

The hardening process begins at the hardware level, where measures like enabling Secure Boot, setting BIOS passwords, and using full-disk encryption help protect against physical and low-level tampering. Once the hardware is secured, you move to operating system hardening, which focuses on tightening default configurations, maintaining rigorous user access management, enforcing encryption, and implementing proactive measures like continuous logging, file integrity monitoring, and rapid, automated patching to address known vulnerabilities.

Application-level security builds upon these hardened foundations by enforcing strong encryption standards (such as TLS), adhering to the principle of least privilege, and monitoring application logs for anomalous behavior. Additionally, it is critical to manage the [software supply chain](https://canonical.com/knowledge/security-and-compliance/what-is-software-supply-chain-security) by sourcing components from trusted providers and regularly scanning third-party libraries for vulnerabilities, as dependencies often represent a significant risk factor in complex software environments.

{{ lite_video(
 video_id="HltKHtH5Dv4",
 video_title="System hardening explained"
) | safe }}

## Independent industry expertise

Because system hardening is so important to so many organizations, industry standards have been developed to gather the best practices from across the world and formulate a common approach to hardening that is independent from the software producers.

The [Center for Internet Security (CIS)](https://www.cisecurity.org/) publishes hardening benchmarks for many common software applications and operating systems, including Ubuntu, and if you implement the suggestions in these hardening profiles then you can be assured of a comprehensive level of security. [CIS benchmarks](https://ubuntu.com/security/cis) have broad applicability across the world, and are seen as the gold standard for a wide range of industries including financial services, telecommunications companies and critical national infrastructure.

Within the US, the DoD (Department of Defense) publishes a set of similar benchmarks -- DISA-STIGs -- derived from the security controls specified in the NIST SP800-53 standard. These are mandated in many Federal deployments, including [FedRAMP](https://ubuntu.com/security/fedramp) and [CMMC](https://ubuntu.com/security/cmmc). STIGs are published for a wide range of common operating systems and applications, including Ubuntu. These guides are similar in scope and intention to the CIS benchmarks.

## How does Canonical help with system hardening?

Hardening benchmarks such as CIS or the DISA-STIG comprise hundreds of individual customizations and configuration steps. Implementing these manually would be especially tedious and error prone, particularly for organization with large device estates.

To simplify this process, Canonical provides USG – the [Ubuntu Security Guide](https://ubuntu.com/security/certifications/docs/usg) – a tool that automates the hardening process. USG bundles profiles for both CIS and DISA-STIG, and includes the ability to customize the hardening profiles based on individual deployment requirements. USG can both harden a system as well as run audits to ensure the configuration remains compliant, with human- and machine-readable reports.
