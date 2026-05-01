# PPT 小红书笔记

参考 PPT 截图，一键生成小红书排版图和文案。

## 工作流程（6步）

| 步骤 | 操作 | 工具 |
|------|------|------|
| 1 | 看图 → 生成 PPT 提示词 | AI 直接生成 |
| 2 | NotebookLM 生成 PPT/PDF | [notebooklm-py](https://github.com/teng-lin/notebooklm-py) |
| 3 | 去除水印 | [dp-pdf-notebooklm-watermarkremover](https://github.com/kenkl1/dp-pdf-notebooklm-watermarkremover) |
| 4 | PDF 转逐页图片 | [dp-pdf-to-images](https://github.com/kenkl1/dp-pdf-to-images) |
| 5 | 小红书排版 | [dp-xhsppt-output_layout](https://github.com/kenkl1/dp-xhsppt-output_layout) |
| 6 | 生成小红书文案 | [dp-xhs-note](https://github.com/kenkl1/dp-xhs-note) |

## 目录结构

```
E:\AI教师PPT工作流\
├── 00-对标库\
│   ├── 对标PPT图片\          ← 输入：参考PPT截图
│   └── 对标小红书文案\       ← 参考文案风格
├── 01-notebooklm原文件\
│   ├── ppt提示词\            ← 生成的提示词
│   └── notebooklm生成pdf\    ← 原始PDF
├── 02-去水印后pdf\           ← 无水印PDF
├── 03-逐页ppt图片\           ← 每页图片
├── 04-排版后图片\            ← 小红书排版图
└── 05-小红书笔记\             ← 生成的文案
```

## 快速开始

1. 准备好参考 PPT 截图
2. 调用 `/dp-notebooklm-ppttoxhs`
3. 选择从第几步开始
4. 等待自动完成

## 工具链

| 工具 | 说明 |
|------|------|
| [dp-ppt-style-gen](https://github.com/kenkl1/dp-ppt-style-gen) | PPT 风格分析 |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | NotebookLM API |
| [dp-pdf-notebooklm-watermarkremover](https://github.com/kenkl1/dp-pdf-notebooklm-watermarkremover) | 去水印 |
| [dp-pdf-to-images](https://github.com/kenkl1/dp-pdf-to-images) | PDF 转图 |
| [dp-xhsppt-output_layout](https://github.com/kenkl1/dp-xhsppt-output_layout) | 小红书排版 |
| [dp-xhs-note](https://github.com/kenkl1/dp-xhs-note) | 小红书文案生成 |

## 输出示例

### Step 5 输出：排版图
- `layout1.png` - 左侧9缩略图 + 右侧3大图
- `layout2.png` - 三层瀑布流
- `layout3.png` - 上下交替排列

### Step 6 输出：文案
```markdown
# 小红书笔记标题
# 小红书商品标题
# 小红书正文文案
#话题
```

保存位置：`05-小红书笔记\{时间戳}_{标题}.md`
