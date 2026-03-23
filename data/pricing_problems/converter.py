#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Tuple


def infer_type_and_shape(value: Any) -> Tuple[str, list]:
    if isinstance(value, bool):
        return "bool", []
    if isinstance(value, int):
        return "int", []
    if isinstance(value, float):
        return "float", []
    if isinstance(value, str):
        return "string", []
    if isinstance(value, list):
        if not value:
            return "list", [0]
        if all(isinstance(x, int) for x in value):
            return "list[int]", [len(value)]
        if all(isinstance(x, (int, float)) for x in value):
            return "list[float]", [len(value)]
        if all(isinstance(x, str) for x in value):
            return "list[string]", [len(value)]
        return "list", [len(value)]
    if isinstance(value, dict):
        return "dict", [len(value)]
    return "unknown", []


def to_converted_parameters(structured: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    params = {}
    raw_params = structured.get("parameters", {})
    if not isinstance(raw_params, dict):
        return params

    for name, meta in raw_params.items():
        if isinstance(meta, dict) and "value" in meta:
            value = meta.get("value")
            definition = meta.get("description", f"Parameter {name}")
        else:
            # 兼容非标准格式：parameters 直接给值
            value = meta
            definition = f"Parameter {name}"

        typ, shape = infer_type_and_shape(value)
        params[name] = {
            "definition": definition,
            "shape": shape,
            "type": typ,
            "value": value,
        }
    return params


def to_description(structured: Dict[str, Any], source_name: str) -> str:
    problem_id = structured.get("problem_id", source_name)
    ptype = structured.get("problem_type", {}) if isinstance(structured.get("problem_type", {}), dict) else {}
    pclass = ptype.get("class", "Unknown")
    domain = ptype.get("domain", "Unknown")

    objective = structured.get("objective", {}) if isinstance(structured.get("objective", {}), dict) else {}
    obj_sense = objective.get("sense", "maximize")
    obj_expr = objective.get("expression", "")

    constraints = structured.get("constraints", [])
    if not isinstance(constraints, list):
        constraints = []

    variables = structured.get("variables", {})

    lines = [
        f"PROBLEM ID: {problem_id}",
        f"PROBLEM TYPE: {pclass}",
        f"DOMAIN: {domain}",
        "",
        "PROBLEM INFO:",
        "- This problem is converted from a structured JSON instance.",
        "- Parameters are provided in converted_parameters.json.",
        "",
        "VARIABLES:",
    ]

    # 兼容 variables 为 dict/list 两种格式
    if isinstance(variables, dict) and variables:
        for vname, vmeta in variables.items():
            if isinstance(vmeta, dict):
                vtype = vmeta.get("type", "unknown")
                vdesc = vmeta.get("description", "")
                vshape = vmeta.get("shape", None)
                detail = f"type={vtype}"
                if vshape is not None:
                    detail += f", shape={vshape}"
                if vdesc:
                    detail += f", desc={vdesc}"
                lines.append(f"- {vname}: {detail}")
            else:
                lines.append(f"- {vname}")
    elif isinstance(variables, list) and variables:
        for item in variables:
            if isinstance(item, dict):
                vname = item.get("name", "unknown_var")
                vtype = item.get("type", "unknown")
                vdesc = item.get("description", "")
                detail = f"type={vtype}"
                if vdesc:
                    detail += f", desc={vdesc}"
                lines.append(f"- {vname}: {detail}")
            else:
                lines.append(f"- {item}")
    else:
        lines.append("- No explicit variables provided.")

    lines.extend(
        [
            "",
            "OBJECTIVE:",
            f"- Sense: {obj_sense}",
            f"- Expression: {obj_expr}",
            "",
            "CONSTRAINTS:",
        ]
    )

    if constraints:
        for c in constraints:
            if not isinstance(c, dict):
                continue
            cid = c.get("id", "unknown_constraint")
            cexpr = c.get("expression", "")
            lines.append(f"- [{cid}] {cexpr}")
    else:
        lines.append("- No explicit constraints provided.")

    lines.extend(
        [
            "",
            "TASK:",
            "Build and solve the corresponding optimization model.",
            "",
        ]
    )
    return "\n".join(lines)


def convert_one_file(json_path: Path, output_root: Path) -> Tuple[bool, str]:
    folder_name = json_path.stem
    out_dir = output_root / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        with json_path.open("r", encoding="utf-8") as f:
            structured = json.load(f)
    except Exception as e:
        return False, f"读取失败: {json_path.name} ({e})"

    if not isinstance(structured, dict):
        return False, f"格式错误: {json_path.name} 顶层不是 JSON object"

    description = to_description(structured, json_path.stem)
    converted_params = to_converted_parameters(structured)

    desc_path = out_dir / "description.txt"
    params_path = out_dir / "converted_parameters.json"

    with desc_path.open("w", encoding="utf-8") as f:
        f.write(description)

    with params_path.open("w", encoding="utf-8") as f:
        json.dump(converted_params, f, indent=2, ensure_ascii=False)

    return True, f"已转换: {json_path.name} -> {out_dir.name}/"


def list_json_files(input_dir: Path, recursive: bool) -> list[Path]:
    pattern = "**/*.json" if recursive else "*.json"
    files = [p for p in input_dir.glob(pattern) if p.is_file()]
    # 避免误处理输出文件
    excluded = {"converted_parameters.json"}
    files = [p for p in files if p.name not in excluded]
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="批量转换 pricing_problems 下结构化 JSON 为 OptiMUS 输入目录。"
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        default="./",
        help="输入目录（默认: ./）",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="输出根目录（默认与 input_dir 相同）",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="是否递归扫描子目录中的 JSON",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else input_dir

    if not input_dir.exists():
        print(f"错误: 输入目录不存在: {input_dir}")
        return

    json_files = list_json_files(input_dir, recursive=args.recursive)

    if not json_files:
        print(f"未找到 JSON 文件: {input_dir}")
        return

    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"共发现 {len(json_files)} 个 JSON 文件\n")

    ok_count = 0
    fail_count = 0

    for jf in json_files:
        # 避免把已经转换后的子目录里的 JSON 再次当作原始题目处理（递归模式下）
        if jf.parent != input_dir and (jf.parent / "description.txt").exists():
            continue

        ok, msg = convert_one_file(jf, output_dir)
        if ok:
            ok_count += 1
            print(f"✅ {msg}")
        else:
            fail_count += 1
            print(f"❌ {msg}")

    print("\n" + "=" * 60)
    print(f"完成: 成功 {ok_count}，失败 {fail_count}")


if __name__ == "__main__":
    main()
