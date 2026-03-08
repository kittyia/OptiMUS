# # main.py 文件开头
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

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

# 设置环境变量
os.environ["API_KEY"] = args.api_key
os.environ["BASE_URL"] = args.base_url
os.environ["MODEL"] = args.model




import time
from pathlib import Path

from rag.rag_utils import RAGMode
from parameters import get_params
from constraint import get_constraints
from constraint_model import get_constraint_formulations
from target_code import get_codes
from generate_code import generate_code
from utils import load_state, save_state, Logger
from objective import get_objective
from objective_model import get_objective_formulation
from execute_code import execute_and_debug
from utils import create_state, get_labels


def run_optimization(dir_path, model="Qwen/Qwen3-8B",
                     devmode=1, rag_mode=None):
    """
    运行优化问题的主函数

    Args:
        dir_path: 问题数据目录
        api_key: API密钥
        base_url: API基础URL
        model: 模型名称
        devmode: 开发模式 (1 或 0)
        rag_mode: RAG模式
    """
    # 参数设置
    dir = dir_path
    DEV_MODE = devmode
    RAG_MODE = rag_mode
    ERROR_CORRECTION = True
    MODEL = model

    if DEV_MODE:
        run_dir = os.path.join(dir, f"run_dev")
    else:
        # Get git hash
        git_hash = os.popen("git rev-parse HEAD").read().strip()
        run_dir = os.path.join(dir, f"run_{time.strftime('%Y%m%d')}_{MODEL}_{git_hash}_RAG")

    if not os.path.exists(run_dir):
        os.makedirs(run_dir)

    state = create_state(dir, run_dir)
    labels = "None"
    save_state(state, os.path.join(run_dir, "state_1_params.json"))

    logger = Logger(f"{run_dir}/log.txt")
    logger.reset()

    # Get objective
    state = load_state(os.path.join(run_dir, "state_1_params.json"))
    objective = get_objective(
        state["description"],
        state["parameters"],
        check=ERROR_CORRECTION,
        logger=logger,
        model=MODEL,
        rag_mode=RAG_MODE,
        labels=labels,
    )
    print(objective)
    state["objective"] = objective
    save_state(state, os.path.join(run_dir, "state_2_objective.json"))

    # Get constraints
    state = load_state(os.path.join(run_dir, "state_2_objective.json"))
    constraints = get_constraints(
        state["description"],
        state["parameters"],
        check=ERROR_CORRECTION,
        logger=logger,
        model=MODEL,
        rag_mode=RAG_MODE,
        labels=labels,
    )
    print(constraints)
    state["constraints"] = constraints
    save_state(state, os.path.join(run_dir, "state_3_constraints.json"))

    # Get constraint formulations
    state = load_state(os.path.join(run_dir, "state_3_constraints.json"))
    constraints, variables = get_constraint_formulations(
        state["description"],
        state["parameters"],
        state["constraints"],
        check=ERROR_CORRECTION,
        logger=logger,
        model=MODEL,
        rag_mode=RAG_MODE,
        labels=labels,
    )
    state["constraints"] = constraints
    state["variables"] = variables
    save_state(state, os.path.join(run_dir, "state_4_constraints_modeled.json"))

    # Get objective formulation
    state = load_state(os.path.join(run_dir, "state_4_constraints_modeled.json"))
    objective = get_objective_formulation(
        state["description"],
        state["parameters"],
        state["variables"],
        state["objective"],
        model=MODEL,
        check=ERROR_CORRECTION,
        rag_mode=RAG_MODE,
        labels=labels,
    )
    state["objective"] = objective
    print("DONE OBJECTIVE FORMULATION")
    save_state(state, os.path.join(run_dir, "state_5_objective_modeled.json"))

    # Get codes
    state = load_state(os.path.join(run_dir, "state_5_objective_modeled.json"))
    constraints, objective = get_codes(
        state["description"],
        state["parameters"],
        state["variables"],
        state["constraints"],
        state["objective"],
        model=MODEL,
        check=ERROR_CORRECTION,
    )
    state["constraints"] = constraints
    state["objective"] = objective
    save_state(state, os.path.join(run_dir, "state_6_code.json"))

    # Run the code
    state = load_state(os.path.join(run_dir, "state_6_code.json"))
    generate_code(state, run_dir)
    execute_and_debug(state, model=MODEL, dir=run_dir, logger=logger)

    return True


def main():
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
