import random
from random import randint
import networkx as nx
import math
import matplotlib.pyplot as plt
import Evaluation as eval

#This is local search heuristic Simulated Annealing.

def anneal_DS(old_solution, allocated_network_topology):
#This is algortihm 9 - Optimize DDS placement
    #print('----------SA---------')

    #get the cost from the initialized solution.
    #old_solution = solution(allocated_network_topology)
    old_cost = cost(old_solution, allocated_network_topology)

    T = 1.0
    T_min = 0.000500
    alpha = 0.9
    c = 0.25
    linear_factor = 0.25
    i = 1
    while T > T_min:

        print('/')
        #indicating the max iteration number for the algorithm.

        while i < 300:
            #Logarithmic schedule
            #T = c / (math.log(i) + 1)
            #Linear schedule
            #T -= linear_factor
            #Adaptive
            #if T < 00.9:
            #    T = T * 0.9
            #elif T < 0.9:
            #    T = T * 0.5
            #else:

            #    T = T * 0.1

            new_solution = neighbor(old_solution,allocated_network_topology)
            new_cost = cost(new_solution, allocated_network_topology)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > random.random():
                #check this.
                old_solution = new_solution
                old_cost = new_cost
            i += 1
        #else:
        #    T = 0
            assert i == i

        T = T*alpha
        eval.eval_annealing_DS(T)

    print('DS-annealing finished!')
    print('cost',old_cost)

    #plt.show()
    assert cost != 0
    return old_solution


def solution(allocated_network_topology):
    #This method finds the existing solution based on the allocate_DS()
    #A list containing the placed nodes is derived from the graph - to minimize memory and iterations through the whole graph

    solution = []
    for node in allocated_network_topology.nodes(data=True):
        if node[1]['placed'] == True:
            n = len(node[1])
            for i in range(n):
                list.append(solution,node)
                break

    return solution

def neighbor(solution, allocated_network_topology):
    #This is algortihm 10 - Neighbour / New solution
    #this function finds the neighbour of the node. - We use a list representing the nodes in the graph.
    #To avoid copying the whole graph - hence, making it more scalable.

    assert len(solution) > 0

    old_solution = solution
    #Copying the old solution to manipulate
    new_solution = old_solution

    placed = False
    while placed == False:

        #picks random in solution
        #random_node = random.choice(solution_nodes)
        random_pick = random.choice(new_solution)
        random_node = random_pick[0]
        print('random node', random_node)

        #getting the random node's  neigbours from the graph
        nodes_neighbours = list(allocated_network_topology.neighbors(random_node))
        #Shuffling the nodes-neighbour
        random.shuffle(nodes_neighbours)

        n = len(nodes_neighbours)

        #--------------------------------------------------------------------

        assert len(nodes_neighbours) > 0
        #Checking if the random-nodes-neighbours is already in the list.
        for o, p in enumerate(nodes_neighbours):
            neighbouring_node = nodes_neighbours[o]
            print('neighbouring node',neighbouring_node)

            #Finding the neighbours neighbour in order to check for the connectivity contraint.
            neighbours_neighbours = list(allocated_network_topology.neighbors(neighbouring_node))
            u = len(neighbours_neighbours)
            u -= 1

            #trying to catch the exception - the exception means that the random-neighbour is not in the list.
            try:
                neighbouring_node_int = int(neighbouring_node)
                check = new_solution[neighbouring_node_int][0]
                break
            except IndexError:

                if allocated_network_topology.node[neighbouring_node]['storage_capacity'] >= allocated_network_topology.node[random_node]['storage_capacity'] and allocated_network_topology.node[neighbouring_node]['storage_usage'] == 0 and u > 2:

                    print('loop')
                    #switching the random node with the random node's neighbour. - look at RB_placement for optimized code.
                    #Checking all nodes in the network topology
                    for node in allocated_network_topology.nodes(data=True):
                        #picks the random neighbour in the graph
                        if node[0] == neighbouring_node:
                            print('loop2')
                            #takes the length of the node's attributes and appending it to the solution.
                            #print(neighbouring_node)
                            k = len(node[1])
                            list.append(new_solution,node)
                            print('placed node', node)
                            list.remove(new_solution, random_pick)
                            print('node removed', random_pick)
                            break
                    break

        #list.append(new_solution,nodes)
        print('new sol', new_solution)
        return new_solution

def cost(solution, allocated_network_topology):
    #This is algortihm 11 - Cost
    #Here goes the cost solution. This method calculates the cost from the new-solution generated by the previous method.

    assert len(solution) > 0

    latencies = []
    while True:
        #print('--went here--')
        #Iterates the new solution for the source node from which we want to find the latency
        for u, i in enumerate(solution[:-1]):
            current_source = int(solution[u][0])

            next_source    = solution[u+1][0]
            #iterates the new solution for the target want to find the latency to.
            for j, L in enumerate(solution):
                target = int(solution[j][0])
                #This picks the current source in the new_solution - this is done because we want to
                #compare the source node with every node in the same cluster/same DS.
                if current_source != next_source and target != current_source:
                    #And marks the latency between
                    assert isinstance(current_source, int)
                    assert isinstance(target, int)

                    #Here we pick the target with the same cluster ID as the current source.
                    if solution[j][1]['cluster_ID'] == solution[u][1]['cluster_ID']:
                        assert solution[j][1]['cluster_ID'] != None
                        assert solution[u][1]['cluster_ID'] != None
                        try:
                            latency =  nx.shortest_path_length(allocated_network_topology, source=current_source, target=target)
                            latencies.append(latency)
                            assert len(latencies) != 0
                        except nx.NetworkXNoPath:
                            print('no path between', current_source, 'and', target)
                            pass
                        continue
                        #else if current_cluster-ID does have a match
                    else:
                        assert isinstance(solution[j][1]['cluster_ID'], int)
                        continue
        cost = sum(latencies)
        eval.eval_topology_DS(cost)
        print(cost)
        #could MST been used here? - using the solution as a graph.
        return cost

def acceptance_probability(old_cost, new_cost, T):

    assert old_cost > 0
    assert new_cost > 0

    if new_cost < old_cost:
        acceptance_probability = 1.0

    else:
        try:
            acceptance_probability = math.exp((new_cost - old_cost) / T)
        except (OverflowError , ZeroDivisionError):
            print('overflowerror')
            acceptance_probability = float('inf')

    print('acceptance prop', acceptance_probability)
    print('temperature', T)
    return acceptance_probability

def place_optimization(solution, allocated_network_topology):
    assert len(solution) > 0
    ##This method places the final annealed solution in the actual graph.
    print('final solution',solution)
    #Remove all storage in node. - to make space for a clean solution
    #allocated_network_topology.add_node(random_node, storage_usage=0, placed=False)

    for node in allocated_network_topology.nodes(data=True):
        graph_node = node[0]
        allocated_network_topology.add_node(graph_node, storage_usage=0, placed=False)
    #Place Storage - taking the storage-usage of the randomly picked node and puts it into the randomly picked node's also randomly picked neibour
    for node in allocated_network_topology.nodes(data=True):
        graph_node = node[0]
        for u, i in enumerate(solution):
            solution_node = solution[u][0]
            allocated_network_topology.add_node(solution_node, storage_usage=allocated_network_topology.node[solution_node]['storage_capacity'], placed=True)

    return

    ###When scaling - be sure- that it compares target to all the nodes in cluster_ID!!!