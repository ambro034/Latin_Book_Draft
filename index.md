---
layout: home
title: BeOps - Best Practices for DevOps and SRE
permalink: /
---

# BeOps - Best Practices for DevOps and SRE

Welcome to BeOps, your comprehensive resource for DevOps best practices, Kubernetes deep dives, and Site Reliability Engineering (SRE) principles.

## 🚀 Latest Posts

{% for post in site.posts limit:5 %}
### [{{ post.title }}]({{ post.url | relative_url }})
**{{ post.date | date: "%B %d, %Y" }}** - {{ post.category | capitalize }}

{{ post.excerpt | strip_html | truncatewords: 30 }}

{% endfor %}

## 📚 Categories

- **[DevOps]({{ '/devops/' | relative_url }})** - Best practices and methodologies
- **[Kubernetes]({{ '/k8s/' | relative_url }})** - Container orchestration and management
- **[SRE]({{ '/sre/' | relative_url }})** - Site Reliability Engineering principles
- **[AI]({{ '/ai/' | relative_url }})** - AI engineering and operations

## 🔗 Quick Links

- [About]({{ '/pages/about/' | relative_url }}) - Learn more about BeOps
- [Contact]({{ '/pages/contact/' | relative_url }}) - Get in touch
- [RSS Feed]({{ '/feed.xml' | relative_url }}) - Subscribe to updates
