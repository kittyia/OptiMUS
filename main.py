import os
import time
import json
import argparse

# Parse CLI args early so we can set OpenAI-related env vars before importing modules
parser = argparse.ArgumentParser(description="Run the optimization problem")
parser.add_argument("--dir", type=str, help="Directory of the problem")
parser.add_argument("--devmode", type=int, default=1)
parser.add_argument("--rag-mode", type=str, default=None, help="RAG mode (name or value)")
parser.add_argument("--openai-api-key", "-k", type=str, default=None, help="OpenAI API key")
parser.add_argument("--openai-api-base", "-b", type=str, default=None, help="OpenAI API base URL")
parser.add_argument("--model-name", "-m", type=str, default=None, help="Model name to use")
args = parser.parse_args()

# If provided on the CLI, override environment variables (this makes CLI take precedence over .env)
if args.openai_api_key:
    os.environ["OPENAI_API_KEY"] = args.openai_api_key
if args.openai_api_base:
    os.environ["OPENAI_API_BASE"] = args.openai_api_base
if args.model_name:
    os.environ["MODEL_NAME"] = args.model_name

# Now import the rest of the application (these modules may read env vars at import-time)
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
from rag.rag_utils import RAGMode


# Convert rag-mode CLI arg (string) to the enum if provided
_selected_rag_mode = None
if args.rag_mode is not None:
    # Try by name first, then by integer value
    try:
        _selected_rag_mode = RAGMode[args.rag_mode]
    except Exception:
        try:
            _selected_rag_mode = RAGMode(int(args.rag_mode))
        except Exception:
            _selected_rag_mode = None


if __name__ == "__main__":

    dir = args.dir
    # Read the params state
    ########## SET THIS BEFORE RUNNING! ##########
    DEV_MODE = args.devmode
    RAG_MODE = _selected_rag_mode
    ERROR_CORRECTION = True
    MODEL = os.environ.get("MODEL_NAME", "Qwen/Qwen3-8B")
    # MODEL = "llama3-70b-8192"
    ##############################################

    if DEV_MODE:
        run_dir = os.path.join(dir, f"run_dev")
    else:
        # Get git hash
        git_hash = os.popen("git rev-parse HEAD").read().strip()
        run_dir = os.path.join(dir, f"run_{time.strftime('%Y%m%d')}_{MODEL}_{git_hash}_RAG")

    if not os.path.exists(run_dir):
        os.makedirs(run_dir)

    state = create_state(dir, run_dir)
    labels = get_labels(dir)
    save_state(state, os.path.join(run_dir, "state_1_params.json"))

    logger = Logger(f"{run_dir}/log.txt")
    logger.reset()
    
    # # ###### Get objective
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
    # #######
    # # # ####### Get constraints
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
    # # # #######
    # ####### Get constraint formulations
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
    #######
    # ####### Get objective formulation
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
    # #######

    # # ####### Get codes
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
    # # #######

    ####### Run the code
    state = load_state(os.path.join(run_dir, "state_6_code.json"))
    generate_code(state, run_dir)
    execute_and_debug(state, model=MODEL, dir=run_dir, logger=logger)
    #######
