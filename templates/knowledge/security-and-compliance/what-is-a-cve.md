---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Security and compliance"
  publish_date: 2026-07-13
  tag: "Security"
  title: "What is a CVE?"
  breadcrumb: "What is a CVE?"
  description: "Understanding the Common Vulnerabilities and Exposures (CVE) system is key to security. Learn how CVEs are scored, categorized, and managed by Canonical."
  copydoc: "https://docs.google.com/document/d/1NBwrYlWd-ecv4WQ-RUVvk6Z0WcLnUq2y8N3tJuKHhbQ"
  hero_title: "What is a CVE?"
  cta:
    description: "Learn more about how to track and mitigate CVEs in your software and in the Ubuntu ecosystem. Explore our guides for vulnerability management."
    buttons:
      - text: "Explore our security"
        url: "https://www.canonical.com/solutions/open-source-security"
        type: "button"
        variant: "positive"
      - text: "Discover Ubuntu Pro"
        url: "https://www.ubuntu.com/pro/why-pro"
        type: "button"
      - text: "Get a comprehensive guide to vulnerability management &rsaquo;"
        url: "https://ubuntu.com/engage/vulnerability-management"
        type: "link"
  blog:
    title: "Latest from our blog"
    id: 4195
---

CVE stands for Common Vulnerabilities and Exposures.  The CVE system is used to identify, define, and catalog publicly disclosed cybersecurity vulnerabilities, giving them clear identity for wider awareness, tracking, and remediation.
In this article, you’ll get an in-depth explanation of what CVEs are, how they are scored, and how to manage and remediate CVEs on Ubuntu.


## Understanding CVEs

The CVE List is one of the oldest and most widely used registries of publicly disclosed security vulnerabilities. It contains thousands of CVE records. A CVE record consists of a CVE ID and metadata: description, scores, list of affected products (including Common Platform Enumerations and package URLs), and more.

When someone discovers a vulnerability in a software package, it is often assigned a unique CVE ID (for example, [CVE-2021-44228](https://ubuntu.com/security/CVE-2021-44228)). This creates a common language for professionals to track and fix issues across different tools and platforms.

Sometimes, CVE records are better known by unofficial nicknames. For example, CVE-2021-44228 is more widely recognized as “Log4Shell”; other famous examples include Heartbleed, GHOST, Shellshock, and BlueKeep.   
It’s important to note that while terms like “vulnerability” are sometimes used interchangeably with “CVE,” these concepts are different and do not always refer to the same entities.

### What is the difference between CVEs and vulnerabilities?

A vulnerability is a fundamental flaw or specific weakness in code or system design that could be exploited by a threat actor to gain unauthorized access or perform malicious actions.

In contrast, a CVE record is an official categorization for a specific, publicly disclosed vulnerability. It is marked with a unique, alphanumeric identity number that is used to track, communicate, and catalog that vulnerability across the tech industry.

In general, all CVEs are vulnerabilities, but not all vulnerabilities are CVEs.

[Learn more about CVEs in detail  &rsaquo;](https://ubuntu.com/security/cves/about)

## How are CVEs created?

CVE Numbering Authorities (CNAs) publish CVE records in a structured process.

1. Reporting: The researcher reports a discovered vulnerability to the software maintainer or a CNA (like Canonical for Ubuntu-related issues).
2. Verification: The CNA will publish a record after another entity has confirmed  the report is a genuine security vulnerability.
3. Reservation: The CNA reserves a CVE ID from the CVE List.
4. Public disclosure and entry:  The CNA publishes the CVE record in the CVE List. The CVE record contains details about the vulnerability, such as affected products, scores, etc.

## How are CVE records scored?

Vulnerabilities are often scored using the Common Vulnerability Scoring System (CVSS) framework. This framework assigns a numerical score from 0.0 to 10.0, where 10.0 represents the highest level of severity. The current standard, CVSS v4.0, attempts to provide an accurate assessment of a CVE record’s:

* Base metrics
* Threat metrics
* Environmental metrics
* Supplementary metrics

### Base metrics

The base metric group evaluates the intrinsic qualities of a vulnerability that generally remain constant over time and across different user environments. This group is split into two categories: exploitability and impact.

* Exploitability metrics assess the difficulty of the attack, looking at factors like the attack vector (network vs. local), attack complexity, and whether a user must interact with the system for the exploit to work.
* Impact metrics measure the potential damage to the confidentiality, integrity, and availability for both the vulnerable system and any subsequent systems that might be affected by a successful exploit.

### Threat metrics

This group primarily focuses on exploit maturity. This tracks whether a vulnerability is being actively attacked in the wild, if only a theoretical proof-of-concept exists, or if there are no reported exploits at all. It should be noted that this metric can change over time.

If the vulnerability is being exploited, or if exploit kits are known to exist in the public, then the threat level – and therefore the final score – increases to reflect the heightened urgency.

### Environmental metrics

A vulnerability's risk varies depending on its context; for example, a bug on an internet-facing web server is more dangerous than the same bug on an isolated internal machine. Environmental metrics allow an organization to customize the score based on their specific infrastructure, security requirements, and other such contexts.

Environmental metrics are generally meant to be specified by a consumer of the CVSS score (an end user). Existing mitigations, such as firewalls or mandatory access controls, may lower the practical severity of the flaw within a specific network.

### Supplemental metrics

Introduced in CVSS v4.0, the supplemental metric group provides additional context without directly altering the numerical score. These metrics describe extrinsic attributes that help security teams prioritize remediation based on their specific needs. Examples include whether an attack can be automated at scale, the recovery effort required after a successful breach, and the safety impact, which is particularly critical for industrial or medical environments where a software flaw could pose a direct risk to human life.

## Why do some CVEs have nicknames?

CVE names bridge the gap between a dry technical record and public awareness. While a standard ID like CVE-2014-0160 is perfect for a database, it sometimes doesn’t capture the attention of non-technical stakeholders. By giving a CVE a name (such as Heartbleed or Log4Shell), researchers can more clearly communicate about a specific vulnerability with media, government agencies, and companies.

A bug is more likely to get a name if it:

* Affects a near-universal software component (like OpenSSL or Bash)
* Has been "hidden in plain sight" for decades
* Requires an industry-wide effort to coordinate a fix

### Are named CVEs more dangerous?

A CVE with a name is not automatically or implicitly more dangerous than unnamed CVEs, because a name is a measure of notoriety and not of technical danger. While many named CVEs are indeed severe, there are thousands of unnamed CVEs with a perfect 10/10 "Critical" rating that never receive a catchy title.

Instead, the severity of a vulnerability is indicated by its assessment, such as its CVSS score.

There is another class of vulnerabilities called Zero-Day vulnerabilities. These represent vulnerabilities known to a threat actor and possibly exploited prior to the software vendor becoming aware of the flaw and distributing security updates or mitigations. The ‘Zero-Day’ label does not indicate any information about severity, as it can be applied to any vulnerability, irrespective of its exploitability or impact. As such, a risk evaluation needs to be based on an appropriate assessment of the vulnerability, rather than on the ‘Zero-Day’ label.

## How does Canonical assess CVEs?

CVE scoring can be very useful for prioritizing and triaging a response, but only if the CVE score is accurate to your specific environment. A "Critical" CVSS score would still be assigned to a vulnerability that is mitigated by default in a particular distribution through intrinsic security controls, such as compilation hardening. But this does not mean the vulnerability should be prioritized before a non-mitigated one with a “High” CVSS score. For this reason, many vendors supplement CVSS scores with additional prioritization criteria.

Canonical assesses CVEs and newly discovered vulnerabilities using its own matrix of priority levels. In this process, the Ubuntu Security team reviews new vulnerabilities when they are identified. If they affect packages distributed with supported Ubuntu releases, the team evaluates the impact and assigns a priority level.

These priority levels are distinct from other published severity levels such as CVSS scores.

Ubuntu Priority assesses factors like severity, estimated number of affected users, software configuration, active or likelihood of exploitation, and more, to judge the relative importance of the CVE on the Ubuntu ecosystem. The Ubuntu Priority does not implicitly convey risk, just like a CVSS score does not convey risk.

The matrix scores vulnerabilities across 5 levels of severity. These are:

* Critical: A very damaging problem, typically exploitable for nearly all users in a default installation of Ubuntu. Includes remote root privilege escalations, remote data theft, and massive data loss.
* High: A significant problem, typically exploitable for nearly all users in a default installation of Ubuntu. Includes serious remote denial of service, local root privilege escalations, local data theft, and data loss.
* Medium: A significant problem, typically exploitable for many users. Includes network daemon denial of service, cross-site scripting, and gaining user privileges.
* Low: A security problem, but hard to exploit due to the environment, requires a user-assisted attack, has a small install base, or does very little damage. These tend to be included in security updates only when higher priority issues require an update or if many low priority issues have built up.
* Negligible: Technically a security problem, but only theoretical in nature, requires a very special situation, has almost no install base, or does no real damage. These typically will not receive security updates unless there is an easy fix and some other issue causes an update.

The assigned priority of a CVE impacts what actions Ubuntu Security Engineers will take. These actions will be communicated though Statuses, which are communicated in every package.

[Learn more about how Ubuntu Security engineers prioritize CVEs  &rsaquo;](https://ubuntu.com/blog/securing-open-source-through-cve-prioritisation)

While not its primary design purpose, the Ubuntu Priority can be used by Ubuntu users to prioritize remediation, but not in isolation. The information in the [Ubuntu CVE Tracker](https://ubuntu.com/security/cves) can aid in this assessment. When the assigned Priority is High or above in priority, the tracker will include an explanation for the priority, such as for [CVE-2026-42765](https://ubuntu.com/security/CVE-2026-42765).

### What are Ubuntu CVE statuses?

When a new vulnerability is disclosed by Ubuntu security engineers, they provide statuses for every package in every supported version. The status provides important information about the vulnerability to users.

For example, a vulnerability could be listed as “Needs Evaluation”, “Not affected”, “Vulnerable”, “Fixed”, and more.

[Learn more about CVE reports in Ubuntu  &rsaquo;](https://ubuntu.com/security/cves)

## How does Canonical help with managing CVEs?

Canonical bridges the gap between the global security community and the open source software you use, transforming raw vulnerability data into verified, actionable patches for your environments.

### Expert assessment and triaging

The Ubuntu Security Team reviews every incoming CVE to determine its actual risk within the Ubuntu ecosystem and Canonical’s broader portfolio, providing tailored prioritization and stable fixes.

The team assigns an Ubuntu-specific priority (Negligible to Critical) that accounts for built-in OS mitigations like AppArmor or compiler hardening.

### Security information and tooling

Canonical delivers security intelligence via Ubuntu Security Notices (USNs) in both [human-friendly](https://ubuntu.com/security/notices) and machine-readable formats ([OVAL](https://ubuntu.com/security/oval), [OSV](https://ubuntu.com/security/osv), [VEX](https://ubuntu.com/security/vex)). The machine-readable formats are often consumed by third-party scanners, increasing their report accuracy and reducing false positives in your audits.

### Security maintenance and support

Canonical provides security fixes and maintenance for five years with every Ubuntu LTS. Canonical also backports security patches to older LTS releases, allowing you to close vulnerabilities without the operational risk or instability of a major version upgrade.

While standard support covers "Main" packages, Ubuntu Pro significantly expands your security coverage:

* **Universe Coverage:** Security maintenance for thousands of open source packages, including popular stacks like PHP and Python.
* **Extended Lifecycle:** Up to 15 years of security maintenance through ESM and the Legacy add-on, protecting aging infrastructure long after community support ends.

[Learn more about Ubuntu Pro &rsaquo;](https://www.ubuntu.com/pro)

### Zero-downtime patching for selected critical and high kernel CVEs

Canonical Livepatch eliminates the trade-off between security and uptime by delivering kernel fixes while the system runs, allowing immediate remediation of high-risk kernel CVEs without a system reboot.

[Read about livepatch &rsaquo;](https://ubuntu.com/security/livepatch)

### Compliance automation, hardening tools, and profiles

Ubuntu Pro enables compliance with CIS and DISA-STIG benchmarks, through the Ubuntu Security Guide and Landscape. These tools enable fleet-wide auditing, remediation, and monitoring for configuration drift from a single interface.

The ecosystem supports federal standards with FIPS 140-3 certified modules and continuous and automated patching.