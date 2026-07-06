import collections
import itertools
import json
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def insert(self, val):
        if self.val == val:
            raise ValueError(f"Duplicate value: {val}")

        if val < self.val:
            if self.left is None:
                self.left = TreeNode(val)
            else:
                self.left.insert(val)
        else:
            if self.right is None:
                self.right = TreeNode(val)
            else:
                self.right.insert(val)


def build_tree(seq):
    def _build(value):
        if value is None:
            return None
        return TreeNode(value)

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


def build_binary_search_tree(seq: list):
    if not seq:
        return None

    it = iter(seq)
    root = TreeNode(next(it))
    for value in it:
        root.insert(value)

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


def max_depth(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    left_depth = max_depth(root.left) + 1
    right_depth = max_depth(root.right) + 1
    return max(left_depth, right_depth)


def serialize(root: Optional[TreeNode]) -> str:
    queue = collections.deque()
    if root is not None:
        queue.append(root)

    out = []
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)

    # Remove trailing nulls
    while out[-1] is None:
        out.pop()
    return json.dumps(out)
