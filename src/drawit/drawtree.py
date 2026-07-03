import json
import os
import shutil
import subprocess
import tempfile
import webbrowser
from typing import Optional

import click
from graphviz import Digraph

from .tree import TreeNode, build_tree


def add_node_edges(dot: Digraph, node: TreeNode):
    node_id = str(id(node))
    dot.node(node_id, label=str(node.val))

    if node.left:
        left_id = str(id(node.left))
        dot.edge(node_id, left_id)
        add_node_edges(dot, node.left)

    if node.right:
        right_id = str(id(node.right))
        dot.edge(node_id, right_id)
        add_node_edges(dot, node.right)


def draw(root: Optional[TreeNode]) -> Optional[Digraph]:
    if root is None:
        return None

    dot = Digraph()
    dot.attr("node", shape="circle")
    add_node_edges(dot, root)
    return dot


def normalize_sequence(seq: list[str]) -> list[str]:
    def normalize(token: str):
        try:
            return json.loads(token)
        except json.JSONDecodeError:
            return token

    return [normalize(token) for token in seq]


def display_png_file(path: str):
    print(path)
    if shutil.which("timg"):
        subprocess.run(["timg", path])
    elif shutil.which("imgcat"):
        subprocess.run(["imgcat", path])
    elif "KITTY_PID" in os.environ:
        subprocess.run(["kitty", "+kitten", "icat", path])
    else:
        url = f"file://{path}"
        webbrowser.open(url)


@click.command
@click.argument("seq", nargs=-1)
def main(seq):
    seq = normalize_sequence(seq)
    root = build_tree(seq)
    graph = draw(root)

    if graph is None:
        return

    out_file = tempfile.NamedTemporaryFile(delete=False)
    out_file.close()
    out_path = f"{out_file.name}.png"

    graph.render(filename=out_file.name, format="png", cleanup=True)
    display_png_file(out_path)
