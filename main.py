import markdown
import re
import logging
import os
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension



preamble = """\
<html lang="en">
<head>
{meta}
<meta charset="UTF-8">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<div id="resume">
"""

postamble = """\
</div>
</body>
</html>
"""

def title(md: str) -> str:
    """
    Return the contents of the first markdown heading in md, which we
    assume to be the title of the document.
    """
    for line in md.splitlines():
        if re.match("^#[^#]", line):  # starts with exactly one '#'
            return line.lstrip("#").strip()
    raise ValueError(
        "Cannot find any lines that look like markdown h1 headings to use as the title"
    )


def make_html(md: str, prefix: str = "resume") -> str:
    """
    Compile md to HTML and prepend/append preamble/postamble.

    Insert <prefix>.css if it exists.
    """
    try:
        with open(prefix + ".css") as cssfp:
            css = cssfp.read()
    except FileNotFoundError:
        print(prefix + ".css not found. Output will by unstyled.")
        css = ""

    try:
        with open(prefix + "-meta.html") as metafp:
            meta = metafp.read()
    except FileNotFoundError:
        print(prefix + "-meta.html not found. Output will by unstyled.")
        meta = ""

    return "".join(
        (
            preamble.format(title=title(md), meta=meta, css=css),
            markdown.markdown(md),
            postamble,
        )
    )

# https://stackoverflow.com/questions/29259912/how-can-i-get-a-list-of-image-urls-from-a-markdown-file-in-python
# First create the treeprocessor
class ImgExtractor(Treeprocessor):
    def run(self, doc):
        "Find all images and append to markdown.images. "
        self.md.images = []
        for image in doc.findall('.//img'):
            self.md.images.append(image.get('src'))

# Then tell markdown about it

class ImgExtExtension(Extension):
    def extendMarkdown(self, md):
        img_ext = ImgExtractor(md)
        md.treeprocessors.register(img_ext, 'img_ext', 15)

# Finally create an instance of the Markdown class with the new extension



file = "README.md"
output_dir = "public"
output_file = "index.html"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

prefix, _ = os.path.splitext(os.path.abspath(file))

with open(file, encoding="utf-8") as mdfp:
    md = mdfp.read()
html = make_html(md, prefix=prefix)

with open(output_dir + "/" + output_file, "w", encoding="utf-8") as htmlfp:
    htmlfp.write(html)
    logging.info(f"Wrote {htmlfp.name}")

md_images = markdown.Markdown(extensions=[ImgExtExtension()])
md_images.convert(md)

for image in md_images.images:
    if image.startswith("https://"):
        continue

    if dirname := os.path.dirname(image):
        os.makedirs(f"{output_dir}/{dirname}", exist_ok=True)

    os.system(f"cp {image} {output_dir}/{dirname}")
