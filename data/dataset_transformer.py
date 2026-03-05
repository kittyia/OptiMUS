import json
import os
import re


def parse_multi_json_file(file_path):
    """
    解析包含多个独立JSON对象的文件（每个对象占一行）
    """
    problems = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # 跳过空行
                continue

            try:
                # 尝试解析每一行作为独立的JSON对象
                problem = json.loads(line)
                problems.append(problem)
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse line {line_num} in {file_path}: {e}")
                print(f"Line content: {line[:100]}...")  # 只显示前100个字符
                continue

    print(f"Successfully parsed {len(problems)} problems from {file_path}")
    return problems


def safe_json_parse(data):
    """
    安全地解析可能为字符串的JSON数据
    """
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {}
    return data if isinstance(data, (dict, list)) else {}


def ensure_dict(data):
    """
    确保数据是字典类型，如果是字符串则尝试解析
    """
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse string as JSON: {data[:100]}...")
            return {}
    return data if isinstance(data, dict) else {}


def transform_parameters(original_params):
    """
    将原始参数格式转换为目标格式
    原始格式: {"param_name": value}
    目标格式: {"param_name": {"definition": "...", "shape": [], "type": "...", "value": value}}
    """
    # 确保original_params是字典
    original_params = ensure_dict(original_params)

    transformed = {}

    for param_name, param_value in original_params.items():
        # 根据参数值推断类型
        if isinstance(param_value, bool):
            param_type = "bool"
        elif isinstance(param_value, int):
            param_type = "int"
        elif isinstance(param_value, float):
            param_type = "float"
        elif isinstance(param_value, str):
            param_type = "string"
        elif isinstance(param_value, list):
            param_type = "list"
            # 检查列表中的元素类型
            if param_value and all(isinstance(x, int) for x in param_value):
                param_type = "list[int]"
            elif param_value and all(isinstance(x, float) for x in param_value):
                param_type = "list[float]"
            elif param_value and all(isinstance(x, str) for x in param_value):
                param_type = "list[string]"
        elif isinstance(param_value, dict):
            param_type = "dict"
        else:
            param_type = "unknown"

        # 创建参数定义
        transformed[param_name] = {
            "definition": f"Parameter {param_name}",
            "shape": get_shape_from_value(param_value),
            "type": param_type,
            "value": param_value
        }

    return transformed


def get_shape_from_value(value):
    """
    根据参数值推断shape
    """
    if isinstance(value, (bool, int, float, str)) or value is None:
        return []
    elif isinstance(value, list):
        if not value:  # 空列表
            return [0]
        if isinstance(value[0], list):
            # 二维列表
            return [len(value), len(value[0]) if value[0] else 0]
        else:
            # 一维列表
            return [len(value)]
    elif isinstance(value, dict):
        # 对于字典，返回键的数量
        return [len(value)]
    else:
        return []


def determine_problem_type(problem_info):
    """
    根据问题信息判断问题类型（LP/MIP/NLP）
    """
    # 确保problem_info是字典
    problem_info = safe_json_parse(problem_info)

    if not isinstance(problem_info, dict):
        return 'Unknown'

    # 检查变量类型
    variables = problem_info.get('variables', {})
    variables = ensure_dict(variables)

    # 判断是否有整数变量
    has_integer = False
    if isinstance(variables, dict):
        for var_name, var_info in variables.items():
            # 确保var_info是字典
            var_info = ensure_dict(var_info)
            var_type = var_info.get('type', '').lower() if isinstance(var_info, dict) else ''
            if var_type in ['integer', 'binary']:
                has_integer = True
                break

    # 判断是否有非线性约束或目标
    has_nonlinear = False
    constraints = problem_info.get('constraints', [])
    if not isinstance(constraints, list):
        constraints = []

    objective = problem_info.get('objective', {})
    objective = ensure_dict(objective)

    # 检查约束中是否有非线性运算（如乘方、除法等）
    nonlinear_indicators = ['**', 'pow', '/', 'math.exp', 'math.log', '^', 'sqrt', 'math.sqrt', '**2', '**3']

    for constraint in constraints:
        # 确保constraint是字典
        constraint = ensure_dict(constraint)
        if not isinstance(constraint, dict):
            continue

        formulation = constraint.get('formulation', '')
        code = str(constraint.get('code', ''))
        for indicator in nonlinear_indicators:
            if indicator in formulation or indicator in code:
                has_nonlinear = True
                break
        if has_nonlinear:
            break

    # 检查目标中是否有非线性运算
    if not has_nonlinear and isinstance(objective, dict):
        obj_formulation = objective.get('formulation', '')
        obj_code = str(objective.get('code', ''))
        for indicator in nonlinear_indicators:
            if indicator in obj_formulation or indicator in obj_code:
                has_nonlinear = True
                break

    # 确定问题类型
    if has_nonlinear:
        return 'NLP'
    elif has_integer:
        return 'MIP'
    else:
        return 'LP'


def create_problem_folder(problem_data, folder_name, base_dir):
    """
    为单个问题创建文件夹和所需文件
    """
    # 确保problem_data是字典
    if isinstance(problem_data, str):
        try:
            problem_data = json.loads(problem_data)
        except json.JSONDecodeError:
            print(f"Error: Cannot parse problem data for {folder_name}")
            return 'Unknown'

    # 创建问题文件夹
    prob_dir = os.path.join(base_dir, folder_name)
    os.makedirs(prob_dir, exist_ok=True)

    # 写入desc.txt
    description = problem_data.get('description', 'No description available')
    with open(os.path.join(prob_dir, 'desc.txt'), 'w', encoding='utf-8') as f:
        f.write(description)

    # 获取原始参数并转换为目标格式
    original_params = problem_data.get('parameters', {})
    transformed_params = transform_parameters(original_params)

    # 写入params.json
    with open(os.path.join(prob_dir, 'params.json'), 'w', encoding='utf-8') as f:
        json.dump(transformed_params, f, indent=2, ensure_ascii=False)

    # 获取problem_info并确定问题类型
    problem_info = problem_data.get('problem_info', {})
    problem_type = determine_problem_type(problem_info)
    labels = {'problem_type': problem_type}

    # 写入labels.json
    with open(os.path.join(prob_dir, 'labels.json'), 'w', encoding='utf-8') as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)

    print(f"Created {folder_name}: {problem_type}")
    return problem_type


def convert_json_to_dataset(json_file, output_dir, prefix='prob'):
    """
    将JSON文件转换为数据集
    """
    # 解析包含多个JSON对象的文件（每行一个）
    problems = parse_multi_json_file(json_file)

    if not problems:
        print(f"Warning: No valid problems found in {json_file}")
        return 0

    print(f"\nProcessing {len(problems)} problems from {json_file}")

    # 统计问题类型
    type_stats = {'LP': 0, 'MIP': 0, 'NLP': 0, 'Unknown': 0}

    # 为每个问题创建文件夹
    for i, problem in enumerate(problems, 1):
        try:
            folder_name = f"{prefix}_{i}"
            problem_type = create_problem_folder(problem, folder_name, output_dir)
            type_stats[problem_type] = type_stats.get(problem_type, 0) + 1
        except Exception as e:
            print(f"Error processing problem {i}: {e}")
            type_stats['Unknown'] += 1

    # 打印统计信息
    print(f"\nProblem type statistics for {os.path.basename(json_file)}:")
    for ptype, count in type_stats.items():
        if count > 0:
            print(f"  {ptype}: {count}")

    return len(problems)


def create_dataset_structure(test_file, validation_file, output_base_dir='dataset'):
    """
    创建完整的数据集结构
    """
    # 创建基础输出目录
    os.makedirs(output_base_dir, exist_ok=True)

    # 处理test.json
    print("\n" + "=" * 50)
    print(f"Processing test file: {test_file}")
    print("=" * 50)
    test_dir = os.path.join(output_base_dir, 'test')
    os.makedirs(test_dir, exist_ok=True)
    test_count = convert_json_to_dataset(test_file, test_dir, prefix='test_prob')

    # 处理validation.json
    print("\n" + "=" * 50)
    print(f"Processing validation file: {validation_file}")
    print("=" * 50)
    val_dir = os.path.join(output_base_dir, 'validation')
    os.makedirs(val_dir, exist_ok=True)
    val_count = convert_json_to_dataset(validation_file, val_dir, prefix='val_prob')

    # 创建数据集信息文件
    dataset_info = {
        'test_count': test_count,
        'validation_count': val_count,
        'total_problems': test_count + val_count,
        'test_file': test_file,
        'validation_file': validation_file,
        'structure': {
            'test': 'test/',
            'validation': 'validation/'
        }
    }

    with open(os.path.join(output_base_dir, 'dataset_info.json'), 'w', encoding='utf-8') as f:
        json.dump(dataset_info, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 50)
    print("Dataset creation completed!")
    print("=" * 50)
    print(f"Output directory: {output_base_dir}")
    print(f"Test problems: {test_count}")
    print(f"Validation problems: {val_count}")
    print(f"Total problems: {test_count + val_count}")

    # 显示目录结构
    print("\nDirectory structure:")
    print(f"{output_base_dir}/")
    print("├── test/")
    for i in range(1, min(test_count + 1, 6)):
        print(f"│   ├── test_prob_{i}/")
        print(f"│   │   ├── desc.txt")
        print(f"│   │   ├── params.json")
        print(f"│   │   └── labels.json")
    if test_count > 5:
        print(f"│   │   ... (and {test_count - 5} more)")
    print("├── validation/")
    for i in range(1, min(val_count + 1, 6)):
        print(f"│   ├── val_prob_{i}/")
        print(f"│   │   ├── desc.txt")
        print(f"│   │   ├── params.json")
        print(f"│   │   └── labels.json")
    if val_count > 5:
        print(f"│   │   ... (and {val_count - 5} more)")
    print("└── dataset_info.json")


def main():
    # 配置文件路径
    test_file = './NLP4LP_original_format/test.json'
    validation_file = './NLP4LP_original_format/validation.json'
    output_dir = 'NLP4LP'

    # 检查输入文件是否存在
    if not os.path.exists(test_file):
        print(f"Error: {test_file} not found!")
        print("Please check the file path.")
        return

    if not os.path.exists(validation_file):
        print(f"Error: {validation_file} not found!")
        print("Please check the file path.")
        return

    # 创建数据集
    create_dataset_structure(test_file, validation_file, output_dir)

    # 打印使用说明
    print("\n" + "=" * 50)
    print("How to use with main.py:")
    print("=" * 50)
    print("# Run a single test problem:")
    print(f"python main.py --dir {output_dir}/test/test_prob_1 --model Qwen/Qwen3-8B")
    print("\n# Run a single validation problem:")
    print(f"python main.py --dir {output_dir}/validation/val_prob_1 --model Qwen/Qwen3-8B")
    print("\n# Batch run all test problems (Windows PowerShell):")
    print(
        f"Get-ChildItem {output_dir}/test | ForEach-Object {{ python main.py --dir $_.FullName --model Qwen/Qwen3-8B }}")
    print("\n# Batch run all validation problems (Windows PowerShell):")
    print(
        f"Get-ChildItem {output_dir}/validation | ForEach-Object {{ python main.py --dir $_.FullName --model Qwen/Qwen3-8B }}")


if __name__ == "__main__":
    main()