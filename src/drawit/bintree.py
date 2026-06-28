import itertools
import subprocess
import json
import tempfile
import graphviz
import webbrowser
import click


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(seq):
    def _build(value):
        if value is None:
            return None
        return TreeNode(value)

    if not seq:
        return None

    if not seq:
        return None

    sides = itertools.cycle(["left", "right"])
    seq = iter(seq)
    root = _build(next(seq))
    que = [root]

    for side, value in zip(sides, seq):
        node = _build(value)
        setattr(que[0], side, node)
        if node:
            que.append(node)
        if side == "right":
            que.pop(0)

    return root



def build_graph(node: TreeNode, g: graphviz.Digraph, parent_id=None, edge_label=""):
    if node is None:
        return

    # Use id(node) to make node IDs unique even if values repeat
    node_id = str(id(node))
    g.node(node_id, label=str(node.val))

    if parent_id is not None:
        g.edge(parent_id, node_id, label=edge_label)

    build_graph(node.left, g, node_id, "L")
    build_graph(node.right, g, node_id, "R")



def iterm_display(path: str):
    subprocess.run(["imgcat", path])
@click.command
@click.option("-v", "--viewer", type=click.Choice(["iterm", "web"]), default="iterm")
@click.argument("seq", nargs=-1)
def main(viewer, seq):
    seq = [json.loads(x) for x in seq]
    root = build_tree(seq)
    g = graphviz.Digraph(format="png")
    build_graph(root, g)

    output = tempfile.NamedTemporaryFile(delete=False, prefix="bintree_")
    output.close()
    output_path =  f"{output.name}.png"
    g.render(output.name, cleanup=True)

    if viewer == "iterm":
        iterm_display(output_path)
    elif viewer == "web":
        webbrowser.open_new_tab(f"file://{output_path}")

