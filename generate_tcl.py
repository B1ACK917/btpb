# generate humaneval format tcl benchmarks
import json
import os

from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

from utils.prompts import system_prompt_gen, prompt_gen


def prepare():
    load_dotenv()

    # read env
    task_per_gen = int(os.getenv("TASK_PER_GEN"))
    round_gen = int(os.getenv("ROUND_GEN"))
    base_url = os.getenv("BASE_URL_GEN")
    api_key = os.getenv("API_KEY_GEN")

    # prepare for llm
    with open(os.path.join("data", "generate_example.json")) as file:
        raw_file = json.load(file)
        example_json = json.dumps(raw_file, ensure_ascii=False)
    system_prompt = system_prompt_gen
    prompt = prompt_gen.format(task_per_gen=task_per_gen,
                               example_json=example_json)
    client = OpenAI(api_key=api_key, base_url=base_url)

    # prepare output dir
    os.makedirs("output", exist_ok=True)

    return client, system_prompt, prompt, round_gen


def send_to_generator(client, system_prompt, prompt):
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL_GEN"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            response_format={"type": "json_object"},
            max_tokens=8192,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error sending request to OpenAI API: {e}")
        return None


def main():
    client, system_prompt, prompt, round_gen = prepare()
    generated = []

    for _ in tqdm(range(round_gen)):
        response = send_to_generator(client, system_prompt, prompt)

        if response:
            try:
                generated.extend(json.loads(response)["tasks"])
            except Exception as e:
                print(e)
        else:
            continue

        output = os.path.join("output", "generated.json")
        with open(output, "w") as file:
            file.write(json.dumps(generated, ensure_ascii=False, indent=4))
            print(f"Generated Tasks Write to {output}")


if __name__ == "__main__":
    main()
