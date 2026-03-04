# OptiMUS 项目整体框架解析

## 你的理解总结

你说的是：
```
问题描述 → 结构化(约束+目标+参数) → 数学建模 → 生成代码 → 求解+修复循环
```

## ✅ 你的理解是对的，但不够完整

让我用 `main.py` 的代码逐步验证：

---

## 完整的 7 个处理步骤

### 【步骤 1】初始化 - 问题结构化

```python
# 第 43-46 行
state = create_state(dir, run_dir)
# 从 desc.txt 和 params.json 读取
# state = {
#     "description": "问题描述",
#     "parameters": {参数定义}
# }
```

**输入：** `desc.txt`（自然语言）+ `params.json`（参数定义）

**输出：** 初始 state（包含问题描述和参数定义）

---

### 【步骤 2】提取目标函数

```python
# 第 51-60 行
objective = get_objective(
    state["description"],
    state["parameters"],
    ...
)
state["objective"] = objective
save_state(state, "state_2_objective.json")
```

**输入：** 问题描述 + 参数定义

**LLM 工作：**
1. 分析问题描述
2. 识别优化目标（最大化/最小化什么）
3. 返回目标描述

**输出：** 目标函数（仅自然语言描述）
```python
objective = {
    "description": "最大化周总利润",
    "formulation": None,  # ← 还没有数学化
    "code": None          # ← 还没有代码
}
```

---

### 【步骤 3】提取约束条件

```python
# 第 62-72 行
constraints = get_constraints(
    state["description"],
    state["parameters"],
    ...
)
state["constraints"] = constraints
save_state(state, "state_3_constraints.json")
```

**输入：** 问题描述 + 参数定义

**LLM 工作：**
1. 分析问题描述
2. 识别所有约束条件
3. 返回约束列表

**输出：** 约束条件（仅自然语言描述）
```python
constraints = [
    {"description": "木材限制：...", "formulation": None, "code": None},
    {"description": "劳动力限制：...", "formulation": None, "code": None},
    {"description": "最少订单量：...", "formulation": None, "code": None},
]
```

---

### 【步骤 4】对约束进行数学建模

```python
# 第 74-85 行
constraints, variables = get_constraint_formulations(
    state["description"],
    state["parameters"],
    state["constraints"],  # ← 输入之前提取的约束
    ...
)
state["constraints"] = constraints
state["variables"] = variables
save_state(state, "state_4_constraints_modeled.json")
```

**输入：** 问题描述 + 参数 + 约束描述

**LLM 工作（对每个约束逐一处理）：**
1. 根据约束描述生成数学公式
2. 定义可能需要的新变量
3. 生成可能需要的辅助约束

**输出：** 数学化的约束 + 定义的变量
```python
constraints = [
    {
        "description": "木材限制：...",
        "formulation": "$5 \times x_{chair} + 20 \times x_{table} \leq 1000$",  # ← 已数学化
        "code": None
    },
    ...
]

variables = {
    "x_chair": {"shape": [], "type": "integer", ...},
    "x_table": {"shape": [], "type": "integer", ...},
}
```

---

### 【步骤 5】对目标函数进行数学建模

```python
# 第 87-95 行
objective = get_objective_formulation(
    state["description"],
    state["parameters"],
    state["variables"],      # ← 使用之前定义的变量
    state["objective"],      # ← 输入之前提取的目标
    ...
)
state["objective"] = objective
save_state(state, "state_5_objective_modeled.json")
```

**输入：** 问题描述 + 参数 + 变量 + 目标描述

**LLM 工作：**
1. 根据目标描述和定义的变量生成数学公式

**输出：** 数学化的目标函数
```python
objective = {
    "description": "最大化周总利润",
    "formulation": "$\max 50 \times x_{chair} + 80 \times x_{table}$",  # ← 已数学化
    "code": None
}
```

---

### 【步骤 6】生成求解代码

```python
# 第 97-108 行
constraints, objective = get_codes(
    state["description"],
    state["parameters"],
    state["variables"],
    state["constraints"],    # ← 输入已数学化的约束
    state["objective"],      # ← 输入已数学化的目标
    ...
)
state["constraints"] = constraints
state["objective"] = objective
save_state(state, "state_6_code.json")
```

**输入：** 问题描述 + 参数 + 变量 + 数学化的约束 + 数学化的目标

**LLM 工作：**
1. 根据数学公式生成 Python 代码（使用 PuLP 求解器库）
2. 为每个约束生成 Python 代码
3. 为目标函数生成 Python 代码

**输出：** 可执行的 Python 代码
```python
objective = {
    "description": "最大化周总利润",
    "formulation": "$...$",
    "code": "model.setObjective(..., GRB.MAXIMIZE)"  # ← 已生成代码
}

constraints = [
    {
        "description": "木材限制",
        "formulation": "$...$",
        "code": "model.addConstr(5*x_chair + 20*x_table <= 1000, 'wood')"
    }
]
```

---

### 【步骤 7】执行代码 + 调试循环

```python
# 第 110-113 行
generate_code(state, run_dir)           # 生成 solution.py 文件
execute_and_debug(state, model=MODEL, dir=run_dir, logger=logger)
# ← 执行代码，如果出错则自动修复（循环重试）
```

**工作流程：**
```
execute_and_debug() 内部：

while 尝试次数 < 最大尝试次数:
    try:
        执行生成的 solution.py
        如果成功：
            ✅ 返回最优解结果
    except 代码执行错误:
        ❌ 捕获错误
        调用 LLM 修复代码
        重新尝试 (max_tries = 10)
```

**输出：** 求解结果 (solution_output.json)
```json
{
    "status": "Optimal",
    "objective_value": 4400,
    "solution": {
        "x_chair": 40,
        "x_table": 30
    }
}
```

---

## 完整流程图

```
【输入】
  desc.txt (自然语言描述)
  params.json (参数定义)

         ↓

【Step 1】初始化
  state = {"description": ..., "parameters": ...}

         ↓

【Step 2】提取目标 (get_objective)
  LLM: 分析→识别→输出目标描述
  objective = {"description": "最大化...", "formulation": None, "code": None}

         ↓

【Step 3】提取约束 (get_constraints)
  LLM: 分析→识别→输出约束列表
  constraints = [{"description": "...", "formulation": None, "code": None}, ...]

         ↓

【Step 4】约束数学建模 (get_constraint_formulations)
  LLM: 对每个约束→数学化→生成新变量
  constraints = [{"description": "...", "formulation": "$...$", ...}, ...]
  variables = {"x_chair": {...}, "x_table": {...}, ...}

         ↓

【Step 5】目标数学建模 (get_objective_formulation)
  LLM: 数学化目标函数
  objective = {"description": "...", "formulation": "$...$", ...}

         ↓

【Step 6】生成代码 (get_codes)
  LLM: 根据数学公式→生成 Python 代码
  objective = {"...", "code": "model.setObjective(...)"}
  constraints = [{"...", "code": "model.addConstr(...)"}, ...]

         ↓

【Step 7】执行 + 调试循环 (execute_and_debug)
  while 尝试次数 < max_tries:
    执行代码
    if 成功:
      ✅ 返回最优解
    else:
      ❌ LLM 修复错误
      重新尝试

         ↓

【输出】
  solution_output.json (最优解结果)
```

---

## 与你的总结对比

| 你的理解 | 实际情况 |
|---------|---------|
| 结构化 | ✅ Step 1-3：提取目标、约束、参数 |
| 数学建模 | ✅ Step 4-5：对约束和目标进行数学化 |
| 生成代码 | ✅ Step 6：LLM 生成 Python 代码 |
| 求解+修复循环 | ✅ Step 7：execute_and_debug 中的循环重试 |

---

## 关键补充：你遗漏的部分

### 1. **多层次的处理**
你的理解：`结构化 → 建模 → 代码 → 循环`

**实际：** 结构化分成 3 步
- Step 1: 初始化（读取输入）
- Step 2: 提取目标（自然语言 → 目标描述）
- Step 3: 提取约束（自然语言 → 约束描述）

然后建模分成 2 步
- Step 4: 约束建模（描述 → 数学公式 + 新变量）
- Step 5: 目标建模（描述 → 数学公式）

### 2. **参数始终参与**
每个 LLM 调用都会输入参数定义，帮助 LLM 理解有哪些数据可用。

### 3. **状态链传递**
每一步都会保存中间状态（state_1.json → state_2.json → ... → state_6.json），这样：
- 可以断点恢复
- 可以逐步调试
- 可以追踪每一步的输出

### 4. **调试循环是最后一步**
前 6 步都是用 LLM 逐步构建模型，最后第 7 步才进入"执行-修复-重试"的循环。

---

## 总结

你的理解框架**95% 正确**，但更准确的说法是：

```
自然语言输入
    ↓
【结构化】 Step 1-3: 提取目标、约束、参数定义
    ↓
【数学建模】 Step 4-5: 约束和目标数学化
    ↓
【代码生成】 Step 6: 生成 Python/Gurobi 代码
    ↓
【执行+调试】 Step 7: 执行→如果出错→LLM 修复→重试（循环，最多 10 次）
    ↓
最优解结果
```

**关键词：** 7 步流程，不是你理解的 4 步，但整体思路是对的。

