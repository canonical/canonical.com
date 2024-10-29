# ![Canonical](https://assets.ubuntu.com/v1/9ce5bce5-canonical-logo3.png?h=32 "Canonical")&nbsp;[Canonical.com](https://canonical.com)

### **The Next-Gen Codebase for Canonical's Official Website**

[![Build Status](https://circleci.com/gh/canonical-web-and-design/canonical.com.svg?style=shield)](https://circleci.com/gh/canonical-web-and-design/canonical.com)
[![Code Coverage](https://codecov.io/gh/canonical-web-and-design/canonical.com/branch/master/graph/badge.svg)](https://codecov.io/gh/canonical-web-and-design/canonical.com)

Welcome to the repository for Canonical's new **canonical.com** website—built with a focus on performance, scalability, and ease of development.

---

## 🏗️ Architecture Overview

This site is powered by the lightweight, yet robust [Flask](http://flask.pocoo.org/) framework. To leverage features shared across Canonical sites, we integrate the [base-flask-extension](https://github.com/canonical-web-and-design/canonicalwebteam.flask-base) module, making the codebase modular and maintainable.

---

## 🛠️ Development Setup

### Quick Start with `dotrun`

For an easy setup, run the website locally with [`dotrun`](https://github.com/canonical-web-and-design/dotrun/):

```bash
dotrun
```

After running the server, the website will be accessible at <http://localhost:8002>. 

Once you start modifying files, the server will automatically reload, making the changes available for immediate preview.

---

## 🌱 Greenhouse API Integration

To work locally on the **/careers** section, you’ll need to set up an environment variable for the Greenhouse API:

1. Add `HARVEST_API_KEY` to your `.env` file.
2. Retrieve your API key from the [Greenhouse admin panel](https://canonical.greenhouse.io/configure/dev_center/credentials).

With this setup, you’ll have full access to the careers data when developing locally.

---

## 🚀 Deployment

Deployment configurations are ready in the `deploy` folder for efficient production deployment.

---

## 📄 License

- **Content License:** This project’s content is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/).
- **Code License:** The underlying code that formats and displays the content is licensed under [LGPLv3](https://opensource.org/license/lgpl-3-0/), courtesy of [Canonical Ltd](http://www.canonical.com/).

--- 
