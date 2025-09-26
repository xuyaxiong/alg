import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def visualize_graph(graph, path_edges=None, source=0, save_path="graph", title="图可视化（红色边：最短路径树）"):
    """
    可视化图或最短路径树，支持中文显示，并保存为 PNG 文件，自动添加 .png 后缀。
    
    参数:
        graph: 邻接表表示的图，graph[u] = [(v, w), ...] 表示从 u 到 v 的边权为 w
        path_edges: 可选，最短路径树的边列表 [(u, v, w), ...]，如 Dijkstra 返回的 path_edges
        source: 源点，用于高亮显示，默认 0
        save_path: 保存 PNG 文件的路径或文件名（不含后缀时自动添加 .png），默认 'graph'
        title: 图表标题，支持中文，默认 '图可视化（红色边：最短路径树）'
    
    返回:
        None，显示图形并保存为 PNG
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']  # 优先使用 SimHei
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 确保 save_path 以 .png 结尾
    if not save_path.lower().endswith('.png'):
        save_path = save_path + '.png'
    
    # 创建有向图
    G = nx.DiGraph()
    
    # 添加节点
    V = len(graph)
    G.add_nodes_from(range(V))
    
    # 添加所有图的边
    for u in range(V):
        for v, w in graph[u]:
            G.add_edge(u, v, weight=w)
    
    # 设置布局
    pos = nx.spring_layout(G)
    
    # 创建图形
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='SimHei')
    
    # 绘制所有边（灰色）
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1)
    
    # 如果提供了 path_edges，绘制最短路径树的边（红色加粗）
    if path_edges:
        path_edge_list = [(u, v) for u, v, _ in path_edges]
        nx.draw_networkx_edges(G, pos, edgelist=path_edge_list, edge_color='red', width=2)
    
    # 绘制边权值
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_family='SimHei')
    
    # 高亮源点
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='lightgreen', node_size=500)
    
    # 设置标题
    plt.title(title, fontsize=14, fontfamily='SimHei')
    plt.axis('off')  # 关闭坐标轴
    
    # 保存为 PNG
    try:
        plt.savefig(save_path, format='png', dpi=300, bbox_inches='tight')
        print(f"图形已保存为 {save_path}")
    except Exception as e:
        print(f"保存图形失败：{e}")
    
    # 显示图形
    plt.show()