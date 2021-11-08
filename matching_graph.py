import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class Fragment:
    def __init__(self, id):
        self.id = id
        self.filename = ''
        self.fractures = []


class Fracture:
    def __init__(self, id, parent_id):
        self.id = id
        self.parent_id = parent_id
        self.filename = ''
        self.matrix = np.identity(4)
        self.pair = None

    def output(self):
        print('='*40 + '>')
        print('fracture id: ', self.id)
        print('parent id: ', self.parent_id)
        if self.pair:
            print('pair id: ', self.pair.id)
        print('transform matrix: \n', self.matrix)


COLOR = ['r', 'g', 'b', 'c', 'y', 'm', 'b', 'cornsilk']

def load_match_pair(match_pair_file_name):
    match_pair = {}
    fragments = {}
    content = open(match_pair_file_name)
    for pair in content:
        parent_id1 = int(pair.split('&')[0].split('-')[1])
        parent_id2 = int(pair.split('&')[1].strip('\n').split('-')[1])
        fracture1 = Fracture(pair.split('&')[0], parent_id1)
        fracture2 = Fracture(pair.split('&')[1].strip('\n'), parent_id2)
        fracture1.pair = fracture2
        fracture2.pair = fracture1
        if parent_id1 not in fragments:
            fragments[parent_id1] = [fracture1]
        else:
            fragments[parent_id1].append(fracture1)
            
        if parent_id2 not in fragments:
            fragments[parent_id2] = [fracture2]
        else:
            fragments[parent_id2].append(fracture2)

        match_pair[pair.split('&')[0]] = pair.split('&')[1].strip('\n')
    return match_pair, fragments


def abstract_pairs(pairs):
    labels = {}
    nodes = []
    edges = []
    colors = []
    i = 0;
    for key in pairs.keys():
        labels[i] = key
        labels[i + 1] = pairs[key]
        colors.append(COLOR[int(key.split('-')[1]) % len(COLOR)])
        colors.append(COLOR[int(pairs[key].split('-')[1]) % len(COLOR)])
        nodes.append(i)
        nodes.append(i + 1)
        edges.append((i, i + 1))
        i += 2
    return nodes, edges, labels, colors


def draw_graph(dir, id, post):
    G = nx.cubical_graph()
    pos = nx.spring_layout(G)  # positions for all nodes
    pairs, fragments = load_match_pair(dir + id + post)
    for key in fragments:
        for fracture in fragments[key]:
            fracture.output()
    nodes, edges, labels,colors = abstract_pairs(pairs)
    # nodes
    options = {"node_size": 1000, "alpha": 0.8}
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=colors, **options)

    # edges
    # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=edges,
        width=8,
        alpha=0.5,
        edge_color="goldenrod",
    )

    # for key in pair.keys():
    #     g.add_node(key)
    #     g.add_node(pair[key])
    #     g.add_edge(key, pair[key])
    # nx.draw(g, with_labels=True)
    nx.draw_networkx_labels(G, pos, labels, font_size=16)
    plt.show()


if __name__ == "__main__":
    draw_graph('./match-pair/', 'plate-1', '.txt')