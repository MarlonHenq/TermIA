#!/usr/bin/env python3
import click
from openai import OpenAI
import sys
import webbrowser
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if OPENAI_API_KEY is None:
    click.echo("API key not found. Please set it in the .env file")
    sys.exit()

client = OpenAI(api_key=OPENAI_API_KEY)

# Prompt para uso direto no terminal (respostas curtas, comandos, etc.)
PROMPT_TERMINAL = (
    "You are an AI that is running in a CLI on a user's terminal. "
    "Respond with short, concise answers. Use colors in your output to highlight things "
    "(Available colors: normal=\033[92m, alert=\033[93m, command=\033[94m, reset=\033[0m). "
    "Separate command steps clearly. If the user input is a direct question about a specific command "
    "and you can provide a working one-liner (with all params), repeat it at the end like this: COMMAND=your_command_here"
)

# Prompt para uso com entrada via pipe (respostas melhores)
PROMPT_PIPE = (
    "You are an AI receiving the contents of a file, script, or program via stdin. "
    "Interpret what the user has sent and explain it clearly and thoroughly. "
    "If it's a script or code, describe its purpose, structure, and potential effects. "
    "You can use terminal colors to improve clarity "
    "(Available colors: normal=\033[92m, alert=\033[93m, command=\033[94m, reset=\033[0m). "
    "Do not return COMMAND= at the end unless it's strictly necessary. "
    "The user is looking for insight or interpretation, not just execution."
)

def send_request_to_openai(query, is_pipe=False):
    prompt = PROMPT_PIPE if is_pipe else PROMPT_TERMINAL

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ]
    )

    return ''.join(choice.message.content for choice in response.choices)

def parse_command(text):
    lines = text.strip().split('\n')
    
    if lines[-1].startswith("COMMAND="):
        command_body = lines[-1][8:] 
        text_without_command = '\n'.join(lines[:-1])
        return True, text_without_command, command_body
    else:
        return False, text, None

def run_command(command):
    print("\nRun '\033[94m" + command + "\033[0m'?" + " [y/n]")
    response = input()
    if response.lower() == 'y':
        os.system(command)

@click.group(invoke_without_command=True)
@click.option('-o', '--open', 'open_in_browser', is_flag=True, help='Open ChatGPT in the browser')
@click.option('-f', '--force', is_flag=True, help='Force the command being executed without asking for confirmation')
@click.argument('query', nargs=-1, required=False)
@click.pass_context
def cli(ctx, open_in_browser, force, query):
    if open_in_browser:
        webbrowser.open('https://chatgpt.com/')
        sys.exit(0)

    if ctx.invoked_subcommand is None:
        is_pipe = not sys.stdin.isatty()
        stdin_text = sys.stdin.read() if is_pipe else ''
        query_text = ' '.join(query) if query else ''

        full_input = f"{stdin_text.strip()}\n{query_text.strip()}".strip()

        if full_input:
            response = send_request_to_openai(full_input, is_pipe=is_pipe)
            returns = parse_command(response)

            click.echo(returns[1])

            if returns[0] and not is_pipe:
                if force:
                    print("\n\033[93mCommand executed! \033[0m")
                    os.system(returns[2])
                else:
                    run_command(returns[2])
        else:
            click.echo(ctx.get_help())

@cli.command()
@click.argument('command', required=False)
@click.pass_context
def help(ctx, command):
    """Show help for a specific command"""
    if command:
        cmd = cli.get_command(ctx, command)
        if cmd:
            click.echo(cmd.get_help(ctx))
        else:
            click.echo(f"No such command: {command}")
    else:
        click.echo(ctx.parent.get_help())

if __name__ == '__main__':
    cli()
