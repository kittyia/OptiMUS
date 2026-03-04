"""
完整示例：OptiMUS v0.3 使用指南

演示如何从纯自然语言问题直接生成优化模型
"""

# ============================================================================
# 示例：家具生产问题
# ============================================================================

# 文件 1：desc.txt （纯自然语言）
# ============================================================================

DESC_TXT_CONTENT = """
A furniture manufacturing company needs to plan their weekly production.

The company produces two products:
1. Chairs - can be sold for $50 each
2. Tables - can be sold for $80 each

Production Constraints:
- Each chair requires 5 pounds of wood and 2 hours of labor
- Each table requires 20 pounds of wood and 6 hours of labor
- The company has 1000 pounds of wood available per week
- The company has 240 hours of labor available per week
- The company must produce at least 10 chairs per week to meet minimum orders
- The company can produce at most 30 tables per week due to market demand
- Both production quantities must be non-negative

Business Goal:
Maximize the total weekly profit from selling chairs and tables.
"""

# 文件 2：params.json （参数定义 + 具体值）
# ============================================================================

PARAMS_JSON_CONTENT = {
    "profit_chair": {
        "definition": "Profit per unit of chair",
        "shape": [],
        "type": "float",
        "value": 50
    },
    "profit_table": {
        "definition": "Profit per unit of table",
        "shape": [],
        "type": "float",
        "value": 80
    },
    "wood_per_chair": {
        "definition": "Wood required per chair (in pounds)",
        "shape": [],
        "type": "float",
        "value": 5
    },
    "wood_per_table": {
        "definition": "Wood required per table (in pounds)",
        "shape": [],
        "type": "float",
        "value": 20
    },
    "labor_per_chair": {
        "definition": "Labor hours required per chair",
        "shape": [],
        "type": "float",
        "value": 2
    },
    "labor_per_table": {
        "definition": "Labor hours required per table",
        "shape": [],
        "type": "float",
        "value": 6
    },
    "total_wood": {
        "definition": "Total available wood (in pounds)",
        "shape": [],
        "type": "int",
        "value": 1000
    },
    "total_labor": {
        "definition": "Total available labor hours",
        "shape": [],
        "type": "int",
        "value": 240
    },
    "min_chairs": {
        "definition": "Minimum demand for chairs",
        "shape": [],
        "type": "int",
        "value": 10
    },
    "max_tables": {
        "definition": "Maximum demand for tables",
        "shape": [],
        "type": "int",
        "value": 30
    }
}

# 文件 3：labels.json （问题标签 - 可选）
# ============================================================================

LABELS_JSON_CONTENT = {
    "types": ["Mathematical Optimization", "Linear Programming"],
    "domains": ["Production Planning", "Operations Management"]
}

# ============================================================================
# 使用步骤
# ============================================================================

USAGE_STEPS = """
步骤 1：创建目录
-------
mkdir furniture_problem
cd furniture_problem

步骤 2：创建 desc.txt
-------
（将 DESC_TXT_CONTENT 的内容保存到 desc.txt）

步骤 3：创建 params.json
-------
（将 PARAMS_JSON_CONTENT 转为 JSON 保存到 params.json）

步骤 4：创建 labels.json
-------
（将 LABELS_JSON_CONTENT 转为 JSON 保存到 labels.json）

步骤 5：运行 OptiMUS
-------
cd ..
python main.py --dir furniture_problem --devmode 1

步骤 6：查看结果
-------
furniture_problem/run_dev/
├── state_1_params.json           # 提取的参数
├── state_2_objective.json        # 提取的目标函数
├── state_3_constraints.json      # 提取的约束
├── state_4_constraints_modeled.json  # 数学化的约束
├── state_5_objective_modeled.json    # 数学化的目标
├── state_6_code.json             # 生成的代码
├── solution.py                   # Python 求解代码
├── solution_output.json          # 求解结果
└── params.json                     # 参数数值
"""

# ============================================================================
# 系统会自动做的事情
# ============================================================================

SYSTEM_WORKFLOW = """
您输入：
    desc.txt (纯自然语言)
    params.json (参数和数值)

系统自动执行：

1. create_state()
   ├─ 读取 desc.txt
   ├─ 读取 params.json 中的参数定义和值
   └─ 输出：state_1_params.json

2. get_objective() [LLM]
   ├─ 分析自然语言描述
   ├─ 识别目标函数
   └─ 输出：state_2_objective.json

3. get_constraints() [LLM]
   ├─ 分析自然语言描述
   ├─ 识别所有约束条件
   └─ 输出：state_3_constraints.json

4. get_constraint_formulations() [LLM]
   ├─ 将约束转为数学公式 (LaTeX)
   ├─ 识别新增变量
   └─ 输出：state_4_constraints_modeled.json

5. get_objective_formulation() [LLM]
   ├─ 将目标转为数学公式 (LaTeX)
   └─ 输出：state_5_objective_modeled.json

6. get_codes() [LLM]
   ├─ 生成 Python + PuLP 代码
   └─ 输出：state_6_code.json

7. generate_code()
   ├─ 保存生成的代码为 solution.py
   └─ 准备执行

8. execute_and_debug()
   ├─ 执行 solution.py
   ├─ 调试错误
   └─ 输出：solution_output.json (求解结果)

最终输出：
    solution.py - 可执行的优化模型代码
    solution_output.json - 最优解和目标值
"""

# ============================================================================
# 输出示例
# ============================================================================

EXPECTED_OUTPUT_EXAMPLE = """
最终生成的 solution.py 会包含类似的代码：

from pulp import *

# 读取参数
profit_chair = 50
profit_table = 80
wood_per_chair = 5
wood_per_table = 20
labor_per_chair = 2
labor_per_table = 6
total_wood = 1000
total_labor = 240
min_chairs = 10
max_tables = 30

# 定义问题
problem = LpProblem("Furniture_Production", LpMaximize)

# 定义变量
x_chair = LpVariable("x_chair", lowBound=0, cat='Integer')
x_table = LpVariable("x_table", lowBound=0, cat='Integer')

# 目标函数
problem += profit_chair * x_chair + profit_table * x_table

# 约束
problem += wood_per_chair * x_chair + wood_per_table * x_table <= total_wood
problem += labor_per_chair * x_chair + labor_per_table * x_table <= total_labor
problem += x_chair >= min_chairs
problem += x_table <= max_tables

# 求解
problem.solve()

# 输出结果
print(f"Status: {LpStatus[problem.status]}")
print(f"Chairs: {x_chair.varValue}")
print(f"Tables: {x_table.varValue}")
print(f"Total Profit: {value(problem.objective)}")

---

最终输出（solution_output.json）：
{
  "status": "Optimal",
  "objective_value": 4400,
  "solution": {
    "x_chair": 40,
    "x_table": 30
  }
}
"""

# ============================================================================
# 与 agents/ 版本的区别
# ============================================================================

VERSION_COMPARISON = """
OptiMUS v0.3 (optimus_tools.py) vs OptiMUS v2 (agents/)

入口：
    v0.3: main.py, optimus_tools.py
    v2: run.py, agents/manager.py

输入：
    v0.3: desc.txt + params.json
    v2: desc.txt + params.json

需要手动提供：
    v0.3: ❌ 不需要（LLM 自动提取）
    v2: ✅ 需要（background, parameters, constraints, objective）

处理方式：
    v0.3: 顺序工作流
    v2: Agent 协作系统

适用场景：
    v0.3: 小到中等规模问题，自动化程度高
    v2: 大型复杂问题，Agent 可协作修正

论文：
    v0.3: OptiMUS-0.3 (2407.19633)
    v2: OptiMUS v2 (2402.10172)
"""

if __name__ == "__main__":
    import json

    print("=" * 80)
    print("OptiMUS v0.3 完整使用指南")
    print("=" * 80)

    print("\n【输入文件 1】desc.txt")
    print("-" * 80)
    print(DESC_TXT_CONTENT)

    print("\n【输入文件 2】params.json")
    print("-" * 80)
    print(json.dumps(PARAMS_JSON_CONTENT, indent=2))

    print("\n【输入文件 3】labels.json")
    print("-" * 80)
    print(json.dumps(LABELS_JSON_CONTENT, indent=2))

    print("\n【使用步骤】")
    print("-" * 80)
    print(USAGE_STEPS)

    print("\n【系统工作流】")
    print("-" * 80)
    print(SYSTEM_WORKFLOW)

    print("\n【预期输出】")
    print("-" * 80)
    print(EXPECTED_OUTPUT_EXAMPLE)

    print("\n【版本对比】")
    print("-" * 80)
    print(VERSION_COMPARISON)

