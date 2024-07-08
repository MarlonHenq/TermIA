#!/usr/bin/env python3
import click
from openai import OpenAI
import sys
import webbrowser
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if OPENAI_API_KEY == None:
    click.echo("API key not found. Please set it in the .env file")
    sys.exit()

client = OpenAI(api_key=OPENAI_API_KEY)
def send_request_to_openai(query):
    to_return = ''

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106", # gpt-3.5-turbo-1106
    messages=[
        {"role": "system", "content": "You are an AI that is running a CLI application on a user's terminal. Return short texts, separate the commands and add commands to make it colorful. (Dont use markdown) (Available colors tags:to normal texts=\033[92m,to alerts=\033[93m,to commands=\033[94m,to reset terminal color=\033[0m).If there is a one-line command in the response and you have all its parameters (that is, it could only be run with a direct copy) return it again at the end like this: COMMAND=command_body"},
        {"role": "user", "content": query},
    ]
    )

    for choice in response.choices:
        to_return = to_return + choice.message.content
    
    return to_return

def parse_command(text):
    lines = text.strip().split('\n')
    
    #Verificar se a última linha está no formato "COMMAND=command_body"
    if lines[-1].startswith("COMMAND="):
        command_body = lines[-1][8:] 
        text_without_command = '\n'.join(lines[:-1])  #Texto sem a última linha
        return True, text_without_command, command_body
    else:
        return False, text, None
    
def run_command(command):
    print("\nRun '\033[94m" + command + "\033[0m'?" + " [y/n]")
    response = input()
    if response == 'y':
        os.system(command)
    

@click.group(invoke_without_command=True)
@click.option('-o', '--open', 'open_in_browser', is_flag=True, help='Open ChatGPT in the browser')
@click.option('-f', '--force', is_flag=True, help='Force the command being executed without asking for confirmation')
@click.argument('query', nargs=-1, required=False)
@click.pass_context
def cli(ctx, open_in_browser, force, query):
    global OPENAI_API_KEY

    if open_in_browser:
        webbrowser.open('https://chatgpt.com/')
        sys.exit(0)

    if not OPENAI_API_KEY:
        click.echo("API key not found. Please set it in the .env file or use the '-k' option.")
        sys.exit(1)

    if ctx.invoked_subcommand is None:
        if query:
            send = ' '.join(query)
            response = send_request_to_openai(send)
            returns = parse_command(response)

            click.echo(returns[1])

            if returns[0]:
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
