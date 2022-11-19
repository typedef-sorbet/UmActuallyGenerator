from typing import List
import imgkit       # For rendering HTML to an image
import json         # ...for JSON
import argparse     # For parsing arguments
import random       # For filenames

from PIL import Image, ImageChops
from jinja2 import Environment, FileSystemLoader, select_autoescape       # For templating HTML
from os.path import exists

jinja_env = Environment(
    loader = FileSystemLoader("templates/"),
    autoescape = select_autoescape()
)

imgkit_opts = {
    "crop-x": 10,
    "crop-w": 628
}

def trim(im):
    bg = Image.new("RGB", im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im.convert("RGB"), bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im

def from_json(json_str):
    json_data = json.loads(json_str)

    if not json_data:
        return None, "Unable to parse JSON data"

    return json_data, None

def from_stdin():
    return [{
        "title": input("Title of the property in question: "),
        "category": input("Category of the property in question (e..g. 'Horror', 'Anime', etc.): "),
        # Lord forgive me.
        "statement": input("Statement (Place the incorrect part of the statement in square brackets, [like this])"),
        "correction": input("Correction: "),
        "details": input("Additional details: ")
    }], None

def from_file(filename):
    if exists(filename):
        with open(filename, "r") as infile:
            return from_json(infile.read())
    else:
        return None, "File does not exist"

def main():
    parser = argparse.ArgumentParser(
        prog = "UmActuallyGenerator",
        description = "Creates a custom \"Um, Actually\" card",
    )

    parser.add_argument('-j', '--json')
    parser.add_argument('filename', nargs="?", default=None)

    args = parser.parse_args()

    if args.json:
        template_data, reason = from_json(args.json)
    elif args.filename:
        template_data, reason = from_file(args.filename)
    else:
        template_data, reason = from_stdin()

    if not template_data:
        print(reason)
        return
    elif not isinstance(template_data, List):
        template_data = [template_data]

    template = jinja_env.get_template("card.html")

    for dikt in template_data:
        rand = random.randint(10000, 99999)
        imgkit.from_string(template.render(data=dikt), f"out/{dikt['title'].replace(' ', '_')}_{rand}.png", options=imgkit_opts)

        im = Image.open(f"out/{dikt['title'].replace(' ', '_')}_{rand}.png")
        im = trim(im)
        im.save(f"out/{dikt['title'].replace(' ', '_')}_{rand}.png")
        

if __name__ == "__main__":
    main()