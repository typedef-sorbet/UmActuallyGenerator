from typing import List     # For knowing whether an object is a list
import imgkit               # For rendering HTML to an image
import json                 # ...for JSON
import argparse             # For parsing arguments
import random               # For filenames

from PIL import Image, ImageChops                                       # For image processing
from jinja2 import Environment, FileSystemLoader, select_autoescape     # For templating HTML
from os.path import exists, abspath                                     # For filesystem stuff
from os import mkdir                                                    # ^^^^^^^^^^^^^^^^^^^

jinja_env = Environment(
    loader = FileSystemLoader("templates/"),
    autoescape = select_autoescape()
)

# Don't crop vertically; trim() needs to be able to grab whitespace from (0,0)
imgkit_opts = {
    "crop-x": 10,
    "crop-w": 628,
    "enable-local-file-access": None
}

# Trims bordering pixels from the image; border color inferred from top-left pixel
# Props to fraxel for the basics of this function, and Matt Pitkin for RGBA workarounds
# https://stackoverflow.com/questions/10615901/trim-whitespace-using-pil
def trim(im):
    bg = Image.new("RGB", im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im.convert("RGB"), bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im

# Create dict from JSON string
def from_json(json_str):
    json_data = json.loads(json_str)

    if not json_data:
        return None, "Unable to parse JSON data"

    return json_data, None

# Create List[Dict] from user input
def from_stdin():
    return [{
        "title": input("Title of the property in question: "),
        "category": input("Category of the property in question (e..g. 'Horror', 'Anime', etc.): "),
        "statement": input("Statement (Place the incorrect part of the statement in square brackets, [like this]): "),
        "correction": input("Correction: "),
        "details": input("Additional details: ")
    }], None

# Create dict from JSON file
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

    # Default to using a list of dicts -- if we only got one element, chuck it into a list anyways.
    if not template_data:
        print(reason)
        return
    elif not isinstance(template_data, List):
        template_data = [template_data]

    template = jinja_env.get_template("card.html")

    if not exists("out/"):
        mkdir("out/")

    for dikt in template_data:
        # Render HTML viewport, with some extra whitespace
        rand = random.randint(10000, 99999)
        imgkit.from_string(template.render(data=dikt, bg_path=abspath("templates/card_bg.svg")), f"out/{dikt['title'].replace(' ', '_')}_{rand}.png", options=imgkit_opts)

        # Trim aforementioned whitespace so the image doesn't look terrible
        im = Image.open(f"out/{dikt['title'].replace(' ', '_')}_{rand}.png")
        im = trim(im)
        im.save(f"out/{dikt['title'].replace(' ', '_')}_{rand}.png")
        

if __name__ == "__main__":
    main()
