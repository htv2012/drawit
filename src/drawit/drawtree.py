import io
import json
import os
import shutil
import subprocess
import tempfile
import webbrowser
from typing import Optional

import click
import drawtree
from graphviz import Digraph

from .tree import TreeNode, bfs, build_id, build_tree


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


def draw_tree_using_text(seq):
    nodes = ",".join("#" if tok is None else str(tok) for tok in seq)
    text = "{%s}" % nodes
    drawtree.draw_level_order(text)


def draw_tree_using_mermaid(seq):
    # build the binary tree
    root = build_tree(seq)

    # generate the Mermaid script
    script = build_mermaid_script(root)
    with tempfile.NamedTemporaryFile(
        prefix="tree_", suffix=".mmdc", delete=False, mode="wt"
    ) as script_path:
        script_path.file.write(script)

    # generate the picture and display it
    png_path = tempfile.NamedTemporaryFile(prefix="tree_", suffix=".png", delete=False)
    png_path.close()
    subprocess.run(
        ["mmdc", "--input", script_path.name, "--output", png_path.name],
        capture_output=True,
        text=True,
        check=True,
    )
    display_png_file(png_path.name)


def add_node_edges(graph: Digraph, node: TreeNode):
    node_id = str(id(node))
    graph.node(node_id, label=str(node.val))

    if node.left:
        left_id = str(id(node.left))
        graph.edge(node_id, left_id)
        add_node_edges(graph, node.left)

    if node.right:
        right_id = str(id(node.right))
        graph.edge(node_id, right_id)
        add_node_edges(graph, node.right)


def build_graph(root: Optional[TreeNode]) -> Optional[Digraph]:
    if root is None:
        return None

    graph = Digraph()
    graph.attr("node", shape="circle")
    add_node_edges(graph, root)
    return graph


def normalize_sequence(seq: list[str]) -> list[str]:
    def normalize(token: str):
        try:
            return json.loads(token)
        except json.JSONDecodeError:
            return token

    return [normalize(token) for token in seq]


def draw_tree_using_graphviz(seq: list):
    root = build_tree(seq)
    graph = build_graph(root)

    if graph is None:
        print("empty tree")
    else:
        out_file = tempfile.NamedTemporaryFile(delete=False)
        out_file.close()
        out_path = f"{out_file.name}.png"

        graph.render(filename=out_file.name, format="png", cleanup=True)
        display_png_file(out_path)


@click.command
@click.argument("seq", nargs=-1)
def main(seq):
    seq = normalize_sequence(seq)
    if shutil.which("mmdc"):
        draw_tree_using_mermaid(seq)
    elif shutil.which("dot"):
        draw_tree_using_graphviz(seq)
    else:
        draw_tree_using_text(seq)
