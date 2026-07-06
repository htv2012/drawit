import json
import os
import shutil
import subprocess
import tempfile
import webbrowser

import click
import matplotlib.pyplot as plt
import networkx as nx

from .tree import TreeNode, build_tree, max_depth
from .version import __version__


def build_drawing_specifications(root: TreeNode) -> dict:
    depth = max_depth(root)
    node_size = 800
    font_size = 10
    if depth > 6:
        node_size = 200
        font_size = 3
    elif depth > 4:
        node_size = 400
        font_size = 6

    return dict(
        node_size=node_size,
        font_size=font_size,
        node_color="LightBlue",
        arrows=True,
        font_weight="bold",
    )


def draw_tree_using_networkx(root: TreeNode, filename: str = "binary_tree.png"):
    G = nx.DiGraph()
    pos = {}

    def parse_tree(node, x=0, y=0, layer=1):
        if node:
            node_id = id(node)
            G.add_node(node_id, label=node.val)
            pos[node_id] = (x, y)

            # Dynamically calculate spacing based on tree depth layer
            width = 1.0 / (2**layer)

            if node.left:
                left_id = id(node.left)
                G.add_edge(node_id, left_id)
                parse_tree(node.left, x - width, y - 1, layer + 1)

            if node.right:
                right_id = id(node.right)
                G.add_edge(node_id, right_id)
                parse_tree(node.right, x + width, y - 1, layer + 1)

    parse_tree(root)

    # Extract labels for the nodes
    labels = nx.get_node_attributes(G, "label")

    # Setup a headless matplotlib figure (prevents GUI window popups)
    fig = plt.figure(figsize=(6, 4))

    # Draw the networkx graph
    specifications = build_drawing_specifications(root)
    nx.draw(G, pos, labels=labels, with_labels=True, **specifications)

    # Save directly to the filesystem
    plt.savefig(filename, format="png", bbox_inches="tight", dpi=300)

    # Completely destroy and clear the figure from memory
    plt.close(fig)


def display_png_file(path: str, web: bool):
    print(path)
    if web:
        url = f"file://{path}"
        webbrowser.open(url)
    elif shutil.which("timg"):
        subprocess.run(["timg", path])
    elif shutil.which("imgcat"):
        subprocess.run(["imgcat", path])
    elif "KITTY_PID" in os.environ:
        subprocess.run(["kitty", "+kitten", "icat", path])
    else:
        url = f"file://{path}"
        webbrowser.open(url)


def normalize_sequence(seq: list[str]) -> list[str]:
    def normalize(token: str):
        try:
            return json.loads(token)
        except json.JSONDecodeError:
            return token

    return [normalize(token) for token in seq]


@click.command
@click.version_option(__version__)
@click.option("-w", "--web", is_flag=True, default=False)
@click.argument("seq", nargs=-1)
def main(web, seq):
    seq = normalize_sequence(seq)
    if not seq:
        print("Empty tree")
        return

    out_file = tempfile.NamedTemporaryFile(delete=False)
    out_file.close()
    out_path = f"{out_file.name}.png"

    root = build_tree(seq)
    draw_tree_using_networkx(root, out_path)
    display_png_file(out_path, web)
