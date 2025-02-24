---
layout: archive
title: "Notes"
permalink: /Notes/
author_profile: true
---


## 说明

- 我的笔记不止包含书面整理,部分还会有**辅助完成作业/整理复习资料**等能够提高效率,节省重复性工作时间的**Python程序**
- 部分笔记是**收费**的.如果您需要获取这部分笔记,请浏览[此页](https://iculizhi.github.io/Notes/notes).
- 未来的课程我也将延续这一风格,用自然语言处理,处理自然语言组成的课程[手动狗头].
- 这些笔记不会泄露任何**不公开的学习资料,考试往年题**等.
- 也欢迎同学们来我的网站[卖笔记](https://iculizhi.github.io/Notes/notes),已有合作者: [qlc](https://github.com/Achyutace)


{% include base_path %}
## 预告

- 本学期确定新开坑: ych中宏, 数理经济学
- 暂定不开但是我也选: cv导论, 财会, ljl计组(前人之述备矣), 操作系统实验班(我并非sys人)
- 加入相应[学习小组](https://iculizhi.github.io/Blogs/%E5%8E%BB%E4%B8%AD%E5%BF%83%E5%8C%96%E5%AD%A6%E4%B9%A0%E5%B0%8F%E7%BB%84)请戳我

## 专业课

{% assign paths = "概论统计A(现为信概统).md,hjfpython.md,Data-Structure-and-Algorithm-A-of-pku.md,数学分析3.md,信数.md" | split: "," %}

{% for post in site.Notes reversed %}
  {% for path in paths %}
    {% if post.path contains path %}
      {% include archive-single.html %}
      {% break %}
    {% endif %}
  {% endfor %}
{% endfor %}


## 公共课
{% assign paths = "PKU-2024-IBAL-cracked-version.md,金融学概论.md,地震概论.md" | split: "," %}

{% for post in site.Notes reversed %}
  {% for path in paths %}
    {% if post.path contains path %}
      {% include archive-single.html %}
      {% break %}
    {% endif %}
  {% endfor %}
{% endfor %}

## 经双
{% assign paths = "博弈论.md,宏观经济与健康.md" | split: "," %}

{% for post in site.Notes reversed %}
  {% for path in paths %}
    {% if post.path contains path %}
      {% include archive-single.html %}
      {% break %}
    {% endif %}
  {% endfor %}
{% endfor %}

## 其他
{% assign paths = "社会主义学习.md" | split: "," %}

{% for post in site.Notes reversed %}
  {% for path in paths %}
    {% if post.path contains path %}
      {% include archive-single.html %}
      {% break %}
    {% endif %}
  {% endfor %}
{% endfor %}

<script src="https://giscus.app/client.js"
        data-repo="ICUlizhi/ICUlizhi.github.io"
        data-repo-id="R_kgDOKfCXRQ"
        data-category="Announcements"
        data-category-id="DIC_kwDOKfCXRc4CknGa"
        data-mapping="url"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="1"
        data-input-position="top"
        data-theme="light"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>