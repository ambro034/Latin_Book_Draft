---
layout: home
title: BeOps - Best Practices for DevOps and SRE
permalink: /
---

Welcome to BeOps, your comprehensive resource for DevOps best practices, Kubernetes deep dives, Site Reliability Engineering (SRE) principles, and applied AI for operations.

## 📚 Browse by Category

{% for cat in site.data.categories %}
{% assign cat_posts = site.posts | where: "category", cat.slug | sort: "date" | reverse %}
### [{{ cat.title }}]({{ '/' | append: cat.slug | append: '/' | relative_url }})
_{{ cat.description }}_

{% if cat_posts.size == 0 %}
- _No posts yet — check back soon._
{% else %}
{% for post in cat_posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) <span class="post-date">— {{ post.date | date: "%b %-d, %Y" }}</span>
{% endfor %}
{% endif %}

{% endfor %}

## 🔗 Quick Links

- [About]({{ '/pages/about/' | relative_url }}) — Learn more about BeOps
- [Contact]({{ '/pages/contact/' | relative_url }}) — Get in touch
- [RSS Feed]({{ '/feed.xml' | relative_url }}) — Subscribe to updates
