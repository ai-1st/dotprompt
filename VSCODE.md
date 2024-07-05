# Creating a VS Code Plugin for Running .prompt Files

<!-- This file was produced by https://github.com/ai-1st/dotprompt and shouldn't be edited directly. -->

This guide will walk you through the process of creating a Visual Studio Code extension that allows running `.prompt` files using the `dotprompt` CLI command.

## Prerequisites

1. Node.js and npm installed on your system
2. Visual Studio Code
3. Basic knowledge of TypeScript and VS Code extension development

## Step 1: Set up the Extension Project

1. Install the Yeoman generator and VS Code Extension generator:
   ```
   npm install -g yo generator-code
   ```

2. Generate a new VS Code extension project:
   ```
   yo code
   ```

3. Follow the prompts:
   - Choose "New Extension (TypeScript)"
   - Name your extension (e.g., "dotprompt-runner")
   - Provide a description
   - Choose "Yes" for initializing a git repository

4. Navigate to your extension directory:
   ```
   cd dotprompt-runner
   ```

## Step 2: Implement the Extension Logic

1. Open the `src/extension.ts` file and replace its contents with the following code:

```typescript
import * as vscode from 'vscode';
import { exec } from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('dotprompt-runner.run', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const document = editor.document;
            if (document.languageId === 'prompt' || document.fileName.endsWith('.prompt')) {
                const filePath = document.fileName;
                exec(`dotprompt "${filePath}"`, (error, stdout, stderr) => {
                    if (error) {
                        vscode.window.showErrorMessage(`Error: ${error.message}`);
                        return;
                    }
                    if (stderr) {
                        vscode.window.showErrorMessage(`Error: ${stderr}`);
                        return;
                    }
                    vscode.window.showInformationMessage(`Output: ${stdout}`);
                });
            } else {
                vscode.window.showWarningMessage('This is not a .prompt file');
            }
        }
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
```

2. Update the `package.json` file to include the command and file type:

```json
{
  "contributes": {
    "commands": [
      {
        "command": "dotprompt-runner.run",
        "title": "Run .prompt file"
      }
    ],
    "languages": [
      {
        "id": "prompt",
        "extensions": [".prompt"],
        "aliases": ["Prompt", "prompt"]
      }
    ]
  }
}
```

## Step 3: Test the Extension

1. Press F5 to run the extension in a new VS Code window.
2. Create a new file with a `.prompt` extension.
3. Use the Command Palette (Ctrl+Shift+P) and search for "Run .prompt file".
4. The extension should execute the `dotprompt` command on the current file.

## Step 4: Package and Publish the Extension

1. Install `vsce`:
   ```
   npm install -g vsce
   ```

2. Package your extension:
   ```
   vsce package
   ```

3. This will create a `.vsix` file that you can install in VS Code or publish to the VS Code Marketplace.

## Notes

- Ensure that the `dotprompt-cli` is installed and accessible in the system PATH.
- You may want to add error handling for cases where the `dotprompt` command is not found.
- Consider adding configuration options to allow users to customize the command or its behavior.

Remember to thoroughly test your extension before publishing it to ensure it works as expected across different environments and use cases.