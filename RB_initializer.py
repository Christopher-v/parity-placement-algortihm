import networkx as nx
import math
import operator
from random import randint
import pandas as pd
import SA_DS_placement as sa_ds
import time

#This is the seconds constructive heuristic which places the parity-blocks

def find_highest_node_in_cluster(solution):
#This is algortihm 4 - Find biggest node in each clique

    #This method finds the node with highest storage capacity in the solution.
    #This is done because the redundant blocks need to be the atleast the same size as the biggest node in a cluster

    assert len(solution) > 0
    #Find all nodes in a cluster.

    cluster_count = []
    node_count = []

    while True:
        #Iterates the solution
        for u, i in enumerate(solution[:-1]):
            current_node = solution[u][0]
            next_node    = solution[u+1][0]
            #iterates the solution for other nodes and..
            for j, L in enumerate(solution):
                search_node = solution[j][0]
                if current_node != next_node:
                    #..picks the ones with within the same cluster.
                    assert isinstance(current_node, int)
                    referece_cluster = solution[u][1]['cluster_ID']
                    temp_cluster     = solution[j][1]['cluster_ID']
                    #Here we pick nodes with the same cluster ID as the current node.
                    if temp_cluster == referece_cluster:
                        assert solution[j][1]['cluster_ID'] != None
                        assert solution[u][1]['cluster_ID'] != None
                        highest_storage = 0
                        temp_node     = solution[j][1]['storage_capacity']
                        node_count.append(search_node)
                        #looking for the node with highest storage - by matching them
                        if temp_node > highest_storage:
                            highest_storage = + temp_node
                            #if the search node has been visited - break the loop
                            cluster_count.append((referece_cluster, highest_storage, solution[j][0]))
                            #print(cluster_count)
                            continue

                        if referece_cluster in cluster_count[0]:
                            print('break')
                            break
                    else:
                        continue

        #to avoid duplicates the list is converted to a set

        biggest_cluster_node = remove_duplicates(cluster_count)


        #biggest cluster node is: 1:the cluster 2: its highest storage cap 3: one of the nodes with the highest cap.
        return biggest_cluster_node

def place_GB(biggest_cluster_node, allocated_network_topology):
    #Thisis Algortihm 5 - Place group block
    #This method finds the group block of a cluster and stores it in a neighbouring cluster.

    assert len(biggest_cluster_node) > 0

    print('biggest_cluster_node',biggest_cluster_node)
    cluster_nodes = list.copy(biggest_cluster_node)

    #this is not root.
    r_blocks = []

    #Find the neighbouring cluster from the current node.
    while cluster_nodes is not None:
        print('-----went here----')
        cluster_node = cluster_nodes.pop()
        #Making a BFS from the current node (the one with the highest capacity first)
        root = cluster_node[2]
        edges = nx.bfs_edges(allocated_network_topology, root)
        nodes = [root] + [v for u, v in edges]
        assert len(nodes) > 0

        #print(nodes)
        #This  BFS to find a node outside of the cluster and find a node inside a another clusters.
        for u, i in enumerate(nodes):
            search_node          = nodes[u]
            current_node         = cluster_node[2]
            search_cluster       = allocated_network_topology.node[search_node]['cluster_ID']
            current_cluster      = allocated_network_topology.node[current_node]['cluster_ID']
            current_cluster_req  = allocated_network_topology.node[search_node]['storage_capacity']
            search_cluster_cap   = allocated_network_topology.node[search_node]['storage_capacity']
            search_cluster_usage = allocated_network_topology.node[search_node]['placed']
            #Finding the search nodes' neighbours, to ensure that is has two neighbours.
            neighbours_neighbours = list(allocated_network_topology.neighbors(search_node))
            u = len(neighbours_neighbours)
            u -= 1

            #Constraints - node is not in current cluster AND is in a cluster AND is vacant AND has a capacity hihgher than the node
            if search_cluster != current_cluster and search_cluster is not None and search_cluster_cap >= current_cluster_req and u > 2 and search_cluster_usage == False:
                #Setting in: node - the node's cluster - the cluster which it replicates and the redundant-block type - group block
                try:
                    r_blocks.append([search_node, search_cluster, current_cluster, 'R_blocks'])

                    cluster_node = cluster_nodes.pop()
                    #Making a BFS from the current node (the one with the highest capacity first)
                    root = cluster_node[2]
                    edges = nx.bfs_edges(allocated_network_topology, root)
                    nodes = [root] + [v for u, v in edges]
                    assert len(nodes) > 0


                    print('r-block placed', search_node)
                    continue
                except KeyError and IndexError:
                    break

            elif u >= len(nodes):
                print('redundant-block not placed')
                break
            else:
                continue

                #Else: try the neighbour in cluster.
                #Else: Worst-case - put it outside of cluster.
                #DO:  AND find a vacant redundant block in current cluster. (These two clusters should be marked neighoburs)
        print('group blocks', r_blocks)
        return r_blocks

def find_neighbour_cluster(r_blocks, allocated_network_topology):
    assert len(r_blocks) > 0
    #This is algortihm 6 - Find neighbour clique
    #This method finds the neighbouring cluster from a redundant block.

    neighbours = []
    latencies = []

    #Looking though the redundant blocks in order to find the closest clusters.
    for u, i in enumerate(r_blocks[:-1]):
        search_block = r_blocks[u][0]
        lowest_latency = math.inf
        current_cluster       = allocated_network_topology.node[search_block]['cluster_ID']
        #print('search_block',search_block)
        #print('r_blocks', r_blocks)

        #Looking through each node that reaches a redundant blocks- in order to find its closest neighbour
        for j, L in enumerate(r_blocks):
            target = r_blocks[j][0]
            target_cluster = allocated_network_topology.node[target]['cluster_ID']

            #Finding two close clusters. by: checking shortest path from all clusters to each other. - picking the shortest path.
            if target_cluster != current_cluster:
                #print(target)
                try:
                    latency =  nx.shortest_path_length(allocated_network_topology, source=search_block, target=target)

                except nx.NetworkXNoPath:
                    print('no path between', search_block, 'and', target)
                    pass
                #finding the lowest latency between nodes - in order to find the neighbouring cluster
                if latency <= lowest_latency:
                    lowest_latency = latency
                    latencies.append([lowest_latency, target, search_block])
                elif latency >= lowest_latency:
                    continue

    #iterating the list of neighbours to find the closest one for each search block.
    for u, i in enumerate(latencies[:-1]):
        assert len(latencies) > 0
        search_block2 = latencies[u][2]
        target2       = latencies[u][1]
        next_block2   = latencies[u+1][2]
        lowest_latency2 = math.inf
        while search_block2 is not next_block2:
            latency2 = latencies[u][0]
            if lowest_latency2 > latency:
                lowest_latency2 = latency2
                #These two blocks are close together.
                neighbours.append([target2, search_block2])

                break
    #print('group blocks neighbours',neighbours)

    #Using a set to remove unnesecarry duplicates. - this leaves only pairs of neighbours
    set_neighbours = ([ [k] + v for (k, v) in dict( [ [a[0], a[1:]] for a in reversed(neighbours) ] ).items() ])

    return set_neighbours

def place_SgB(r_blocks, neighbours, allocated_network_topology, solution):
    #This algortihm 7 - Place sub group blocks
    #This method places a SgB blocks based on two neighbouring redundant-blocks found in the previous methods. -
    #The neighbours is said to be closest to each other. - Hence the SgB should recover these two.
    #To find a close neighbouring cluster which can contain the SgB, a BFS is used from one a the two neighbours.
    #Also the SgB-blocks is placed based on constraints -
    assert len(neighbours) > 0

    placed = False
    SgB_blocks = []

    while placed != True:

        print('neighbours',neighbours)

        try:
            neighbour = neighbours.pop()
        except IndexError:
            print('placed')
            placed = True
            break

        if check_cluster2(solution, neighbour[1], allocated_network_topology) >= 3:
            print('passed-1')
            root = neighbour[1]
            edges = nx.bfs_edges(allocated_network_topology, root)
            nodes = [root] + [v for u, v in edges]
            rr = len(nodes)
            rr -= 1
            assert len(nodes) > 0

            for u, i in enumerate(nodes):
                search_node          = nodes[u]
                r_node1              = neighbour[0]
                r_node2              = neighbour[1]
                search_cluster       = allocated_network_topology.node[search_node]['cluster_ID']
                current_cluster      = allocated_network_topology.node[r_node1]['cluster_ID']
                current_cluster_req  = allocated_network_topology.node[r_node1]['storage_capacity']
                search_cluster_cap   = allocated_network_topology.node[search_node]['storage_capacity']
                search_cluster_usage = allocated_network_topology.node[search_node]['placed']
                #Finding the search nodes' neighbours, to ensure that is has two neighbours.
                neighbours_neighbours = list(allocated_network_topology.neighbors(search_node))
                nn = len(neighbours_neighbours)
                nn -= 1

                #Constraints - node is not in current cluster AND is in a cluster AND is vacant AND has the capacity
                if search_cluster != current_cluster and search_cluster is not None and search_cluster_cap >= current_cluster_req and nn > 2 and search_cluster_usage == False and check_r_blocks(r_blocks, search_node) == False:
                    print('passed3')

                    #Setting in: node - the node's cluster -, the source node - , the cluster which it replicates and the redundant-block type - group block
                    #search_node = the actual sgB-block, r_node1 = one of the redundant blocks and r_node2 is the redundant block in the neighbouring cluster.
                    SgB_blocks.append([search_node, r_node1, r_node2, 'SgB_blocks'])
                    print('sgd block placed')
                    break
        #---------------------------------------

        if check_cluster2(solution, neighbour[0], allocated_network_topology) >= 3:
            print('passed-2')
            root = neighbour[0]
            edges = nx.bfs_edges(allocated_network_topology, root)
            nodes = [root] + [v for u, v in edges]
            rr = len(nodes)
            rr -= 1
            assert len(nodes) > 0

            for u, i in enumerate(nodes):
                search_node          = nodes[u]
                r_node1              = neighbour[0]
                r_node2              = neighbour[1]
                search_cluster       = allocated_network_topology.node[search_node]['cluster_ID']
                current_cluster      = allocated_network_topology.node[r_node1]['cluster_ID']
                current_cluster_req  = allocated_network_topology.node[r_node1]['storage_capacity']
                search_cluster_cap   = allocated_network_topology.node[search_node]['storage_capacity']
                search_cluster_usage = allocated_network_topology.node[search_node]['placed']
                #Finding the search nodes' neighbours, to ensure that is has two neighbours.
                neighbours_neighbours = list(allocated_network_topology.neighbors(search_node))
                nn = len(neighbours_neighbours)
                nn -= 1

                #Constraints - node is not in current cluster AND is in a cluster AND is vacant AND has the capacity
                if search_cluster != current_cluster and search_cluster is not None and search_cluster_cap >= current_cluster_req and nn > 2 and search_cluster_usage == False and check_r_blocks(r_blocks, search_node) == False:

                    print('passed3')
                    #Setting in: node - the node's cluster -, the source node - , the cluster which it replicates and the redundant-block type - group block
                    #search_node = the actual sgB-block, r_node1 = one of the redundant blocks and r_node2 is the redundant block in the neighbouring cluster.
                    SgB_blocks.append([search_node, r_node1, r_node2, 'SgB_blocks'])
                    print('sgd block placed')
                    break

        else:
            print('skipped')

    #BFS to a close cluster which is not in the two neighoburing clusters.

    print('sub_group_blocks', SgB_blocks)
    return SgB_blocks

def place_Global_B(r_blocks, biggest_cluster_node ,allocated_network_topology):
#This is algortihm 8 - Place Global-group blocks
    G_block = []

    #highest_node = max((biggest_cluster_node),key=)

    max_highest_node = max(enumerate(biggest_cluster_node), key=operator.itemgetter(1))
    highest_node = max_highest_node[1][1]

    #Place the global block in the center of the graph. - if not occupied, else place in one of the neighbours.
    giant_component = max(nx.connected_component_subgraphs(allocated_network_topology), key=len)
    find_center_node = nx.center(giant_component)
    center_node = find_center_node[0]

    while True:
        cap    = allocated_network_topology.node[center_node]['storage_capacity']
        placed = allocated_network_topology.node[center_node]['placed']

        #Finding the search nodes' neighbours, to ensure that is has two neighbours.
        neighbours_neighbours = list(allocated_network_topology.neighbors(center_node))
        u = len(neighbours_neighbours)
        u -= 1

        if cap >= highest_node and placed == False and u > 2 and check_r_blocks(r_blocks, center_node) == False:

            G_block.append([center_node, 'G_block'])
            break

            #if the center node is filled - take a random node's  neigbours from the graph
        else:
            nodes_neighbours = list(allocated_network_topology.neighbors(center_node))
            n = len(nodes_neighbours)
            n -= 1
            random_neighbour_index = randint(0,n)
            random_neighbour      = nodes_neighbours[random_neighbour_index]
            center_node = random_neighbour
            continue
    assert len(G_block) > 0
    print('Global block', G_block)
    return G_block

def check_r_blocks(r_blocks, node):


    r_block_check = False
    n = len(r_blocks)

    for u, i in enumerate(r_blocks):
        search_block = r_blocks[u][0]

        if node == search_block:
            r_block_check = True
            #print(search_block)
            break

    return r_block_check

def check_cluster(allocated_network_topology, node):

    cluster_contains = 1

    neighbours_neighbours = list(allocated_network_topology.neighbors(node))
    u = len(neighbours_neighbours)
    u -= 1

    search_id = allocated_network_topology.node[node]['cluster_ID']
    for i in (neighbours_neighbours):
        print('checking cluster')
        target_id = allocated_network_topology.node[i]['cluster_ID']

        #print(node)
        print(allocated_network_topology.node[i])
        #print('neighbours',neighbours_neighbours)

        #picks the random neighbour in the graph
        if search_id == target_id:
            cluster_contains = cluster_contains + 1
            #print('search',search_id)
            print('number of nodes in cluster',cluster_contains)
            continue

        elif i >= u and cluster_contains == 1:
            cluster_contains = 1
            break

    print('cluster_check',cluster_contains)
    return cluster_contains

def check_cluster2(solution, node, allocated_network_topology):

    cluster_contains = 1

    L = len(solution)
    L -= 1

    search_id = allocated_network_topology.node[node]['cluster_ID']
    print('search_id', search_id)
    for u, i in enumerate(solution):
        target_id = solution[u][1]['cluster_ID']

        if search_id == target_id:
            cluster_contains = cluster_contains + 1
            #print('search',search_id)
            print('number of nodes in cluster',cluster_contains)
            continue

        elif u >= L and cluster_contains == 1:
            cluster_contains = 1
            print('skipped')
            break

    print('cluster_check',cluster_contains)
    return cluster_contains


def remove_duplicates(cluster_count):

    d = []
    seen = set()
    for bact in cluster_count:
        if bact[0] not in seen: # membership test
            seen.add(bact[0])
            d.append(bact)

    #print('d!!!!!!!!!!!!!!!!!',d)
    return d


