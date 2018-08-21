import networkx as nx
import matplotlib.pyplot as plt
import Initializer as ini
import Main as main
import Evaluation as eval

def draw_cluster(graph_topology):

   # pos = nx.spring_layout(Graph, iterations=10)
   # nx.draw_networkx_nodes(Graph,pos, cmap=plt.get_cmap('Blues'), node_size = 200)
   # nx.draw_networkx_edges(Graph,pos, edge_cmap=plt.get_cmap('jet'))
   # nx.draw_networkx_labels(Graph,pos)

    node_color = []
    # for each node in the graph
    for node in graph_topology.nodes(data=True):
        if node[1] != None:
            node_color.append('red')
        if node[1]['cluster_ID'] != None:
            node_color.append('blue')
        if node[1]['placed'] == True:
            node_color.append('yellow')

    pos =   nx.get_node_attributes(graph_topology, 'pos')
    pos = nx.spring_layout(graph_topology, iterations=10)
    nx.draw_networkx_nodes(graph_topology, cmap=plt.get_cmap('Blues'), node_size = 100, node_color=node_color, pos=pos)
    nx.draw_networkx_edges(graph_topology,pos, edge_cmap=plt.get_cmap('jet'))
    nx.draw_networkx_labels(graph_topology,pos)

    #nx.draw(graph_topology, with_labels=False, node_size=25, node_color=node_color)
    plt.show()


'''
    # if the node has the attribute group1
    if 'group1' in node[1]['group']:
        node_color.append('blue')

    # if the node has the attribute group1
    elif 'group2' in node[1]['group']:
        node_color.append('red')

    # if the node has the attribute group1
    elif 'group3' in node[1]['group']:
        node_color.append('green')

    # if the node has the attribute group1
    elif 'group4' in node[1]['group']:
        node_color.append('yellow')

    # if the node has the attribute group1
    elif 'group5' in node[1]['group']:
        node_color.append('orange')
'''

    # draw graph with node attribute color


#Print the graph in order to see allocated nodes.
def print_topology(allocated_topology, Storage_requirments):

    count = 0
    for node in allocated_topology.nodes(data=True):
        if node[1]['placed'] == True:
            count = count + node[1]['storage_usage']
            print(node)
    #eval.eval_usage_DS(count, sum(Storage_requirments))
    print('storage-usage',count)
    print('storage requirments',sum(Storage_requirments))

    return

