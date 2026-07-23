# Akuiro (周朕葵) · Personal Homepage

个人主页 + 轻量笔记系统,部署在 GitHub Pages。

🔗 在线地址:<https://APhysickui.github.io/>

这是一个纯静态站点:首页是个人简介(教育、科研、项目、荣誉),外加一个
**Markdown 笔记系统**——把 `.md` 文件丢进 `notes/`,运行一个脚本就能生成
带数学公式、表格渲染的独立文章页,并自动更新首页的 Notes 列表。

---

## 致谢 / 源码来源

首页布局与 `stylesheet.css` 改编自 **Jon Barron** 的学术主页模板:
<https://jonbarron.info/>(原始 README 见 Git 历史)。原模板以简洁的
表格布局著称,本项目在其基础上做了中文化、响应式图片、以及笔记系统的扩展。

## 功能特性

- **双语版式**:各板块标题为「英文 + 中文小标签」(如 `Research 科研经历`)。
- **响应式图片**:头像和项目图不写死尺寸,靠 CSS `aspect-ratio` + `object-fit:cover`
  自动裁剪——头像自动裁成圆形,项目图自动裁成 3:2。**换图直接替换文件即可,无需手动裁剪。**
- **移动端适配**:窄屏下头像、项目图、文字自动堆叠为单列(见 `stylesheet.css` 的
  `@media (max-width: 600px)`)。
- **Markdown 笔记系统**(`build_notes.py`):
  - LaTeX 数学公式(行内 `$...$`、行间 `$$...$$`、`\begin{}` 环境),用 MathJax 渲染。
  - Markdown 表格、代码块、引用、有序/无序列表、分隔线。
  - 支持**中文文件名**,链接自动 URL 编码。
  - 首页 Notes 列表自动生成:自动提取正文摘要、按日期排序(新的在前)。
  - 零第三方依赖,仅用 Python 标准库。

## 目录结构

```
.
├── index.html          # 首页(手写;Notes 列表由脚本自动注入)
├── stylesheet.css      # 全站样式(改编自 Jon Barron 模板 + 笔记样式)
├── build_notes.py      # 笔记构建脚本:Markdown → HTML
├── notes/              # 笔记目录
│   ├── *.md            #   ← 你写的 Markdown 源文件
│   └── *.html          #   ← 脚本自动生成,请勿手动编辑
├── images/             # 头像、项目图、favicon
├── data/               # CV(PDF / TeX 源)
├── .nojekyll           # 关闭 GitHub Pages 的 Jekyll 处理(纯静态站必需)
└── .gitignore
```

## 如何添加一篇笔记

1. 在 `notes/` 里新建一个 `.md` 文件(文件名可用中文,会成为默认标题)。
2. 运行:
   ```bash
   python3 build_notes.py
   ```
3. 检查生成结果,然后 `git add / commit / push`。

脚本会为每个 `.md` 生成同名 `.html` 页面,并重新生成首页 `index.html` 中
`<!-- NOTES:START -->` 与 `<!-- NOTES:END -->` 之间的列表。**除了写 Markdown,
其余全自动。**

### 可选:自定义标题 / 日期 / 摘要

在 `.md` 文件顶部加一段 front matter(可选,不写则用文件名作标题、文件修改日期作日期、
正文首句作摘要):

```markdown
---
title: 自定义标题
date: 2026-07-20
summary: 一句话简介,显示在首页列表里
---

正文从这里开始……
```

## 本地预览

在仓库根目录起一个本地服务器预览(推荐,路径和跳转都与线上一致):

```bash
python3 -m http.server 8000
# 然后浏览器打开 http://localhost:8000/
```

不建议直接双击打开 `.html`:`file://` 协议下样式表的相对路径可能加载失败。
另外 MathJax 通过 CDN 加载,预览公式时需联网。

## 部署(GitHub Pages）

本仓库名为 `APhysickui.github.io`,属于 GitHub Pages 用户站点:推送到 `main`
分支后,GitHub 会自动把根目录发布到 <https://APhysickui.github.io/>。

部署前请确保已在本地跑过 `python3 build_notes.py`,把最新的 `notes/*.html`
和更新后的 `index.html` 一起提交(生成的 HTML 需要纳入版本控制,GitHub Pages
不会替你构建)。

## 支持的 Markdown 语法一览

| 语法 | 支持 |
| --- | --- |
| 标题 `#`–`######` | ✅ |
| **粗体** / *斜体* / `行内代码` | ✅ |
| 围栏代码块 ```` ``` ```` | ✅ |
| 有序 / 无序列表 | ✅ |
| 表格 | ✅ |
| 引用 `>` | ✅ |
| 分隔线 `---` | ✅ |
| 链接 `[文字](url)` | ✅ |
| LaTeX 公式 `$...$` / `$$...$$` | ✅(MathJax) |
| 图片 `![]()` / 嵌套列表 | ⚠️ 暂未支持 |

## 许可

首页模板版权归原作者 Jon Barron;个人内容(简介、笔记、CV 等)版权归周朕葵所有。

