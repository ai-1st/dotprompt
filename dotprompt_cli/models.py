# This file was produced by AI from a prompt and shouldn't be edited directly.

import os
from typing import List, Optional
from langchain_core.messages import BaseMessage
from langchain_aws import ChatBedrock
from langchain_anthropic import ChatAnthropic


def llm_invoke(
    provider: str = "bedrock",
    model: str = "anthropic.claude-3-5-sonnet-20240620-v1:0",
    messages: List[BaseMessage] = [],
) -> str:
    if provider == "bedrock":
        chat = ChatBedrock(
            model_id=model, region_name="us-east-1", model_kwargs={"max_tokens": 4096}
        )
    elif provider == "anthropic":
        chat = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            timeout=None,
            max_retries=2,
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    try:
        response = chat.invoke(messages)
        return response.content
    except Exception as e:
        print(f"Error invoking LLM: {str(e)}")
        return ""
