# BTPB: Basic Tcl Problems and Benchmark Dataset

The **BTPB (Basic Tcl Problems and Benchmark)** dataset is a collection of **984 Tcl tasks** designed to evaluate the Tcl programming capabilities of large language models (LLMs), and **19990 Tcl tasks** translated from code_alpaca_20k to train LLM in the SFT stage. The dataset is composed of the following:

- **19990 tasks** translated from **code_alpaca** dataset to Tcl which can be used in LLM's SFT.

- **363 tasks** generated using **Deepseek-V3**.
- **295 tasks** translated from the **HumanEval** dataset to Tcl.
- **326 tasks** translated from the **MBPP** dataset to Tcl.



## Tcl For SFT

The `data/tcl_alpaca.json` is the 19990 tasks we translated from code_alpaca, the format follows the alpaca template as:

- `instruction`: `str`, describes the task the model should perform. Each of the 20k instructions is unique.
- `input`: `str`, optional context or input for the task. For example, when the instruction is "Summarize the following article", the input is the article.
- `output`: `str`, the answer to the instruction.



## Tcl For Benchmark

The 3 files `tcl_task_generated.json, tcl_task_generated.json, tcl_task_generated.json` under `data` directory are the tasks we provide to test the LLM's Tcl programming capabilities.

You can simply use them with the `test_llm.py` script, which we will talk about in next chapter.

**All of these tasks have passed the assertions** defined within them, so they can be considered correct. In fact, we attempted to convert nearly the entire HumanEval and MBPP datasets, but the vast majority failed to pass the assertions and were consequently discarded. The remaining tasks represent what we believe to be high-quality benchmark data.



## Scripts

We provide 3 scripts for community to use:

- **generate_tcl.py**: This is the script we used to generate `tcl_task_generated.json`. If you are not satisfied with these tasks, you can generate your own Tcl tasks at any time by configuring the variables in the `.env` file.
- **task_validate.py**: This is the script we used to validate whether the tasks are legitimate. We converted almost the entire HumanEval and MBPP datasets, but only about **30%** of them passed the assertions. As a result, we retained only these valid tasks, while the ones that failed were considered "low-quality" and discarded.
- **test_llm.py**: This is the script we used to test LLMs. It utilizes API calls for testing, enabling it to evaluate almost any model without being limited to those that can only be loaded locally using `transformers`. You can configure the variables in the `.env` file to use this script. All tasks, LLM responses, and whether they pass the assertions will be output to the `output/llm/<dataset>` folder.



## Usage

1. Create a Python virtual environment to avoid conflicts: You can use either `conda` or `venv` to accomplish this.

   ```shell
   # conda
   conda create -n btpb python=3.12 -y
   conda activate btpb
   
   # or venv
   # python -m venv venv
   # source venv/bin/activate
   
   # install requirement
   pip install -r requirements.txt
   ```

   

2. Create your `.env` file

   ```
   cp .env.example .env
   ```

   Here is the vars in the `.env` file

   ```shell
   BASE_URL_GEN="<base-url-for-generate>"
   API_KEY_GEN="<api-key-for-generate>"
   MODEL_GEN="<model-name>"
   TASK_PER_GEN=10
   ROUND_GEN=10
   
   BASE_URL_TEST="<base-url-for-test>"
   API_KEY_TEST="<api-key-for-test>"
   ```

   - BASE_URL_GEN: The LLM api for generating Tcl tasks.
   - API_KEY_GEN: The api key for use LLM.
   - MODEL_GEN: openai api required the model, for example, **text-davinci-003** for gpt or **deepseek-chat** for deepseek
   - TASK_PER_GEN: How many tasks to generate per round
   - ROUND_GEN: Total generate round, the generated count will be **TASK_PER_GEN * ROUND_GEN**.
   - BASE_URL_TEST: The LLM api for test Tcl capabilities when using `test_llm.py`.
   - API_KEY_TEST: The api key for test (if have).



3. Run scripts
   - If you want to generate your own Tcl tasks, modify the **BASE_URL_GEN, API_KEY_GEN, MODEL_GEN, TASK_PER_GEN, ROUND_GEN** and use `python generate_tcl.py`  to run.
   - If you want to test the LLM's Tcl capability, modify the **BASE_URL_TEST, API_KEY_TEST** and use `python test_llm.py` to run benchmarks. You can change the dataset in the code's prepare function.

