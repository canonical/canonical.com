---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Cloud and infrastructure"
  publish_date: 2026-09-07
  tag: "Networking"
  title: "What is cloud networking?"
  breadcrumb: "What is cloud networking?"
  description: "Learn what cloud networking is and how it connects workloads across apps, workloads, users, and services using software-defined infrastructure."
  copydoc: "https://docs.google.com/document/d/1Bkncfivt-Gxjm74CW6u7U1zSroCXLUN5SSHyQgPkCaA"
  hero_title: "What is cloud networking?"
  cta:
    description: "Cloud networking choices shape performance, security, and operations. Explore Canonical’s open infrastructure stack, learn how OVN works, or talk to our team about your architecture."
    buttons:
      - text: "Explore Canonical’s infrastructure solutions"
        url: "https://canonical.com/solutions/infrastructure"
        type: "button"
      - text: "Learn how OVN powers cloud networking"
        url: "https://canonical.com/blog/data-centre-networking-what-is-ovn"
        type: "button"
        variant: "positive"
      - text: "Get in touch ›"
        url: "https://canonical.com/solutions/networking/contact-us"
        type: "link"
  blog:
    title: "Latest from our blog"
    id: 1848
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-lite-video.jinja" import lite_video %}

Cloud networking is the architecture and software layer in a stack, which uses software-defined resources to connect apps, workloads, users, and services across cloud environments. It provides virtual networks, routing, security, and load balancing, enabling teams to manage connectivity through APIs, automation, and policy instead of manual device configuration.

## What does cloud networking do?

Cloud networking connects users to applications and enables applications to communicate with each other. It also links workloads to storage and databases, bridges cloud environments with data centers, and ties together containers, virtual machines, and physical servers while exposing internal services to external networks.

Cloud networking includes the software, architecture, and operational model used to provide network connectivity in public clouds, private clouds, hybrid clouds, and multi-cloud environments.

A useful way to understand cloud networking is to start with the cloud model itself. Cloud computing depends on on-demand access to shared resources such as networks, servers, storage, applications, and services. Networking is therefore part of the cloud foundation, not an optional layer added later.

## Why does cloud networking matter?

Cloud platforms are dynamic. Workloads move, scale, restart, and change frequently. Traditional network operations were designed for more static environments, where servers had stable locations and long lifecycles. In contrast, cloud networking makes network resources programmable, repeatable, and aligned with these shorter workload lifecycles.

Cloud networking directly governs the core traffic and infrastructure operations:

{{ text_list_kh (items=[
  "Traffic management: it governs both east-west traffic (traffic between workloads) and north-south traffic (traffic entering and leaving the cloud)",
  "Operational impact: cloud networking directly influences application availability, tenant isolation, and security policy enforcement.",
  "Performance and compliance: it impacts performance, latency, and IP management while playing a critical role in disaster recovery, compliance, and day-2 operations."
])}}

In telco and enterprise environments, cloud networking also has to respect brownfield constraints. (pre-existing IT processes.) Existing routing, firewalling, address plans, monitoring systems, and operational processes rarely disappear when a cloud platform arrives. A good cloud networking design integrates with those realities instead of ignoring them.

## How does cloud networking work?

Cloud networking works by separating network intent from the underlying infrastructure.

This is a declarative model: an operator defines what the network should provide. Through virtualization, the cloud platform then translates that intent into configuration across software switches, routers, agents, tunnels, firewall rules, routing tables, and sometimes physical network devices. This is a continuous process: the cloud platform constantly reconciles the desired network state with the physical and virtual infrastructure.

For example, an operator may create a virtual network, attach workloads to it, define security rules, and expose an application through a load balancer. The cloud networking layer turns those requests into the required data path and control plane changes.

Most cloud networking systems include three broad layers:

{{ text_list_kh(
  type="number"
  items=[
  "The physical underlay network (provides basic IP connectivity between physical hosts)",
  "The virtual or software-defined overlay network (provides logical networks for workloads)",
  "The control plane that manages network state (manages the desired state and programs the data path)"
]) }}

### How does cloud networking affect security?

Cloud networking is a core part of cloud security architecture. It controls which systems can communicate with each other, and how traffic enters or leaves the cloud environment.

Cloud networking designed with security in mind typically applies these best practices:

{{ text_list_kh (items=[
  "Default-deny policy where appropriate",
  "Least-privilege access between workloads",
  "Segmentation between tenants and environments",
  "Strong ingress and egress controls",
  "Encryption where required by policy",
  "Audit trails for network changes",
  "Clear ownership of firewall and policy rules",
  "Regular review of exposed services"
])}}

Security policy should be automated where possible. Manual policy changes are hard to audit and drift easily from the intended design.

### How does cloud networking affect performance?

Performance depends on both the control plane and data path. The control plane must handle network state changes reliably. The data path must forward traffic with the required throughput, latency, and packet loss characteristics.

Performance-sensitive environments should test for:

{{ text_list_kh (items=[
  "Realistic packet size distribution and mixed east-west/north-south traffic",
  "Gateway throughput under load",
  "Overhead introduced by overlay encapsulation",
  "Impact of firewall rules and policy enforcement",
  "Load balancer behavior under realistic conditions",
  "System-level factors, like NUMA memory access, CPU allocation, NIC capabilities",
  "Failure scenarios, to assess recovery and resilience"
])}}

Average throughput alone is not enough. Operators also need tail latency, jitter, packet loss, and recovery time measurements.

### How should cloud networking handle day-2 operations?

A cloud networking design is only sustainable if it can be operated, maintained, and recovered over time. This is what Day-2 operations cover: the ongoing processes that keep the network aligned with its intended design.

Sustainable cloud networking operations require:

{{ text_list_kh (items=[
  "Upgrade procedures",
  "Backup and restore processes",
  "Control plane health checks",
  "Data path validation",
  "Capacity planning",
  "Change management",
  "Observability and alerting",
  "Tenant troubleshooting workflows",
  "Failure testing",
  "Documentation for common incidents"
])}}

Cloud networking should be treated as a long-running platform capability, not a deployment task. The network will change as workloads, sites, policies, and teams change.

[Get expert help designing and operating your cloud infrastructure.](https://canonical.com/consulting)

## Cloud networking vs traditional networking

Traditional networking and cloud networking are not opposites. Cloud networking builds on traditional networking concepts, then makes them programmable and workload-aware.

| Area          | Traditional networking           | Cloud networking |
| ------------- | -------------------------------- | ------------------------------------------------------ |
| Primary unit  | Device, VLAN, interface, route   | Workload, service, policy, virtual network             |
| Change model  | Manual or device automation      | API-driven and platform-driven                         |
| Lifecycle     | Often tied to the infrastructure | Tied to the workload and platform lifecycle            |
| Isolation     | VLANs, VRFs, firewalls           | Virtual networks, namespaces, policies                 |
| Operations    | Network team centered            | Shared across network, platform, and application teams |
| Scale pattern | Planned infrastructure growth    | Dynamic workload growth                                |
| Observability | Device and link focused          | Flow, workload, service, and policy focused            |

The best cloud networking designs keep the strengths of traditional networking. They use sound routing, clear failure domains, predictable address plans, and measurable operational processes. They also add automation where it reduces manual work and improves consistency.

### What is the difference between cloud networking and network virtualization?

Network virtualization is one part of cloud networking. Network virtualization creates logical network resources on top of physical infrastructure. Cloud networking uses network virtualization, but also includes routing, security, load balancing, DNS, observability, automation, and operational practices.

## What are the core cloud networking services?

Cloud networking provides a comprehensive suite of services that span infrastructure foundations, traffic management, advanced security, and deep observability.

### Virtual networks

A virtual network is an isolated, software-defined network space for workloads. It lets teams segment applications, tenants, environments, and security zones without creating a separate physical network for each one.

In public clouds, this pattern is often exposed as a virtual private cloud (VPC). In OpenStack, a similar concept is exposed through the tenant network. The terminology changes across platforms, but the purpose is consistent: virtual networks create logical boundaries for secure, multi-tenant cloud environments.

### Subnets and IP address management

Subnets are subdivisions of a virtual network. They define IP address ranges within a network. Cloud platforms usually include IP address management so workloads can receive addresses automatically.

While cloud networking uses automations makes provisioning easier, it does not remove the need for routing design, address allocation, or overlap prevention.

### Routing

Routing is the process of directing traffic flow across virtual networks, subnets, tenants, and external environments.

Routing can be centralized, distributed, or integrated with the physical network. The right model depends on scale, performance, failure domains, and operational ownership.

### Gateways

Gateways are the integration points that connect cloud networks to other networks. They often provide internet access, private data center connectivity, virtual private network connectivity, or access to external services.

In private clouds and telco clouds, gateways are the boundary where the cloud architecture meets the wider enterprise or operator network.

### Load balancers

Load balancers are essential components that distribute traffic across multiple application instances. They help applications scale and ensure that they remain available when individual instances fail or change.

In Kubernetes, load balancers enable stable access to Pods via Services, while in infrastructure clouds, load balancers often expose virtual machine workloads or application endpoints to the network.

### Network security policy

Network security policies are rules that define which workloads, users, and services can communicate across a cloud environment. They control traffic based on factors such as source, destination, port, protocol, workload identity, namespace, tenant, or network boundary.

Cloud platforms expose these policies through controls such as security groups, Kubernetes network policies, access control lists, and firewall rules. In cloud environments, security policy should follow the workload lifecycle as closely as possible.

### DNS and service discovery

DNS and service discovery are mechanisms that help workloads find each other by name instead of fixed IP address. They provide stable references for applications, even when workloads move, restart, or scale.

This is especially important in Kubernetes, where Pods are created and destroyed frequently and Services provide stable access to changing groups of Pods.

### Overlays and tunnels

Overlay networks are logical networks built on top of an IP underlay. They often use encapsulation so workloads can communicate across hosts as if they were on the same logical network. This decouples workload networking from the physical network and its constraints. 

While this abstraction is essential for agility, it also introduces trade-offs, including encapsulation overhead, troubleshooting complexity, and additional control plane requirements.

### Network observability

Network observability is the ability to understand how traffic moves, where it is affected, and why failures occur across a cloud environment. Operators need visibility into flows, latency, packet drops, policy decisions, address usage, and failures.

Observability is a Day-2 requirement. A network design that is hard to observe will be hard to operate.

## What are the different types of cloud networking?

Cloud networking is found across different cloud deployment models, spanning public, private, hybrid, multi-cloud, and edge, and telco cloud environments. Each model uses the same basic networking concepts, but the operational responsibility, integration points, and design constraints differ.

### Public cloud networking

Public cloud networking provides network services inside an environment managed by an external provider. Users create virtual networks, subnets, routing rules, gateways, and load balancers through APIs or consoles.

The public cloud provider manages the underlying infrastructure. The user manages the logical network design and policy.

### Private cloud networking

Private cloud networking provides cloud network services in an organization’s own environment. Unlike public cloud models, the operational responsibility resides entirely within the organization – a common requirement in regulated industries, telco clouds, research environments, and large enterprises.

Private cloud networking is often rolled out using platforms such as OpenStack, Kubernetes. In addition, private cloud platforms often integrate with networking tools like OVN, Open vSwitch, and Linux networking. Because the organization owns the full stack, it manages the complete lifecycle, including the physical underlay and platform maintenance.

### Hybrid cloud networking

Hybrid cloud networking is any architecture that connects private environments with public cloud environments. It often involves routing, private connectivity, VPNs, identity boundaries, DNS integration, and policy alignment, to create a unified cloud platform across a mix of private and public infrastructure..

As such, hybrid cloud networking is usually focused on ensuring operational consistency across different environments.

### Multi-cloud networking

Multi-cloud networking refers to architecture that connects workloads and services across more than one cloud provider or cloud platform. Unlike hybrid cloud networking, which bridges public and private cloud environments, multi-cloud networking is focused on managing interoperability and traffic across different providers. 

It is often used for resilience, regulatory requirements, application placement, or supplier diversity.

Multi-cloud networking can add complexity quickly, as it introduces considerable architectural overhead. As a result, teams need clear ownership for IP addressing, routing, identity, policy, observability, and incident response.

### Edge cloud networking

Edge cloud networking is the extension of the network fabric to workloads placed close to users, devices, factories, radio sites, or enterprise locations. This model is defined by physical constraints, such as limited space, limited power, intermittent connectivity, and strict latency requirements.

Edge cloud networking is particularly prominent in telco environments: for example, 5G business services require infrastructure to be closer to the user, rather than being routed from a distant data center. You’ll often see edge cloud networking integrated with transport networks, service chains, radio access networks, and operational support systems.

### Cloud networking for telco clouds

Telco cloud networking builds upon the same core concepts as other cloud environments, such as virtual networks, routing, security policy, and load balancing, but adapts them to the unique, high-performance demands of the telecommunications industry.

Telco clouds carry live traffic, such as calls, data sessions, and network control signals, where performance and availability requirements are stricter than in most enterprise environments. Delays, packet loss, or unexpected restarts that might be tolerated in a standard cloud workload are not acceptable here.

These constraints shape what telco cloud networking needs to support. This includes network functions, control plane workloads (which manage network state and routing decisions), user plane workloads (which carry live subscriber traffic), edge sites, and regulated operations.

Meeting these demands requires predictable performance, deterministic operations, strong isolation, and long lifecycle support. Telco environments also need integration with existing transport networks, routing policies, timing systems, and operational support systems that predate the cloud.

Because telco infrastructure evolves slowly, cloud networking must support both modern cloud-native applications and older virtualised network functions on the same platform, using Kubernetes for CNFs, OpenStack for VNFs, and physical networking where software switching introduces too much latency.

Where software networking alone cannot meet throughput or latency demands, technologies such as SR-IOV, DPDK, and SmartNICs move packet processing closer to the hardware. This reduces flexibility, so a pragmatic design applies hardware acceleration only where the workload requires it.

## What are the benefits of cloud networking?

Cloud networking helps teams move faster, scale infrastructure more easily, and protect sensitive data through programmable connectivity, automated policy, and consistent network controls.

Cloud networking can help organizations improve:

{{ text_list_kh (items=[
  "Speed: because teams can create, update, and remove network resources through APIs instead of waiting for manual device-by-device configuration",
  "Consistency: because automation reduces configuration drift",
  "Isolation: because tenants and applications can use separate logical networks",
  "Scalability: because networks can follow workload growth",
  "Portability: because open architectures reduce dependence on one environment",
  "Operations: because policy and connectivity can become part of platform workflows"
])}}

## What are the challenges of cloud networking?

To implement cloud networking effectively, organizations must address six critical areas: multi-layer visibility,  ownership, lifecycle management, performance tuning, legacy integration, and operational complexity.

Let’s look into these challenges in more detail::

{{ text_list_kh (items=[
  "Multi-layer visibility: operators need to understand both the physical underlay and the virtual overlay. A packet may cross a virtual switch, tunnel, host firewall, routing namespace, load balancer, and physical fabric.",
  "Ownership: cloud networking sits between network engineering, platform engineering, security, and application teams. Clear responsibility matters.",
  "Lifecycle management: cloud platforms change over time. Networking components need upgrades, testing, rollback plans, and compatibility management.",
  "Performance tuning: overlay networks, policy enforcement, encryption, and service proxies can affect latency and throughput. Performance-sensitive workloads need careful placement and data path design.",
  "Legacy integration: most organizations already have routing domains, address plans, DNS systems, firewalls, monitoring tools, and operational processes. Cloud networking must fit into that environment.",
  "Operational complexity: cloud networking can also increase complexity if teams introduce overlays, policies, and abstractions without clear ownership."
])}}

## What is the future of cloud networking?

Cloud networking is evolving toward more automation, stronger policy models, better observability, and tighter integration with workload platforms:

{{ text_list_kh (items=[
  "More Kubernetes-native networking",
  "More multi-cluster and hybrid connectivity",
  "Wider use of IPv6 and dual-stack designs",
  "More policy automation",
  "Stronger integration between network and identity",
  "More use of hardware offload for demanding workloads",
  "Increased focus on operational simplicity",
  "More open source networking in private and edge clouds"
])}}

The direction is clear: cloud networking is becoming part of the platform engineering model. Network expertise remains essential, but the interface is increasingly declarative, automated, and workload-aware.

## How can Canonical support your cloud networking requirements?

Canonical’s approach to cloud networking starts from a simple principle: network infrastructure should be as programmable and consistent as the cloud platforms it supports.

Each solution from Canonical comes with cloud networking components suited to how it is deployed and operated:

{{ text_list_kh (items=[
  "<a href="https://ubuntu.com/kubernetes">Canonical Kubernetes</a> is Canonical's CNCF-conformant Kubernetes distro with long-term support. It  standardizes on Cilium with Gateway API support. ",
  "<a href="https://canonical.com/openstack">Canonical OpenStack</a> is Canonical's enterprise cloud platform built on distilled upstream OpenStack. It provides private cloud infrastructure and uses OVN as its software-defined networking backend. ",
  "<a href="https://canonical.com/microcloud">MicroCloud</a> is Canonical’s lightweight private cloud stack and uses MicroOVN to bring the same OVN-based model into smaller private cloud and edge deployments."
])}}

The unifying thread is open source infrastructure, upstream alignment, and operational consistency across the cloud footprint. Operators should be able to understand, automate, observe, and maintain the networking layer over time, whether they run Kubernetes, OpenStack, MicroCloud, or a combination of them.

### What is OVN in cloud networking?

Before we dive into specific solutions, we need to mention OVN, the system that runs across Canonical Openstack and MicroCloud. Open Virtual Network (OVN) is an open source software-defined networking system for Open vSwitch. It provides logical networking features like switches, routers, and security policies, translating them into rules enforced across nodes.

[Learn how OVN connects cloud workloads ›](https://canonical.com/blog/data-centre-networking-what-is-ovn)

OVN acts as a centralized control plane, letting operators define networks in logical terms while automatically applying them across the infrastructure. This enables scalable, consistent networking without manual host configuration, making it well suited for dynamic cloud and edge environments.

### Cloud networking in Kubernetes

[Kubernetes networking](https://documentation.ubuntu.com/canonical-kubernetes/latest/snap/explanation/networking/) connects Pods, Services, Nodes, and external clients. Kubernetes defines the model, while the Container Network Interface (CNI) plugin implements the data path, policy behavior, and integration with the infrastructure network.

Canonical Kubernetes standardizes on Cilium as the default CNI. Cilium uses eBPF to handle networking and network policy directly on each node, reducing the gap between what the application expects and how packets are actually handled. The choice of CNI is not a side decision in Kubernetes. It shapes service routing, policy enforcement, observability, upgrade behavior, and performance across the entire cluster lifecycle. Standardizing on one default gives platform teams a more consistent operational model.

[Canonical Kubernetes also supports the Kubernetes Gateway API](https://documentation.ubuntu.com/canonical-kubernetes/latest/snap/howto/networking/default-gateway) for north-south traffic management: a more expressive and extensible model than Ingress, allowing teams to define routing, traffic splitting, and HTTP routing rules as native Kubernetes resources.

Common cloud networking functions in Kubernetes include:

{{ text_list_kh (items=[
  "<strong>Pod-to-Pod connectivity</strong>: ensuring that pods can communicate reliably across nodes without manual configuration",
  "<strong>Service discovery</strong>: allowing applications to find and communicate with each other using stable endpoints",
  "<strong>Ingress and egress traffic</strong>: managing how traffic enters and leaves the cluster",
  "<strong>Network policy</strong>: defining rules to control traffic flow between pods ",
  "<strong>Load balancing</strong>: distributing traffic across multiple pods or services to improve availability and performance",
  "<strong>Multi-network attachments</strong>: enabling pods to connect to multiple networks for advanced use cases",
  "<strong>IPv4 and IPv6 support</strong>: dual-stack networking for broader compatibility",
  "<strong>Integration with physical or virtual infrastructure</strong>: connecting Kubernetes networking with existing data center or cloud environments"
])}}

For telco and high-performance workloads, Kubernetes networking may also involve Single Root I/O Virtualization (SR-IOV), Data Plane Development Kit (DPDK), CPU pinning, huge pages, and multiple network interfaces. These techniques can improve performance, but they also add operational constraints. They should be used where the workload needs them, not as a default for every application.

[Learn how Canonical Kubernetes supports open telco cloud infrastructure ›](https://ubuntu.com/blog/bringing-canonical-kubernetes-to-sylva-a-new-chapter-for-european-telco-clouds)

### Cloud networking in OpenStack

OpenStack networking is commonly provided by Neutron ,OpenStack's dedicated networking service. Neutron provides network connectivity as a service between interface devices managed by other OpenStack services, such as virtual network interfaces attached to instances.

In Canonical OpenStack, OVN serves as the software-defined networking backend. It enables scalable and distributed network operations, by managing logical constructs such as networks, routers, and access control policies, ensuring consistent behavior across the cloud environment.

[Find out more about Canonical OpenStack architecture ›](https://canonical.com/openstack/architecture)

OpenStack users interact with Neutron APIs to design provider networks, tenant networks, routers, security groups, and external connectivity. OVN then turns that logical model into distributed switching and routing behavior across the cloud.

A typical OpenStack cloud networking design  encompasses the following functional areas.

#### Network connectivity and routing

{{ text_list_kh (items=[
  "<strong>Tenant networks</strong>: isolated virtual networks created for individual projects or tenants, each their own IP addressing and topology.",
  "<strong>Provider networks</strong>: networks that map directly to the underlying physical infrastructure, enabling instances for external connectivity.",
  "<strong>Virtual routers</strong>: software-based routers that handle routing, NAT, and gateway functions between networks.",
  "<strong>Distributed east-west routing</strong>: routing of traffic between instances within the cloud (east-west) that is distributed across compute nodes.",
  "<strong>North-south gateways</strong>: components that manage traffic entering and leaving the cloud environment, connecting internal networks to external networks or the internet.",
  "<strong>Integration with the physical fabric</strong>: connecting virtual networking constructs with the underlying physical infrastructure."
])}}

#### Security and access

{{ text_list_kh (items=[
  "<strong>Security groups</strong>: sets of firewall rules applied to instances to control inbound and outbound traffic at the virtual NIC level.",
  "<strong>Floating IPs</strong>: publicly routable IP addresses that can be dynamically associated with instances, enabling external access, without changing the instance’s private IP.",
])}}

#### Management and services

{{ text_list_kh (items=[
  "<strong>DHCP services</strong>: services that automatically assign IP addresses and network configuration (such as gateway and DNS) to instances when they boot.",
  "<strong>Metadata services</strong>: endpoints that provide instances with configuration data, such as SSH keys, user data, and instance-specific information at runtime.",
])}}

For private cloud and telco cloud environments, OpenStack networking remains important because many operators still need virtual machine infrastructure, strong tenant isolation, and infrastructure-as-a-service APIs. The main operational challenge is lifecycle consistency. Networking must remain reliable through upgrades, host maintenance, capacity growth, and changing tenant requirements.

### Cloud networking in MicroCloud

MicroCloud is Canonical’s lightweight private cloud stack. It combines LXD for compute, MicroCeph for storage, and MicroOVN for networking.

[Discover the MicroCloud components ›](https://canonical.com/microcloud/what-is-microcloud)

From a networking perspective, MicroCloud is useful because it brings OVN-based cloud networking into a smaller operational footprint. That makes it relevant for edge sites, labs, remote offices, and compact private cloud deployments where operators still need virtual networking, isolation, routing, and lifecycle-managed infrastructure.

MicroCloud’s networking model uses OVN to provide logical networks for instances. LXD integrates with OVN networks, and those networks can connect to existing bridge or physical networks for access beyond the local cloud.

This is a practical example of cloud networking at the edge. The same basic concepts appear in larger clouds: an underlay network, logical overlays, routing, external access, and a control plane that manages network intent.

## Frequently asked questions about cloud networking

### What is an example of cloud networking?

An example of cloud networking is a private cloud where virtual machines run on OpenStack, containers run on Kubernetes, and OVN provides virtual networking between workloads. The platform creates networks, routes traffic, applies policy, and connects services to external networks.

### Is cloud networking the same as cloud computing?

Cloud networking is part of cloud computing. Cloud computing includes compute, storage, networking, applications, and services. Cloud networking provides the connectivity and policy layer that lets those resources communicate.

### Is cloud networking the same as SDN?

Cloud networking is broader than SDN (software-defined networking). SDN provides software-based control of network behavior. Cloud networking uses SDN concepts as part of a full cloud operating model that includes workloads, APIs, automation, security, and lifecycle management.

### What should teams consider when designing cloud networking?

A practical cloud networking design starts with the operating model.

Teams should answer these questions early on:

{{ text_list_kh (items=[
  "Who owns the physical underlay?",
  "Who owns the cloud network control plane?",
  "Who defines tenant and application policy?",
  "How are IP addresses allocated?",
  "How does the cloud connect to external networks?",
  "Where does routing happen?",
  "Where does security policy apply?",
  "How are failures detected?",
  "How are upgrades tested?",
  "How are performance requirements measured?"
])}}

These questions are more important than selecting a tunnel protocol or a specific plugin first. Technology choices should follow the operational model, workload requirements, and failure assumptions.

### What is an overlay network?

An overlay network is a logical network built on top of another network. In cloud environments, overlays often use tunnels to connect workloads across hosts while keeping tenant networks separate from the physical underlay.

### What is the underlay network?

The underlay network is the physical or base IP network that connects servers, switches, routers, and sites. The cloud overlay depends on the underlay for reachability and performance.

### What is north-south traffic?

North-south traffic is traffic that enters or leaves a cloud environment. Examples include user traffic from the internet, traffic to a corporate data center, or traffic to an external service.

### What is east-west traffic?

East-west traffic is traffic between workloads inside the cloud environment. Examples include communication between application services, databases, message queues, and internal APIs.
