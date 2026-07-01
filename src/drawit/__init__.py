import io
import json
import shutil
import subprocess
import tempfile
import webbrowser
from typing import Optional

import click
import drawtree

from .tree import TreeNode, bfs, build_id, build_tree


def build_mermaid_script(root: Optional[TreeNode]):
    null_count = 0
    buf = io.StringIO()
    buf.write("flowchart TD\n")
    for node in bfs(root):
        node_id = build_id(node)
        buf.write(f"    {node_id}(({node.val}))\n")
    buf.write("\n")

    for node in bfs(root):
        if node.left is None and node.right is None:
            continue

        node_id = build_id(node)

        if node.left is not None:
            buf.write(f"    {node_id} --> {build_id(node.left)}\n")
        else:
            buf.write(f"    {node_id} ~~~ null_{null_count}(( ))\n")
            null_count += 1

        if node.right is not None:
            buf.write(f"    {node_id} --> {build_id(node.right)}\n")
        else:
            buf.write(f"    {node_id} ~~~ null_{null_count}(( ))\n")
            null_count += 1

    # format the null nodes (placeholders) to be invisible
    buf.write("\n")
    for i in range(null_count):
        buf.write(f"style null_{i} fill:none,stroke:none,color:none\n")

    return buf.getvalue()


def show_tree_as_text(seq):
    nodes = ",".join("#" if tok == "null" else tok for tok in seq)
    text = "{%s}" % nodes
    drawtree.draw_level_order(text)


def show_tree_as_pic(seq):
    # build the binary tree
    seq = [json.loads(x) for x in seq]
    root = build_tree(seq)

    # generate the Mermaid script
    script = build_mermaid_script(root)
    with tempfile.NamedTemporaryFile(
        prefix="tree_", suffix=".mmdc", delete=False, mode="wt"
    ) as script_path:
        script_path.file.write(script)

    # generate the picture
    png_path = tempfile.NamedTemporaryFile(prefix="tree_", suffix=".png", delete=False)
    png_path.close()

    subprocess.run(
        ["mmdc", "--input", script_path.name, "--output", png_path.name],
        capture_output=True,
        text=True,
        check=True,
    )

    # display the picture
    print(script_path.name)
    print(png_path.name)
    webbrowser.open(f"file://{png_path.name}")


@click.command
@click.option(
    "-f",
    "--format",
    type=click.Choice(["text", "pic"], case_sensitive=False),
    default="pic",
)
@click.argument("seq", nargs=-1)
def main(format, seq):
    if format == "pic" and shutil.which("mmdc"):
        show_tree_as_pic(seq)
    else:
        show_tree_as_text(seq)
