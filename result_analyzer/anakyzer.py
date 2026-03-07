#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from pathlib import Path

BASE_DIR = Path("../data/nlp4lp")


def extract_optimal_value(text):
    """从code_output.txt中提取Optimal Objective Value数值"""
    match = re.search(r"Optimal Objective Value:\s*([\d.]+)", text)
    return float(match.group(1)) if match else None


def analyze_error_type(text):
    """分析建模错误的类型"""
    if "Model has 0 linear objective coefficients" in text:
        return "缺少目标函数"
    else:
        return "其他错误"


def main():
    # 统计变量
    total = 0
    no_code_output = 0
    correct = 0
    modeling_error = 0

    # 错误类型统计
    error_types = {
        "缺少目标函数": 0,
        "其他错误": 0
    }

    print("开始分析...\n")

    for folder in sorted([f for f in BASE_DIR.iterdir() if f.is_dir()]):
        # 检查run_dev文件夹
        run_dev = folder / "run_dev"
        if not run_dev.exists():
            print(f"  ⚠️  {folder.name}: 缺少run_dev文件夹")
            continue

        # 查找solution_***.json文件
        solution_files = list(folder.glob("solution*.json"))
        if not solution_files:
            continue

        total += 1
        print(f"[{total}] 分析: {folder.name}")

        # 检查code_output.txt
        code_output = run_dev / "code_output.txt"
        if not code_output.exists():
            print(f"  ⚠️  缺少code_output.txt")
            no_code_output += 1
            continue

        # 读取code_output.txt
        with open(code_output, 'r') as f:
            output_text = f.read()

        # 提取计算结果
        result_value = extract_optimal_value(output_text)
        if result_value is None:
            print(f"  ⚠️  无法提取Optimal Objective Value")
            no_code_output += 1
            continue

        # 读取solution.json
        solution_file = solution_files[0]  # 取第一个
        with open(solution_file, 'r') as f:
            solution = json.load(f)

        # 提取参考结果
        reference_value = solution.get("objective")
        if reference_value is None:
            print(f"  ⚠️  solution.json中没有objective字段")
            modeling_error += 1
            error_types["其他错误"] += 1
            continue

        # 计算差异
        if reference_value == 0:
            diff_percent = abs(result_value - reference_value)
        else:
            diff_percent = abs(result_value - reference_value) / abs(reference_value) * 100

        print(f"  计算结果: {result_value}")
        print(f"  参考结果: {reference_value}")
        print(f"  差异: {diff_percent:.2f}%")

        if diff_percent <= 1.0:
            print(f"  ✅ 正确")
            correct += 1
        else:
            print(f"  ❌ 建模错误")
            modeling_error += 1

            # 分析错误类型
            error_type = analyze_error_type(output_text)
            error_types[error_type] += 1
            print(f"     错误类型: {error_type}")

        print()

    # 输出统计
    print("=" * 60)
    print("分析完成")
    print("=" * 60)
    print(f"总数据实例: {total}")
    print(f"✅ 正确: {correct}")
    print(f"❌ 建模错误: {modeling_error}")
    print(f"⚠️  代码执行错误: {no_code_output}")

    if modeling_error > 0:
        print("\n📊 建模错误类型分布:")
        for error_type, count in error_types.items():
            if count > 0:
                percentage = count / modeling_error * 100
                print(f"  • {error_type}: {count} ({percentage:.1f}%)")

    if total > 0:
        print(f"\n正确率: {correct / total * 100:.1f}%")


if __name__ == "__main__":
    main()