# This file was produced by https://github.com/ai-1st/dotprompt and shouldn't be edited directly.

import sys
from langchain_aws import ChatBedrock
import argparse

def rewrite_text(input_text):
    chat = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1"
    )

    prompt = f"""
    Please rewrite the following text in professional American English:

    {input_text}

    Maintain the original meaning and intent, but improve the language, grammar, and style to make it suitable for a professional context.
    """

    response = chat.invoke(prompt)
    return response.content

def main():
    parser = argparse.ArgumentParser(description="Rewrite text in professional American English using an LLM.")
    parser.add_argument("text", nargs="?", help="The text to rewrite. If not provided, reads from stdin.")
    args = parser.parse_args()

    if args.text:
        input_text = args.text
    else:
        input_text = sys.stdin.read().strip()

    if not input_text:
        print("Error: No input text provided.")
        sys.exit(1)

    rewritten_text = rewrite_text(input_text)
    print(rewritten_text)

if __name__ == "__main__":
    main()