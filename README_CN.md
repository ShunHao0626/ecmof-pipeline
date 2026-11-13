# EC-MOF 数据流水线

[English](README.md) · **简体中文**

EC-MOF Data Pipeline 是一个面向科研的工作流程，用于构建并核验导电金属有机框架（electrically conductive metal-organic frameworks, EC-MOFs）的结构化数据。它整合了文献整理、PDF 转 Markdown、MOF 记录规范化以及基于原文证据的核验。

本仓库包含代码与研究者自建的结构化数据。出版社 PDF、补充材料、提取出的图像及全文副本均有意排除在外。

## 项目状态

本仓库是早期科研原型的首个整理版本，提供一个小型命令行接口、测试、JSON Schema 草案，以及经过机械修复的 71 条记录科研快照。数据的科学审阅仍在进行中。

| 组件 | 状态 |
| --- | --- |
| 文献整理 | 本地流程已记录 |
| PDF 转 Markdown | 作为可选功能提供 |
| 结构化 MOF 记录 | 包含 71 条记录的草稿快照 |
| 精确与模糊核验 | 已提供 |
| 基于 Transformer 的语义核验 | 旧原型，尚未打包 |
| 命令行接口 | 已提供 |
| 自动化测试 | 已包含 |

在逐字段核验状态审阅完成之前，结果应视为科研标注，而非权威化学记录。

## 目标

- 以 DOI 等稳定标识符整理 EC-MOF 文献。
- 将本地获取的论文转换为机器可读文本，供私人研究使用。
- 用统一的 JSON 结构表示结构、合成、表征与性能信息。
- 通过精确、模糊与语义匹配，将抽取值与原文进行比对。
- 记录核验证据，而不在 JSON 文件中插入非法注释。
- 生成小规模、可复现、可检查与扩展的数据集。

## 流程

```text
本地文献库
        |
        v
PDF 文本 / Markdown 提取
        |
        v
结构化 MOF 信息抽取
        |
        v
结构规范化
        |
        v
证据核验
        |
        v
带版本号的 JSON 数据集 + 核验报告
```

本地文献库是流程的输入，不属于 Git 仓库。

## 数据模型

规范化后的记录应包含以下顶层字段：

```json
{
  "MOF_name": "",
  "molecular_formula": "",
  "source_paper": "",
  "metal_node": {},
  "ligand": {},
  "topology": "",
  "Dimensionality": "",
  "Crystal_system": "",
  "Space_group": "",
  "properties": {},
  "characterization_data": {},
  "synthesis_method": "",
  "reaction_conditions": {},
  "raw_materials": "",
  "composition_structure": "",
  "application": ""
}
```

清洗过程将统一命名规范、区分缺失值与确实未注明的值、展开意外嵌套的记录，并将核验错误移入机器可读的元数据中。

## 核验方法

当前原型结合了几种证据检查方式：

1. 对标点、空白及化学式变体进行文本规范化。
2. 与原文分块进行精确与模糊匹配。
3. 可配置的词汇匹配阈值及明确的证据报告。

早期原型还尝试过科学语言 Transformer 模型。该依赖较重的路径在首个整理版本中未启用，只有在模型版本固定且具备测试后才会重新引入。

自动匹配可能产生假阳性与假阴性。化学式、晶体学参数、单位及数值性能在发表或用于下游科学研究前应经人工审阅。

## 仓库结构

```text
ecmof-pipeline/
├── src/ecmof_pipeline/
│   ├── literature.py
│   ├── convert.py
│   ├── normalize.py
│   ├── validate.py
│   └── cli.py
├── data/
│   ├── processed/
│   │   └── ecmof.json
│   └── samples/
├── schemas/
├── tests/
├── pyproject.toml
└── README.md
```

## 安装

创建独立环境并以可编辑模式安装：

```bash
git clone <repository-url>
cd ecmof-pipeline
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

核心核验功能目前依赖 `numpy`、`torch`、`transformers`、`scipy`、`pdfplumber` 及模糊字符串匹配工具。PDF 转换另需 PyMuPDF、MinerU 或 `pymupdf4llm` 等可选依赖。

## 命令行接口

```bash
# 将本地论文转换为 Markdown
python -m ecmof_pipeline convert \
  --input /path/to/local/papers \
  --output /path/to/local/markdown

# 规范化分散的抽取文件
python -m ecmof_pipeline normalize \
  --input data/raw \
  --output data/processed/ecmof.json

# 对照本地原文核验记录
python -m ecmof_pipeline validate \
  --data data/processed/ecmof.json \
  --papers /path/to/local/papers \
  --report validation-report.json
```

## 数据与版权政策

除非许可明确允许，本仓库不会分发出版社 PDF、补充材料或全文 Markdown 副本。记录应以 DOI 或其他文献信息标注来源，以便用户通过出版社、存储库或机构渠道获取原文。

只应提交研究者自建的标注以及小规模、可合法再分发的示例。

## 已知局限

- 草稿数据集中仍存在取值类型与命名风格不一致的问题。
- 部分源片段含有非标准的 `//error` 注释，需要修复。
- 一个草稿汇总文件中意外嵌套了一组记录。
- 基于模型的相似度只是证据辅助，并非科学验证。
- 原始脚本中含有平台相关路径，需要去除。
- 可复现性取决于模型版本与 PDF 文本提取质量。

## 可复现性

公开发布时应记录：

- 数据集版本与校验值。
- Schema 版本。
- Transformer 模型及其版本。
- 匹配阈值。
- PDF 提取后端及其版本。
- 抽取与核验日期。

生成的缓存、日志、模型权重、私有文献与临时转换输出应保存在 Git 之外，或通过 `.gitignore` 忽略。

## 参与贡献

首个整理版本发布后欢迎贡献，包括 Schema 讨论、核验测试、DOI 更正、抽取问题报告以及人工核验过的记录。请勿提交受版权保护的论文文件。

## 引用

带版本号的引用格式将随首个公开数据集发布提供。在此之前，请引用仓库地址及所用的具体 commit。

## 许可

尚未选定公开许可。代码与数据许可将在首个公开版本发布前另行说明；第三方原始文献不在本仓库许可范围内。
