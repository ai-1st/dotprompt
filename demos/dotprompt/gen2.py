import os
import click
from langchain_aws import ChatBedrock

@click.command()
@click.argument('prompt_file', type=click.Path(exists=True))
def generate_code(prompt_file):
    """Generate code from a prompt file."""
    # Read the prompt from the file
    with open(prompt_file, 'r') as f:
        prompt = f.read()

    # Initialize the ChatBedrock model
    chat = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1"
    )

    # Define system instructions and one-shot example
    system_message = "Output just the file content, nothing else. Do not enclose the code in triple quotes."
    example_user = "Hello world in python"
    example_assistant = "print('Hello world')"

    # Generate code using the chat model
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": example_user},
        {"role": "assistant", "content": example_assistant},
        {"role": "user", "content": prompt}
    ]
    response = chat.invoke(messages)

    # Get the generated code
    generated_code = response.content

    # Determine the output file name
    output_file = prompt_file.rsplit('.', 1)[0]

    # Write the generated code to the output file
    with open(output_file, 'w') as f:
        f.write(generated_code)

    click.echo(f"Code generated and saved to {output_file}")

if __name__ == '__main__':
    generate_code()