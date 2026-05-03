---
name: dp-notebooklm-ppttoxhs
description: PPT转小红书笔记自动化工作流：粘贴参考PPT截图 → 自动生成小红书排版图。当用户说"跑完整流程"、"执行PPT工作流"、"一键生成小红书图片"时触发。整合 dp-ppt-style-gen + notebooklm-py + dp-pdf-notebooklm-watermarkremover + dp-pdf-to-images + dp-xhsppt-output_layout 五个工具。启动后先介绍6步流程，由用户指定从第几步开始。
---

# PPT小红书笔记 —— 自动化工作流

从参考PPT截图自动生成小红书排版图的完整流程。

## 目录结构

```
E:\AI教师PPT工作流\
├── 00-对标库\对标PPT图片\          ← 输入：参考PPT截图
├── 01-notebooklm原文件\notebooklm生成pdf\  ← 提示词 + 原始PDF
├── 02-去水印后pdf\                 ← 无水印PDF
├── 03-逐页ppt图片\                 ← 每页图片
└── 04-排版后图片\                  ← 最终输出
```

## 工作流程（6步）

| 步骤 | 操作 | 执行者 |
|------|------|--------|
| 1 | 看图 → 生成PPT提示词 | AI（我）直接执行 |
| 2 | NotebookLM 生成 PPT/PDF | AI 调用 notebooklm-py |
| 3 | 去除水印 | AI 调用去水印脚本 |
| 4 | PDF 转逐页图片 | AI 调用 PDF 转图脚本 |
| 5 | 小红书排版 | AI 调用排版脚本 |
| 6 | 生成小红书标题文案 | AI 直接生成 |

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
[████████░░░░░░░░░░░░░░░] 25%  Step 2 进行中
├── Step 1 生成提示词  ✓ 完成
├── Step 2 NotebookLM  ▸ 进行中（生成 Slide Deck...）
├── Step 3 去除水印    ○ 待执行
├── Step 4 PDF转图片    ○ 待执行
├── Step 5 小红书排版  ○ 待执行
└── Step 6 生成文案    ○ 待执行
```

- 每完成一个子操作，立即输出进度更新（百分比、当前操作、文件名/数量/路径等细节）
- 子操作内也分阶段显示（如 Step 2：创建notebook → 添加源 → 生成中 → 下载中）
- 全部完成后汇总输出所有文件路径

### Step 1：看图生成PPT提示词

**交互**：用户选 Step 1 后，依次收集以下信息：

1. **图片路径**：请用户提供参考PPT截图路径（支持 PNG/JPG）
2. **主题**：这个风格，做一个关于____的PPT？
3. **页数**：建议多少页？（不填默认8页）
4. **补充要求**：有无特殊要求？（不填则按参考图风格执行）

收到图片路径后，用 Read 工具读取图片。看图后按上述顺序收集信息，确认后再生成提示词。

**执行**：
1. 用 Read 工具读取图片，看图提取设计规范（不输出中间过程）
2. 收集用户输入（主题、页数、补充要求）
3. 读取 `references/ppt-generate-prompt.md`，结合设计规范 + 用户需求生成逐页提示词
4. 保存为 Markdown：
   - **路径**：`E:\AI教师PPT工作流\01-notebooklm原文件\ppt提示词\{YYYYMMDD_HHMMSS}_{主题}.md`
   - 文件头含主题、时间戳、页数结构
   - 逐页提示词用 `---第X页---` 分隔

**输出示例**：`...\ppt提示词\20260501_171118_二十四节气.md`

> 直接输出最终提示词，不输出分析过程。

### Step 2：NotebookLM 生成 PPT/PDF

```bash
notebooklm create "PPT：[主题]" --json
# 解析输出获取 notebook_id → nb_id

# 提示词文件路径格式：E:\AI教师PPT工作流\01-notebooklm原文件\ppt提示词\{时间戳}_{主题}.md
notebooklm source add "E:\AI教师PPT工作流\01-notebooklm原文件\ppt提示词\{时间戳}_{主题}.md" -n <nb_id> --json
# 解析输出获取 source_id

notebooklm source wait <source_id> -n <nb_id> --timeout 120

notebooklm generate slide-deck --format detailed -n <nb_id> --json
# 解析输出获取 artifact_id（task_id）

notebooklm artifact wait <artifact_id> -n <nb_id> --timeout 900

notebooklm download slide-deck "E:\AI教师PPT工作流\01-notebooklm原文件\notebooklm生成pdf\{主题}_{时间戳}.pdf" -n <nb_id>
```

**输出**：`E:\AI教师PPT工作流\01-notebooklm原文件\notebooklm生成pdf\{主题}_{时间戳}.pdf`
> 例：`...\notebooklm生成pdf\二十四节气_20260501_171118.pdf`

### Step 3：去除水印

```bash
python ~/.claude/skills/dp-pdf-notebooklm-watermarkremover/scripts/download.py \
  "E:\AI教师PPT工作流\01-notebooklm原文件\notebooklm生成pdf\slides.pdf" \
  --output "E:\AI教师PPT工作流\02-去水印后pdf\{主题}_{时间戳}_nowatermark.pdf"
```

**输出**：`E:\AI教师PPT工作流\02-去水印后pdf\{主题}_{时间戳}_nowatermark.pdf`

### Step 4：PDF 转逐页图片

```python
import sys, importlib.util
spec = importlib.util.spec_from_file_location(
    "convert",
    str(Path.home() / ".claude/skills/dp-pdf-to-images/scripts/convert.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.convert_pdf_to_images(
    pdf_path=r"E:\AI教师PPT工作流\02-去水印后pdf\{主题}_nowatermark.pdf",
    output_dir=r"E:\AI教师PPT工作流\03-逐页ppt图片\{主题}_{时间戳}",
    dpi=150, format="jpg", max_size_mb=5,
)
```

**输出**：`E:\AI教师PPT工作流\03-逐页ppt图片\{主题}_{时间戳}\page_001.jpg` ...

### Step 5：小红书排版

**自动生成全部3种布局，用尽所有图片**：
- `layout1`：左侧9缩略图 + 右侧3大图（需要12张图）
- `layout2`：三层瀑布流，用尽所有图片
- `layout3`：上下交替排列，用尽所有图片

```bash
python ~/.claude/skills/dp-xhsppt-output_layout/ppt_layout.py \
  "E:\AI教师PPT工作流\03-逐页ppt图片\{主题}_{时间戳}" \
  -o "E:\AI教师PPT工作流\04-排版后图片\{主题}_{时间戳}" \
  -l all
```

**输出**：多个文件，命名格式为 `layout{N}_{MM}.png`（如 `layout1_01.png`, `layout2_01.png`, `layout3_01.png` 等）

### Step 6：生成小红书标题和文案

基于 PPT 主题，生成小红书风格内容：
- **标题**：吸引眼球，含emoji，贴合平台风格
- **文案**：配合排版图使用，2-3段正文

直接输出在对话里，不保存文件。

## 当前进度追踪

进入 skill 时，先扫描各目录，自动判断当前进度：

**进度检查顺序**：
1. 检查 `01-notebooklm原文件\ppt提示词\` 下最新 `.md` 文件 → 有则 Step 1 完成
2. 检查 `01-notebooklm原文件\notebooklm生成pdf\` 下最新 `.pdf` 文件 → 有则 Step 2 完成
3. 检查 `02-去水印后pdf\{主题}_{时间戳}_nowatermark.pdf` 是否存在 → 有则 Step 3 完成
4. 检查 `03-逐页ppt图片\{主题}_{时间戳}\` 下图片数量 → 有则 Step 4 完成
5. 检查 `04-排版后图片\{主题}_{时间戳}\layout1.png` 是否存在 → 有则 Step 5 完成（3张layout都会生成）

**显示格式**（每次汇报进度时使用）：

```
PPT小红书笔记 — 当前进度
[████████░░░░░░░░░░░░░░░] 25%  Step 2 进行中
├── Step 1 生成提示词  ✓ 完成
├── Step 2 NotebookLM  ▸ 进行中（生成 Slide Deck...）
├── Step 3 去除水印    ○ 待执行
├── Step 4 PDF转图片    ○ 待执行
├── Step 5 小红书排版  ○ 待执行
└── Step 6 生成文案    ○ 待执行
```

**执行中进度规则**：
- 每完成一个子操作，立即输出进度更新
- 包含：进度百分比、当前操作名称、具体细节（文件名、数量、路径等）
- 子操作内也需分阶段显示（如 Step 2：创建notebook → 添加源 → 生成中 → 下载中）

**完成后**：汇总输出所有文件路径，并在汇总中列出全部6步的完成状态，格式如下：

```
PPT小红书笔记 — 完成！
[████████████████████████] 100%

├── Step 1 生成提示词    ✓ 完成（X页提示词）
├── Step 2 NotebookLM   ✓ 完成（PDF: X.XMB）
├── Step 3 去除水印      ✓ 完成（去水印后: X.XMB）
├── Step 4 PDF转图片     ✓ 完成（X张图片，XMB）
├── Step 5 小红书排版   ✓ 完成（X张排版图）
└── Step 6 生成文案      ✓ 完成（标题+正文已输出）

输出文件：
- 提示词: ...\ppt提示词\{时间戳}_{主题}.md
- PDF: ...\notebooklm生成pdf\{主题}_{时间戳}.pdf
- 去水印PDF: ...\02-去水印后pdf\{主题}_{时间戳}_nowatermark.pdf
- 逐页图片: ...\03-逐页ppt图片\{主题}_{时间戳}\（X张）
- 排版图片: ...\04-排版后图片\{主题}_{时间戳}\（X张）
```

## 断点续跑

```bash
python ~/.claude/skills/dp-notebooklm-ppttoxhs/scripts/run_pipeline.py --start 3
```
