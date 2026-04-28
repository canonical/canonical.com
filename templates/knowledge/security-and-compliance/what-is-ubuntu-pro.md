---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Security and compliance"
  tag: "Ubuntu Pro"
  title: "What is Ubuntu Pro?"
  breadcrumb: "What is Ubuntu Pro"
  description: "Learn what’s included in Ubuntu Pro, Canonical’s comprehensive subscription for open source security, support, and compliance. Get info on its costs and features."
  copydoc: "https://docs.google.com/document/d/1wd1QsGDUoewkSEJ0WDANYPqTvdBoH-_JYgYTQn7gvWM"
  hero_title: "What is Ubuntu Pro?"
  cta:
    buttons:
      - text: "Talk to an expert"
        url: "https://ubuntu.com/contact-us/form?product=pro"
        type: "button"
        variant: "positive"
      - text: "Get Ubuntu Pro"
        url: "https://ubuntu.com/pro/subscribe"
        type: "button"
      - text: "Learn more about Ubuntu Pro ›"
        url: "https://ubuntu.com/pro"
  blog:
    title: "Latest from our blog"
    id: 3586
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}

Ubuntu Pro is Canonical’s comprehensive subscription for open source security, support, and compliance. Learn what's included in an Ubuntu Pro subscription, from 15-year security maintenance to 24/7 technical support and automated hardening tools for IT admins.

## What does Ubuntu Pro do?

Ubuntu Pro is a security and compliance subscription that provides timely patches and security maintenance for the operating systems, applications, and other layers of IT operations. It helps enterprises and their engineers to secure their software and systems, and creates an easier path to meeting security standards compliance through hardening tools, automations, and a range of other features.

[Learn more about Ubuntu Pro ›](http://www.ubuntu.com/pro)


### How does Ubuntu Pro differ from standard Ubuntu?

It is a common misconception that Ubuntu Pro is a different version or a separate operating system that requires a fresh installation. In reality, there is only one Ubuntu operating system. Ubuntu Pro is an additional layer of services and a security subscription that can be toggled on or off within any existing Ubuntu LTS (Long Term Support) installation. When you upgrade to Ubuntu Pro, you are not changing your OS – you are simply attaching your machine to a subscription that unlocks expanded security maintenance and enterprise-grade maintenance tools.

### Is Ubuntu Pro mandatory for using Ubuntu?

No, Ubuntu Pro is not mandatory for using Ubuntu. Ubuntu remains an open source operating system that is free to download and use. You can continue to run standard Ubuntu LTS (Long Term Support) without a subscription for as long as you like. Standard LTS provides five years of free security maintenance for the Main repository, which covers the core OS.

Ubuntu Pro should be treated as an optional security and compliance subscription that sits on top of your existing OS. It doesn't replace your current Ubuntu installation, it simply unlocks additional security features and patches that aren't included in the standard version. While not required, the subscription provides significant advantages like up to 15 years of security maintenance, Kernel Livepatch, compliance automation tools, and fleet management.

## What is included in Ubuntu Pro?

An Ubuntu Pro subscription gives users access to the following:

{{ text_list_kh(
  items=[
  "Security maintenance for the entire tech stack, from OS to infrastructure and applications",
  "Kernel Livepatch automatically applies critical kernel updates in-memory, ensuring security without requiring a system reboot",
  "Centralized fleet management with Landscape",
  "Compliance profiles for the most popular security standards",
  "24/7 break-fix and bug-fix support, available as an add-on (Ubuntu Pro + Support)"
]) }}


### Security maintenance and vulnerability management

Ubuntu Pro automates vulnerability management by providing timely security patches for the entire Ubuntu Archive, covering both the Main and Universe packages. It uses a backporting approach, where security fixes are applied to stable software versions to ensure security without breaking the operating environment's existing behavior.

{{ text_list_kh(
  items=[
  "Ubuntu Pro extends security maintenance from the standard 5 years to 10 years via ESM (Expanded Security Maintenance) and to 15 years with Legacy add-on",
  "Kernel Livepatch automatically applies critical kernel patches in-memory, allowing systems to stay secure without rebooting",
  "Patches are tested and backported by Canonical engineers specifically for LTS releases, reducing the risk of regressions",
  "While patching is largely automated via unattended-upgrades, administrators use the pro client to monitor and manage the system"
]) }}

Here are some commands you could use on your machine:

{{ text_list_kh(
  items=[
  "<code>pro security-status</code>: Shows which packages are missing security updates",
  "<code>sudo pro fix CVE-YYYY-XXXX</code>: Instantly triages and applies the fix for a specific vulnerability",
  "<code>sudo pro enable esm-apps</code> or <code>sudo pro enable livepatch</code>: to enable specific services"
]) }}

[View a complete list of helpful terminal commands ›](https://documentation.ubuntu.com/pro-client/en/latest/references/commands/)


### System hardening

Ubuntu Pro includes the Ubuntu Security Guide (USG), an automated tool designed to harden and audit systems according to industry-standard security benchmarks. Rather than manually configuring hundreds of individual security settings, administrators can use USG to align their systems with CIS (Center for Internet Security) Benchmarks and DISA-STIG (Security Technical Implementation Guides).

The tool provides two primary functions:

{{ text_list_kh(
  items=[
  "It scans your system and generates a detailed HTML or XML report showing exactly where your current configuration fails to meet specific security standards",
  "It can automatically apply the necessary configuration changes, such as tightening file permissions, disabling unused network protocols, or enforcing strict password policies, to bring the system into compliance"
]) }}

### System management

Managing a large fleet of Ubuntu Pro machines is primarily handled through Landscape, Canonical's centralized systems management tool. Landscape allows administrators to manage up to 40,000 machines from a single dashboard. It automates the distribution of security patches, monitors system health, and ensures compliance across physical, virtual, and cloud-based Ubuntu environments. Landscape is available with an Ubuntu Pro subscription.

[Learn more about fleet management with Landscape ›](https://ubuntu.com/landscape)


### Support for public cloud instances (AWS, Azure, or Google Cloud)

Dependencies can present several flaws that can introduce risk into your programs or supply chain. Exploiting such weaknesses can allow attackers to gain unauthorized access, manipulate data, or disrupt services. 

Ubuntu Pro is available for your public cloud instances on AWS, Azure, and Google Cloud marketplaces. Ubuntu Pro + Support can be enabled for all AWS, Azure, and Google Cloud instances through [a custom request to Canonical](https://ubuntu.com/contact-us/form?product=pro).


## Does Ubuntu Pro provide 24/7 "Human-in-the-loop" technical support?

Yes, Ubuntu Pro provides 24/7 "human-in-the-loop" technical support through the Ubuntu Pro + Support tier. This is not chatbot-driven; instead, you interact with experienced human open-source engineers who assist with troubleshooting, "break-fix" scenarios, bug reporting, and other problems.

The 24/7 coverage is specifically designed for mission-critical production environments where downtime has a significant business impact.

{{ text_list_kh(
  items=[
  "Users can open unlimited support tickets or call the support line to speak directly with an engineer",
  "For Severity 1 issues (e.g., the production service is down), Canonical provides a 1-hour initial response SLA and will work with customers continuously until a resolution or workaround is found",
  "In the 24/7 tier, engineers provide regular follow-up updates every few hours to keep customers informed until the incident is resolved"
]) }}

### What are the SLAs for the Ubuntu Pro + Support tier?

The Ubuntu Pro + Support tier complements the security maintenance offering, providing a structured support system designed to meet the varying availability requirements of modern enterprises. While an Ubuntu Pro subscription itself provides the technical foundation for long-term security maintenance, the Ubuntu Pro + Support tier adds direct access to Canonical’s engineering experts. Support is generally divided into two main categories: Weekday Support and 24/7 Support.

The responsiveness of the support team is governed by the severity of the issue, ensuring that critical production failures receive immediate attention while non-urgent requests are handled within reasonable business timeframes.

[Read more about Ubuntu Pro + Support and SLAs here ›](https://ubuntu.com/support)

## How can I get Ubuntu Pro?

Users looking to get Ubuntu Pro can acquire a subscription through Canonical’s online Ubuntu Pro store, or by contacting Canonical’s support services staff. Ubuntu Pro subscriptions are free for personal users on up to 5 machines, and enterprises can try it for free for 30 days.

[Visit the Ubuntu Pro Store ›](https://ubuntu.com/pro/subscribe)

[Contact Canonical for support ›](https://ubuntu.com/contact-us/form?product=pro)


### What does Ubuntu Pro cost?

An Ubuntu Pro subscription typically starts between $25 and $500 per year, depending on the tier and the type of machine you are covering. Free tiers also exist for personal users on a limited number of machines. Support and Legacy can be added on top of your subscription for a fee.

[Explore Ubuntu Pro’s pricing breakdown ›](https://ubuntu.com/pricing/pro)

### What do the different tiers or plans in Ubuntu Pro include?

{{ text_list_kh(
  items=[
  "<strong>Personal:</strong> This tier is designed for individual users, developers, and small-scale home labs. It provides the full technical suite of Ubuntu Pro at no cost for up to 5 machines (or 50 machines for official Ubuntu Community members).",
  "<strong>Enterprise:</strong> This is the standard paid tier for organizations that have their own internal Linux expertise but need enterprise-grade security and compliance tools. It is billed per workstation ($25/year) or per server ($500/year).",
  "<strong>Ubuntu Pro + Support:</strong> This is the highest tier, combining all technical features with direct access to Canonical’s engineering team. It is intended for mission-critical environments where downtime is a high risk. It includes 24/7 or 24/5 \"human-in-the-loop\" support for troubleshooting \"break-fix\" issues.",
  "<strong>Legacy add-on:</strong> Available as an add-on to paid plans, this tier extends the total security maintenance window from 10 years to 15 years."
]) }}

### Is Ubuntu Pro good value for money?

Yes, Ubuntu Pro offers exceptional value by turning high-cost, manual engineering tasks into a predictable and affordable operational expense. For enterprises, the value proposition is simple: it is significantly cheaper to subscribe to Ubuntu Pro than to dedicate expensive engineering resources to manual security maintenance.

Research shows that the average IT team spends approximately 6 to 8 hours per week, nearly a full business day, on manual security patching and vulnerability tracking. At an average senior engineer's salary, this manual labor costs an organization tens of thousands of dollars per year, per staff member. By automating this process across thousands of packages, Ubuntu Pro reclaims hundreds of engineering hours per year, allowing your team to focus on high-value development rather than routine maintenance.


## How can I check the security coverage of all packages on my Ubuntu machine?

The most direct way to get this information is by running the `pro security-status` command in your Linux terminal. This command gives users a breakdown of packages from Main and Universe repositories, how long they will be supported for and identifies the packages installed on the machine that would benefit from an Ubuntu Pro subscription.

### How do I install Ubuntu Pro?

Because Ubuntu Pro is a service subscription rather than a new operating system, you don’t "install" it in the traditional sense. Instead, you attach your existing Ubuntu LTS installation to a subscription by obtaining a token from the [Ubuntu Pro dashboard](https://ubuntu.com/pro/dashboard) and running `sudo pro attach <TOKEN>`. Once attached, you can confirm that your services are active by running `pro status` in the CLI terminal.

### Can I try Ubuntu Pro before I buy it?

For organizations that need to evaluate Ubuntu Pro at scale, Canonical offers a 30-day free trial. This allows users to test enterprise-exclusive features like the Landscape management dashboard and automated compliance tools (CIS/FIPS) in specific environments.

[Start a 30-day free trial ›](https://ubuntu.com/pro/subscribe)


### Does Canonical sell Ubuntu Pro via partners, vendors, or resellers?

Yes, Canonical works with a global network of partners to ensure organizations can purchase and implement Ubuntu Pro through their preferred procurement channels. Organizations have the option of bundling Ubuntu Pro with hardware direct from select suppliers, purchasing through a regional reseller, or selecting a managed service provider option.

There are several ways to buy Ubuntu Pro beyond a direct contract with Canonical.

[Find a Canonical partner here ›](https://canonical.com/partners/find-a-partner)
