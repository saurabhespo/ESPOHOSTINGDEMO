import os

import config
import yaml
import pandas as pd
import json
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = config.AZURE_OPENAI_API_KEY
os.environ["AZURE_OPENAI_ENDPOINT"] = config.AZURE_OPENAI_ENDPOINT


def get_prompt(prompt_name):
    with open(config.PROMPT_FILE, "r", encoding="utf-8") as f:
        prompts = yaml.safe_load(f)
    prompt = prompts[prompt_name]

    return prompt


def get_questions():
    with open(config.QUES_FILE, "r", encoding="utf-8") as f:
        questions = yaml.safe_load(f)
        followup = pd.Series(questions)
        followup = followup.sample(3, replace=False,  axis=0).to_json()
     
        input_data = {
        "follow_up_questions": [
        
        ]
         }
        additional_questions=json.loads(followup)
    for key in sorted(additional_questions.keys()):
       input_data["follow_up_questions"].append({"question": additional_questions[key]})

        # Convert to JSON format
    output_json = json.dumps(input_data, indent=2)
    return output_json

def get_history():
    with open(config.HISTORY_FILE, "r", encoding="utf-8") as f:
        history = yaml.safe_load(f)

    return history


def write_history(data):
    with open(config.HISTORY_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False)

    return None


def get_model(temperature=0.1):

    model = AzureChatOpenAI(
        openai_api_version=config.OPENAI_API_VERSION,
        azure_deployment=config.AZURE_DEPLOYMENT,
        temperature=temperature,
    )
    return model


if __name__ == "__main__":
    x = get_questions()
    print(x)
