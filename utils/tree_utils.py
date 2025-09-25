import networkx as nx
import matplotlib.pyplot as plt

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Noto Sans CJK SC', 'Arial']  # 优先使用 SimHei，备选 Noto Sans CJK SC
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def visualize_tree(root, filename="tree", title="二叉树"):
    """
    使用NetworkX和Matplotlib可视化二叉树，父节点居中，边为直线，节点为浅绿色，正确显示左（蓝色）右（红色）边，支持单节点，生成PNG图像。
    
    参数:
        root: 树的根节点（Node对象，包含value, left, right属性）
        filename: 输出文件名（不含扩展名，默认为"tree"）
        title: 图的标题（显示在图像顶部，默认为"二叉树"）
    """
    G = nx.DiGraph()
    pos = {}
    labels = {}
    edges = []
    edge_colors = []
    edge_labels = {}
    
    # 计算节点位置和边
    def compute_positions(node, x=0, y=0, dx=1.0, dy=1.0):
        if not node:
            return
        # 添加当前节点
        G.add_node(node.value)
        pos[node.value] = (x, y)
        labels[node.value] = str(node.value)
        # 计算子节点位置
        left_dx = dx / 2
        if node.left:
            edges.append((node.value, node.left.value))
            edge_colors.append('dodgerblue')  # 左子树边：鲜蓝色
            edge_labels[(node.value, node.left.value)] = 'L'
            compute_positions(node.left, x - left_dx, y - dy, left_dx, dy)
        if node.right:
            edges.append((node.value, node.right.value))
            edge_colors.append('crimson')  # 右子树边：深红色
            edge_labels[(node.value, node.right.value)] = 'R'
            compute_positions(node.right, x + left_dx, y - dy, left_dx, dy)
    
    # 创建图表
    plt.figure(figsize=(8, 6))
    plt.title(title, fontsize=16, pad=20)
    
    if root:
        compute_positions(root)
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_shape='o', node_color='lightgreen', 
                              node_size=500, edgecolors='black', linewidths=1)
        # 绘制边
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, width=2)
        # 绘制节点标签
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=12, font_family='SimHei')
        # 绘制边标签
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    else:
        plt.text(0.5, 0.5, "空树", fontsize=12, ha='center', va='center')
    
    # 保存图像
    plt.savefig(f"{filename}.png", bbox_inches='tight', dpi=100)
    plt.close()
    return G