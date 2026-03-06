#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
from pathlib import Path

# 配置
API_KEY = "*********"
BASE_URL = "https://1yvxf19722895.vicp.fun/v1"
MODEL = "Qwen/Qwen3-8B"
BASE_DIR = Path("./data/nlp4lp")


def main():
    print("开始批量测试...\n")

    python_exe = Path(__file__).parent / ".venv" / "Scripts" / "python.exe"
    main_script = Path(__file__).parent / "main.py"

    success = 0
    total = 0

    for folder in sorted([f for f in BASE_DIR.iterdir() if f.is_dir()]):
        # 检查文件
        if not (folder / "description.txt").exists() or not (folder / "converted_parameters.json").exists():
            continue

        total += 1
        print(f"测试: {folder.name}")

        # 运行命令
        cmd = [
            str(python_exe), str(main_script),
            "--api_key", API_KEY, "--base_url", BASE_URL,
            "--model", MODEL, "--dir", str(folder.absolute())
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"  ✅ 成功\n")
            success += 1
        else:
            print(f"  ❌ 失败: {result.stderr[:100]}...\n")

    print(f"\n完成: {success}/{total} 成功")


if __name__ == "__main__":
    main()