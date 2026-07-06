---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Cloud and infrastructure"
  tag: "Containers"
  title: "What is container security?"
  breadcrumb: "What is container security?"
  description: |
    Knowledge hub article explaining challenges, best practices, 
    and Canonical’s developer tooling related to container security.
  hero_title: "What is container security?"
  cta:
    description: |
      Explore Canonical’s container offerings, and find out more about how 
      Canonical’s approach to secure containers, long-term support, and defense in depth 
      helps make containers safer and more sustainable.
    buttons:
      - text: "Read about our solutions"
        url: "https://ubuntu.com/containers"
        type: "button"
        variant: "positive"
      - text: "Learn to secure containers at scale ›"
        url: "https://ubuntu.com/engage/container-security-guide"
  blog:
    title: "Latest articles on container security"
    id: 1695
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-image.jinja" import image_kh %}
{% from "macros/_macros-lite-video.jinja" import lite_video %}

Container security is the continuous process of protecting an entire containerized environment – 
including the applications, the software packages they rely on, and the cloud infrastructure they 
run on – from cyberattacks, software vulnerabilities, and other threats.


## Container security: an overview

Container security involves continuously protecting applications, images, and infrastructure 
throughout the whole cloud-native lifecycle. Unlike traditional software, containerized workloads 
are dynamic, ephemeral, and frequently updated from multiple sources. Therefore, it is imperative 
that security is considered at every step of the software supply chain. Securing your containers 
should begin when you first build your images, and continue through the deployment phase and 
beyond, with active protection during runtime.


## What are the biggest challenges in container security?

Challenges in container security are varied, ranging from the wide attack surface of bloated 
container images, to the security scanning gap of typical distroless images. 
Some of the biggest challenges include:

{{ text_list_kh(
  items=[
    "Vulnerability bloat",
    "Supply chain risks",
    "Security scanning gap",
    "Elevated privileges",
    "Absence of a long-term support strategy"
]) }}

### CVE noise and alert fatigue

Standard container images are often shipped with a full OS, shell, package manager, and 
utilities, resulting in chunky containers and a wide attack surface. The inclusion of unnecessary 
components leads to vulnerability bloat, as modern security scanners flag all known issues within 
an image. As a result, security and engineering teams waste significant effort triaging huge 
volumes of Common Vulnerabilities and Exposures (CVE) alerts, for components that may not be used 
by the application at runtime.

### Software supply chain blind spots

Supply chain risks can be introduced by pulling pre-built images from public registries without 
verifying their contents. Modern applications are built using a deep stack of dependencies, some 
of which may come from unverified upstream sources. If these dependencies are bundled into a 
container, it can expose organizations consuming this container to the risk of deploying 
malicious code or unpatched software directly into production. Whilst containers may be 
ephemeral, software contracts are not, and relying on semantic versioning as a software contract 
can lead to breaking changes in an application’s dependencies.

### Distroless security gap

In an attempt to combat vulnerability bloat, many organizations attempt to build distroless 
images. The typical approach to building distroless images is top-down, inflating the base image 
and cherry-picking to trim it down. The complex builds, specialized tooling, and deep distro 
knowledge required to build a distroless image with full accuracy mean that package metadata, 
crucial for precise security scanning, is often omitted, leading to inaccurate CVE reporting.

### Misconfiguration

Containers that execute as `root` or run with elevated privileges can allow malicious users to 
exploit vulnerabilities and escape the container’s isolation, compromising the underlying host 
operating system.

### Poor support and patching strategies

The dynamic nature of container environments, and the disjointed lifecycles of the underlying 
components, means that there is significant overhead in maintaining a secure posture, requiring 
continuous tracking of various End-of-Life (EOL) dates and applying patches across thousands of 
images. In the absence of a long-term support strategy, images quickly become non-compliant, and 
hazardous technical debt gets accumulated.


## What are the best practices for container security?

The core best practices for container security are:

{{ text_list_kh(
  items=[
    "Minimal base images",
    "Principle of least privilege",
    "Secure software supply chain",
    "Security scanning integration",
    "Strictly immutable containers",
    "Long-term maintenance strategy",
    "Security in depth"
]) }}

### Use minimal base images

Moving away from general-purpose OS base images to minimal images helps to reduce attack surface, 
removing unnecessary components that an attacker could exploit. Canonical’s OCI-compliant, 
[chiseled Ubuntu containers](https://ubuntu.com/containers/chiseled), known as rocks, contain the 
minimal set of dependencies needed for your application to run, without shells, utilities, and 
package managers.

### Ensure non-root execution

Containers should never run as `root`. Adhering to the principle of least privilege (running 
processes as an unprivileged user) prevents compromised containers from taking over the 
underlying host. Rocks are designed to execute as non-root out of the box.

### Build from trusted sources

Containers should only be built from trusted sources. Pulling in undocumented dependencies from 
public registries introduces massive risk. Rocks eliminate the software supply chain security 
gap, by ensuring every required package comes from a Canonical-maintained source 
(e.g., the Ubuntu archives).

### Monitor and implement CVE reporting

Leverage scanning tools in your CI/CD pipelines to catch CVEs before deployment. Ensure that your 
minimal images retain package metadata, so they can be accurately scanned for vulnerabilities 
without risk of returning false negatives. Canonical’s chiseled approach ensures that rocks are 
minimal in size, but retain the required metadata for scanning accuracy.

### Build using immutable containers

Patching, updating, or modifying a running container in production should be avoided, to prevent 
configuration drift and ensure that unnecessary privileges and utilities (e.g., requiring `root` 
and `apt` to install packages) are eliminated. If a vulnerability is found, the image must be 
rebuilt at the source and redeployed. Rocks enforce this immutability by default, by shipping 
without tools like `apt`, `wget`, or `bash` inside the container, making it practically 
impossible for administrators and threat actors to alter the runtime environment.

### Long-term maintenance

Containers should be based on a foundation that offers long-term security patching. By aligning 
your container strategy with an enterprise lifecycle, such as Ubuntu LTS, you can ensure that 
your containers will receive continuous CVE fixes for years without having to constantly migrate 
to new images.

### Implement multi-layer protection

Instead of relying on a single security control, multiple independent layers of protection should 
be put in place across every level of the system. This ensures that, if one defense is bypassed, 
the next layer is ready to contain the threat.

[Learn more about security in depth ›](https://canonical.com/knowledge/security-and-compliance/what-is-security-in-depth)


## How does Canonical help with container security?

Adhering to container security best practices is made easy with Canonical’s products. Users have 
the option to [consume off-the-shelf OCI-compliant images](https://hub.docker.com/u/ubuntu), 
known as rocks, which are secured and maintained under Ubuntu Pro. Alternatively, they can craft 
their own rocks using Rockcraft and Chisel, or request custom images to be delivered through 
Container Build Service. Canonical’s offerings that help with container security include:

{{ text_list_kh(
  items=[
    "Rocks",
    "Chisel",
    "Pebble",
    "Rockcraft",
    "Container Build Service"
]) }}

### What are rocks?

[Rocks](https://documentation.ubuntu.com/rockcraft/stable/explanation/rocks/) are Canonical’s 
OCI-compliant, minimal container images. They are hardened by design, and built from trusted, 
heavily audited Ubuntu sources. Running as non-root by default, rocks enforce the principle of 
least privilege, and their minimal size means a small attack surface, whilst retaining the 
crucial package metadata needed for accurate security scans. 
Key aspects that set rocks apart include:

{{ text_list_kh(
  items=[
    "<strong>Opinionated and consistent design:</strong> All rocks follow the same design, minimizing full-stack disparity and adoption overhead.",
    "<strong>User-centric experience:</strong> Rocks are described in a declarative format and built on top of familiar and reliable Ubuntu images.",
    "<strong>Seamless chiseling experience:</strong> Rocks can be effortlessly chiseled using off-the-shelf primitives, harnessing the advantages of “distroless” to deliver compact and secure Ubuntu-based container images.",
    "<strong>Package metadata:</strong> Rocks extend the OCI image information by including additional metadata inside each rock, allowing container applications to easily inspect the properties of the image they are running on, at execution time."
]) }}

[Learn more about rocks ›](https://documentation.ubuntu.com/rockcraft/stable/explanation/rocks/)

### Package slicing with Chisel

Chisel is a novel package manager that slices packages to create compact, secure software. 
The engine behind rocks, Chisel builds images bottom-up, installing only the bare minimum files 
and dependencies an application needs to run. It omits shells, utilities, and package managers, 
stripping attackers of the tools they need to enact living-off-the-land attacks. Unlike 
traditional distroless approaches, Chisel preserves slice metadata, so that security scanners can 
accurately report CVEs rather than false negatives.

[Read more about Chisel ›](https://documentation.ubuntu.com/rockcraft/stable/explanation/chisel/)

{{ image_kh(url="https://assets.ubuntu.com/v1/a44c165a-kh_cloud_infra.png",
  alt="Image depicting a side-by-side comparison of 3 rocks: \n1. Python rock with an Ubuntu base: This contains additional utilities, leading to a wider attack surface. It is 42MB, and 114MB in Docker local registry. \n2. Python rock with a bare base: This contains no additional utilities, but includes the entire Python package and dependencies. It is 28MB, and 74MB in Docker local registry. \n3. Chiseled Python rock: This has no additional utilities, and only includes the necessary bits of Python and dependencies. It is 13MB, is STIG/CIS compliant off-the-shelf, and provides a 61%+ CVE reduction compared to equivalent standard or distroless images.",
  width="2748",
  height="1546",
  hi_def=True,
  loading="lazy",
  caption="Build minimal images using Chisel"
  ) | safe
}}

{{ lite_video(video_id="yQukQb-n99E",
  video_title="Reinventing distroless with chiseled Ubuntu containers") | safe
}}

### Container-optimized service management

Pebble is a container-optimized service manager that enables the seamless orchestration of a 
collection of local service processes as an organised set. It is the default entrypoint for all 
rocks, providing a predictable and powerful abstraction layer between the user and the container 
application. Pebble uses declarative YAML files to orchestrate services natively, eliminating the 
security risk posed when using imperative shell scripts to start multiple processes in a container.

[Read more about Pebble ›](https://documentation.ubuntu.com/rockcraft/stable/explanation/pebble/)

### Building rocks

Rockcraft is a tool to build rocks, driven by a declarative rockcraft.yaml file. Unlike complex, 
multi-stage Dockerfiles that may hide unverified upstream code or insecure configurations, 
Rockcraft standardizes the build process, producing minimal images through a repeatable, 
auditable build pipeline.

[Craft your own rock ›](https://documentation.ubuntu.com/rockcraft/stable/)

### Container Build Service

With Container Build Service, Canonical can build, maintain, and secure minimal container images 
at a user’s request, onboarding any open source dependency needed, providing an LTS commitment of 
up to 15 years, and fixing critical CVEs in a timely manner.

[Learn more about Container Build Service ›](https://ubuntu.com/containers/container-build-service)
