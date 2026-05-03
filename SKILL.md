---
name: dp-notebooklm-ppttoxhs
description: PPT转小红书笔记自动化工作流：粘贴参考PPT截图 → 自动生成小红书排版图。当用户说"跑完整流程"、"执行PPT工作流"、"一键生成小红书图片"时触发。整合 dp-ppt-style-gen + notebooklm-py + dp-pdf-notebooklm-watermarkremover + dp-pdf-to-images + dp-xhsppt-output_layout 五个工具。启动后先介绍6步流程，由用户指定从第几步开始。
---

# PPT小红书笔记 —— 自动化工作流

从参考PPT截图自动生成小红书排版图的完整流程。

## 目录结构

```
E:\AI教师PPT工作流\
├── 01-ppt提示词\
│   ├── 未使用/   ← Step1 生成提示词
│   └── 已完成/   ← Step2 取用后
├── 02-notebooklm生成pdf\
│   ├── 未使用/   ← Step2 生成PDF
│   └── 已完成/   ← Step3 取用后
├── 03-去除水印后pdf\
│   ├── 未使用/   ← Step3 原始PDF来源
│   └── 已完成/   ← Step3 去水印后 → Step4 取用
├── 04-逐页ppt图片\
│   ├── 未使用/   ← Step4 输入来源
│   └── 已完成/   ← Step4 转图后 → Step5 取用
├── 05-小红书排版图片\
│   ├── 未使用/   ← Step5 输入来源
│   └── 已完成/   ← Step5 排版后 → Step6 取用
└── 06-小红书笔记文案\
    └── 已完成/   ← Step6 最终输出
```

## 工作流程（6步）

```
用户发截图
    ↓
Step1 生成PPT提示词 → 保存到【01-ppt提示词\未使用】
    ↓
Step2 NotebookLM → 取用【01-ppt提示词\未使用】→ PDF保存到【02-notebooklm生成pdf\未使用】
                 → 01-ppt提示词\未使用 的文件 → 移动到【01-ppt提示词\已完成】
    ↓
Step3 去除水印 → 取用【02-notebooklm生成pdf\未使用】→ 去水印保存到【03-去除水印后pdf\已完成】
              → 02-notebooklm生成pdf\未使用 的文件 → 移动到【02-notebooklm生成pdf\已完成】
    ↓
Step4 PDF转图片 → 取用【03-去除水印后pdf\已完成】→ 图片保存到【04-逐页ppt图片\已完成】
    ↓
Step5 小红书排版 → 取用【04-逐页ppt图片\已完成】→ 排版图保存到【05-小红书排版图片\已完成】
    ↓
Step6 生成文案 → 取用【05-小红书排版图片\已完成】→ 文案保存到【06-小红书笔记文案\已完成】
```

## 触发方式

用户说以下任一内容时启动：
- "跑完整PPT流程"
- "执行notebooklm ppt工作流"
- "一键生成小红书图片"
- 直接发截图路径 + "按这个风格做"

## 交互入口

**不扫描目录**，直接介绍流程并询问从第几步开始。

---

**PPT小红书笔记 — 自动化工作流 共 6 步**

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 看图 → 生成提示词 | 用户发参考PPT截图路径，我来生成提示词 |
| 2 | NotebookLM 生成 PPT | 上传提示词 → 生成 slide deck → 下载 PDF |
| 3 | 去除水印 | 去掉 "Made with NotebookLM" 水印 |
| 4 | PDF 转逐页图片 | 逐页输出为 JPG，每张 ≤5MB |
| 5 | 小红书排版 | 自动生成 3 种布局排版图 |
| 6 | 生成标题文案 | 自动生成小红书标题 + 正文 |

**请告诉我：从第几步开始？**

- 直接发截图路径 → 从 Step 1 开始
- 已生成提示词 → 从 Step 2 开始
- PDF已有需去水印 → 从 Step 3 开始
- 以此类推

---

## 进度显示规则

**只有开始执行时才显示进度**，入口只显示上方简洁表格。进度格式：

```
PPT小红书笔记 — 进度
[████████░░░░░░░░░░░░░░░░░░░] 33%  Step 2 进行中
├── Step 1 生成提示词    ✓ 完成
├── Step 2 NotebookLM   ▸ 进行中（生成 Slide Deck...）
├── Step 3 去除水印      ○ 待执行
├── Step 4 PDF转图片     ○ 待执行
├── Step 5 小红书排版    ○ 待执行
└── Step 6 生成文案      ○ 待执行
```

- 每完成一个子操作，立即输出进度更新（百分比、当前操作、文件名/数量/路径等细节）
- 子操作内也分阶段显示（如 Step 2：创建notebook → 添加源 → 生成中 → 下载中）
- 全部完成后汇总输出所有文件路径

---

## Step 1：看图生成PPT提示词

**交互**：用户选 Step 1 后，依次收集以下信息：

1. **图片路径**：请用户提供参考PPT截图路径（支持 PNG/JPG）
2. **主题**：这个风格，做一个关于____的PPT？
3. **页数**：建议多少页？（不填默认8页）
4. **补充要求**：有无特殊要求？（不填则按参考图风格执行）

收到图片路径后，用 `/dp-ppt-style-gen` skill 来分析图片，提取设计规范。

**注意**：不要自己用 Read 工具尝试读取图片（会失败），直接调用 `/dp-ppt-style-gen` skill，传入图片路径作为参数。

**执行**：
1. 调用 `/dp-ppt-style-gen` skill 传入图片路径，获取设计规范（不输出中间分析过程）
2. 收集用户输入（主题、页数、补充要求）
3. 读取 `references/ppt-generate-prompt.md`，结合设计规范 + 用户需求生成逐页提示词
4. **保存为 Markdown 到 `01-ppt提示词\未使用`**：
   - **路径**：`E:\AI教师PPT工作流\01-ppt提示词\未使用\{YYYYMMDD_HHMMSS}_{主题}.md`
5. 告知用户保存路径，询问是否进入 Step 2

**进度**：生成提示词 → **保存到 `01未使用`** → 告知用户 → 可进入 Step 2

---

## Step 2：NotebookLM 生成 PPT/PDF

**取用** `01-ppt提示词\未使用` 中的提示词文件。

```bash
# 1. 创建 notebook
notebooklm create "PPT：[主题]" --json
# 解析输出获取 notebook_id → nb_id

# 2. 添加提示词（从 01未使用 取用）
notebooklm source add "E:\AI教师PPT工作流\01-ppt提示词\未使用\{时间戳}_{主题}.md" -n <nb_id> --json
# 解析输出获取 source_id

# 3. 等待源上传完成
notebooklm source wait <source_id> -n <nb_id> --timeout 120

# 4. 生成 slide deck
notebooklm generate slide-deck --format detailed -n <nb_id> --json
# 解析输出获取 artifact_id

# 5. 等待生成完成
notebooklm artifact wait <artifact_id> -n <nb_id> --timeout 900

# 6. 下载 PDF → 保存到 02未使用
notebooklm download slide-deck "E:\AI教师PPT工作流\02-notebooklm生成pdf\未使用\{主题}_{时间戳}.pdf" -n <nb_id>
```

**完成后**：
- PDF 在 `02-notebooklm生成pdf\未使用`
- 提示词从 `01-ppt提示词\未使用` **移动到** `01-ppt提示词\已完成`
- 告知用户可进入 Step 3

**进度**：创建notebook → 添加源 → 生成中 → 下载中 → 提示词归位 → 告知用户

---

## Step 3：去除水印

**取用** `02-notebooklm生成pdf\未使用` 中的原始 PDF，执行去水印。

```bash
python ~/.claude/skills/dp-pdf-notebooklm-watermarkremover/scripts/download.py \
  "E:\AI教师PPT工作流\02-notebooklm生成pdf\未使用\{主题}_{时间戳}.pdf" \
  --output "E:\AI教师PPT工作流\03-去除水印后pdf\已完成\{主题}_{时间戳}_nowatermark.pdf"
```

**完成后**：
- 去水印 PDF 保存到 `03-去除水印后pdf\已完成`
- 原始 PDF 从 `02-notebooklm生成pdf\未使用` **移动到** `02-notebooklm生成pdf\已完成`
- 告知用户可进入 Step 4

**进度**：取用 02未使用 → 去水印 → 保存到 03已完成 → 移动原始PDF到 02已完成

---

## Step 4：PDF 转逐页图片

**取用** `03-去除水印后pdf\已完成` 中的去水印 PDF。

```python
import sys, importlib.util
spec = importlib.util.spec_from_file_location(
    "convert",
    str(Path.home() / ".claude/skills/dp-pdf-to-images/scripts/convert.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.convert_pdf_to_images(
    pdf_path=r"E:\AI教师PPT工作流\03-去除水印后pdf\已完成\{主题}_{时间戳}_nowatermark.pdf",
    output_dir=r"E:\AI教师PPT工作流\04-逐页ppt图片\已完成\{主题}_{时间戳}",
    dpi=150, format="jpg", max_size_mb=5,
)
```

**输出**：`04-逐页ppt图片\已完成\{主题}_{时间戳}\page_001.jpg` ...

**进度**：读取 PDF → 逐页转换中（X/Y）→ 全部完成

---

## Step 5：小红书排版

**取用** `04-逐页ppt图片\已完成` 中的逐页图片。

**自动生成全部3种布局，用尽所有图片**：
- `layout1`：左侧9缩略图 + 右侧3大图
- `layout2`：三层瀑布流
- `layout3`：上下交替排列

```bash
python ~/.claude/skills/dp-xhsppt-output_layout/ppt_layout.py \
  "E:\AI教师PPT工作流\04-逐页ppt图片\已完成\{主题}_{时间戳}" \
  -o "E:\AI教师PPT工作流\05-小红书排版图片\已完成\{主题}_{时间戳}" \
  -l all
```

**输出**：`05-小红书排版图片\已完成\{主题}_{时间戳}\layout{N}_{MM}.png`

**进度**：读取图片 → 生成 layout1 → layout2 → layout3 → 全部完成

---

## Step 6：生成小红书标题和文案

**取用** `05-小红书排版图片\已完成` 中的排版图。

调用 `/dp-xhs-note` skill 生成完整的小红书文案，包括：
- 小红书笔记标题（20字内，含emoji）
- 小红书商品标题（30字内，含关键词）
- 小红书正文文案（爆款风格，含痛点升华、金句结尾）
- 话题标签（5个hashtag）

**输出**：
- 保存为 Markdown：`E:\AI教师PPT工作流\06-小红书笔记文案\未发布\{时间戳}_{标题}.md`
- 在对话里也输出一遍，方便用户直接复制

> 调用方式：`Skill("dp-xhs-note")`，传入主题和时间戳信息。

**进度**：读取排版图 → 生成文案 → 保存到 `06未发布` → 输出

---

## 完成后汇总格式

```
PPT小红书笔记 — 完成！
[████████████████████████] 100%

├── Step 1 生成提示词    ✓ 完成（X页 → 01未使用）
├── Step 2 NotebookLM   ✓ 完成（PDF → 02未使用 → 01已完成）
├── Step 3 去除水印      ✓ 完成（去水印PDF → 03已完成 → 02已完成）
├── Step 4 PDF转图片     ✓ 完成（X张 → 04已完成）
├── Step 5 小红书排版    ✓ 完成（X张 → 05已完成）
└── Step 6 生成文案      ✓ 完成（文案 → 06已完成）

输出文件：
- 提示词: ...\01-ppt提示词\已完成\{时间戳}_{主题}.md
- 原始PDF: ...\02-notebooklm生成pdf\已完成\{主题}_{时间戳}.pdf
- 去水印PDF: ...\03-去除水印后pdf\已完成\{主题}_{时间戳}_nowatermark.pdf
- 逐页图片: ...\04-逐页ppt图片\已完成\{主题}_{时间戳}（X张）
- 排版图片: ...\05-小红书排版图片\已完成\{主题}_{时间戳}（X张）
- 文案: ...\06-小红书笔记文案\未发布\{时间戳}_{标题}.md
```

## 断点续跑

```bash
python ~/.claude/skills/dp-notebooklm-ppttoxhs/scripts/run_pipeline.py --start 3
```
