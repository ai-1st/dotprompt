# DotPrompt

DotPrompt is a revolutionary approach to programming that explores the idea of code being 100% produced by AI, with humans only editing the prompts used to generate the code. This project, authored by Dmitry Degtyarev, introduces a new paradigm in software development where the source code is generated from ".prompt" files.

## Overview

In traditional programming, code is built through a series of iterations, either by humans or AI. The resulting code doesn't reveal which prompts were used to build it, making it difficult to alter these prompts later. DotPrompt addresses this limitation by introducing a system where:

1. Code is entirely produced by AI.
2. Humans focus on editing the prompts used by AI to generate the code.
3. ".prompt" files contain the prompts used to produce actual code files.
4. A simple script executes these .prompt files to build the code.

## Key Features

- **Self-generation**: The builder script itself can be generated from a .prompt file, allowing the generator to generate itself.
- **Multi-level abstraction**: .prompt files can be built from other .prompt files, enabling higher-level idea representation.
- **Reverse engineering**: Potential for reverse engineering prompt files from existing source code.

## Future Enhancements

- Ability to produce multiple files from a single prompt (e.g., code and unit tests).
- Automated error correction based on unit test results and error messages.

## Installation

To install DotPrompt, use the following pip command:

```
pip3 install dotprompt-cli
```

## Usage

The DotPrompt CLI supports the following parameters:

```
Usage: dotprompt [OPTIONS] INPUT_FILE

  CLI application to process prompt files and generate code.

  This application takes a prompt file stored in the local filesystem and produces a raw code file,
  stored along with the prompt. The prompt files have a ".prompt" suffix.

Options:
  --recursive      Process included files recursively
  --from-scratch   Generate code from scratch, ignoring existing output file
  --provider TEXT  LLM provider (bedrock or anthropic)
  --model TEXT     LLM model to use
  --help           Show this message and exit.
```

### Parameters

- `INPUT_FILE`: Path to the input .prompt file (required)
- `--recursive`: Flag to recursively process included files
- `--from-scratch`: Flag to generate code from scratch, ignoring existing output file
- `--provider`: LLM provider (bedrock or anthropic, default is 'bedrock')
- `--model`: LLM model to use (default is 'anthropic.claude-3-5-sonnet-20240620-v1:0')

## License

This project is licensed under the MIT License.

## Contact

For more information or to get in touch with the author, visit [https://twitter.com/Mitek99](https://twitter.com/Mitek99).