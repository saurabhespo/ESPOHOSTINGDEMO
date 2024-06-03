import os

import config
import yaml
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = config.AZURE_OPENAI_API_KEY
os.environ["AZURE_OPENAI_ENDPOINT"] = config.AZURE_OPENAI_ENDPOINT


def get_prompt(prompt_name):
    with open(config.PROMPT_FILE, "r", encoding="utf-8") as f:
        prompts = yaml.safe_load(f)
    prompt = prompts[prompt_name]

    return prompt


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
    x = get_history()
    print(x)
