#!/usr/bin/env python3
"""
NotebookLM PPT Pipeline - 断点续跑脚本

步骤2-5自动化执行，步骤1由AI（/dp-ppt-style-gen）生成提示词。
用法：python run_pipeline.py --start 3 --topic "二十四节气" --timestamp "20260501_171118"
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

# 路径配置
PIPELINE_DIR = Path(r"E:\AI教师PPT工作流")

PROMPTS_DIR = PIPELINE_DIR / r"01-notebooklm原文件\ppt提示词"
PDF_RAW_BASE = PIPELINE_DIR / r"01-notebooklm原文件\notebooklm生成pdf"
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
PDF_RAW_BASE.mkdir(parents=True, exist_ok=True)

PATHS = {
    "prompts_dir": PROMPTS_DIR,
    "pdf_clean":   PIPELINE_DIR / r"02-去水印后pdf\slides_nowatermark.pdf",
    "pages_dir":   PIPELINE_DIR / r"03-逐页ppt图片",
    "final_dir":   PIPELINE_DIR / r"04-排版后图片",
}


def get_latest_prompts_file():
    """获取最新生成的提示词文件（按时间戳排序）"""
    md_files = list(PATHS["prompts_dir"].glob("*.md"))
    if not md_files:
        return None, None, None
    sorted_files = sorted(md_files, key=lambda f: f.name)
    latest = sorted_files[-1]
    # 解析 {时间戳}_{主题}.md
    m = re.match(r'^(\d{8}_\d{6})_(.+)\.md$', latest.name)
    if m:
        timestamp = m.group(1)
        topic = m.group(2)
        return latest, topic, timestamp
    return latest, None, None


def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_step(name, cmd):
    print(f"\n{'='*50}")
    print(f"  步骤: {name}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                            env={**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"})
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode != 0:
        print(f"[ERROR] '{name}' 失败，退出码: {result.returncode}")
        sys.exit(1)
    print(f"[OK] {name} 完成")
    return result


def parse_json_output(stdout):
    try:
        return json.loads(stdout.strip())
    except Exception:
        return None


def nb_login():
    result = subprocess.run(
        "notebooklm status",
        shell=True, capture_output=True, text=True,
        env={**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    if "Authenticated" not in result.stdout and result.returncode != 0:
        print("[INFO] 需要登录 NotebookLM，正在打开浏览器...")
        subprocess.run("notebooklm login", shell=True)
        input("登录完成后按 Enter 继续...")


# -------------------------------------------------------------------
# 步骤函数
# -------------------------------------------------------------------

def step2_notebooklm(topic=None, timestamp=None):
    """上传提示词到 NotebookLM，生成 slide deck"""

    prompts_file, parsed_topic, parsed_ts = get_latest_prompts_file()
    if not prompts_file:
        print(f"[ERROR] 提示词文件不存在: {PATHS['prompts_dir']}/*.md")
        print("请先运行 /notebooklm-ppt-pipeline 生成提示词")
        sys.exit(1)
    topic = topic or parsed_topic or "PPT"
    timestamp = timestamp or parsed_ts or time.strftime("%Y%m%d_%H%M%S")
    print(f"[INFO] 使用提示词文件: {prompts_file.name}")
    print(f"[INFO] 主题: {topic}  时间戳: {timestamp}")

    # 创建独立输出目录：.../notebooklm生成pdf/{主题}_{时间戳}/
    pdf_raw = PDF_RAW_BASE / f"{topic}_{timestamp}.pdf"
    PATHS["pdf_raw"] = pdf_raw

    nb_login()

    # 1. 创建 notebook
    result = run_step("创建 NotebookLM notebook",
                     f'notebooklm create "PPT：{topic}" --json')
    data = parse_json_output(result.stdout)
    nb_id = (data or {}).get("notebook", {}).get("id") if data else None
    if not nb_id:
        nb_id = input("请手动输入 notebook ID: ").strip()

    # 2. 添加提示词文件
    result = run_step("添加提示词来源",
                     f'notebooklm source add "{prompts_file}" -n {nb_id} --json')
    data = parse_json_output(result.stdout)
    source_id = (data or {}).get("source", {}).get("id") if data else None
    if not source_id:
        source_id = input("请手动输入 source ID: ").strip()

    # 3. 等待源处理
    print("\n[INFO] 等待源处理完成（通常 30s - 2min）...")
    result = subprocess.run(
        f'notebooklm source wait {source_id} -n {nb_id} --timeout 120',
        shell=True, capture_output=True, text=True,
        env={**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    if result.returncode == 2:
        print("[WARN] 源处理超时，继续尝试生成...")
    elif result.returncode != 0:
        print("[WARN] 源处理异常，继续尝试生成...")

    # 4. 生成 slide deck
    result = run_step("生成 Slide Deck",
                     f'notebooklm generate slide-deck --format detailed -n {nb_id} --json')
    data = parse_json_output(result.stdout)
    artifact_id = (data or {}).get("task_id") if data else None
    if not artifact_id:
        artifact_id = input("请手动输入 artifact ID: ").strip()

    # 5. 等待生成完成（5-15分钟）
    print(f"\n[INFO] 等待 artifact {artifact_id} 完成（最多15分钟）...")
    result = subprocess.run(
        f'notebooklm artifact wait {artifact_id} -n {nb_id} --timeout 900',
        shell=True, capture_output=True, text=True,
        env={**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    if result.returncode == 2:
        print("[ERROR] 生成超时，请稍后检查 artifact list 并重试")
        print(f"  notebooklm artifact list -n {nb_id}")
        sys.exit(1)
    elif result.returncode != 0:
        print("[ERROR] 生成失败")
        sys.exit(1)

    # 6. 下载 PDF（文件名：{主题}_{时间戳}.pdf）
    run_step("下载 Slide Deck PDF",
             f'notebooklm download slide-deck "{pdf_raw}" -n {nb_id}')


def step3_watermark():
    """去除 NotebookLM 水印"""
    if "pdf_raw" not in PATHS or not PATHS["pdf_raw"].exists():
        print(f"[ERROR] 源 PDF 不存在")
        sys.exit(1)
    ensure_dir(PATHS["pdf_clean"].parent)
    run_step("去除水印",
            f'python "{SKILL_SCRIPTS["watermark"]}" "{PATHS["pdf_raw"]}" --output "{PATHS["pdf_clean"]}"')


def step4_pdf_to_images():
    """PDF 逐页转图片"""
    if not PATHS["pdf_clean"].exists():
        print(f"[ERROR] 无水印 PDF 不存在: {PATHS["pdf_clean"]}")
        sys.exit(1)
    ensure_dir(PATHS["pages_dir"])

    import importlib.util
    spec = importlib.util.spec_from_file_location("convert", SKILL_SCRIPTS["convert"])
    convert_mod = importlib.util.load_source("convert", str(spec.loader.load_module.__file__))
    convert_mod.convert_pdf_to_images(
        pdf_path=str(PATHS["pdf_clean"]),
        output_dir=str(PATHS["pages_dir"]),
        dpi=150, format="jpg", max_size_mb=5,
    )
    print("[OK] PDF 转逐页图片 完成")


def step5_layout():
    """小红书排版"""
    pages = list(PATHS["pages_dir"].glob("*.jpg")) + list(PATHS["pages_dir"].glob("*.png"))
    if not pages:
        print(f"[ERROR] 逐页图片目录为空: {PATHS["pages_dir"]}")
        sys.exit(1)

    page_count = len(pages)
    layout = "layout2" if page_count == 5 else "layout1"
    print(f"[INFO] 检测到 {page_count} 页，使用 {layout}")

    ensure_dir(PATHS["final_dir"])
    run_step("生成小红书排版图",
            f'python "{SKILL_SCRIPTS["layout"]}" "{PATHS["pages_dir"]}" -l {layout} -o "{PATHS["final_dir"]}"')


# -------------------------------------------------------------------
# 主程序
# -------------------------------------------------------------------

SKILL_SCRIPTS = {
    "watermark": Path.home() / ".claude/skills/dp-pdf-notebooklm-watermarkremover/scripts/download.py",
    "convert":   Path.home() / ".claude/skills/dp-pdf-to-images/scripts/convert.py",
    "layout":    Path.home() / ".claude/skills/dp-xhsppt-output_layout/ppt_layout.py",
}

def main():
    parser = argparse.ArgumentParser(description="NotebookLM PPT Pipeline")
    parser.add_argument("--start", choices=["2", "3", "4", "5"], default="2")
    parser.add_argument("--end", choices=["2", "3", "4", "5"], default="5")
    parser.add_argument("--topic", default=None, help="PPT 主题名称")
    parser.add_argument("--timestamp", default=None, help="时间戳 YYYYMMDD_HHMMSS")
    args = parser.parse_args()

    start = int(args.start)
    end = int(args.end)

    print("=" * 60)
    print("  PPT小红书笔记 — 自动化工作流")
    print(f"  执行步骤: {start} → {end}")
    print("=" * 60)

    steps = [
        ("2. NotebookLM生成PPT",  step2_notebooklm),
        ("3. 去除水印",            step3_watermark),
        ("4. PDF转逐页图片",        step4_pdf_to_images),
        ("5. 小红书排版",          step5_layout),
    ]

    for i, (name, fn) in enumerate(steps, 2):
        if i < start:
            print(f"[SKIP] {name}")
            continue
        if i > end:
            print(f"[STOP] {name} (end)")
            break
        if i == 2:
            fn(topic=args.topic, timestamp=args.timestamp)
        else:
            fn()

    print("\n" + "=" * 60)
    print("  全部完成！")
    print(f"  最终输出: {PATHS["final_dir"]}")
    print("=" * 60)


if __name__ == "__main__":
    main()
