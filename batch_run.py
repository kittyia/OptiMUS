#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

# 直接导入 main.py 中的函数
from main import run_optimization


def main():
    parser = argparse.ArgumentParser(description="批量运行测试脚本")

    parser.add_argument("--api_key", type=str, required=True,
                        help="API密钥")
    parser.add_argument("--base_url", type=str, required=True,
                        help="API基础URL")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-8B",
                        help="模型名称 (默认: Qwen/Qwen3-8B)")
    parser.add_argument("--base_dir", type=str, default="./data/nlp4lp",
                        help="数据基础目录 (默认: ./data/nlp4lp)")
    parser.add_argument("--devmode", type=int, default=1,
                        help="开发模式 (默认: 1)")

    args = parser.parse_args()

    print("开始批量测试...\n")
    print(f"API地址: {args.base_url}")
    print(f"模型: {args.model}")
    print(f"数据目录: {args.base_dir}")
    print(f"开发模式: {args.devmode}\n")

    base_dir = Path(args.base_dir)

    if not base_dir.exists():
        print(f"❌ 错误: 找不到数据目录 {base_dir}")
        return

    success = 0
    total = 0
    failed_folders = []

    for folder in sorted([f for f in base_dir.iterdir() if f.is_dir()]):
        # 检查必要文件
        if not (folder / "description.txt").exists() or not (folder / "converted_parameters.json").exists():
            continue

        total += 1
        print(f"[{total}] 测试: {folder.name}")

        try:
            # 直接调用函数，不用 subprocess！
            run_optimization(
                dir_path=str(folder.absolute()),
                api_key=args.api_key,
                base_url=args.base_url,
                model=args.model,
                devmode=args.devmode,
                rag_mode=None
            )
            print(f"  ✅ 成功\n")
            success += 1

        except Exception as e:
            print(f"  ❌ 失败: {str(e)[:100]}...\n")
            failed_folders.append(folder.name)

    # 输出统计
    print("=" * 60)
    print(f"完成: {success}/{total} 成功")
    if failed_folders:
        print(f"\n失败的文件夹: {', '.join(failed_folders)}")


if __name__ == "__main__":
    main()