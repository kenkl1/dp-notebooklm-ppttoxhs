# 目录路径参考

所有路径均基于 `E:\AI教师PPT工作流\` 根目录。

## 各步骤路径速查

| 变量 | 完整路径 |
|------|---------|
| `REF_IMAGES` | `E:\AI教师PPT工作流\00-对标库\对标PPT图片` |
| `REF_XHS_COPY` | `E:\AI教师PPT工作流\00-对标库\对标小红书文案` |
| `PROMPTS_DIR` | `E:\AI教师PPT工作流\01-notebooklm原文件\notebooklm生成pdf` |
| `CLEAN_PDF_DIR` | `E:\AI教师PPT工作流\02-去水印后pdf` |
| `PAGES_DIR` | `E:\AI教师PPT工作流\03-逐页ppt图片` |
| `FINAL_DIR` | `E:\AI教师PPT工作流\04-排版后图片` |
| `XHS_NOTE_DIR` | `E:\AI教师PPT工作流\05-小红书笔记` |

## 关键文件

| 说明 | 路径 |
|------|------|
| 提示词文本（Markdown格式） | `...\ppt提示词\{时间戳}_{主题}.md` |
| NotebookLM PDF | `...\notebooklm生成pdf\{主题}_{时间戳}.pdf` |
| 去水印 PDF | `...\02-去水印后pdf\slides_nowatermark.pdf` |
| 逐页图片 | `...\03-逐页ppt图片\page_001.jpg` ... |
| 最终排版图 | `...\04-排版后图片\layout1.png` |

## 各工具参考文档

| 工具 | 路径 |
|------|------|
| dp-ppt-style-gen | `~/.claude/skills/dp-ppt-style-gen/SKILL.md` |
| notebooklm-py | `~/.claude/skills/notebooklm-py/SKILL.md` |
| 去水印脚本 | `~/.claude/skills/dp-pdf-notebooklm-watermarkremover/scripts/download.py` |
| PDF转图片脚本 | `~/.claude/skills/dp-pdf-to-images/scripts/convert.py` |
| 排版脚本 | `~/.claude/skills/dp-xhsppt-output_layout/ppt_layout.py` |