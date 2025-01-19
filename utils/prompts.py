system_prompt_gen = "You are a helpful assistant."
prompt_gen = """
Please refer to the following output and write {task_per_gen} more questions that can test LLM's Tcl ability, which will be returned in JSON format.

EXAMPLE JSON OUTPUT:
{example_json}
"""

system_prompt_test = """
You are a Tcl function generator, pleas write Tcl function based on user request, you should only return completed Tcl function ended with }
"""

prompt_test = """
This is a requirement for tcl functions:
{requirement}
You should start with:
{proc_start}
"""