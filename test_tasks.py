# Test tasks from generated
import json
import os
from utils.helper import test_tcl, write_tcl
from tqdm import tqdm

task_path = os.path.join("output", "generated.json")
output_path = os.path.join("output", "generated_valid.json")


def test_task(task):
    tcl_proc = task["declaration"] + task["canonical_solution"]
    example_test_code = task["example_test"]
    tcl_script = tcl_proc+"\n"+example_test_code
    write_tcl(tcl_script)
    success = test_tcl()
    return success


def run_test_task(tasks):
    passed = []
    for task in tqdm(tasks, postfix="Running tclsh to test assert"):
        if test_task(task):
            passed.append(task)
    print(f"{len(passed)} of {len(tasks)} passed assertion test.")
    return passed


def main():
    with open(task_path) as file:
        tasks = json.load(file)
    print(f"Total {len(tasks)} tasks.")
    
    passed = run_test_task(tasks)
    with open(output_path, "w") as file:
        file.write(json.dumps(passed, ensure_ascii=False, indent=4))
    print(f"Valid Tcl tasks write to {output_path}.")


if __name__ == "__main__":
    main()
