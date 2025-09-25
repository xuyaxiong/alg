import sys
import os

# 添加项目根目录到 sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from utils.tree_utils import visualize_tree


class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # 节点高度（叶子节点高度为1）


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        """返回节点高度（空节点为0）"""
        return node.height if node else 0

    def balance_factor(self, node):
        """计算平衡因子（左子树高度 - 右子树高度）"""
        return self.height(node.left) - self.height(node.right) if node else 0

    def update_height(self, node):
        """更新节点高度"""
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def right_rotate(self, y):
        """对节点 y 进行右旋"""
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        """对节点 x 进行左旋"""
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, root, value):
        """插入键值并保持平衡"""
        # 标准 BST 插入
        if not root:
            return AVLNode(value)
        if value < root.value:
            root.left = self.insert(root.left, value)
        elif value > root.value:
            root.right = self.insert(root.right, value)
        else:
            return root  # 不允许重复键

        # 更新高度
        self.update_height(root)

        # 检查平衡因子
        balance = self.balance_factor(root)

        # 左左（LL）情况
        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)
        # 右右（RR）情况
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)
        # 左右（LR）情况
        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # 右左（RL）情况
        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_node(self, root):
        """找到子树中的最小节点"""
        current = root
        while current.left:
            current = current.left
        return current

    def delete(self, root, value):
        """删除键值并保持平衡"""
        if not root:
            return root
        if value < root.value:
            root.left = self.delete(root.left, value)
        elif value > root.value:
            root.right = self.delete(root.right, value)
        else:
            # 找到要删除的节点
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            # 有两个子节点
            min_node = self.get_min_node(root.right)
            root.value = min_node.value
            root.right = self.delete(root.right, min_node.value)

        # 更新高度
        self.update_height(root)

        # 检查平衡因子
        balance = self.balance_factor(root)

        # 左左（LL）情况
        if balance > 1 and self.balance_factor(root.left) >= 0:
            return self.right_rotate(root)
        # 左右（LR）情况
        if balance > 1 and self.balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # 右右（RR）情况
        if balance < -1 and self.balance_factor(root.right) <= 0:
            return self.left_rotate(root)
        # 右左（RL）情况
        if balance < -1 and self.balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, value):
        """查找键值"""
        if not root or root.value == value:
            return root
        if value < root.value:
            return self.search(root.left, value)
        return self.search(root.right, value)

    def insert_key(self, value):
        """公共插入接口"""
        self.root = self.insert(self.root, value)

    def delete_key(self, value):
        """公共删除接口"""
        self.root = self.delete(self.root, value)

    def search_key(self, value):
        """公共查找接口"""
        return self.search(self.root, value)

    def inorder(self, root, result):
        """中序遍历（验证树结构）"""
        if root:
            self.inorder(root.left, result)
            result.append(root.value)
            self.inorder(root.right, result)

    def print_inorder(self):
        """打印中序遍历"""
        result = []
        self.inorder(self.root, result)
        print("中序遍历:", result)


# 测试代码
if __name__ == "__main__":
    avl = AVLTree()
    keys = [10, 20, 30, 25, 28, 27]
    for value in keys:
        avl.insert_key(value)
        print(f"插入 {value} 后", end=" ")
        avl.print_inorder()
        visualize_tree(avl.root, f"插入{value}", f"插入{value}")

    print("\n查找 25:", "找到" if avl.search_key(25) else "未找到")

    avl.delete_key(25)
    print("删除 25 后", end=" ")
    avl.print_inorder()
    visualize_tree(avl.root, f"删除25", f"删除25")
