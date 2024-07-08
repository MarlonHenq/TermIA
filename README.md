# TermIA - An AI terminal interface
A simple CLI that communicates with the OpenIA api

## Installation

copy or rename the `example.env` file to `.env`

```bash
cp example.env .env
```
Change the API key in the `.env` file

```text
OPENAI_API_KEY="YOUR_API_KEY"
```

Copy the file to `/usr/bin/` and give it execution permissions

```bash
sudo cp termIA.py /usr/bin/termIA
sudo cp .env /usr/bin/.env
sudo chmod +x /usr/bin/termIA
```

## Usage

Create a prompt

```bash
termIA "Your prompt here" 
#or
termIA Your prompt here
```
note: use '-f' to force rum the command without prompt

```bash
termIA -f "Your prompt here" 
```

Open ChatGPT on Chrome

```bash
termIA -o
```

Open Help menu

```bash
termIA --help
```