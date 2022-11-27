## Overview

UmActuallyGenerator allows the creation of custom "Um, Actually"-eqsue question cards from JSON data.

![Here's an example.](https://raw.githubusercontent.com/typedef-sorbet/UmActuallyGenerator/master/examples/example_1.png)

## Requirements

wkhtmltopdf

## Usage

JSON data can be provided either on the command-line or via a file:

```bash
    # JSON via Command Line:
    python3 main.py --json '{...}'

    # JSON from file:
    python3 main.py data.json
```

Question card data can also be collected via stdin if no arguments are given.

## JSON Schema

```json
{
    "title": "Title of the property/subject in question (e.g. God of War, Akira, etc.)",
    "category": "Genre of the property/subject in question (e.g. Games, TV, etc.)",
    "statement": "The incorrect statement to be read. The incorrect part to be highlighted should be placed within square brackets [like this]",
    "correction": "The correction to the above statement",
    "details": "Additional details about the correction"
}
```
