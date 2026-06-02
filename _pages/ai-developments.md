---
title: AI Developments
layout: home
permalink: /ai-developments/
is_category: true
description: Things I'm building in applied AI — proxies, inference plumbing, and tools.
---

Things I'm building in applied AI — inference proxies, serving plumbing, and the
small tools that turn "I read about it" into "I shipped it."

{% assign category_posts = site.categories.ai-developments | default: site.posts | where: "category", "ai-developments" %}
{% if category_posts.size == 0 %}
_No posts yet in this category._
{% else %}
{% for post in category_posts %}
- **[{{ post.title }}]({{ post.url | relative_url }})** — {{ post.date | date: "%B %d, %Y" }}
{% endfor %}
{% endif %}

[← Back to home]({{ '/' | relative_url }})
