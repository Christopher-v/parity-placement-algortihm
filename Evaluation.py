import matplotlib.pyplot as plt
#import numpy
import pandas as pd

#This is the evaluation methods used for extracting the data for the test-cases.
#-Hopefully the names of the functions is self-explanatory

all_cost = []
last_costs = []

acceptance = []
temp = []
seconds = []
usages = []
requirements = []
RB_usages = []
no_of_groups = []
data_node = []
parity_node = []

def eval_topology_RB(cost):

    list.append(all_cost, cost)

    #print(all_cost)
    plt.plot(all_cost)
    plt.ylabel('Overall latency')
    plt.xlabel('Iterations')
    return all_cost

def eval_topology_DS(cost):

    #print('hej fra eval')
    list.append(all_cost, cost)

    #print(all_cost)
    plt.plot(all_cost)
    plt.ylabel('Overall - Latency')
    plt.xlabel('Iterations')
    return all_cost

def eval_annealing_DS(T):

    #print('hej fra eval')

    list.append(temp, T)
    print('temp', temp)

    return

def csv1():

    df = pd.DataFrame(temp)
    df.to_csv("/home/christopher/IdeaProjects//evaluation/anneal_DS/Exponential/schedule.csv")

    return

def eval_seonds_DS(sec):

    #print('hej fra eval')

    list.append(seconds, sec)
    print('sec', sec)

    return

def csv_sec():

    df = pd.DataFrame(seconds)
    df.to_csv("/home/christopher/IdeaProjects/evaluation/scalability-parity/seconds-GNP-200.csv")

    return

def eval_usage_DS(usage, req):

    #print('hej fra eval')
    list.append(usages, usage)
    list.append(requirements, req)
    print('usage', usage)
    print('requirement', req)
    return

def csv_usage():

    df = pd.DataFrame(usages)
    df.to_csv("/home/christopher/IdeaProjects/evaluation/usage_DS/usage-caveman-55.csv")
    tf = pd.DataFrame(requirements)
    tf.to_csv("/home/christopher/IdeaProjects/evaluation/usage_DS/req-caveman-55.csv")
    return

def eval_groups(allocated_topology):
    groups = []
    group_count = []
    seen = set()
    count = 0
    for node in allocated_topology.nodes(data=True):
        if node[1]['placed'] == True:
            if node[1]['cluster_ID'] not in seen: # membership test
                seen.add(node[1]['cluster_ID'])
            elif node[1]['cluster_ID'] in seen:
                list.append(groups, node[1]['cluster_ID'])
                setgroups = set(groups)
                no_groups = len(setgroups)
                print('number of groups',no_groups)
    no_of_groups.append(no_groups)
    print('count groups', no_of_groups)

    return no_of_groups

def csv_group(no_of_groups):

    df = pd.DataFrame(no_of_groups)
    df.to_csv("/home/christopher/IdeaProjects/evaluation/group-DS/groups-gnp-10.csv")

    return

def eval_occu_nodes_parity(allocated_topology):
    count_data = 0
    count_parity = 0
    for node in allocated_topology.nodes(data=True):
        if node[1]['placed'] == True:

            if node[1]['r_block'] is False:
                count_data += 1
                #print('data-blocks', count_data)
            elif node[1]['r_block'] is not None:
                count_parity += 1
                #print('parity-blocks', count_parity)

    list.append(data_node, count_data)
    list.append(parity_node, count_parity)
    print('data nodes',data_node)
    print('parity nodes', parity_node)
    return

def csv_occu_nodes_parity():

    df = pd.DataFrame(data_node)
    df.to_csv("/home/christopher/IdeaProjects/evaluation/occupied_nodes_RB/data_nodes_caveman_5.csv")
    tf = pd.DataFrame(parity_node)
    tf.to_csv("/home/christopher/IdeaProjects/evaluation/usage_DS/parity_nodes_caveman_5.csv")
    return


def eval_usage_RB(allocated_topology):

    count_data = 0
    count_parity = 0
    for node in allocated_topology.nodes(data=True):
        if node[1]['placed'] == True:

            if node[1]['r_block'] is False:
                count_data = + count_data +  node[1]['storage_usage']

                #print('data-blocks', count_data)
            elif node[1]['r_block'] is not None:
                count_parity = + count_parity +  node[1]['storage_usage']
                #print('parity-blocks', count_parity)

    #print('hej fra eval')
    list.append(usages, count_data)
    list.append(RB_usages, count_parity)
    print('DS_usage', count_data)
    print('RB_usage', count_parity)
    return

def csv_usage_RB():

    df = pd.DataFrame(usages)
    df.to_csv("/home/christopher/IdeaProjects/evaluation/usage_RB/DS_usage-caveman-20.csv")
    tf = pd.DataFrame(RB_usages)
    tf.to_csv("/home/christopher/IdeaProjects/evaluation/usage_RB/RB_usage-caveman-20.csv")
    return

def eval_cost_annealing():

    latest_cost = all_cost[-1]
    last_costs.append(latest_cost)

def csv_cost_annealing():

    df = pd.DataFrame(last_costs)
    df.to_csv("/home/christopher/IdeaProjects/evaluation/anneal_DS/Adaptive/adaptive-anneal-02.csv")
