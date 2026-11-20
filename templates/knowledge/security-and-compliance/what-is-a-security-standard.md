---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Security and compliance"
  tag: "Compliance"
  title: "What is a security standard?"
  breadcrumb: "What is a security standard?"
  description: "Explains what security standards are, and why they are relevant."
  copydoc: "https://docs.google.com/document/d/1x_OaXJ4esHzn7CYICrHRr9yHFpRmwRcmJaWI9BPfX_c"
  hero_title: "What is a security standard?"
  cta:
    description: "Implement comprehensive security for your Ubuntu deployments."
    buttons:
      - text: "Contact us"
        url: "https://ubuntu.com/security/contact-us"
        type: "button"
        variant: "positive"
      - text: "Explore security standards supported by Ubuntu Pro ›"
        url: "https://ubuntu.com/security/security-standards"
        type: "link"
  blog:
    title: "Latest from our blog"
    id: 1228
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}

A security standard is a formal document that details how to build and maintain secure software systems. Security standards provide a common, auditable understanding of IT security best practices.

In this article, you’ll learn how Ubuntu Pro helps organizations meet their compliance requirements for many of the most widely-used standards.

## Security standards: an overview

Security standards are formal documents produced by government or industry bodies that describe in detail how to build and maintain software systems securely. The aim of security standards is to give everyone a common understanding of the expectations around IT security. This gives producers and consumers of software a consistent mechanism to assess system security and implement minimum security thresholds, as well as providing a consistent baseline for auditors to make their assessments against.

### What is the purpose of a security standard?

When building or deploying software, “being secure” is everyone’s goal. However, this goal is vague: without a specific definition, every organization would have their own version of “being secure”, making it impossible for users or customers to know if a system is actually safe and their data is protected.

Security standards are the documents that solve this. They define how security should be implemented, in terms that are generic enough to apply across different organizations, and in ways that are specific enough to be auditable.

### What do security standards entail?

While some security standards describe how to implement specific technologies (such as the FIPS 140 cryptography standard), most will detail how an organization should implement a complete security management program. For example, standards such as ISO27001, SOC2, [FedRAMP](https://ubuntu.com/security/fedramp), [CMMC](https://ubuntu.com/security/cmmc), and [NIS2](https://ubuntu.com/security/nis2) cover all the steps an organization needs to take to ensure that security is built into their policies and procedures, and that security risks are being adequately assessed throughout the organization.

When working with security standards, it is important to engage with an external auditor and demonstrate to potential customers and users that your organization has correctly implemented the controls and measures laid out in the standards.

### What are some examples of security standards?

There are myriad international, regional, and industry standards that have been published. Some of the more widely-known standards include:

{{ text_list_kh(
  type="bullet",
  items=[
  "ISO/IEC 2700X - a family of standards that offers a universal structure for creating, executing, and refining an Information Security Management System (ISMS) to assess and manage IT security risks. These standards are widely recognized and adopted around the world.",
  "NIST SP 800-171 - a US standard that outlines the necessary controls to safeguard Controlled Unclassified Information (CUI) within non-federal environments, which establishes rigorous criteria for any entity managing sensitive federal data. Adherence to these guidelines is typically mandatory for securing federal contract opportunities.",
  "<a href=\"https://ubuntu.com/security/pci-dss\">PCI-DSS</a> - a comprehensive framework for securing sensitive cardholder information within organizations processing payment data, with the intention of strengthening data protections and mitigating the risks of financial fraud.",
  "<a href=\"https://ubuntu.com/security/nis2\">NIS2</a> - a European Union cybersecurity framework of security requirements for a wide range of critical industries, designed to strengthen the resilience of the EU's digital infrastructure.",
  "<a href=\"https://ubuntu.com/security/fips\">FIPS 140</a> - a NIST standard for implementing and using cryptography securely.",
  "<a href=\"https://ubuntu.com/security/disa-stig\">DISA-STIG</a> - a US framework for configuring and hardening software systems.",
  "<a href=\"https://ubuntu.com/security/fedramp\">FedRAMP</a> - based on the NIST SP 800-53 standard, achieving FedRAMP Authority To Operate is required in order to offer cloud services to the US Federal Government marketplace."
]) }}

[Get a full breakdown of the most important security standards ›](https://ubuntu.com/security/security-standards)

### Security standards vs compliance frameworks

Compliance frameworks and security standards are all part of the same family of publications, varying only in the level of technical details they contain. Compliance frameworks, like the widely-used NIST CSF, focus on more high-level alignment. They help organizations map security practices with legal, regulatory, or business goals. Security standards such as FIPS 140 are prescriptive sets of technical or operational rules. They tell you exactly how to implement, configure, and manage technology to achieve a specific level of security.

### How does Canonical help with security standards?

Many of these security standards are wide-ranging cybersecurity frameworks that touch almost every aspect of an organization. In most cases, it’s not simply a case of deploying a certain product or piece of technology in order to become compliant. However, where standards do set specific technology requirements, there are three areas where Ubuntu Pro can help you meet these standards: vulnerability patching, system hardening, and asset management.

Every security standard will require security vulnerabilities, or [CVEs](/knowledge/security-and-compliance/what-is-a-cve), to be patched in a timely manner. Ubuntu Pro extends support for Ubuntu LTS releases to up to 15 years, with Canonical directly patching and maintaining the open source packages in Ubuntu. 

Another key requirement that’s common across almost all standards is around deploying and maintaining software in a known-good secure configuration. Ubuntu is a versatile platform that can be used in a wide range of environments, but when it comes to strict security standards, many organizations turn to industry benchmarks for secure configurations, such as CIS or DISA-STIG. Ubuntu Pro includes the USG (Ubuntu Security Guide) tool which can harden Ubuntu systems in accordance with these profiles, and audit them on an ongoing basis.

All security standards will demand that an organization is aware of its IT assets and manages these appropriately. For this, Ubuntu Pro includes [Landscape](https://ubuntu.com/landscape), a systems management tool for tracking and managing Ubuntu systems at scale. Landscape includes the ability to assess systems for CVE risks and prioritize deploying fixes, as well as hardening and auditing Ubuntu systems using USG profiles.
