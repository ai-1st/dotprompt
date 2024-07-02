# This file was produced by AI from a prompt and shouldn't be edited directly.

import os
import re
import click
from .models import llm_invoke

def expand_directives(content, skip_directives):
    if skip_directives:
        return content

    def replace_directive(match):
        directive, filename = match.groups()
        if directive == 'raw':
            with open(filename, 'r') as f:
                return f.read()
        elif directive == 'prompt':
            with open(filename, 'r') as f:
                prompt_content = f.read()
            return expand_directives(prompt_content, False)

    pattern = r'@(raw|prompt)\((.*?)\)'
    return re.sub(pattern, replace_directive, content)

@click.command()
@click.argument('prompt_file', type=click.Path(exists=True))
@click.option('--skip-directives', is_flag=True, help='Skip expanding @raw and @prompt directives')
@click.option('--provider', default='bedrock', type=click.Choice(['bedrock', 'anthropic']), help='LLM provider')
@click.option('--model', default='anthropic.claude-3-sonnet-20240229-v1:0', help='LLM model')
def main(prompt_file, skip_directives, provider, model):
    output_file = prompt_file[:-7] if prompt_file.endswith('.prompt') else prompt_file + '.out'

    with open(prompt_file, 'r') as f:
        prompt_content = f.read()

    expanded_prompt = expand_directives(prompt_content, skip_directives)

    system_message = {
        "role": "system",
        "content": "Output just the file content, nothing else. Do not print any introductory text before the code. Do not enclose the code in triple quotes. Include a comment in the code saying that this file was produced by AI from a prompt and shouldn't be edited directly, unless generating json or other file formats that don't support comments."
    }

    user_message = {
        "role": "user",
        "content": "Hello world in python"
    }

    assistant_message = {
        "role": "assistant",
        "content": "print('Hello world')"
    }

    prompt_message = {
        "role": "user",
        "content": expanded_prompt
    }

    messages = [system_message, user_message, assistant_message, prompt_message]

    response = llm_invoke(provider, model, messages)

    with open(output_file, 'w') as f:
        f.write(response)

    click.echo(f"Generated code has been saved to {output_file}")

if __name__ == '__main__':
    main()