import sys
import os

# 添加项目根目录到 sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from utils.graph_utils import visualize_graph
import heapq


def dijkstra(graph, source=0):
    V = len(graph)
    dist = [float("inf")] * V  # 到各顶点的距离
    dist[source] = 0
    parent = [-1] * V  # 前驱节点
    min_heap = [(0, source, -1)]  # (距离, 顶点, 父节点)
    visited = [False] * V
    path_edges = []  # 存储最短路径树边: (u, v, weight)

    while min_heap:
        d, u, p = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True
        if p != -1:  # 跳过源点
            # 查找边权重
            for v, w in graph[p]:
                if v == u:
                    path_edges.append((p, u, w))
                    break
        for v, w in graph[u]:
            if not visited[v] and dist[v] > d + w:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(min_heap, (dist[v], v, u))

    return dist, path_edges


if __name__ == "__main__":
    graph = [
        [(1, 2), (2, 3)],  # 0
        [(0, 2), (2, 1), (3, 1)],  # 1
        [(0, 3), (1, 1), (3, 2)],  # 2
        [(1, 1), (2, 2)],  # 3
    ]
    dist, path_edges = dijkstra(graph, 0)
    visualize_graph(graph, path_edges)
