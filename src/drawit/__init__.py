import collections
import io
import itertools
import json
from typing import Optional

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


def bfs(root: Optional[TreeNode]):
    que = collections.deque()
    que.append((root))

    while que:
        node = que.popleft()
        if node is None:
            continue

        yield node
        que.append((node.left))
        que.append((node.right))


def build_id(node: Optional[TreeNode]) -> str:
    return f"node_{node.val}"


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

    # format the null nodes
    buf.write("\n")
    for i in range(null_count):
        buf.write(f"style null_{i} fill:none,stroke:none,color:none\n")

    return buf.getvalue()


@click.command
@click.argument("seq", nargs=-1)
def main(seq):
    seq = [json.loads(x) for x in seq]
    root = build_tree(seq)
    script = build_mermaid_script(root)
    print(script)
