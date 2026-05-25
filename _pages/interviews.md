---
title: Interviews
layout: home
permalink: /interviews/
is_category: true
description: Conversations with engineers and architects working at the frontier.
---

# Interviews

Long-form conversations with practitioners building real AI, platform, and reliability systems. Identifying details are removed unless the interviewee opts in.

{% assign category_posts = site.categories.interviews | default: site.posts | where: "category", "interviews" %}
{% if category_posts.size == 0 %}
_No interviews published yet — check back soon._
{% else %}
{% for post in category_posts %}
- **[{{ post.title }}]({{ post.url | relative_url }})** — {{ post.date | date: "%B %d, %Y" }}
{% endfor %}
{% endif %}

[← Back to home]({{ '/' | relative_url }})
