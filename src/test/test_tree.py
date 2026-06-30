from drawit.tree import TreeNode


def create_tree():
    root = TreeNode(5)
    assert root.val == 5
    assert root.left is None
    assert root.right is None
