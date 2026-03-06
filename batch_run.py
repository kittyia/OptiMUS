#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import argparse
from pathlib import Path


def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="批量运行测试脚本")

    parser.add_argument("--api_key", type=str, required=True,
                        help="API密钥")
    parser.add_argument("--base_url", type=str, required=True,
                        help="API基础URL")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-8B",
                        help="模型名称 (默认: Qwen/Qwen3-8B)")
    parser.add_argument("--base_dir", type=str, default="./data/nlp4lp",
                        help="数据基础目录 (默认: ./data/nlp4lp)")

    args = parser.parse_args()

    print("开始批量测试...\n")
    print(f"API地址: {args.base_url}")
    print(f"模型: {args.model}")
    print(f"数据目录: {args.base_dir}\n")

    python_exe = Path(__file__).parent / ".venv" / "Scripts" / "python.exe"
    main_script = Path(__file__).parent / "main.py"
    base_dir = Path(args.base_dir)

    if not python_exe.exists():
        print(f"❌ 错误: 找不到Python解释器 {python_exe}")
        return

    if not base_dir.exists():
        print(f"❌ 错误: 找不到数据目录 {base_dir}")
        return

    success = 0
    total = 0

    for folder in sorted([f for f in base_dir.iterdir() if f.is_dir()]):
        # 检查文件
        if not (folder / "description.txt").exists() or not (folder / "converted_parameters.json").exists():
            continue

        total += 1
        print(f"测试: {folder.name}")

        # 运行命令
        cmd = [
            str(python_exe), str(main_script),
            "--api_key", args.api_key,
            "--base_url", args.base_url,
            "--model", args.model,
            "--dir", str(folder.absolute())
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"  ✅ 成功\n")
            success += 1
        else:
            # 只显示错误的前几行
            error_lines = result.stderr.strip().split('\n')[:3]
            print(f"  ❌ 失败: {' '.join(error_lines)}...\n")

    print(f"\n完成: {success}/{total} 成功")


if __name__ == "__main__":
    main()