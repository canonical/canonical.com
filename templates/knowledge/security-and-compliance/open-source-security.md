---
wrapper_template: "knowledge/_base_kh_markdown.html"
context:
  category: "Security and Compliance"
  tag: "Security"
  title: "What is open source security?"
  breadcrumb: "What is open source security?"
  description: "Understand open source security and explore best practices, including dependency management, code signing, SBOMs, vulnerability management, and careful backporting of legacy code."
  copydoc: "https://docs.google.com/document/d/16lg3gVWgHMZKmVmDhKFbmLxyF5xV22amaL0Alczk4bc/edit?tab=t.0#heading=h.bo1zcf2r6drh"
  hero_title: "What is open source security?"
  cta:
    description: "Explore why Canonical is the best option for open source security"
    buttons:
      - text: "Learn more about Ubuntu Pro"
        url: "http://www.ubuntu.com/pro"
        type: "button"
        variant: "positive"
  blog:
    title: "Latest articles on open source security"
    id: 1364
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-lite-video.jinja" import lite_video %}

Open source security is a set of practices that aim to identify, manage and mitigate security risks related to the use of open source components in software and systems. Explore open source security best practices, including dependency management, code signing, SBOMs, vulnerability management, and backporting.

## Is open source secure?

It’s not uncommon to encounter this question: is open source software secure? After all, open source is produced by hundreds of thousands of contributors, and can be sourced from a variety of different sources. This variety of sources introduces risk management challenges, but it’s also its strength: open source software benefits from having much greater public scrutiny on its code. Proprietary software does not have any more inherent safety or security benefits than open source software. Like closed source and proprietary software, open source software does have vulnerabilities. Its security depends on whether it’s properly maintained and patched against newly discovered or existing vulnerabilities.  There are many ways you can mitigate the vulnerabilities and risks of open source software, including techniques like dependency management, vulnerability management, automated patching, code signing, integrity verification, and more.

[Read our article on the security of open source versus proprietary software](https://canonical.com/blog/does-open-source-software-have-the-same-safety-as-proprietary-software)


## Best practices for securing open source
There are two essential practices when it comes to securing open source software deployments: preventing attacks using known methods, and maintaining software in the face of new vulnerabilities. 


### Prevention starts with defense in depth
One important aspect of securing open source software is maintaining defense in depth for your software platforms.  

Defense in depth, or security in depth, is a cybersecurity strategy that reduces cyberattack risks for organizations by creating security controls, checks, processes, and procedures across many different layers of the organization, including the systems, networks, hiring practices, work processes, and communications. 

Defense in depth is important because if one particular component of the stack is vulnerable, an attacker can’t gain a foothold and harm your systems any further. This can be achieved by a combination of different techniques, such as using confinement technologies, locking down the configuration options, and removing unnecessary components that might aid a malicious actor. This security philosophy aims to build multiple defense layers that can prevent, detect, minimize, or contain cyberattacks and cyberthreats, even if one or multiple layers are breached or fail.

### Maintenance and patching for open source software

Whether code is open or proprietary, the most crucial security measure is patching and updating that software, and the best way to do this is to consume the software from a trusted source which provides strong security maintenance commitments. 

Regularly patching your open source software enables you and your customers to remain safe from newly discovered threats.

[Understand Canonical’s solutions for open source security](https://canonical.com/solutions/open-source-security)


### [Dive into security in depth](https://canonical.com/blog/ubuntu-security-defense-in-depth)


## What is dependency management?

Managing and securing your software and all of its dependencies is a vital part of maintaining open source security. Let’s dive into some key information about dependencies.


### What are dependencies?
In software engineering, dependencies refer to external components, libraries, modules, or services that a software application or system relies on to function correctly. These external elements are not part of the core codebase but are integrated into the software’s build or runtime environment.

[Read a blog about software dependencies&nbsp;&rsaquo;](https://canonical.com/blog/what-are-dependencies)

### What are direct dependencies and what are transitive dependencies?

In software, you will encounter two kinds of dependencies: direct dependencies and indirect dependencies (also known as transitive dependencies). 

All dependencies are essential for a piece of software to work properly. Direct dependencies are all the libraries that you explicitly declare, include, or use in your software project or code. 

In contrast, indirect dependencies are the dependencies of your direct dependencies, and can also be the dependencies of other indirect dependencies. These could include libraries, modules, or components that your direct dependencies rely on to function. These indirect dependencies are not explicitly declared, but are pulled in through the direct dependencies, or exist as dependencies on existing dependencies.  

{{ lite_video(video_id="1eqEpf9hPKk", video_title="What are open source dependencies?") | safe }}

### Why are dependencies a risk in software development?

Dependencies can present several flaws that can introduce risk into your programs or supply chain. Exploiting such weaknesses can allow attackers to gain unauthorized access, manipulate data, or disrupt services. 

There are two important things to highlight about dependencies: 

{{ text_list_kh(
  type="number",
  items=[
  "The more dependencies you have, the bigger your attack surface (generally speaking). That's simply because you have more software.",
  "Getting your dependencies from trusted sources can reduce the risk of sourcing compromised packages. Some ecosystems are more susceptible to compromises compared to others."
]) }}

When it comes to dependencies, it’s about finding a balance between quality and quantity. For example, relying on five tiny and well maintained libraries is better than relying on a single big, poorly written, or unmaintained library.

### What is dependency management?

In software development, dependency management refers to the process of identifying, mapping, and maintaining the extensive list of direct and indirect dependencies that your software contains, as well as maintaining the long-term security of these dependencies.

### Why is dependency management important?

Dependency management in software development is important because dependencies in software represent an attack vector that could be used to attack and breach your software. If your application relies on a particular package, framework, or library that becomes affected by known vulnerabilities, your app could be compromised or at risk. Dependency management is an ongoing process that aims to prevent, mitigate, or contain these risks.

### What are the best ways to manage dependencies?

Organizations need two things to address the root issue that leaves them vulnerable:

{{ text_list_kh(
  items=[
  "A trusted source that vets and monitors software packages",
  "Timely, automatic security updates that do not break functionality and maintain software stability"
]) }}

## What are trusted sources?

Almost all software relies on third-party packages in order to function. To use these packages safely and securely, you need to ensure they are drawn from a reliable, vetted, and security maintained source: a trusted source.

### Why are trusted sources important for your software?

Your entire software supply chain needs a verified, security maintained source in order to ensure that the packages, updates, and patches you’re receiving to these libraries, components, and packages are authentic and reliable.

The most convenient and simple way to manage your software supply chain is to source updates through your operating system (OS). This method allows you to consume updates for your dependencies in one single place, rather than an app-by-app or project-by-project basis – making for easier monitoring and compliance work. As an example, you can get updates for all packages in Ubuntu and Canonical’s open source portfolio via [Ubuntu Pro.](http://www.ubuntu.com/pro)

### Timely, automatic security updates

Once you have a trusted source for your patches and packages, you’ll need some way to apply these  updates at regular intervals. 

Applying these security updates automatically has several advantages over manual methods:

{{ text_list_kh(
  items=[
  "Minimized attack window: Rapidly closes the gap between vulnerability disclosure and exploit development by applying patches before attackers can strike.",
  "Scalable management: Automates the tracking of thousands of security updates, eliminating the human error and \"patch fatigue\" associated with manual maintenance.",
  "Simplified compliance: Streamlines adherence to regulations like the EU CRA and SOC 2 by providing centralized logging and proof of timely remediation."
]) }}

## What is code signing and integrity verification?

Code signing and identity verification are techniques that allow you to double-check your software’s integrity and confirm that it has not been altered from an expected or authorized state. 

### What is integrity verification?

In software, integrity verification is a security technique that ensures that software and auxiliary data are secure and unaltered from their intended, original states, during distribution and  throughout their lifecycle. Integrity verification uses various techniques, such as code signing, digital signatures, and hashing, to check and confirm that code has not been corrupted, tampered with, or otherwise subjected to unwanted or unauthorized changes after it was created. 

### What is code signing?

Code signing is integrity verification that also ties the verified software to a particular author, vendor, or supplier. Code signing confirms the authorship and integrity of software and auxiliary data with a digital signature.

### Why are code signing and integrity verification important?

Integrity verification and code signing are essential for securing the open source software supply chain by providing a cryptographic guarantee that code originates from a trusted source and has not been tampered with. These mechanisms help to prevent supply chain attacks and ensure that only authorized, authentic software is deployed. This is essential for organizations that need to meet strict regulatory compliance standards.


## What is a software bill of materials?

Effective security relies upon tracking the components and dependencies contained within your software. SBOMs (software bill of materials) help you achieve this.

### What is a software bill of materials?

In software development, a software bill of materials, or SBOM, is a detailed and accessible list of all the components that make up your software and where they come from. An SBOM may also indicate what was used to produce those components.

### What does an SBOM help with?

An SBOM:

{{ text_list_kh(
  type="bullet",
  items=[
  "Tells users and developers about an application’s code and contents",
  "Reveals the dependencies of an application’s software",
  "Highlights potential supply chain attack vectors",
  "Reveals potential compliance issues over software sourcing",
  "Helps to manage licences",
  "Helps with risk assessment and software inventory"
]) }}

SBOMs are often required to meet compliance requirements for cybersecurity regulations such as the Cyber Resilience Act. 

Combining SBOMs with vulnerability data feeds provides you with visibility into vulnerabilities present in your systems.

### What should a basic SBOM include?

SBOMs can come in different levels of depth and detail, depending on the region or compliance requirements. 

A base SBOM outlines the core tools, frameworks, libraries, modules, and other components that make up the software. This approach should tell the user the basic and top-level information about the components that go into your software, and the environment that was used to build a software package. 

This would include:

{{ text_list_kh(
  type="bullet",
  items=[
  "The name of the component",
  "The version or version string of the component being used in your product",
  "The authors or creators of the component"
]) }}

### What should an advanced SBOM include?

For more mature organizations and software, an SBOM will go beyond a base SBOM to include detailed information about each individual module. This could include:

{{ text_list_kh(
  items=[
  "The suppliers of the component",
  "The relationships, dependencies, and connections between components",
  "Lifecycle dates",
  "The licence information of the component"
]) }}

### How should you distribute or publish your SBOM?

Your SBOM should be as publicly accessible as possible. You can make your SBOM available to the public and regulators in a human- and machine-readable format.

### When should you update your SBOM?

Because of patches, updates, migrations, and alterations, software changes all the time. Every time you build a new software distribution artifact, you should generate a new SBOM.


[Get a detailed overview of SBOMs](https://canonical.com/blog/what-is-sbom-software-bill-of-materials-explained)

## Vulnerability assessment vs management

While both vulnerability assessment and vulnerability management are crucial for a strong security posture, they address different aspects of risk. 

### What is vulnerability assessment?

A vulnerability assessment is the process of identifying and reporting known software vulnerabilities found in a system at a particular moment in time. This is normally highly automated and performed on a frequent basis by using a service, or software application, known as a vulnerability scanner. It is a central part in an organization’s wider [vulnerability management](https://ubuntu.com/blog/what-is-vulnerability-management) strategy, but it can also be performed as part of your regular risk assessments. 

Government regulations and industry standards often mandate vulnerability assessments. As an example, certain compliance levels of the [PCI DSS standard](https://ubuntu.com/blog/how-canonical-enables-pci-dss-compliance) used by the major payment card companies require merchants that take online payments to implement vulnerability assessments using Approved Scanning Vendors. 

Even when there are no regulatory compliance requirements, best practice dictates that vulnerability scans should still be performed – after all, vulnerabilities increase risk and there are few things worse for one’s security posture than not knowing which vulnerabilities exist. It is generally not recommended to leave yourself exposed to threats, just because you are not mandated to perform scans. 

[Learn how to conduct a vulnerability assessment](https://ubuntu.com/blog/how-to-conduct-a-vulnerability-assessment)

### What is vulnerability management?
In contrast, vulnerability management is an ongoing, cyclical process. It is the holistic process of identifying and handling weaknesses in an organization’s networks, systems, and devices. Vulnerability management serves as part of an overarching risk management strategy that aims to reduce cyber incident risk to acceptable levels and improve overall organizational cybersecurity posture. Different activities involved in vulnerability management include: 

{{ text_list_kh(
  items=[
  "Asset inventory",
  "Risk assessment",
  "Threat intelligence",
  "Patch management",
  "Vulnerability monitoring",
  "Security hardening"
]
)}}

[Learn more about vulnerability management in Ubuntu](https://ubuntu.com/security/vulnerability-management)

## Backporting and legacy code

When applying fixes for vulnerabilities, you may find compatibility issues depending on the software version of the code. This is where backporting comes in. For legacy systems, backporting is the only option to maintain security and stability. 

It’s important to ensure that security approaches take different software versions into account, including legacy systems. Let’s begin with backporting.  

### What is backporting?

In software development, backporting is the process of applying code changes made for new versions of software, to older versions of that software.

When a new vulnerability is discovered in a widely used open source component (like the Linux kernel, OpenSSL, or a common library), the upstream project often only patches the newest release. Backporting ensures stability. For legacy systems, backporting is the only option to maintain security and stability.

For instance, Canonical's security engineers and other contributors backport that fix to all supported Ubuntu LTS releases, ensuring that the patch maintains compatibility and does not break any applications.

### What are legacy systems?

Legacy systems refers to long-standing code or applications that play a critical, functional role in an organization's daily operations while using unsupported or end-of-life components.

The unique challenge of legacy systems is that they require a high degree of specialized knowledge or effort to maintain, often incurring high costs or effort to find, hire, or replace engineers who maintain this high-value software.

As we have noted, the complexity and age of these legacy systems often mean that the only way to maintain stability, security, and compliance is through backporting.

## How does Canonical help with open source security?

Canonical acts as a curator, maintainer, and security-focused vendor across the open source ecosystem, providing scalability, supply chain integrity, and stability for enterprises using open source. 

Canonical does this by providing four key pillars: 

{{ text_list_kh(
  items=[
  "A trusted software supply chain, from the OS to applications",
  "Compliance and hardening",
  "Patching automation tools",
  "Collaboration with leading scanning vendors"
]
) }}

### A trusted software supply chain

Ubuntu is one of the most popular operating systems in the world, and is celebrated for its stability and support. This is because Canonical provides a Long Term Support (LTS) release cycle for Ubuntu, backing every release with a guaranteed 5-year security commitment for the core operating system, extendable for up to 15 years.

With Ubuntu Pro, Canonical provides streamlined security, compliance, hardening, automation, and support for the full stack. Developers can get security maintenance and long term stability for all aspects of open source infrastructure, applications, and a wide selection of the most popular and relied-upon open source software in the world, including GCC, PostgreSQL, OpenSSL, Nagios, Rust, PHP, Redis, and more.

### Compliance and hardening

A number of compliance and hardening features are available through Canonical. With Ubuntu Pro, developers can get easy access to: 

{{ text_list_kh(
  items=[
  "Compliance profiles for the most popular security standards",
  "Security hardening features to enable easy compliance with common regulatory frameworks including FIPS 140, DISA-STIG, CIS, FedRAMP, CMMC, PCI-DSS & Cyber Essentials."
]
) }}

### Patching automation tools

Canonical provides stability and security to its user base through a number of patching automation and vulnerability management tools. This includes: 

{{ text_list_kh(
  items=[
  "Fast remediation of vulnerabilities with tested vulnerability fixes",
  "Timely, rebootless patches for critical and high severity Linux kernel vulnerabilities between security maintenance windows, while the system runs, thanks to [Livepatch](https://ubuntu.com/security/livepatch)",
  "High levels of automation for security patching, auditing, compliance, and access management across your entire organization or fleet of devices through [Landscape](https://ubuntu.com/landscape)"
]
) }}

### Collaboration with leading scanning vendors

Canonical actively [partners closely with companies like Black Duck and Tenable](https://canonical.com/blog/canonical-announces-ubuntu-security-research-alliance-program) to reduce the number of false positives in scanning tools on Ubuntu and improve on-platform security for Ubuntu users through more proactive threat detection and the latest accurate vulnerability data. 

Canonical's security team and other contributors continuously monitor for vulnerabilities and issue Ubuntu Security Notices (USNs), providing timely, verified patches for critical and severe vulnerabilities.
