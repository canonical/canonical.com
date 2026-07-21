---
effective_date: "26 JUNE 2026"
---

<!--
  HOW TO MAINTAIN THIS DOCUMENT
  ==============================
  This file is the source of truth for the Ubuntu Pro Description page.
  Update individual sections in place rather than replacing the entire file.

  SECTION DELIMITERS
  ------------------
  Each section begins with a delimiter comment that tells the page which
  part of this file belongs to which exportable section:

     <!-- section: introduction --\>
     <!-- section: security-compliance --\>
     <!-- section: support --\>
     <!-- section: support-services-process --\>
     <!-- section: add-ons --\>
     <!-- section: managed-services --\>
     <!-- section: firefighting-support --\>
     <!-- section: ops-consultancy --\>
     <!-- section: professional-support-services --\>
     <!-- section: embedded-services --\>
     <!-- section: definitions --\>

  Do not rename these ids — they must match the keys in _DEF_TERMS inside webapp/ubuntu_pro_description.py.

  ANCHOR LINKS
  ------------
  Links to external URLs: write normally, e.g.
     [Ubuntu lifecycle](https://ubuntu.com/about/release-cycle)

  Links to definition terms: use #def-<slug>, e.g.
     [Environment](#def-environment)
     [CVEs (High and Critical)](#def-cves-high-and-critical)
  The full list of valid #def-* slugs is in _DEF_TERMS in
  webapp/ubuntu_pro_description.py.

  EFFECTIVE DATE
  --------------
  The date shown at the top of the page is set in EFFECTIVE_DATE inside
  webapp/ubuntu_pro_description.py — not here.
-->
<!-- section: introduction -->

## Introduction

Ubuntu Pro is a subscription that gives you an additional stream of security updates and packages that meet compliance requirements, such as FIPS or FedRAMP, on top of an Ubuntu LTS. For support and managed solutions customers, it also includes expert support for [troubleshooting](#def-troubleshooting), [break-fix](#def-break-fix-support) and [bug-fix](#def-bug-fix-support) on the full open-source stack or on its subset (Infra-only).

As a customer, you are entitled to the following coverage, depending on the appropriate support level on a per-machine basis.

Each subscription can cover one or more:

1. **Physical server:** The subscription is attached to a physical host. Where all physical hosts in an [Environment](#def-environment) are subscribed, the subscription also applies to [Ubuntu Guests](#def-ubuntu-guest) in the Environment that are operated by the subscriber for the subscriber's internal business purposes.
2. **Virtual machine:** The subscription is attached to an Ubuntu virtual machine or automatically attached at launch under a public cloud (Google Cloud, AWS, Azure, etc.). This subscription covers Ubuntu images running on virtual machines or in containers.
3. **Desktop:** The subscription is limited to a machine with [Desktop use cases](#def-desktop-use-case). It can also cover Ubuntu on [Windows Subsystem for Linux](https://ubuntu.com/wsl) (WSL) and developer tools such as [MicroK8s](https://canonical.com/microk8s), [Data Science Stack](https://ubuntu.com/ai/data-science) and [Multipass](https://canonical.com/multipass).
4. **Device:** The subscription is attached to a physical device for [Device use cases](#def-device-use-case) including customer's hardware that has been certified or enabled by Canonical.

Each subscription can be purchased at one of three support levels:

1. **self-support**
2. **support (weekday)**
3. **support (24/7)**

and must cover all Ubuntu systems within an [Environment](#def-environment).

Additionally, the subscription might cover the full stack (**Ubuntu Pro**), or just the infrastructure subset of the stack (**Ubuntu Pro (Infra-only)**). Unless otherwise stated, a subscription will be Ubuntu Pro.

Detailed pricing can be found at: [https://ubuntu.com/pricing/pro](https://ubuntu.com/pricing/pro)

Ubuntu Pro subscriptions are governed by the terms at [https://ubuntu.com/legal/ubuntu-pro-service-terms](https://ubuntu.com/legal/ubuntu-pro-service-terms) unless otherwise agreed in writing with Canonical.

<!-- section: security-compliance -->

## Security and compliance

As an Ubuntu Pro or Ubuntu Pro (Infra-only) customer, with or without support, you are entitled to the following:

### 1. Expanded Security Maintenance ([ESM](#def-esm))

1. Available fixes for [CVEs (High and Critical)](#def-cves-high-and-critical) and selected medium CVE fixes for a number of packages, as specified below
2. Ubuntu Pro and Ubuntu Pro (Infra-only) subscriptions cover packages in the [Ubuntu Main](#def-ubuntu-main) repository between [end of Standard Support and end of Ubuntu Pro Support](https://ubuntu.com/about/release-cycle) (esm-infra)
3. Only Ubuntu Pro subscriptions cover packages in the [Ubuntu Universe](#def-ubuntu-universe) until the end of [Ubuntu Pro Support](https://ubuntu.com/about/release-cycle) (esm-apps). This coverage is not included in Ubuntu Pro (Infra-only) subscriptions
4. [ESM](#def-esm) does not guarantee:
   1. Fixes for architectures other than the [Covered Architectures](#def-covered-architectures)
   2. [Bug-fixes](#def-bug-fix-support), unless a bug was created by an ESM security fix
   3. A guarantee to fix all High or Critical [CVEs](#def-cves-high-and-critical)
   4. Replacements for cryptography algorithms that are no longer secure

### 2. Legacy add-on

1. The Legacy add-on provides security maintenance (and optional break-fix support) between the [end of Expanded Security Maintenance and the end of Legacy coverage](https://ubuntu.com/about/release-cycle).
2. The Legacy add-on carries the same limitations as those outlined for ESM in 1.4.

### 3. Other security fixes

1. Security fixes for OpenStack, Ceph, MAAS, Kubernetes
   1. Supported versions of Canonical Kubernetes Platform’s k8s snap include:
      1. for long-term supported (LTS) Kubernetes versions, released every two years, security patching for ten years in the “stable” release channel and an additional five years in the “legacy” release channel from the [release date of the Kubernetes version included in the release](https://ubuntu.com/about/release-cycle#canonical-kubernetes-release-cycle)
      2. to enable upgrades between Kubernetes LTS versions every two years, Canonical provides at least 12 months of security patching for non-LTS Kubernetes releases that are between the latest Kubernetes LTS and the previous one
   2. Supported versions of Charmed Kubernetes and MicroK8s clusters include:
      1. security patching for N-4 (the latest and previous four) releases in the “stable” release channel
2. Available [High, Critical CVE](#def-cves-high-and-critical) and selected medium fixes for a number of core ROS packages for ROS 1 Kinetic and Melodic, and ROS 2 Foxy. This includes packages in the [REP-142](https://www.ros.org/reps/rep-0142.html) ‘[ros_base](https://www.ros.org/reps/rep-0142.html#ros-base)’

### 4. [Certified components for compliance, hardening and audit](https://ubuntu.com/security/certifications)

1. FIPS 140-2 Level 1 certified modules for Ubuntu 20.04 LTS, 18.04 LTS and 16.04 LTS releases using the generic kernel
2. FIPS 140-3 Level 1 certified modules for Ubuntu 22.04 LTS releases using the generic kernel (24.04 LTS available for testing and preview)
3. Access to certified CIS Benchmark tooling Levels 1 and 2 for Ubuntu 18.04 LTS and 16.04 LTS
4. Ubuntu Security Guide (USG) for Ubuntu 20.04 LTS, 22.04 LTS, and 24.04 LTS which includes certified DISA-STIG profiles and CIS benchmark tooling Levels 1 and 2
5. Common Criteria EAL2 for Ubuntu 18.04 LTS and 16.04 LTS

### 5. [Kernel Livepatch](https://ubuntu.com/livepatch)

1. Access to Canonical’s kernel livepatch client and security livepatches for selected High and Critical kernel CVEs
2. Kernel Livepatch may provide non-security bug fixes as kernel livepatches
3. Only [Livepatch Covered Kernels](https://ubuntu.com/security/livepatch/docs/livepatch/reference/kernels) are available for livepatching
4. Access to Canonical’s Livepatch on-prem server

### 6. Access to other services

1. Access to the real-time kernel maintained by Canonical for Ubuntu 22.04 LTS with the upstream [5.15-rt](https://cdn.kernel.org/pub/linux/kernel/projects/rt/5.15) patches integrated is provided to meet the low latency requirements
2. Access to Canonical’s Landscape systems management tool
3. Access to the support portal and Knowledge Base

### 7. Subscription limitations

1. Ubuntu Pro subscriptions do not cover virtual machines, containers, workloads or computing capacity running Ubuntu that is provided or made available as a service from the Ubuntu Pro subscriber to a third party.
2. Ubuntu Pro subscriptions may not be used by service providers, including managed service providers, hosting providers, or similar providers, to extend Ubuntu Pro coverage – whether host-based or per-instance – to workloads provided to their customers, including in cloud or hosted environments.

<!-- section: support -->

## Support

You can add different levels of technical support on top of your Infra-only or full Ubuntu Pro subscription. All levels of support are available as a weekday or 24/7 service.

### 8. Scope of Support

1. Included in all scopes

   1. [Certified hardware](#def-certified-hardware), including certified public cloud instances
      1. Support applies to the customer’s hardware that has been certified or enabled.
   2. Ubuntu releases

      1. [Break-fix Support](#def-break-fix-support) for troubleshooting and usage, standard installation, configuration, and maintenance of all packages in the [Ubuntu Main](#def-ubuntu-main) repository of an Ubuntu LTS release when installed using official sources and within the [Ubuntu lifecycle](https://www.ubuntu.com/about/release-cycle)

   3. Supported Services

      1. Additional packages, kernels and services are within the scope of support:

         1. Packages in the Ubuntu Cloud Archive
         2. [Supported](https://ubuntu.com/about/release-cycle) or [enabled](#def-enabled-kernel) Kernels
         3. Landscape client
         4. Kernel Livepatch
         5. Packages and profiles for FIPS, DISA-STIG and Common Criteria EAL2 provided by Ubuntu Pro

      2. Support is not provided for any packages that have been modified by the customer or third parties

   4. Ubuntu Assurance Program
      1. Ubuntu Pro + support customers are entitled to the [Ubuntu Assurance Programme](http://www.ubuntu.com/legal/ubuntu-advantage/assurance). Canonical may update the Assurance Programme and its terms periodically

2. [Infra-only support](#def-infra-support)
   1. Kubernetes, as defined in 9.1
   2. OpenStack, as defined in 9.2
   3. Ceph Storage, as defined in 9.3
   4. MAAS, as defined in 9.4
   5. LXD, as defined in 9.5
   6. MicroCloud, as defined in 9.5
   7. Enterprise Store, as defined in 9.7
   8. All packages in [Ubuntu Main](#def-ubuntu-main)
   9. LTS Ubuntu base images at [https://hub.docker.com/\/ubuntu/,](https://hub.docker.com//ubuntu/) [https://gallery.ecr.aws/lts/ubuntu](https://gallery.ecr.aws/lts/ubuntu)
3. Ubuntu Pro + Support includes the following in addition to infra-only support:

   1. All packages in [Ubuntu](#def-ubuntu-main) [Universe](#def-ubuntu-universe), starting with 18.04 LTS and onwards
   2. Canonical-maintained applications published in the “stable” channel:

      1. [OCI](https://opencontainers.org/)-compliant application images listed in [https://github.com/orgs/canonical/packages?ecosystem=container\&tab=packages\&ecosystem=container\&q=charmed-](https://github.com/orgs/canonical/packages?ecosystem=container&tab=packages&ecosystem=container&q=charmed-) , [hub.docker.com/u/ubuntu/](https://hub.docker.com/u/ubuntu/) and [gallery.ecr.aws/ubuntu](https://gallery.ecr.aws/ubuntu)

         1. Container images are made of multiple layers. The Ubuntu Pro maintenance and support scope is limited to layers with unmodified and up-to-date supported content

         2. Where images are composed of additional layers, Canonical’s coverage will be limited to the Canonical-maintained Ubuntu container image layers and any packages installed from the [Ubuntu Main](#def-ubuntu-main) and [Universe](#def-ubuntu-universe) repositories

         3. Support exclusions

            1. Outdated images: Canonical publishes “stable” channel content via OCI registry image tags, for each supported track. A track is typically associated with an Ubuntu LTS release; where the Canonical-maintained Ubuntu container image includes a specific application, the track may also be associated with an application version. Only the latest stable content is eligible for support under Ubuntu Pro. Any content that is not aligned with one of the available “stable” channel content tags for the given Canonical maintained Ubuntu container image is not considered the latest stable content

            2. Third party software: Canonical may refuse to provide support for issues caused by software in the container image, a container orchestration platform or host operating system if the software, container orchestration platform or host operating system are provided by a third party and not maintained by Canonical

      2. Canonical maintained snaps listed at [https://snapcraft.io/publisher/canonical](https://snapcraft.io/publisher/canonical).
      3. Canonical maintained [charms](#def-charm) listed in [https://charmhub.io/](https://charmhub.io/).
      4. Additional applications listed at [https://ubuntu.com/support](https://ubuntu.com/support)

4. The Legacy add-on, if purchased, extends the support term. The scope of the Legacy add-on is limited regarding:

   1. Severity 1 issues: the maximum level of support provided is Severity 2\. All Severity 1 issues will be prioritised as Severity 2\.
   2. Bug-fix: Bug-fix support is provided only in cases where a bug is preventing migration to a newer version.

### 9. Supported Products

1. [Kubernetes](https://ubuntu.com/kubernetes)

   1. Installations of Kubernetes which are within their [support lifecycle](https://ubuntu.com/about/release-cycle) and which are deployed via:
      1. [Canonical Kubernetes Platform](https://documentation.ubuntu.com/canonical-kubernetes/)
      2. [Charmed Kubernetes](https://ubuntu.com/kubernetes/charmed-k8s)
      3. [MicroK8s](https://microk8s.io/)
      4. A [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)-deployed cluster of unmodified upstream Kubernetes binaries as published by the CNCF, for the [most recent three minor releases](https://kubernetes.io/releases/%20), deployed on Ubuntu as base OS, as long as Ubuntu is deployed using the official Canonical image repository
   2. For any deployment of [Charmed Kubernetes](#def-charmed-kubernetes) and Canonical Kubernetes Platform carried out by Canonical while under contract for a deployment, which results in the customisation of any [Charms](#def-charm), those custom charms will be supported for 90 days after the release of new versions of the charms containing the customization.

      1. All software, including charms, snaps, images and debs, required to deploy Kubernetes is covered by [bug-fix](#def-bug-fix-support) and [break-fix support](#def-break-fix-support)

2. [OpenStack](https://canonical.com/openstack)

   1. Support for OpenStack deployments is limited to Canonical OpenStack (based on OpenStack Charms), aka Charmed OpenStack and Canonical OpenStack (based on Sunbeam).

      1. Support can only be provided for [Environments](#def-environment) with at least 3 deployed nodes for eligible Canonical OpenStack (based on Sunbeam) releases and 12 deployed nodes for any eligible Canonical OpenStack (based on OpenStack Charms) release.

   2. The duration of support depends on the OpenStack product being used and the installed software version. Please refer to the [Canonical OpenStack documentation](https://canonical-openstack.readthedocs-hosted.com/en/latest/reference/release-cycle-and-supported-versions/) for detailed information on supported products and versions.
   3. Charmed OpenStack requirements:
      1. Hardware must meet the minimum criteria as specified by Canonical as part of the [Private Cloud Build](https://ubuntu.com/openstack/consulting) or other Canonical [consulting engagements](https://canonical.com/consulting).
      2. Deployment was done by Canonical via [Private Cloud Build](https://ubuntu.com/openstack/consulting) or it was validated by Canonical.
   4. Canonical OpenStack based on Sunbeam requirements:
      1. Hardware must meet the minimum criteria as specified in the [Canonical OpenStack documentation](https://canonical-openstack.readthedocs-hosted.com/en/latest/reference/enterprise-requirements/)
      2. The OpenStack cloud was deployed with [Sunbeam](https://canonical-openstack.readthedocs-hosted.com/en/latest/how-to/#installation)
   5. OpenStack support includes access to Canonical-provided Microsoft-certified drivers in Windows virtual machine instances
   6. OpenStack support requires all [nodes](#def-node) that participate in the OpenStack deployment to be covered under an active support agreement
   7. Ironic service: In order to be eligible for support, all machines managed by Ironic must be covered under a standalone MAAS support agreement or an Ubuntu Pro subscription. Machines not running Ubuntu can still be covered by MAAS support, even in the absence of Ubuntu Pro eligibility.
   8. Scope of OpenStack support:
      1. [Charms](#def-charm) used for deployment
      2. All Canonical-provided packages, Canonical-maintained snaps and OCI images required to deploy and run OpenStack
      3. Incidents found during the upgrades between major versions of OpenStack or LTS versions of Ubuntu, Juju, and MAAS are supported as long as the upgrade is performed following a documented process as specified by Canonical as part of the Private Cloud Build, Cloud Validation or in Canonical OpenStack (based on Sunbeam) documentation
   9. Limited OpenStack Support
      1. OpenStack clouds, other than Sunbeam-based, not deployed through Private Cloud Build or otherwise validated through Cloud Validation, are limited to [Bug-fix Support](#def-bug-fix-support)
      2. OpenStack support does not include support beyond [Bug-fix Support](#def-bug-fix-support) during the deployment or configuration of an OpenStack cloud
   10. Exclusions
       1. Support excludes customisations which are not considered [Valid Customisations](#def-valid-customisations) or are not covered in Canonical OpenStack (based on Sunbeam) documentation
       2. Support for workloads other than those required to run an OpenStack deployment
       3. Support for virtual machine instances other than [Ubuntu Guests](#def-ubuntu-guest)
       4. Support for incidents and performance degradations resulting from decisions made when self-deployed by the customer and not validated by Canonical or including customisations that are not [Valid Customisation](#def-valid-customisations)

3. [Ceph Storage](https://ubuntu.com/ceph)

   1. Ceph storage support depends on the Ubuntu release deployed on the underlying storage [nodes](#def-node):

      1. Support can only be provided for [environments](#def-environment) with at least three infra nodes and nine storage nodes for eligible Charmed Ceph releases or 3 Ceph nodes for eligible MicroCeph releases

      2. The [version of Ceph](https://ubuntu.com/ceph/docs/supported-ceph-versions) initially included in the release of an LTS version of Ubuntu is supported for the entire lifecycle of that Ubuntu version

      3. Updated releases of Ceph are made available in the Ubuntu Cloud Archive after an LTS version is released. Each Ceph release in the Ubuntu Cloud Archive is supported on an Ubuntu LTS version for a minimum of 18 months from the [release date](#def-release-date) of the Ubuntu version that included the applicable Ceph version

   2. Canonical will provide support for 576TB of raw storage per Ceph storage [node](#def-node). Note that only Ceph storage [nodes](#def-node) count towards the 576TB free tier of raw storage per [node](#def-node)
   3. If the [node](#def-node) allowance is exceeded, [additional Ceph storage support](https://ubuntu.com/pricing/infra) needs to be acquired
   4. Customers who have purchased Ceph storage support for an unlimited amount of storage are limited to support of a single [Ceph cluster](#def-ceph-cluster)
   5. Ceph storage support requires all [nodes](#def-node) that participate in the Ceph storage cluster to be covered under an active support agreement
   6. Full Ceph storage support
      1. Requirements:
         1. The [Ceph storage cluster](#def-ceph-cluster) was deployed via a Private Cloud Build, Ceph Cluster Build or was validated through a Cloud Validation engagement. These requirements don’t apply to [MicroCeph](https://canonical-microceph.readthedocs-hosted.com/en/v19.2.0-squid/).
      2. Scope:
         1. Support for the [Charms](#def-charm), Rocks, or Snaps deployed
         2. Support is included for all packages required to run Ceph as deployed
         3. Any incidents found during the upgrades of Ceph components as part of the regular Ubuntu LTS maintenance cycle
         4. Any incidents found during the upgrades between versions of Ceph or LTS versions of Ubuntu, Juju, and MAAS are supported as long as the upgrade is performed following a documented process as specified by Canonical as part of the Private Cloud Build or Cloud Validation Package
         5. The addition of new Ceph storage [nodes](#def-node) and the replacement of existing [nodes](#def-node) with new [nodes](#def-node) of equivalent capacity are both supported
      3. Covered Software
         1. All software, including [charms](#def-charm), snaps, images and debs required to deploy Ceph as defined under 8.3.1 and 8.3.2. is covered by [bug-fix](#def-bug-fix-support) and [break-fix support](#def-break-fix-support)
   7. Limited Ceph storage support
      1. Stand-alone storage clusters not deployed through a [Ceph Cluster Build Package](https://ubuntu.com/ceph/consulting) or cloud-attached Ceph storage clusters not validated using a Cloud Validation Package are limited to [Bug-fix](#def-bug-fix-support) Support only
      2. Ceph storage support does not include support beyond [Bug-fix](#def-bug-fix-support) Support during the deployment or configuration of a standalone or cloud-attached storage cluster

4. [MAAS](https://maas.io/)
   1. When running on top of Ubuntu, versions of MAAS are supported on a corresponding LTS version of Ubuntu for N-3 MAAS versions
   2. Support scope:
      1. Support for the ability to boot machines using operating system images provided by Canonical
      2. Support for the tooling required to convert certified operating system images not provided by Canonical into MAAS images
   3. To be supported, managed machines must be covered by an Ubuntu Pro subscription if they are running Ubuntu and require support, or a standalone MAAS support agreement if they are not running Ubuntu. The MAAS controllers require a dedicated Ubuntu Pro (Infra-only) or Ubuntu Pro subscription.
   4. Out of scope. MAAS support does not provide:
      1. Support for workloads, packages and service components other than those required to run a MAAS deployment
      2. Support for the [nodes](#def-node) deployed using MAAS but not covered under Ubuntu Pro
      3. Support for design and implementation details of a MAAS deployment
      4. Access to Landscape and Canonical Livepatch Service for machines deployed with MAAS
5. [LXD](https://canonical.com/lxd) and [MicroCloud](https://canonical.com/microcloud)
   1. Versions of LXD and MicroCloud within their [support lifecycle](https://ubuntu.com/about/release-cycle) and all supported versions of Canonical-provided packages and Canonical-maintained snaps required to deploy and run MicroCloud (MicroCloud, MicroCeph. MicroOVN, LXD)
   2. Support needs to be purchased for all MicroCloud cluster members
6. Dedicated Snap Store: When purchased on top of Ubuntu Pro (Infra-only) + Infra Support or Ubuntu Pro + Support, Canonical will provide support for associated Store Services.
7. Enterprise Store
   1. Customer is entitled to a license to use the Enterprise Store per subscription, and may use as many Enterprise Store instances as the number of Ubuntu Pro (Infra-only) or Ubuntu Pro subscriptions purchased.
   2. Canonical will provide Customer support for the Enterprise Store.

### 10. Exclusions

1. Ubuntu Pro Desktop support only covers packages installed from the base Ubuntu desktop image as well as packages necessary for basic network authentication. It does not cover:
   1. Issues relating to dual-booting (cohabitating with other operating systems)
   2. Peripherals which are not certified to work with Ubuntu
   3. Community flavours of Ubuntu
   4. Experimental or beta features.
2. Container images may be generated from Ubuntu Pro bits only if the resulting container images are deployed to Ubuntu Pro-covered machines.

<!-- section: support-services-process -->

## Support Services Process

### 11. Service initiation

1. Upon commencement of the services, Canonical will provide access for a single technical representative to Landscape, the support portal, and the online Knowledge Base
2. The customer, through their initial technical representative, may select their chosen technical representatives who act as primary points of contact for support requests. The customer will receive up to 5 dedicated, personalised credentials for technical representatives per every 500 [nodes](#def-node) or 50,000 devices under support, but not more than a total of 15 credentials
3. The customer may change their specified technical representatives at any time by submitting a support request via the support portal

### 12. Submitting support requests

1. The customer may open a support request once the customer account has been provisioned within the support portal
2. The customer may submit support cases through the support portal or by contacting the support team by telephone, unless otherwise noted
3. A support case should consist of a single discrete problem, issue, or request
4. Cases are assigned a ticket number and responded to automatically. All correspondence not entered directly into the case, including emails and telephone calls, will be logged into the case with a timestamp for quality assurance
5. When reporting a case, the customer should provide an impact statement to help Canonical determine the appropriate severity level. Customers with multiple concurrent support cases may be asked to prioritise cases according to severity of business impact
6. The customer is expected to provide all information requested by Canonical as we work to resolve the case
7. Canonical will keep a record of each case within the support portal enabling the customer to track and respond to all current cases and allowing for review of historical cases

### 13. Support severity levels

1. Once a support request is opened, a Canonical support engineer will validate the case information and determine the severity level, working with the customer to assess the urgency of the case

2. Canonical will work to provide the customer with restoration of the issue, i.e. a temporary work-around or a permanent solution, following the severity levels as described below. As soon as the impacted core functionality is available, the severity level will be lowered to the new appropriate severity level

3. Canonical will use reasonable efforts to respond to support requests made by the customer within the initial and ongoing response times set forth below, based on the applicable service and severity level, but cannot guarantee a work-around, resolution or resolution time

|                                                                                                                                                                                                                                                                     | Self-support<sup>1</sup>                                | Weekday support                                                                                                                               |                                  | 24/7 support                                                                                                                                  |                                  | Firefighting support (24/7 support add-on)                                                                                                                                                                  |                                                                                                                                                                                                                           |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Hours of coverage**                                                                                                                                                                                                                                               | N/A                                                     | 24/5                                                                                                                                          |                                  | 24/7/365                                                                                                                                      |                                  | 24/7/365                                                                                                                                                                                                    |                                                                                                                                                                                                                           |
| **Available channels**                                                                                                                                                                                                                                              | [Knowledge Base](https://support-portal.canonical.com/) | [Support portal](https://support-portal.canonical.com/), including [Knowledge Base](https://support-portal.canonical.com/), phone, and ticket |                                  | [Support portal](https://support-portal.canonical.com/), including [Knowledge Base](https://support-portal.canonical.com/), phone, and ticket |                                  | Video call during Sev 1 case (one at a time per environment), [Support portal](https://support-portal.canonical.com/), including [Knowledge Base](https://support-portal.canonical.com/), phone, and ticket |                                                                                                                                                                                                                           |
| **Number of cases allowed**                                                                                                                                                                                                                                         | N/A                                                     | Unlimited                                                                                                                                     |                                  | Unlimited                                                                                                                                     |                                  | One firefighting Sev 1 case at a time per environment, unlimited cases otherwise                                                                                                                            |                                                                                                                                                                                                                           |
| **Response times**                                                                                                                                                                                                                                                  | **First response**                                      | **First response**                                                                                                                            | **Ongoing response**<sup>3</sup> | **First response**                                                                                                                            | **Ongoing response**<sup>3</sup> | **First response**                                                                                                                                                                                          | **Ongoing response**<sup>3</sup>                                                                                                                                                                                          |
| **Severity 1** A production service or mission-critical system is down, inoperable, or experiencing a total disruption of work, resulting in a critical and immediate impact on core business operations, with no workaround available                              | N/A                                                     | 4 hours                                                                                                                                       | 2 hours                          | 1 hour                                                                                                                                        | 2 hours                          | 1 hour                                                                                                                                                                                                      | Continuous video call until issue is de-escalated to [Severity 2](https://ubuntu.com/legal/solution-support) if issue affects all users or 4 hours of enhanced support since initial response if issue affects some users |
| **Severity 2** Core functionality in a production environment or mission-critical system is severely degraded, resulting in a major functionality impairment where operations can continue only in a restricted fashion, and no workaround is immediately available | N/A                                                     | 8 business hours<sup>2</sup>                                                                                                                  | 8 business hours<sup>2</sup>     | 2 hours                                                                                                                                       | 8 business hours                 | 2 hours                                                                                                                                                                                                     | 8 business hours                                                                                                                                                                                                          |
| **Severity 3** Issues with a medium to low impact on a production environment                                                                                                                                                                                       | N/A                                                     | 12 business hours<sup>2</sup>                                                                                                                 | Weekly                           | 6 hours                                                                                                                                       | Weekly                           | 6 hours                                                                                                                                                                                                     | Weekly                                                                                                                                                                                                                    |
| **Severity 4** Non-urgent requests with low to no impact on production environments                                                                                                                                                                                 | N/A                                                     | 24 business hours<sup>2</sup>                                                                                                                 | N/A                              | 12 hours                                                                                                                                      | NA                               | 12 hours                                                                                                                                                                                                    | N/A                                                                                                                                                                                                                       |

<sup>1</sup>Included with all [Ubuntu Pro](https://ubuntu.com/pro) subscriptions  
<sup>2</sup>Business hours: 8:00 AM to 5:00 PM at the Customer’s location as set in the Canonical Support portal. Weekends are not included.  
<sup>3</sup>Canonical Support will provide follow-up updates within defined time frames after responding to a customer inquiry. These ongoing response time frames are defined based on the severity level of the issue, and counted from the time of the latest severity update.

### 14. Customer assistance

1. Continuous effort support is dependent on the customer being available at all times to assist Canonical, otherwise Canonical may need to reduce the severity level and its ability to respond accordingly

### 15. Hotfixes

1. To temporarily resolve critical support cases, Canonical may provide a version of the affected software (e.g. package) that applies a patch. Such versions are referred to as “hotfixes”. Hotfixes provided by Canonical are supported for 90 days after the corresponding patch has been incorporated into a release of the software in the [Ubuntu Archives](#def-ubuntu-archive), or Canonical hosted store.

2. A patch may be rejected by the applicable upstream project, in which case the hotfix will no longer be supported, and the case will remain open. The final fix will be provided when the upstream accepts it and incorporates it into a release of the software. The customer should update the software to the new release including the stable fix

### 16. Support language

1.  Canonical will provide the support in English unless specified otherwise

### 17. Remote sessions

1. At the discretion of a Canonical engineer, a remote access service might be offered to access a supported system. In such a case, Canonical will determine which remote access service to use. Canonical engineers expect to have read-only access and do not perform any remote actions on a supported system

### 18. Ask for a Peer Review

1. As a normal business practice, Canonical performs peer reviews on a percentage of all cases. Customers can specifically request a peer review on a case within the case comments or by calling the phone number listed in the support portal. An impartial engineer will be assigned to review the case and provide feedback

### 19. Management escalation

1.  The customer may escalate support issues following the escalation process:

1.  Non-urgent needs: Request a management escalation within the case itself. A manager will be contacted to review the case and post a response within 1 business day

1.  Urgent needs can be escalated to Canonical’s Support Engineering Management by emailing [support-manager@canonical.com](mailto:support-manager@canonical.com). If you require further escalation, email Canonical’s Support Director at [operations-director@canonical.com](mailto:operations-director@canonical.com)

### 20. Levels of Support

1. Canonical provides Support at the following levels:
   1. Level 1 Support: Assistance in [troubleshooting](#def-troubleshooting) and restoring your broken application
   2. Level 2 Support: [Troubleshooting](#def-troubleshooting) and [break-fix](#def-break-fix-support) of defects that are rare or need advanced knowledge to resolve. Typically advanced functionality, advanced configuration, or unexpected behaviour
   3. Level 3 Support: Complex defects involving [bug-fixes](#def-bug-fix-support) on Ubuntu and upstream software. Complex defects involving either core functionalities unavailable, severely degraded, or a complex configuration failure with respect to solely Ubuntu and OpenStack as deployed using Canonical’s tooling (Juju and MAAS)

<!-- section: add-ons -->

## Add-Ons

<!-- section: managed-services -->

### 21. Managed Services

1. Managed Services are an add-on to Ubuntu Pro + [Infra Support](#def-infra-support) (24/7) or Ubuntu Pro + Support (24/7). When added, Canonical will manage the [Environment](#def-environment) as described below.

   Environments benefiting from Managed Services can be deployed on-premises, in the public cloud, or on a combination of the two. To be eligible for Managed Services, the Environment must be deployed (manually or automatically) or validated by Canonical.

2. The Managed Services team will remotely operate, monitor, and manage the [Environment](#def-environment) by:

   1. Service continuity

      1. 24/7 Monitoring, excluding security-related monitoring

      2. 24/7 Alerts

      3. Telemetry Dashboards (accessible also to customers)

   2. (Non-security) Incident management

      1. Prevention and recovery of platforms (ie network, power, compute, storage) and services (ie cloud APIs, observability, connectivity) outages

      2. Diagnosis of external service issues (ie firewall, DNSs, proxies)

      3. Root Cause Analysis for S1 incidents

      4. Node crash recovery

   3. Operations

      1. Backup/Restore of control plane services

      2. Patching/Rebooting (cadence)

      3. Packages refreshed (cadence)

      4. Upgrades (with tailored cadence depending on the offer)

      5. Storage and capacity management/warnings

      6. [CVEs (High and Critical)](#def-cves-high-and-critical) patching/mitigation

      7. Compute expansion/contraction/replacement

      8. Storage expansion/contraction/replacement

      9. SSL certificate rotation and updates

      10. Support for OpenStack roles: Admin, Reader, and Member

      11. Permission and authorization

      12. Admin creation and revocation

      13. Performance tuning and diagnostics

   4. Coordination

      1. Weekly meeting (more than a total of 20 nodes)

      2. Monthly as requested by the customer

   5. Ticket-based tracking of cases

   6. Administrative access. Managed Services will provide the customer with access to the following applications and/or services:

      1. The OpenStack or Kubernetes dashboard, API and CLI  
         2. Landscape (restricted to read-only access)  
         3. Monitoring and logging system (restricted to read-only access)  
         4. Only Canonical will have login access to [Environment](#def-environment) [nodes](#def-node)

   7. [Environment](#def-environment) size. Managed Services will add or remove [nodes](#def-node) from the [Environment](#def-environment) as requested by the customer through a support ticket, provided that the [Environment](#def-environment) does not go under the [Minimum Size Requirement](#def-minimum-size-requirement). As all [Environment](#def-environment) [nodes](#def-node) must be covered under the service, additional fees may apply.

   8. OpsConsultancy packages. Managed Services will provide hours of OpsConsultancy required by the customer through a support ticket, provided that the activity the consultancy is required is pertinent with the Environment. The OpsConsulting additional fees apply and will be charged the month after the completion of the consultancy .

   9. For Environments deployed directly from public cloud marketplaces, Customer is responsible for configuring the Environment’s upper and lower node limits at the time of deployment, within the options presented by the marketplace listing. Customer can request to change these limits via Support ticket or, where possible, directly on the marketplace dashboard.

   10. Ubuntu, OpenStack, and Kubernetes upgrades. Managed Services will ensure the customer’s [Environment](#def-environment) remains on a supported LTS version of Ubuntu and OpenStack and/or Kubernetes

       1. Upgrades will be performed on a per-AZ basis within maintenance windows decided in agreement with Customer.

       2. Downtime should be expected for non-cloud-native workloads that cannot be migrated away from the availability zone undergoing upgrade.

       3. If cloud utilization is very high and spare capacity is below 20%, upgrade risks will need to be carefully evaluated with the customer, potentially causing delays or preventing the project from being undertaken.

       4. For applications deployed directly from public cloud marketplaces, Managed Services will perform upgrades in pre-defined standing maintenance windows. These upgrades will be announced with reasonable notice, and Customer may opt to skip to the next standing maintenance window if required.

       5. Customer may pin its project to a specific version by asking Managed Services to disable the upgrades. Subsequent requests for upgrades will be evaluated.

       6. Managed Services will provide planned upgrades and maintenance Monday to Friday during Canonical working days. Standing maintenance periods may be pre-appointed following mutual agreements with Customer.

       7. Customer may skip upgrades up to three times, after which automated upgrades will be disabled.

   11. Managed Applications. Canonical will manage applications from its [managed applications portfolio](https://ubuntu.com/managed/apps). Canonical will expose only API and other user-level interfaces of the applications

3. No other operations will be provided by Managed Services unless contractually agreed between Canonical and Customer prior to the Environment’s deployment. The Managed Service does not provide:

   1. For managed Infrastructure:

      1. Managing, monitoring, backup or recovery of the operating system, customer generated data and any applications running within virtual machine instances or Container Instances

      2. Support for the ability to run virtual machine instances using images other than those provided by Canonical

   2. For self-deployed applications on public clouds, Canonical will not provide Managed Services for external or third-party components integrated within the Canonical-operated Environment.

   3. Evaluation and resolution of any incompatibility or malfunction of external components caused by updates to the [Environment](#def-environment) remains the responsibility of the Customer.

   4. Alternative scheduling of updates or upgrades

   5. Unsupported versions of Ubuntu, OpenStack, Kubernetes, or applications

   6. Adherence to the Customer’s Change Management requirements/regulations without a DSE

   7. Integration with Customer’s ticketing system without a TAM

4. Service conclusion. At the end of the service term, the Managed Service will initiate an operational transfer. Operational transfer includes:

   1. Hand over of all credentials of the hosts, management software, Landscape and Applications to the customer. The continued operation of Landscape is subject to purchase and agreement of appropriate licence terms

   2. Coordination of any applicable training (if purchased)

   3. For self-deployed applications, Managed Services will transfer the access to the environment’s resources exclusively to Customer. This cannot be undone, and future deployments will use the most current component version which may cause incompatibilities with decommissioned [Environments](#def-environment).

5. Customer dependencies. Managed Services requires:

   1. Credentials to the Infrastructure being used for the Applications in the case in which such infrastructure is not managed by Canonical (i.e. Managed OpenStack)
   2. Continuous VPN access for Canonical support personnel to the [Environment](#def-environment)

   3. For self-deployed Environments, continuous access to the Environment’s resources

   4. Utilisation parameters per [Node](#def-node) to be kept below the maximum specified in the design document provided by Canonical when the [Environment](#def-environment) is delivered to the customer

   5. The facility where the [Environment](#def-environment) is hosted to comply with the minimum required measures to function, including but not limited to, connectivity, sufficient power supply, sufficient cooling system, and physical access control to the [Environment](#def-environment)

   6. The entire [Environment](#def-environment) to be covered by Managed Services

6. <a id="def-minimum-size-requirement"></a>Minimum size requirement. Managed Services can only be provided for [Environments](#def-environment) with:

   1. At least 12 deployed nodes for any eligible OpenStack release

      2. At least 9 deployed nodes for any other compatible product

      3. For [Environments](#def-environment) deployed directly from public cloud marketplaces, there is no minimum size requirement.

7. Uptime service level

   1. The Managed Service includes the following uptime service levels:

      |            | DATA PLANE FOR CUSTOMER WORKLOADS THAT ARE DISTRIBUTED ACROSS TWO REGIONS | DATA PLANE FOR CUSTOMER WORKLOADS THAT ARE IN A SINGLE REGION | CONTROL PLANE (OPENSTACK/KUBERNETES API, WEB UI AND CLI) |
      | :--------- | ------------------------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------- |
      | **Uptime** | 99.9%                                                                     | 99.5%                                                         | 99%                                                      |

   2. Data plane includes:

      1. Virtualisation (for workloads that are architected to not depend on a single compute [node](#def-node))

      2. Storage (block & object)

      3. Network for instances

   3. Downtime must be directly attributable to Canonical in order for it to count against the service level and is measured across a 12-month period. Planned maintenance windows and any requests by the customer are not taken into account when calculating uptime. Planned maintenance is carried out as required by Canonical, Monday to Friday during Canonical working days

<!-- section: firefighting-support -->

### 22. Firefighting Support

1. Firefighting Support is an add-on to Ubuntu Pro + [Infra Support](#def-infra-support) (24/7) or Ubuntu Pro + Support (24/7). When added, Canonical will support the [Environment](#def-environment) as described below, with all instances in an environment covered at the same support level. All supported products must be within their [Ubuntu Pro lifecycle](https://ubuntu.com/about/release-cycle).

2. Environments benefiting from Firefighting Support can be deployed on-premises, in the public cloud, or on a combination of the two. To be eligible for Firefighting Support, the Environment must be deployed (manually or automatically) or validated by Canonical.

3. The Firefighting Support Service is (a) a time-bound planned coverage for activities affecting the Supported Products and (b) an incident bridge support service for unplanned Severity 1 incidents. The service is available remotely during the Firefighting Support subscription term.

4. Reactive scope:

   1. Reactive response is available 24/7. For unplanned Severity 1 incidents, Canonical will join a video session within one hour of Severity 1 activation.
   2. Firefighting Support response can only support one issue at a time, per customer per environment. For other issues, 24/7 support SLAs will apply for an unlimited number of cases.
   3. Issues that in Canonical’s opinion, are caused by Customer negligence, external non-Canonical components or non-validated environments, or any cause outside the mentioned scope of this schedule will not be supported or resolved by Canonical.
   4. Firefighting Support will assist with reactive restoration for the first occurrence of any customer-caused issue. For recurring issues 24/7 support will be offered instead.
   5. Canonical will provide support via video call either until the earlier of: (i) the core functionalities being restored, (ii) until the issue is downgraded to Severity 2, or (iii) 4h video call.
   6. Severity 1 issues that downgrade to Severity 2 due to partial restoration or any other cause or where the 4h video call window has lapsed will continue to be addressed asynchronously, based on the 24/7 support services SLAs.
   7. Issue severity is reported by the Customer, based on an initial agreement with Canonical. Canonical will verify, confirm, or re-establish the severity of every case before providing support.

5. Planned coverage scope:

   1. 5 hours per calendar quarter of proactive services for every 10 nodes covered – capped at 30 hours per quarter – are included and may be used for discovery sessions, readiness assessment, risk review, capacity planning, runbook validation, rehearsal support, scheduled standby during agreed coverage windows, and post-coverage review.
   2. For planned coverage, Canonical will provide the pre-agreed preparation services and reserve the applicable coverage time window.
   3. During the Firefighting Support subscription term, unused proactive hours may roll over for one subsequent calendar quarter only, after which they expire.
   4. Additional proactive hours or additional planned activities beyond the included allocation may be purchased under a separate Ops Consultancy or successor services package at Canonical’s then-current rates.
   5. Planned coverage:
      1. For each planned activity, Canonical will reserve expert coverage during the agreed coverage window, if booked at least two weeks in advance.
      2. Before the activity window, Canonical may review the Customer’s implementation plan, assess known risks, validate the runbook, and support agreed readiness activities.
      3. During the activity window, Canonical will remain available for live troubleshooting and escalation support related to the Supported Products.
   6. At the Customer’s request and subject to available included hours, Canonical may join a post-activity review, including lessons learned and stabilisation recommendations.

6. Firefighting Support excludes: (a) ongoing proactive account management, service reviews, or embedded advisory services typically associated with technical account management or designated support engineering services; (b) general IT staff augmentation, software development work, or project delivery work; (c) live support for non-Severity 1 incidents outside the standard support services; (d) 24/7 standby outside agreed planned coverage; or (e) coverage beyond the included proactive hours allocation, unless separately purchased.

<!-- section: ops-consultancy -->

### 23. OpsConsultancy

1. OpsConsultancy is an add-on to Managed Services or Firefighting Support offering. When added, Canonical will provide consultancy hours, from remote, for the topics described below.

2. Architectural changes

   1. Planning or executing changes in network topology

   2. Planning or executing changes to disk layouts

   3. Integrate/Install new applications/agents/software after deployment

   4. Enabling HW offloading or CPU pinning adjustments after deployment

   5. Implement new data replication scenarios after deployment

   6. Addition of any non-standard packages or applications

   7. Migration of the Cloud to alternative Data Centers

   8. Creation of custom dashboards

   9. Permission adjustments (policy changes)

   10. Security Audits other than CVE and CIS scan reports

   11. User permissions changes

   12. Training on Canonical products

   13. Support for custom OpenStack roles

       1. Creation and revocation

       2. Custom permission and authorization

3. Customer-specific training

   1. Training/coaching on Canonical products

   2. Customer’s specific organizational training

   3. Customer’s specific security training

4. Only for Firefighting Support customers (all the above plus)

   1. Operational tasks included in the Managed service

   2. Planning or executing of cloud upgrades/reboots/package or charms refresh

<!-- section: professional-support-services -->

### 24. Professional Support Services

1. The Technical Account Manager service (TAM) is an add-on service offering to enhance support where the TAM acts as a strategic coordinator and trusted advisor

   1. Under these services offerings, Canonical will provide a TAM, who will perform the following services:

      1. Act as the primary point of contact for all support requests originating from the customer department for which the TAM is responsible

      2. Coordinate support requests

      3. Provide best-practice advice on platform and configurations covered by the applicable Ubuntu Pro services

      4. Participate in regularly scheduled review calls addressing the customer's operational issues

      5. Organise multi-vendor issue coordination where applicable. When the root cause is identified, the TAM will work with the vendor for that sub-system, working to resolve the case through their normal support process

      6. Manage support escalations and prioritisation in accordance with Canonical's standard support response definitions and customer needs, including internal coordination with product engineering teams to convey customer feedback and feature requests

      7. Attend applicable Canonical internal training and development activities (in-person and remote) to maintain technical breadth and customer-facing effectiveness

   2. The TAM is available to respond to support cases during the TAM’s working hours. Outside of [Business Hours](#def-business-hours), support will be provided per the Ubuntu Pro Support Process

   3. If a TAM is on leave for longer than five consecutive days, Canonical will assign a temporary backup TAM to cover the leave period. Canonical will coordinate with the customer with respect to foreseeable TAM leave

   4. Canonical will hold a quarterly service review meeting with the customer to assess service performance and determine areas of improvement and to review ongoing risks, priorities, and support trends, aligned with Canonical’s latest roadmaps and informed by upcoming product changes

   5. The TAM will visit the customer’s site annually for on-site technical review

2. Dedicated Support Engineer (DSE) is an add-on service to enhance support, providing a technical specialist for deeper hands-on engagement

   1. Canonical will provide a DSE, who will perform the following services during local [Business Hours](#def-business-hours) during the term of service:

      1. Deliver direct technical support within the customer’s operational context. If required, the DSE may track tasks in the customer’s ticketing system

      2. Understand the products utilised in the customer’s [Environment](#def-environment) that need to be integrated with Canonical’s offerings and assist with those products, to the extent reasonable based on the DSE’s expertise, to ensure the successful usage of offerings from Canonical, working closely with customer engineers on configuration, troubleshooting, and remediation

      3. Provide best-practice advice on platforms and configurations covered by the applicable Ubuntu Pro services, including direct problem-solving and guidance during active incidents

      4. Provide guidance and review plans ahead of significant events in Customer’s platforms, whether driven by changes to the Environment or periods of peak activity

      5. Act as the primary point of contact for all support requests originating from the customer department for which the DSE is responsible, with a focus on day-to-day technical handling and follow-through
      6. Manage support escalations and prioritisation in accordance with Canonical's standard support response definitions and customer needs, including internal coordination with product engineering teams to convey customer feedback and feature requests

      7. Participate in regular review calls addressing the customer's operational issues

      8. Organise multi-vendor issue coordination where applicable. When the root cause is identified, the DSE will work with the vendor for that sub-system, working to resolve the case through their normal support process

      9. Attend applicable Canonical internal training and development activities to maintain depth in the customer’s stack and related technologies

   2. Canonical will hold a quarterly service review meeting with the customer to assess service performance and determine areas of improvement and confirm priorities for the next period of work, aligned with Canonical’s latest roadmaps and informed by upcoming product changes

   3. The DSE is available to respond to support cases during the DSE’s working hours. Outside of [Business Hours](#def-business-hours), support will be provided per the Support Services Process

   4. If a DSE is on leave for longer than five consecutive business days, Canonical will assign a temporary backup DSE to cover the leave period. Canonical will coordinate with the customer with respect to foreseeable DSE leave

   5. The DSE will visit the customer’s site annually for on-site technical review

<!-- section: embedded-services -->

### 25. Embedded Services

1. With Embedded Services you will receive the engineering support and access to Expanded Security Maintenance. Canonical will provide such technical support to unmodified Ubuntu LTS release images when installed using official sources and within its [product life cycle](https://www.ubuntu.com/about/release-cycle).

2. Scope

   1. The scope of the service is limited to the appropriate level as listed above.

3. Engineering Support-only, processes:

   1. You are responsible for resolving all end user issues. Canonical will not be supporting end-users directly. You should utilise the Knowledge Base, Launchpad, and other resources in addition to your own resolution systems to find workarounds or resolutions for any issue prior to opening a support case with Canonical

   2. You will search Launchpad, to ensure that the issue is not already known and being resolved and, if it is, provide suspected bug number to Canonical support as reference. Canonical reserves the right to redirect low-level and untriaged issues to you

   3. You are responsible for specifying how an issue arises and in what sub-system it is taking place. You must provide a repeatable test case that Canonical can recreate on the hardware systems to which Canonical has access

   4. You will work with Canonical to provide any debugging or further testing required. You will provide any technical information as requested to resolve the problem. Failure to provide required information or assistance in gathering such information may result in closure of the case. When the final solution has been provided by Canonical, you are responsible for verifying that it solves the issue

<!-- section: definitions -->

## Definitions

**Applications:** Applications supported or managed by Canonical ([Managed Applications as described in the Add-ons section, under Managed Services, and at https://ubuntu.com/managed](https://ubuntu.com/managed))

**Break-fix Support:** request assistance in the event of an incident and answer questions about Supported Packages and products.

**Bug-fix Support**: support for reported software bugs in Supported Packages only. This does not include [troubleshooting](#def-troubleshooting) of issues to determine if a bug is present

**Business Hours:** 08:00 - 17:00 Monday - Friday local to the customer’s headquarters unless another location is agreed. All times exclude public holidays at the customer’s location.

**Ceph Cluster**: a single Ceph installation in a single physical data center and specified by a unique identifier

**Certified Hardware:** any Ubuntu-certified hardware identified at [https://ubuntu.com/certified](https://ubuntu.com/certified) running a Canonical-provided Ubuntu image certified for that hardware.

**Charm:** a set of scripts compatible with Juju application modelling for the purpose of deploying and configuring relationships between software packages

**Charmed Kubernetes:** Kubernetes deployed using Juju and the official Canonical-Kubernetes bundle on bare metal, Ubuntu Guests, or virtual machines

**Covered Architectures:**

| architecture/ release | 14.04 LTS | 16.04 LTS | 18.04 LTS | 20.04 LTS and newer |
| :-------------------- | --------- | --------- | --------- | ------------------- |
| x86                   | Yes       | Yes       | Yes       | Yes                 |
| arm64                 | No        | No        | Yes       | Yes                 |
| s390x                 | No        | No        | Yes       | Yes                 |
| power                 | No        | No        | Yes       | Yes                 |
| risc-v                | No        | No        | No        | Yes                 |

**CVEs (High and Critical):** High and Critical Common Vulnerabilities and Exposures as assessed by the Ubuntu Security Team. More details can be found at [https://ubuntu.com/security/cves](https://ubuntu.com/security/cves)

**Desktop use case:** unlike Ubuntu machines operated in the datacenter or public clouds, desktop use cases require a human interacting through a display and input devices – such as a keyboard, mouse, trackpad, or assistive technology – to run multiple general-purpose applications in a typical workplace environment. Desktop use cases may also involve developer tools such as MicroK8s and Multipass

**Device use case:** unlike desktop use cases, device use cases involve hardware with specialized, application-specific purposes that may support multiple users or operate unattended, running a limited set of applications for dedicated functions. May or may not include a monitor. Examples: Gateways, Industrial PCs, Robots, Kiosks, Point of Sale devices, Medical devices.

**Enabled kernel**: Kernel version provided as part of Canonical Enablement service, unmodified and [supported](https://ubuntu.com/about/release-cycle)

**Environment**: all machines (or devices) in a private cloud, cluster, fleet, or similar grouping of instances

**End of Life:** a date on which an Ubuntu LTS reaches [end of Legacy coverage](https://ubuntu.com/about/release-cycle) or [end of Expanded Security Maintenance](https://ubuntu.com/about/release-cycle) if the Legacy add-on is not available

**End of Standard Support:** a date (5 years after the [Release Date](#def-release-date)) on which free standard security maintenance service for the [Ubuntu Main](#def-ubuntu-main) repository of an Ubuntu LTS expires

**Expanded Security Maintenance (ESM):** an additional scope of security patching service delivered by the Ubuntu Security Team as found at [https://ubuntu.com/security/esm](https://ubuntu.com/security/esm). It covers fixes to [High and Critical CVE](#def-cves-high-and-critical) for 10 years and could be offered for [Ubuntu Main](#def-ubuntu-main) repository, or both [Ubuntu Main](#def-ubuntu-main) and [Universe](#def-ubuntu-universe) repositories, depending on the Ubuntu Pro subscription (infra-only, Apps-only, or the full Ubuntu Pro)

**Infra support:** support for the base Ubuntu OS image and a set of open source infrastructure components, such as MAAS, Ceph storage and OpenStack. It also covers Kubernetes, MicroCloud and LXD

**Knowledge Base**: the knowledge base is a database of articles for Customer technical operators

**Kubernetes**: the container orchestration software known as “Kubernetes” as distributed by Canonical

**Node**: a physical node or virtual machine provided to Canonical (or paid for) by the Customer for the purposes of running the environment. Any further machines (whether virtual (VM) or container) created on top of a Node are not themselves considered to be nodes

**OpenStack:** the cloud computing software known as “OpenStack” as distributed by Canonical with Ubuntu

**Release date:** the general availability release date of an Ubuntu version as found at [https://ubuntu.com/about/release-cycle](https://ubuntu.com/about/release-cycle)

**Troubleshooting**: the process of identifying, diagnosing, and resolving problems or issues that arise when using a software application or infrastructure, in order to ensure its proper functionality

**Ubuntu Archive**: official online repositories that store software packages and updates for the Ubuntu operating system

**Ubuntu Core:** Ubuntu Core is a version of the Ubuntu operating system designed and engineered for IoT and embedded systems.

**Ubuntu Guest**: a virtual machine instance or Container Instance of Ubuntu

**Ubuntu Main:** the deb package repository of an Ubuntu identified by Canonical as Ubuntu Main

**Ubuntu Universe:** the deb package repository of an Ubuntu identified by Canonical as Ubuntu Universe

**Valid Customisations:** configurations made through Horizon or the OpenStack API of the OpenStack Packages. For the avoidance of doubt, valid customisations do not include architectural changes that are not expressly executed or authorised by Canonical. Configuration options set during a Private Cloud Build should be considered critical to the health of the Cloud. Any changes to these may render the cloud unsupported. Requests for changes should be validated by Canonical to ensure continued support
