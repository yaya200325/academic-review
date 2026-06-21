# academic-review

[English](README.md)

**academic-review** 是一个面向综述论文写作的 Codex Skill。它把综述写作拆成可检查、可续跑的流水线：文献检索、相关性筛选、摘要级知识抽取、提纲规划、分节综合、正文写作、图表插入、语言润色、参考文献校验，以及最终 Word 文档导出。

## 功能定位

- 从选题到 Word 文档的综述论文写作流程
- 支持中文与英文综述
- 适合本科毕业论文文献综述、课程论文综述、专题综述初稿
- 通过阶段性文件保存中间结果，便于长任务续写
- 要求正文论断可追溯到已收集的论文摘要与元数据
- 先写正文、后统一判断图表位置，减少图表与论证脱节
- 使用内置导出脚本生成格式化 `.docx`

## 工作流

```text
Stage 1   Search                -> output/retrieved_papers.json
Stage 2   Screen                -> output/screened_papers.json
Stage 3   Extract               -> output/knowledge.json
Stage 4   Outline               -> output/outline.json + output/review_lock.md
Stage 5   Synthesize            -> output/synthesis_notes.json
Stage 6   Draft                 -> output/draft_text.md
Stage 7   Diagram/Table         -> output/draft_full.md
Stage 8   Polish                -> output/polished.md + output/polish_audit.md
Stage 8.5 Reference Validation  -> output/reference_validation.md
Stage 9   Export                -> output/full_document.md + output/review.docx
```

第 4 阶段是强制确认点：代理需要先展示提纲，用户确认后才继续正文写作。

## 使用示例

```text
使用 academic-review 帮我写一篇关于“图神经网络在推荐系统中的应用”的中文文献综述。
要求：30 篇参考文献，约 7000 字，本科毕业论文文献综述。
```

## 必要输入

| 参数 | 说明 | 示例 |
| --- | --- | --- |
| `topic` | 综述主题 | `图神经网络在推荐系统中的应用` |
| `ref_count` | 目标参考文献数量 | `30` |
| `word_count` | 目标篇幅 | `7000` |
| `language` | 输出语言 | `zh` / `en` |
| `paper_type` | 论文场景 | `course_paper` / `undergraduate_thesis` |

如果缺少关键信息，Skill 会要求代理只追问必要字段。

## 输出

最终交付物是：

```text
output/review.docx
```

生成的 Word 文档包含：

- 标题、摘要、关键词
- 结构化正文
- 重新编号后的文内引用
- 必要的对比表格
- 可用时插入本地生成图片
- 带编号的参考文献列表，存在 DOI 时保留 DOI
- 由导出脚本处理的学术排版

## 安装

将本目录克隆或复制到 Codex skills 目录：

```text
~/.codex/skills/academic-review
```

安装导出脚本依赖：

```bash
pip install -r requirements.txt
```

之后在 Codex 中直接用综述写作需求触发即可。

## 依赖

Skill 本身以指令驱动为主。唯一的生产脚本是 Word 导出器：

| 脚本 | 作用 |
| --- | --- |
| `scripts/docx_export.py` | 将最终 Markdown 文档转换为格式化 Word 文档 |

Python 依赖见 `requirements.txt`：

- `httpx`
- `python-docx`
- `pillow`
- `requests`

## 目录结构

```text
academic-review/
├── SKILL.md
├── manifest.yaml
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
├── schemas/
├── scripts/
│   ├── docx_export.py
│   ├── fix_encoding.py
│   └── utils.py
├── static/
│   ├── core/
│   ├── fragments/
│   └── stages/
└── workflows/
    └── resume-review.md
```

## 设计原则

- **由代理编排，不由脚本编排**：Codex 按阶段执行综述写作流程。
- **证据边界清晰**：正文论断应基于已检索论文的元数据与摘要。
- **阶段可检查**：每个主要阶段都会写入输出文件后再进入下一步。
- **提纲锁定**：正文写作应遵循已确认提纲和 `review_lock.md`。
- **面向导出**：Markdown 是中间格式，`.docx` 是最终交付格式。

## 适用场景

- 本科毕业论文文献综述
- 课程论文综述
- 英文或中文专题综述初稿
- 需要参考文献、图表、Word 导出的长文档综述

## 不适用场景

- 需要系统综述或元分析的严格 PRISMA 流程
- 必须阅读全文并进行实验数据复核的研究任务
- 需要替代导师、作者或审稿人进行最终学术判断的场景


## 许可证

本项目使用 MIT License。详见 [LICENSE](LICENSE)。
