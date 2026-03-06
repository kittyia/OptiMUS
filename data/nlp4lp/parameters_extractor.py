#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path


def load_problem_info(folder_path):
    """加载problem_info.json文件"""
    info_path = folder_path / "problem_info.json"
    if info_path.exists():
        try:
            with open(info_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None


def get_param_info(problem_info, param_name):
    """从problem_info中获取参数信息"""
    if problem_info and "parameters" in problem_info:
        return problem_info["parameters"].get(param_name)
    return None


def main():
    # 基础路径
    base = Path("./")

    if not base.exists():
        print(f"找不到目录: {base}")
        return

    # 找所有 parameters.json
    files = list(base.rglob("parameters.json"))
    print(f"找到 {len(files)} 个参数文件\n")

    # 转换
    success = 0
    for f in files:
        folder = f.parent
        try:
            # 读原文件
            with open(f, 'r', encoding='utf-8') as fp:
                old = json.load(fp)

            # 读同目录下的problem_info.json
            problem_info = load_problem_info(folder)
            if problem_info:
                print(f"📄 {folder.name}: 找到problem_info.json")
            else:
                print(f"⚠️ {folder.name}: 没有problem_info.json")

            # 转成新格式
            new = {}
            for key, val in old.items():
                # 转下划线

                # 从problem_info获取信息
                param_info = get_param_info(problem_info, key)

                # 判断形状
                if isinstance(val, list):
                    if val and isinstance(val[0], list):
                        shape = [len(val), len(val[0])]
                    else:
                        shape = [len(val)]
                else:
                    shape = []

                # 优先使用problem_info中的shape
                if param_info and "shape" in param_info:
                    shape = param_info["shape"]

                # 判断类型
                if isinstance(val, int):
                    vtype = 'int'
                elif isinstance(val, float):
                    vtype = 'float'
                else:
                    vtype = 'string'

                # 获取description
                if param_info and "description" in param_info:
                    description = param_info["description"]
                else:
                    description = key

                new[key] = {
                    "definition": description,
                    "shape": shape,
                    "type": vtype,
                    "value": val
                }

            # 保存
            out_path = folder / "converted_parameters.json"
            with open(out_path, 'w', encoding='utf-8') as fp:
                json.dump(new, fp, indent=2, ensure_ascii=False)

            print(f"✓ {folder.name} 转换成功")
            success += 1

        except Exception as e:
            print(f"✗ {folder.name} 出错: {e}")

    print(f"\n完成: {success}/{len(files)} 个文件转换成功")


if __name__ == "__main__":
    main()