import json
import os
import re

from openai import OpenAI
from tqdm import tqdm
from datetime import datetime
from dotenv import load_dotenv

from utils.helper import test_tcl, write_tcl
from utils.prompts import system_prompt_test, prompt_test


def prepare():
    load_dotenv()

    # prepare input/output vars
    tcl_tasks = os.path.join("data", f"ttbd_benchmark.json")
    test_output_dir = os.path.join("output", "ttbd_benchmark")
    log_file = os.path.join(test_output_dir, "test.log")
    os.makedirs(test_output_dir, exist_ok=True)

    # prepare input data
    repeat_times = 2
    with open(tcl_tasks) as file:
        tasks = json.load(file)
    # generate: tasks[:363]
    # humaneval: tasks[363:658]
    # mbpp: tasks[658:]
    tasks_map = {
        "level1": tasks[:363],
        "level2": tasks[363:658],
        "level3": tasks[658:]
    }
    target_tasks = ["level1", "level2", "level3"]
    if repeat_times > 1:
        for k, v in tasks_map.items():
            tasks_map[k] = v * repeat_times

    # prepare llm
    base_url = os.getenv("BASE_URL_TEST")
    api_key = os.getenv("API_KEY_TEST")
    models = [
        "qwen:7b",
        "llama3.1:7b",
    ]
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    return tasks_map, target_tasks, client, models, test_output_dir, log_file


def generate_with_llm(client, model, task):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt_test},
            {"role": "user",
             "content": prompt_test.format(requirement=task["prompt_text"],
                                           proc_start=task["declaration"])},
        ],
        stream=False,
    )
    task.update({"llm_generate": response.choices[0].message.content})
    return task


def retrieve_tcl_proc(input_string):
    pattern = r"```(?:tcl)?(.*?)```"
    matches = re.findall(pattern, input_string, re.DOTALL)

    cleaned_matches = [match.strip() for match in matches]
    if len(cleaned_matches) > 0:
        return cleaned_matches[0]
    else:
        return input_string.replace("```", "").replace("```tcl", "")


def write_generate(task):
    tcl_proc = task["llm_generate"]
    cleaned_proc = retrieve_tcl_proc(tcl_proc)
    task.update({"cleaned_proc": cleaned_proc})
    example_test_code = task["example_test"]
    tcl_script = cleaned_proc+"\n"+example_test_code
    write_tcl(tcl_script)


def main():
    tasks_map, target_tasks, client, models, test_output_dir, log_file = prepare()
    for model in models:
        print(f"Benchmarking {model}...")
        test_result = []
        for cur_task_name in target_tasks:
            print(f"Running on {cur_task_name}...")
            passed, total = 0, 0
            tasks = tasks_map[cur_task_name]
            for task in tqdm(tasks):
                task = generate_with_llm(client, model, task)
                write_generate(task)
                success = test_tcl()
                task.update({"pass": success})
                passed += 1 if success else 0
                total += 1
                test_result.append(task)
            result_str = f"{model} passed {
                passed} of {total} on {cur_task_name}."
            print(result_str)
            with open(log_file, "a") as file:
                now = datetime.now()
                formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"[{formatted_time}]: {result_str}\n")

        with open(os.path.join(test_output_dir, f"{model.replace(":", "_")}.json"), "w") as file:
            json.dump(test_result, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
