# PPT 小红书笔记

参考 PPT 截图，一键生成小红书排版图。

## 工作流程（6步）

| 步骤 | 操作 |
|------|------|
| 1 | 看图 → 生成 PPT 提示词 |
| 2 | NotebookLM 生成 PPT/PDF |
| 3 | 去除水印 |
| 4 | PDF 转逐页图片 |
| 5 | 小红书排版 |
| 6 | 生成标题文案 |

## 目录结构

```
E:\AI教师PPT工作流\
├── 00-对标库\对标PPT图片\          ← 输入：参考PPT截图
├── 01-notebooklm原文件\notebooklm生成pdf\  ← 提示词 + 原始PDF
├── 02-去水印后pdf\                 ← 无水印PDF
├── 03-逐页ppt图片\{主题}_{时间戳}\   ← 每页图片
└── 04-排版后图片\{主题}_{时间戳}\    ← 最终输出
```

## 快速开始

1. 准备好参考 PPT 截图
2. 调用 `/dp-notebooklm-ppttoxhs`
3. 选择从第几步开始
4. 等待自动完成

## 工具链

- [dp-ppt-style-gen](https://github.com/kenkl1/dp-ppt-style-gen) — PPT 风格分析
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) — NotebookLM API
- [dp-pdf-notebooklm-watermarkremover](https://github.com/kenkl1/dp-pdf-notebooklm-watermarkremover) — 去水印
- [dp-pdf-to-images](https://github.com/kenkl1/dp-pdf-to-images) — PDF 转图
- [dp-xhsppt-output_layout](https://github.com/kenkl1/dp-xhsppt-output_layout) — 小红书排版
