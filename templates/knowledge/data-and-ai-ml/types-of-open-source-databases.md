---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Data and AI/ML"
  publish_date: 2026-09-16
  tag: "Databases"
  title: "What are the different types of open source databases?"
  breadcrumb: "Types of open source databases"
  description: "Explore the main open source database categories, their core features, and how to successfully manage them at scale."
  hero_title: "What are the different types of open source databases?"
  cta:
    description: "Build your data stack with Canonical’s open source solutions."
    buttons:
      - text: "Explore data solutions"
        url: "https://canonical.com/data"
        type: "button"
        variant: "positive"
      - text: "Get in touch"
        url: "https://canonical.com/data#get-in-touch"
        type: "button"
  blog:
    title: "Latest from our blog"
    id: 1234
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-table.jinja" import table_kh %}

Open source databases – or database management systems (DBMS) – now power [over 95% of enterprise IT](https://www.openlogic.com/blog/top-open-source-databases). In this article, we explore open source database categories, their core features, and how to successfully manage them at scale.

## Why SQL vs NoSQL is outdated

Historically, database management systems were divided into two broad categories:

{{ text_list_kh(
  items=[
    "<strong>SQL/Relational DBMS</strong> are primarily optimized for managing data structured around tables, rows, and columns. They rely on the structured query language (SQL) as the standard interface for data management.",
    "<strong>NoSQL/Non-relational DBMS</strong> are optimized for managing unstructured data, such as binary large objects (BLOBs), or semi-structured data, like JSON. They utilize alternative querying methods, either bypassing SQL entirely or using it only as a secondary interface."
]) }}

However, this strict classification is becoming obsolete. Today, major SQL engines like PostgreSQL and MySQL offer robust, built-in JSON support. In fact, they have handled BLOBs since long before NoSQL became mainstream in the enterprise. Similarly, several NoSQL databases now support SQL or a variant of it, such as CQL for [Cassandra](https://canonical.com/data/cassandra) or the SQL plugin for [OpenSearch](https://canonical.com/data/opensearch). With the lines blurred, we can turn to more useful methods of categorization.

## Open source database categories

Instead of classifying open source databases according to the interfaces or paradigms that they support, it’s far more pertinent to categorize them based on the use cases that they are optimized for:

### Transactional and operational

Databases designed for transactional and operational use cases are relational database management systems (RDBMS) such as [PostgreSQL](https://canonical.com/data/postgresql) or [MySQL](https://canonical.com/data/mysql) that prioritize reliability, strict schemas, and predictable concurrency behaviors over extreme speed. These systems guarantee that complex, multi-step operations (like financial transactions or inventory updates) either complete perfectly or fail cleanly without leaving broken data behind. They are the best candidates to power e-commerce checkouts, banking ledgers, user account management, and ERP systems.

### Analytical and data warehousing

Analytical and data warehousing systems are engineered to answer complex questions. Rather than updating single records, they are optimized to scan billions of rows to generate aggregations, averages, and trends. Historically, this type of workload was powered by row-oriented databases using dimensional modeling and Bitmap Indexes to rapidly intersect data. Modern native data warehouses have shifted to columnar storage (rather than rows) to achieve this massive read-speed. PostgreSQL, when used with columnar extensions such as timescale or pg_lake, can provide this capability. Spark is another analytical engine optimized to run massive parallel analytical jobs over disaggregated storage.

### Flexible content management

Flexible content management requires document-oriented NoSQL databases, such as MongoDB, which are optimized for fast-evolving data. They delay schema handling to reading operations (schema-on-read) rather than writing operations (schema-on-write). They also prioritize availability over consistency in distributed deployments. These trade-offs make them ideal for rapid development iterations and powering dynamic content like digital catalogs or CMS backends.

### Search and observability

For search and observability, solutions such as OpenSearch are optimized for ingesting massive streams of data while indexing them to perform advanced fuzzy search queries (using Lucene indexes) and relevance scoring (using vector indexes). These capabilities are essential to find partial matches, typos, or security anomalies across billions of records. Hence, these solutions are often the backbone of modern observability platforms, log analytics, and enterprise search.

### Speed and caching layer

In-memory data stores, like [Valkey](https://canonical.com/data/valkey), are designed to deliver sub-millisecond latency. By keeping data in RAM, they provide blazing-fast read and write operations. They are often used to manage web sessions, power real-time leaderboards, and to accelerate key-based lookups when deployed as a caching layer in front of persistent databases.

### Configuration and consensus

Distributed systems require a reliable way to manage state and store cluster configurations. Consensus-driven, distributed key-value stores such as Apache ZooKeeper or [etcd](https://canonical.com/data/etcd) are built specifically for these distributed coordination use cases. Rather than storing application data, they often act as the highly available “source of truth” to implement service discovery, distributed locking, and cluster state management.

[Learn how to pick the right database in our guide: How to choose a database management system ›](https://ubuntu.com/engage/choose-a-database)

## Feature breakdown of open source databases

{{ table_kh(
  label="Open source database features comparison",
  headers=["Features", "MySQL", "PostgreSQL", "MongoDB", "Valkey", "OpenSearch", "Apache Cassandra", "etcd"],
  rows=[
    ["Primary data paradigm", "Relational", "Relational", "Document", "Key/Value", "Text Search", "Wide-column", "Key/Value"],
    ["Typical observed response times in milliseconds", "1-100", "1-100", "1-100", "0.1-10", "10-1000", "1-100", "1-100"],
    ["Typical observed sizes of a single cluster deployment", "1-10 TBs", "1-100 TBs", "1-100 TBs", "Available memory", "1-100 TBs", "1-100 TBs", "2-8 GB"],
    ["DBMS managed sharding", "With extension", "With extension", "Built-in", "Built-in", "Built-in", "Built-in", ""]
  ],
  note="Only the distributions supported by Canonical are considered in the table above."
) }}

### Supported data types

{{ table_kh(
  label="Supported data types by open source database",
  headers=["Data types", "MySQL", "PostgreSQL", "MongoDB", "Valkey", "OpenSearch", "Apache Cassandra", "etcd"],
  rows=[
    ["Tabular", "Yes", "Yes", "", "", "", "Yes", ""],
    ["JSON", "Yes", "Yes", "Yes", "With extension", "Yes", "Yes", ""],
    ["XML", "Yes", "Yes", "", "", "", "", ""],
    ["Binary", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"],
    ["Generic Text", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"],
    ["Natural Language Text", "Yes", "Yes", "Yes", "With extension", "Yes", "With extension", ""],
    ["Time Series", "", "With extension", "Yes", "With extension", "Yes", "Yes", ""],
    ["Geospatial data", "Yes", "With extension", "Yes", "Yes", "Yes", "", ""],
    ["Graph data", "", "With extension", "", "", "", "", ""],
    ["Vector data", "Yes", "With extension", "", "With extension", "Yes", "Yes", ""]
  ],
  note="Only the distributions supported by Canonical are considered in the table above."
) }}

## What are the challenges with open source databases?

### Security maintenance

Using open source databases significantly increases the complexity of managing the [software supply chain](https://canonical.com/knowledge/security-and-compliance/what-is-software-supply-chain-security). This is because open source database stacks rely on a deep tree of community-maintained packages, extensions, and transitive dependencies, meaning that they are inherently exposed to modern supply chain risks. These risks range from accidental zero-day vulnerabilities to sophisticated repository-hijacking, and malicious code injection. Without a trusted provider delivering automated, certified updates, organizations must dedicate significant internal resources to security maintenance. This involves continuously auditing the database environment, tracking vulnerabilities, and swiftly backporting security patches.

### Solution integration

Databases do not operate in isolation. To run a database successfully, you not only need to worry about the database engine itself, you also need to integrate it with a variety of tools and extensions for monitoring, alerting, high availability, and backup. With a closed source database, the engine ships with these integrated tools, and they are all supported and maintained by the vendor. But with an open source solution, organizations need to select, test, and maintain the integrations themselves – which requires time and expertise.

### Fragmented support

Investigating a production issue often requires diving through multiple stack layers, from the storage and OS kernel right up to the database instance itself. Relying on different vendors for each layer frequently leads to finger-pointing, SLA-breaching resolution times, and frustrated customers. Organizations can mitigate this challenge by choosing a single provider that can deliver enterprise support for the entire open source stack – ensuring that if a database cluster fails, there is a single support stream.

## Which databases does Canonical support?

Canonical delivers long term security maintenance, lifecycle management, and enterprise support for a broad portfolio of the most popular open source databases. These solutions and services solve the challenges traditionally associated with using open source databases, with Canonical acting as the single point of support, avoiding fragmentation and enabling organizations to enjoy all the advantages of open source innovation with the reliability of SLA-backed support.

Canonical’s data solutions portfolio includes:

{{ text_list_kh(
  items=[
    "<a href='https://canonical.com/data/postgresql'>PostgreSQL</a>",
    "<a href='https://canonical.com/data/mysql'>MySQL</a>",
    "<a href='https://canonical.com/data/mongodb'>MongoDB</a>",
    "<a href='https://canonical.com/data/valkey'>Valkey</a>",
    "<a href='https://canonical.com/data/opensearch'>OpenSearch</a>",
    "<a href='https://canonical.com/data/etcd'>etcd</a>",
    "<a href='https://canonical.com/data/cassandra'>Apache Cassandra</a>"
]) }}

Canonical provides each of these databases in various packaging formats for seamless integration with users' existing stacks. All of the databases are available as Ubuntu-based, OCI-compliant container images. Where applicable, they are also available as snaps and deb packages. Canonical's software operators, known as charms, enable automated deployment, integration, and lifecycle management of databases on any infrastructure.

[Explore Canonical’s full data solutions portfolio ›](https://canonical.com/data)

## Canonical’s database services

Beyond support for the software solutions themselves, Canonical provides a comprehensive suite of enterprise-grade services across the data stack, delivered with predictable, per-node pricing.

### Security maintenance

With [Ubuntu Pro](https://ubuntu.com/pro), users get up to 15 years of security maintenance for their entire open source stack, including databases. Organizations benefit from rapid remediation of vulnerabilities for maintained packages, and can take advantage of tools for auditing, patching automation, and management to maximize database uptime. Canonical can also maintain custom database dependencies and versions not covered by Ubuntu Pro through the Container Build Service.

### Support

Canonical’s experts provide [direct support](https://ubuntu.com/support) to keep database deployments running smoothly. Phone and ticket support offers SLA-backed response times to seamlessly resolve incidents. With Firefighting support, Canonical engineers are on call to rapidly address critical issues. Alternatively, organizations can opt for a 24/7 fully managed service, letting Canonical handle end-to-end management and monitoring of the data stack.

### Consulting and training

Consulting and training services enable organizations to tackle complex technical challenges. Canonical delivers instructor-led [courses](https://ubuntu.com/training), hands-on labs, and official [certification exams](https://canonical.com/academy) to empower database teams. Deployment services help organizations design and implement a tailored, production-grade database stack. And on-demand consulting with expert database engineers is available to address specific needs.

[Learn more about Canonical's database services ›](https://canonical.com/data/services)
