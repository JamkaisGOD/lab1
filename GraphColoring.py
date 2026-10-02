import random
import itertools
import networkx as nx
import matplotlib.pyplot as plt

def is_valid_coloring(graph, coloring):
    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            if coloring[node] == coloring[neighbor]:
                return False
    return True

def greedy_coloring(graph):
    coloring = {}
    for node in graph.nodes():
        available_colors = set(range(len(graph.nodes())))
        for neighbor in graph.neighbors(node):
            if neighbor in coloring:
                available_colors.discard(coloring[neighbor])
        coloring[node] = min(available_colors)
    return coloring
n_nodes = 20

G = nx.Graph()
G.add_nodes_from(range(n_nodes))

for i in range(n_nodes):
    for j in range(i + 1, n_nodes):
        if random.random() < 0.1:
            G.add_edge(i, j)


coloring_result = greedy_coloring(G)

print("Coloring Result:", coloring_result)
print('Valid:', is_valid_coloring(G, coloring_result))
print('K:', len(set(coloring_result.values())))

color_map = [coloring_result[node] for node in G.nodes()]
nx.draw(G, node_color=color_map, with_labels=True, font_weight='bold')
plt.show()