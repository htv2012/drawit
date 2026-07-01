import collections
import itertools
from typing import Optional


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


def build_id(node: TreeNode) -> str:
    return f"node_{node.val}"
