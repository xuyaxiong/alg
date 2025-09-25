import sys
import os

# 添加项目根目录到 sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from utils.tree_utils import visualize_tree


# 定义节点类
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# 定义二叉搜索树类
class BinarySearchTree:
    def __init__(self):
        self.root = None

    # 插入新节点
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)
        return node

    # 查找节点
    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    # 删除节点
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # 无子节点或单子节点
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # 两个子节点
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.value)
        return node

    # 找到最小节点（用于删除操作）
    def _find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # 中序遍历（输出升序序列）
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)


# 示例用法
if __name__ == "__main__":
    bst = BinarySearchTree()
    # 插入节点
    values = [5, 3, 7, 1, 4, 9]
    for value in values:
        bst.insert(value)
        visualize_tree(bst.root, f"插入{value}", f"插入{value}")

    # 删除节点
    bst.delete(3)
    visualize_tree(bst.root, f"删除3", f"删除3")
