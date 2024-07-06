# TermIA - An AI terminal interface
A simple CLI that communicates with the OpenIA api

## Installation

Change the API key in the `iaCLI.py` file

```python
api_key = "YOUR_API_KEY"
```

Copy the file to `/usr/bin/` and give it execution permissions

```bash
sudo cp iaCLI.py /usr/bin/iaCLI
sudo chmod +x /usr/bin/iaCLI
```

## Usage

Create a prompt

```bash
iaCLI "Your prompt here" 
#or
iaCLI Your prompt here
```

Open ChatGPT on Chrome

```bash
iaCLI -o
```
