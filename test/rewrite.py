import argparse
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage

def rewrite_text(input_text):
    chat = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1"
    )

    prompt = f"""
    Rewrite the following text in professional American English:

    {input_text}

    Please provide only the rewritten text without any additional comments or explanations.
    """

    messages = [HumanMessage(content=prompt)]
    response = chat.invoke(messages)
    return response.content.strip()

def main():
    parser = argparse.ArgumentParser(description="Rewrite text in professional American English using an LLM.")
    parser.add_argument("input_text", help="The text to be rewritten")
    args = parser.parse_args()

    rewritten_text = rewrite_text(args.input_text)
    print(rewritten_text)

if __name__ == "__main__":
    main()