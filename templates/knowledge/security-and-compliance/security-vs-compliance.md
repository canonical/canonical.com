---
wrapper_template: "knowledge/_base_kh_markdown.html"
context:
  title: "Security vs compliance: what's the difference?"
  breadcrumb: "Security vs compliance: what's the difference?"
  description: "Understand the difference between security and compliance, and explore how they work together to protect your organization. Learn about security controls, frameworks, compliance standards, and assurance."
  cta:
    description: "Ensure your organization meets security and compliance requirements."
    buttons:
      - text: "Learn about Ubuntu Pro"
        url: "https://ubuntu.com/pro"
        type: "button"
        variant: "positive"
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}

Security and compliance are two sides of the same coin, and are sometimes used interchangeably. But they are different things. While security concerns the technical work required to mitigate security risks, compliance is about providing the proof that this work is not just completed, but undergoing continuous improvement.

## How do compliance and security intersect?

The difference between compliance and security is that security is the technical implementation and continuous activities needed to reduce security risks to an acceptable level, whereas compliance is the proof that these practices or activities have been implemented in ways that meet a required standard.

Security and compliance have a symbiotic relationship. Security is about keeping the organization, its assets, and its users or consumers safe, while compliance is about proving that the organization has followed the rules for keeping systems, users, consumers, or the organization itself safe. In some cases, some security measures will work both to reduce organizational risk and will be required by regulations.

The intersection is critical, because security and compliance are interdependent: without proper security measures, a company will not be able to meet regulatory standards for its systems or services; and without clear compliance requirements, a company will not understand the minimum security actions required to meet the necessary standard.

## What is security compliance?

In information systems, security compliance is the continuous process of aligning an organization's systems and practices with a mandatory set of rules, standards, and regulations. 

Security compliance demonstrates an organization's level of alignment with the technical and administrative controls necessary to protect data and maintain trust, as prescribed by external bodies, mandatory legal requirements (like GDPR or HIPAA) or internal policies. 

The primary goal of security compliance is to ensure the implementation of a minimum security baseline as mandated by legal, government, or industry requirements to operate safely.

### How do you achieve security compliance?

In order to achieve the status of security compliance, you need to ensure that your software, services, and organization meet the requirements stipulated in security standards, such as FedRAMP or ISO27001. 

Meeting security compliance involves several steps:

{{ text_list_kh (items=[
  "Following a security framework",
  "Implementing security controls",
  "Developing security features",
  "Obtaining security assurance",
  "Obtaining a certificate of conformity or other such recognition that you meet the required security standards"
])}}

## Security controls, frameworks and features

Security controls, security frameworks, and security features are different but interdependent components of a robust cybersecurity strategy needed to obtain security compliance.

### What are security controls?

Security controls are the specific actions, mechanisms, or tools put in place to protect assets and mitigate risk. They are the tactical actions you take to secure your systems and services against cyberincidents.

### What are security frameworks?

Security frameworks are the structured sets of guidelines, policies, and processes that tell you which controls to use and how to organize them to achieve a defined security baseline. They are the strategic blueprints that the organizations can follow to build a strong security foundation.

### What are security features?

Security features are the specific safeguards, tools, or mechanisms built into hardware, software, or system, that protect assets, prevent unauthorized access, detect threats, and maintain data integrity. Security features are capabilities of systems through which security controls are implemented.

Examples of security features include: 

{{ text_list_kh (items=[
    "Access and authentication",
    "Data protection",
    "Cryptography",
    "Logging and monitoring"
]) }}


[Read our compliance automation documentation](https://ubuntu.com/compliance)

## What is security assurance?

Security assurance refers to the degree of confidence that the security controls and mechanisms that are embedded within a system, product, or service are implemented correctly, function as intended, and are effective at meeting security requirements and protecting assets. 

It is a process that focuses on providing evidence and validation, effectively shifting the perspective from implementing security (the job of the engineers) to demonstrating security (the job of the auditors and compliance teams).

[Read about Ubuntu security assurances](https://ubuntu.com/security/assurances)

### What are the key components of security assurance?

Security assurance is established through a continuous combination of measurement, review, and verification activities.

#### Verification and validation

Verification and validation ensure that the product is being built correctly, and that the end product meets the requirements set out at the start of the development process.

#### Testing and auditing

Testing and auditing involves active scrutiny of the system to test whether it holds up to external attacks, breach attempts, or other attack vectors or stressful operating conditions. This could include penetration testing, vulnerability scanning, or code review.

#### Documentation and certification

Documentation and certification provide measurable proof of assurance. This includes having detailed documentation on the policies, standards, procedures, inventories, that are output from activities (risk assessments, scans), that demonstrate that the system meets established security standards like ISO 27001 or FedRAMP, or attestations from third-parties that the software operates securely.

### Assurance vs. security vs. compliance

While the terms assurance, security, and compliance are related in IT and Information Systems, they each represent different phases of risk management, and together they make up a robust risk management strategy in software development. Security builds the protection, compliance sets the rules for the protection, and assurance proves the protection actually works.

#### Security

Security refers to the action of protecting assets through the implementation of security features, such as installing a firewall or encrypting data at rest.

#### Compliance

Compliance refers to the rule or standard you must follow. For example, PCI DSS requires that you use a firewall.

#### Assurance

Assurance refers to the confidence that the security feature has been configured correctly and that it operates as intended under different environments. For example, in PCI DSS, assurance would demonstrate that a firewall has been configured correctly, that it blocks the right traffic, and that it has been tested to withstand current attacks.

[Read about Canonical's approach to open source security](https://canonical.com/solutions/open-source-security)

## What are security standards?

Security standards are documents that define how security should be implemented in generic enough terms that are applicable across different organizations. They vary in detail from very prescriptive to more flexible frameworks.

Security standards serve as the technical specifications or auditable criteria that operationalize the high-level guidance found in security frameworks.

## What are some examples of security standards?

There are a great number of international and regional security standards, as they can be issued by government agencies (NIST) or industry bodies (PCI Security Standards Council), but the most well-known international standards include:

{{ text_list_kh (items=[
  "Federal Information Processing Standards (FIPS), eg FIPS 140-3",
  "Payment Card Industry Data Security Standard (PCI-DSS)",
  "United Kingdom Cyber Essentials (UK Cyber Essentials)",
  "ISO 27001"
])}}

[Learn more about Ubuntu and security standards](https://ubuntu.com/security)

## How does Canonical help to achieve security and compliance?

Canonical is a leading provider of open source security for a number of reasons, including a 20-year track record in open source and strong collaboration with upstream communities and vulnerability scanning tools. 

We make security and compliance easy by bundling security maintenance, compliance features and support for our entire portfolio in a convenient subscription: [Ubuntu Pro](https://ubuntu.com/pro).

### A trusted development platform

Ubuntu is a trusted platform used in millions of production environments and devices. Ubuntu Pro is a subscription on top of Ubuntu that helps organizations empower their developers to use all the open source available in Ubuntu repositories in a secure, compliant and fully supported manner.

### Security patching and systems management

Ubuntu Pro includes security maintenance for up to 15 years for both the OS and thousands of open source packages. The subscription also includes Livepatch, which offers rebootless security patching automation to address high and critical kernel vulnerabilities that surface between scheduled maintenance windows. Access to Landscape enables centralized administration and fine-grained control over security updates for large Ubuntu estates.

### Hardening and compliance automation

Ubuntu Pro is designed to simplify your security compliance burden for standards and regulations such as NIST CSF, FedRAMP, PCI-DSS, ISO27001, or CIS Benchmarks. Users also benefit from FIPS-certified cryptographic modules, and automated system hardening for CIS Benchmarks and DISA-STIG, and can be deployed on-premise or in the public cloud.

The default configuration of Ubuntu balances usability and security. However, systems carrying dedicated workloads can be further hardened to reduce their attack surface. Canonical provides the Ubuntu Security Guide, an application that automatically hardens systems to DISA STIG and CIS Benchmarks profiles, and generate audit reports, allowing you to deploy workloads that need to operate under strict compliance regimes.