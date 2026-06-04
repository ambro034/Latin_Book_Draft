---
layout: home
title: BeOps - Best Practices for DevOps and SRE
permalink: /
---

Welcome to BeOps, your comprehensive resource for DevOps best practices, Kubernetes deep dives, Site Reliability Engineering (SRE) principles, and applied AI for operations.

## 📝 All posts

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) <span class="post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
{% endfor %}

## 🔗 Quick Links

- [About]({{ '/pages/about/' | relative_url }}): learn more about BeOps
- [Contact]({{ '/pages/contact/' | relative_url }}): get in touch
- [RSS Feed]({{ '/feed.xml' | relative_url }}): subscribe to updates
