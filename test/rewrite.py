# This file was produced by AI from a prompt and shouldn't be edited directly.

import sys
import argparse
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage

def rewrite_text(input_text):
    chat = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1"
    )

    prompt = f"Rewrite the following text in professional American English:\n\n{input_text}"
    
    messages = [HumanMessage(content=prompt)]
    response = chat(messages)
    
    return response.content

def main():
    parser = argparse.ArgumentParser(description="Rewrite text in professional American English using an LLM.")
    parser.add_argument("input", nargs="?", help="Input text to rewrite. If not provided, reads from stdin.")
    
    args = parser.parse_args()
    
    if args.input:
        input_text = args.input
    else:
        input_text = sys.stdin.read().strip()
    
    if not input_text:
        print("Error: No input text provided.")
        sys.exit(1)
    
    try:
        rewritten_text = rewrite_text(input_text)
        print(rewritten_text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()