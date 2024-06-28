"""Generate a file from a prompt.

Copyright (c) 2024 Dmitry Degtyarev
"""

import os
import click

from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

KWARGS = {
    "temperature": float(os.getenv("BEDROCK_TEMPERATURE", "0.5")),
    "top_p": float(os.getenv("BEDROCK_TOP_P", "1")),
    "top_k": int(os.getenv("BEDROCK_TOP_K", "250")),
    "max_tokens": int(os.getenv("BEDROCK_MAX_TOKENS", "4096")),
}

MODEL, REGION = "anthropic.claude-3-5-sonnet-20240620-v1:0", "us-east-1"


@click.command()
@click.argument("filename")
def gen(filename):
    """Simple program generates a file based on prompt."""
    messages = [
        (
            "system",
            """Create a file based on the description provided by the user. 
            Output just the file content, nothing else. Do not enclose the code in triple quotes.""",
        ),
        ("human", "Hello world in python"),
        ("assistant", "print('Hello world')"),
        ("human", "<filename>{filename}</filename>\n{input}"),
    ]
    _prompt = ChatPromptTemplate.from_messages(messages)
    _model = ChatBedrock(model_id=MODEL, model_kwargs=KWARGS, region_name=REGION)
    chain = _prompt | _model | StrOutputParser()
    with open(filename, "r", encoding="utf-8") as rf, open(
        filename.replace(".prompt", ""), "w", encoding="utf-8"
    ) as wf:
        response = chain.invoke({"input": rf.read(), "filename": filename})
        wf.write(response)
    return response


if __name__ == "__main__":
    gen()
