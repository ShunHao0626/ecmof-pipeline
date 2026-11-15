# EC-MOF 数据流水线

[English](README.md) · **简体中文**

本仓库提供 Python 流水线，用于整理文献中的导电金属有机框架（EC-MOF）数据。它规范化抽取记录，并在本地保存的来源论文中定位候选文本证据。

仓库包含**引用 21 个来源的 71 条研究记录**、JSON Schema 草案、命令行工具和测试。证据报告支持逐字段科学复核。

## 研究产物

该流程将结构化记录与本地论文的词汇证据关联。数据集是科研标注，逐字段科学审阅仍在进行。

| 组件 | 状态 |
| --- | --- |
| PDF 转 Markdown | 作为可选功能提供 |
| 结构化 MOF 记录 | 包含 71 条记录的草稿快照 |
| 精确与模糊（词汇层面）证据匹配 | 已提供 |
| 命令行接口 | 已提供 |
| 自动化测试 | 已包含 |

## 目标

- 将本地获取的论文转换为机器可读文本，供私人研究使用。
- 用统一的 JSON 结构表示结构、合成、表征与性能信息。
- 通过精确与模糊的词汇匹配，将抽取值与原文进行比对。
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
结构化 MOF 信息抽取   （在上游完成，不属于本软件包）
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

当前的 `normalize` 步骤会展开意外嵌套的数组，在读取 JSON 时去除遗留的 `//error` 标记，并按预期字段顺序重写每条记录（缺失字段写为 `null`，额外字段保留在其后）。统一命名规范、区分缺失值与确实未注明的值、将核验错误移入机器可读元数据等功能仍在计划中。

## 核验方法

`validate` 命令只做词汇层面的证据匹配：

1. 读取 `--papers` 下的所有文档（`.md`、`.txt` 或 `.pdf`），切分为相互重叠的文本块（默认 1,500 字符，重叠 150 字符）。
2. 对每条记录中所有非空的字符串或数值字段做 Unicode NFKC 规范化、大小写折叠与空白合并；不再对化学式变体或标点做进一步处理。
3. 规范化后的取值若原样出现在某个文本块中，得分为 1.0；否则得分为最长公共子串长度除以取值长度（Python `difflib`）。得分不低于 `--threshold`（默认 0.8）的字段记为 matched。

阅读报告时需注意两点：

- 所有文档的文本块会被合并在一起匹配。记录**不会**限定在其 `source_paper` 字段对应的论文内，因此某个值可能被另一篇论文的文本匹配上。核验单条记录时，应只把对应论文传给 `--papers`。
- 元素符号、单个数字或 `2D` 这类很短的取值几乎能匹配任何文本，证据价值很低。

自动匹配可能产生假阳性与假阴性。化学式、晶体学参数、单位及数值性能在发表或用于下游科学研究前应经人工审阅。

## 仓库结构

```text
ecmof-pipeline/
├── src/ecmof_pipeline/
│   ├── __main__.py
│   ├── cli.py
│   ├── convert.py
│   ├── io.py
│   ├── literature.py
│   ├── normalize.py
│   ├── schema.py
│   └── validate.py
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
git clone https://github.com/ShunHao0626/ecmof-pipeline.git
cd ecmof-pipeline
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .          # 核心功能：无第三方依赖
python -m pip install -e '.[pdf]'   # 可选：PDF 读取与转换
```

核心功能（规范化，以及对照 Markdown 或纯文本原文的核验）只使用 Python 标准库。可选的 `pdf` 依赖组会安装 `pdfplumber`（核验时提取 PDF 文本）和 `pymupdf4llm`（`convert` 命令）。目前不支持其他转换后端。

## 命令行接口

```bash
# 安装后提供的 `ecmof-pipeline` 命令与 `python -m ecmof_pipeline` 等价。

# 将本地论文转换为 Markdown（需要 `pdf` 依赖组）
python -m ecmof_pipeline convert \
  --input /path/to/local/papers \
  --output /path/to/local/markdown

# 规范化分散的抽取文件
# --input 可重复指定，每个值可以是 JSON 文件或目录
python -m ecmof_pipeline normalize \
  --input /path/to/local/raw-json \
  --output data/processed/ecmof.json

# 对照本地原文核验记录
python -m ecmof_pipeline validate \
  --data data/processed/ecmof.json \
  --papers /path/to/local/papers \
  --report validation-report.json \
  --threshold 0.8 \
  --chunk-size 1500
```

## 数据与版权政策

除非许可明确允许，本仓库不会分发出版社 PDF、补充材料或全文 Markdown 副本。记录应以 DOI 或其他文献信息标注来源，以便用户通过出版社、存储库或机构渠道获取原文。

只应提交研究者自建的标注以及小规模、可合法再分发的示例。

## 已知局限

- 草稿数据集中仍存在取值类型与命名风格不一致的问题。
- 部分源片段含有非标准的 `//error` 注释；`load_json` 会自动去除，但被标记的取值仍需人工复核。
- 核验时合并所有输入文档，不会逐条对照记录自身的 `source_paper`（见[核验方法](#核验方法)）。
- 词汇匹配只是证据辅助，并非科学验证。
- `processed/ecmof.json` 快照已展平为 71 条记录，但尚未按 DOI 去重（共引用 21 个不同来源）。
- 可复现性取决于 PDF 文本提取质量。

## 可复现性

公开发布时应记录：

- 数据集版本与校验值。
- Schema 版本。
- 匹配阈值。
- PDF 提取后端及其版本。
- 抽取与核验日期。

生成的缓存、日志、模型权重、私有文献与临时转换输出应保存在 Git 之外，或通过 `.gitignore` 忽略。

## 参与贡献

欢迎贡献，包括 Schema 讨论、核验测试、DOI 更正、抽取问题报告以及人工核验过的记录。请勿提交受版权保护的论文文件。

## 引用

带版本号的引用格式将随首个公开数据集发布提供。在此之前，请引用仓库地址及所用的具体 commit。

## 许可

尚未选定公开许可。代码与数据许可将在首个公开版本发布前另行说明；第三方原始文献不在本仓库许可范围内。
