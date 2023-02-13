import pathlib
import re

"""
This is a hacky attempt to build a readme with code snippets inserted directly from the relevant py files.
"""

# ----------------------------------------

root_path = pathlib.Path(__file__).parent
readme_prebuild_path = root_path / "readme-prebuild.md"
readme_out_path = root_path / "../../README.md"
insert_regex = re.compile("<insert-file: (.+)>")

# ----------------------------------------

def snippet_partial_include(snippet, 
                                   include_open_tag="# <include>", 
                                   include_close_tag="# </include>"):
    include_tag_is_open = False
    out_lines = []
    for line in snippet.splitlines():
        if line.startswith(include_close_tag):
            include_tag_is_open = False
        if include_tag_is_open == True:
            out_lines.append(line)
        if line.startswith(include_open_tag):
            include_tag_is_open = True
    if len(out_lines) > 0:
        return "\n".join(out_lines)
    else:
        return snippet

# ----------------------------------------

print(f"Building {readme_out_path.name}")
readme_compiled = ""
with readme_prebuild_path.open("r") as template_file:
    for line in template_file.readlines():
        insert = insert_regex.match(line)
        if insert:
            path = root_path / insert[1]
            with path.open("r") as snippet:
                snippet_text = snippet.read()
                partial_snippet = snippet_partial_include(snippet_text)
                readme_compiled += partial_snippet
                readme_compiled += "\n"
            print(f"- inserted {path.name}")
        else:
            readme_compiled += line

with readme_out_path.open("w") as out_file:
    out_file.write(readme_compiled)

print(f"Saved {readme_out_path.name}")