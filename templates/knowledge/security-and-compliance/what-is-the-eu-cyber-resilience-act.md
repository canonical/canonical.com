---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Security and compliance"
  tag: "Cyber Resilience Act"
  title: "What is the EU Cyber Resilience Act?"
  breadcrumb: "What is the EU Cyber Resilience Act?"
  description: "What the EU Cyber Resilience Act (CRA) means for manufacturers and developers. Learn about mandatory cybersecurity standards, requirements, deadlines, and penalties."
  hero_title: "What is the European Union Cyber Resilience Act (EU CRA)?"
  cta:
    title: "Find out more"
    description: "Take the next steps in preparing for the CRA. Contact us for detailed guidance and get detailed platform comparisons for the best OS for CRA compliance."
    buttons:
      - text: "Get in touch for CRA help"
        url: "https://canonical.com/solutions/open-source-security/cyber-resilience-act#get-in-touch"
        type: "button"
        variant: "positive"
      - text: "Prepare your devices"
        url: "https://ubuntu.com/engage/cra-regulations-for-ubuntu"
        type: "button"
      - text: "Compare Yocto and Ubuntu Core"
        url: "https://canonical.com/knowledge/internet-of-things/yocto-vs-ubuntu-core"
  blog:
    title: "Latest from our blog"
    id: 4632
---

{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-lite-video.jinja" import lite_video %}

The EU Cyber Resilience Act (CRA) is the first comprehensive framework in the European Union that sets mandatory cybersecurity standards for all "products with digital elements" (PDEs) – essentially any products or devices that can connect to a network. Unlike previous voluntary guidelines, the CRA transforms cybersecurity from a "best practice" into a legal requirement for placing products on the EU market.

Learn more about the specific regulatory and compliance requirements of the CRA, including the penalties, deadlines, regulatory impact, and technical features that need to be delivered for CRA compliance.

## The EU CRA: an overview

The CRA is a piece of European Union legislation that aims to make Products with Digital Elements (PDEs) safer by requiring developers, manufacturers, distributors, and retailers to follow mandatory cybersecurity, documentation, and vulnerability reporting requirements. The CRA applies for the entire product lifecycle, with steep, standardized penalties for failures to meet compliance requirements.

[Read a CISO’s full breakdown of the CRA ›](https://ubuntu.com/blog/a-cisos-comprehensive-breakdown-of-the-cyber-resilience-act)

### Who does the Cyber Resilience Act apply to?

The CRA applies to manufacturers, providers, and importers of PDEs.

{{ text_list_kh(
  type="bullet",
  items=[
  "<strong>Manufacturers:</strong> entities that produce, develop, deliver, or market PDEs to consumers in the EU market.",
  "<strong>Providers:</strong> entities that provide components or software (whether open source or proprietary) used by manufacturers.",
  "<strong>Importers:</strong> entities in the EU who place on the market PDEs manufactured outside of the EU."
]) }}

### What products and devices does the CRA regulate?

The CRA will regulate all manufacturers and developers of products who want to put products on the EU market, regardless of their location or where the product was developed. The CRA will cover all products or devices available in the EU market that are connected to any other device or network to exchange data. This includes PDEs that use:

{{ text_list_kh(
  type="bullet",
  items=[
  "Direct/indirect connection",
  "Physical, wireless/radio or virtual",
  "Remote data processing (including SaaS with remote processing capabilities)"
]) }}

The only exceptions for CRA regulation are:

{{ text_list_kh(
  type="bullet",
  items=[
  "Solutions used for internal purposes",
  "Pure SaaS solutions",
  "PDEs that are already regulated by sector-specific regulations, such as medical devices"
]) }}

## When will the CRA come into force?

The European Parliament formally approved the CRA in March 2024, and it was adopted by the European Council on October 10, 2024. The Cyber Resilience Act entered into force on December 10, 2024, with certain requirements still being phased in. Manufacturers will need to follow CRA reporting obligations as of June 11, 2026. The CRA will be fully enforced by December 11, 2027.

## What are the fines and penalties?

Failing to meet the CRA's requirements carries penalties and fines of up to €15 million or 2.5% of the organization’s worldwide annual turnover (whichever is highest) depending on the seriousness of the violation.

### How will the CRA affect open source developers?

The Cyber Resilience Act will affect open source developers in a number of ways, by formalizing and tightening the demands on developers to document, maintain, secure, and support the software they create.

For open source developers, this will directly translate to:

{{ text_list_kh(
  type="bullet",
  items=[
  "<strong>A shift in accountability:</strong> Manufacturers are now legally responsible for the security of all digital elements in their products, including integrated open source components.",
  "<strong>A mandate for documentation:</strong> Organizations must produce comprehensive Software Bills of Materials (SBOMs), vulnerability reports for the entire product lifecycle, detailed user-facing materials like manuals, and hardening guides.",
  "<strong>Impacts on commercial scope:</strong> Open source projects providing paid support or consulting are generally classified as commercial entities under the act. As such, they fall under the obligations of the CRA.",
  "<strong>New, more stringent requirements for disclosure:</strong> Developers must now report actively exploited vulnerabilities to the European Union Agency for Cybersecurity (ENISA) and other relevant authorities within 24 hours of discovery."
]) }}

{{ lite_video(video_id="GtAZ35hYHP0", video_title="Navigating the EU CRA with immutable IoT") | safe }}

## What are the main Cyber Resilience Act requirements?

The CRA stipulates clear requirements for vulnerability management, risk assessment, documentation, and conformity assessment.

{{ text_list_kh(
  type="bullet",
  items=[
  "<strong>Vulnerability management:</strong> Manufacturers must provide security maintenance throughout the product lifecycle through security patching, and prompt incident response.",
  "<strong>Risk assessment:</strong> Manufacturers must ensure that PDEs have no known exploitable vulnerabilities, are secure by default with minimal attack surface, and minimize processing of data.",
  "<strong>Documentation:</strong> Manufacturers must deliver documentation that fully details product design, delivery and vulnerability management. Documentation must also demonstrate a risk assessment, and provide a Software Bill of Materials (SBOM). They must also publish manuals covering system hardening, for instance.",
  "<strong>Conformity assessment:</strong> Manufacturers must provide a declaration of conformity, either through self assessment or independent third-party auditors."
]) }}

The specific requirements of your PDE will depend on how the CRA classifies your devices or products.

### How does the CRA classify products?

Under the CRA, devices and software are placed into four categories, based on their cybersecurity risk factor, their level of access authority, or their connection to sensitive infrastructure, networks, or systems.

{{ text_list_kh(
  type="bullet",
  items=[
  "<strong>Default products:</strong> Examples include hard drives and smart speakers. These require self assessment (i.e., complete a checklist of requirements and issue a statement of compliance yourself).",
  "<strong>Important Products Class I:</strong> Examples include password managers, operating systems, and wearable devices. These require Independent Body Assessment or formal EU Certification. Important Class I products can also do self-assessment if they follow the <a href=\"https://digital-strategy.ec.europa.eu/en/policies/cra-standardisation\">vertical standard</a>.",
  "<strong>Important Products Class II:</strong> Examples include hypervisors, firewalls, and intrusion detection systems. These require Independent Body Assessment or formal EU Certification.",
  "<strong>Critical Products:</strong> Examples include smartcards, Hardware Security Modules, and smart meter gateways. These require Independent Body Assessment or EU Certification."
]) }}

## How do you prepare for CRA compliance?

Meeting the CRA’s new and strict compliance standards is best achieved by following a 5-step process.

{{ text_list_kh(
type="number",
items=[
"<strong>Define your regulatory exposure.</strong> Convene legal, security, and engineering teams to audit your product portfolio against the final CRA text. Do not assume your software is exempt; it is safer to over-prepare documentation than to risk non-compliance on a \"safe bet.\" Identify which risk category your products inhabit (Default, Class I, Class II, or Critical) to determine if you require third-party certification or can rely on self-assessment.",
"<strong>Standardize technical documentation.</strong> The CRA mandates transparency via a formal technical file. You must be ready to provide EU authorities and customers with:
<ul>
  <li>A machine-readable map of all components and known vulnerabilities.</li>
  <li>Documented analysis of potential cybersecurity threats and mitigation strategies.</li>
  <li>A signed statement verifying the product meets harmonized EU security standards.</li>
  <li>A description of your secure development and vulnerability handling lifecycles.</li>
</ul>",
"<strong>Operationalize vulnerability reporting.</strong> Establish an internal \"fast-track\" unit specifically for disclosure. The CRA requires reporting actively exploited vulnerabilities to ENISA within 24 hours of discovery. This process must be baked into your incident response policy to avoid heavy fines. Move from reactive patching to a proactive \"secure-by-design\" model that mirrors frameworks like NIS2 or ISO27001.",
"<strong>Execute conformity assessments.</strong>  Determine your path to the <a href=\"https://single-market-economy.ec.europa.eu/single-market/goods/ce-marking_en\">CE marking</a>. Depending on your product's class, you may need to facilitate external audits or rigorous internal testing. Plan where this compliance data will live, whether in a <code>README.md</code>, a digital label, or a physical info sheet, to ensure it is \"freely and readily available\" to the end user.
<ul>
  <li><strong>Audit internal silos:</strong> Bridge the gap between legal wording and engineering reality early to avoid late-stage pivot costs.</li>
  <li><strong>Monitor the \"Support Period\":</strong> Ensure your team is staffed to push security updates for the entire expected lifetime of the product (minimum 5 years).</li>
</ul>",
"<strong>Choose trusted suppliers for your software.</strong>  In many cases, many of your CRA requirements can be simplified by actively consuming software specifically from vendors who take on CRA manufacturer responsibility for the packages, software, or devices that they supply to you."
]) }}

[Read our whitepaper to prepare for CRA compliance ›](https://ubuntu.com/engage/cra-regulations-for-ubuntu)

## How does Canonical help with EU CRA compliance?

Canonical is committed to making CRA compliance as easy as possible for our entire range of products and services, and has chosen to meet the challenges and requirements of the CRA head-on.

Canonical has committed to:

{{ text_list_kh(
  type="bullet",
  items=[
  "Ensuring that long-term supported releases of Ubuntu are compliant until their end of life.",
  "Completing CRA certification on relevant Canonical products.",
  "Performing attestation for non-critical Canonical products.",
  "Assuming the manufacturer role for the pieces of software that we ship and that our customers use on their devices.",
  "Providing long-term maintenance for devices under <a href=\"https://ubuntu.com/pro/devices\">Ubuntu Pro</a>."
]) }}

This commitment will ensure device manufacturers and users of Canonical products benefit from our commitments to the CRA.

[Visit our page for CRA compliance ›](https://canonical.com/solutions/open-source-security/cyber-resilience-act)

### A 20 year track record

For over 20 years, Canonical has maintained a rigorous track record of meeting and exceeding strict cybersecurity standards for its operating systems and software. This dedication is evident in our commitment to building optimized images and providing robust security hardening and automation.

Canonical builds products that have been proven to adhere to critical compliance and certification requirements, including key industry and government standards such as FIPS 140-2/3, STIG compliance, and configurations based on CIS (Center for Internet Security) benchmarks. This focus on security and efficiency makes Canonical a trusted partner for deployments requiring the highest levels of assurance.

[Learn about security standards on Ubuntu ›](https://ubuntu.com/security/security-standards)

### A trusted source for open source software

Canonical partners with ODMs and OEMs across industries worldwide to create devices and systems that are reliable, secure by design, and maintained long-term through our LTS commitments. By working closely with silicon vendors, manufacturers, and distributors, Canonical creates optimized security maintenance and support across a growing, expansive ecosystem of certified devices. This means that developers get a trusted source to pull their open source from, and a partner that will help you to address vulnerabilities for better peace of mind.

Through these partnerships, with organizations like Dell, HP, NVIDIA, Advantech, and dozens more, we create an optimized Ubuntu experience on an exceptionally long list of devices that are tested for reliability and performance.

[Learn about our partnerships ›](https://canonical.com/partners)

### Robust long-term security maintenance for the entire PDE lifecycle

Canonical’s approach to security maintenance ensures that your PDEs and regulated devices get long term support across the entire lifecycle. Through Ubuntu Pro, ESM (Expanded Security Maintenance), and the Legacy add-on, Ubuntu LTS releases get up to 15 years of stability and reliability, ensuring that the fixes made to the latest and cutting-edge technologies are also available to highly valuable established systems, devices, and solutions, wherever they are deployed.

[Discover Ubuntu Pro for Devices ›](https://ubuntu.com/pro/devices)

{{ lite_video(video_id="tNECRG5r2sg", video_title="What is Ubuntu Pro?") | safe }}
