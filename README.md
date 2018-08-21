# parity-placement-algortihm
This project deals with parity placement in a Fog Computing setting. 
The project simulates a Configartion Agent which is able to detect failures and reconfigure streams in a Fog Continuum. 
It is based on my master thesis. - "Algorithms for the Optimization of Redundant Storage Allocation on a Fog Computing Platform"
- https://www.dropbox.com/s/047ohpekqdgynb8/Christopher%20Vik%20Msc%20Thesis.pdf?dl=0

The algortihms presented in this projekt deals with three sub-problems: 

1. - Allocates a DDS in cliques

A constructive heuristic algorithm
Works as a greedy initialization solution 
Does it 3 procedures
-Find storage capacities
-Find clique sum
-Allocate DDS

2. - Places the parity-blocks

A constructive heuristic algorithm
Works as a greedy initialization solution 
Does it 5 procedures
-Find biggest node in each clique
-Place group blocks
-Find neighbour clique
-Place sub-group blocks
-Place Global-group blocks

3 - Simulated Annealing
A local search heuristic 
Finds a ‘near-optimal’ solution 
Reducing latency
Does it 3 procedures
-Optimize DDS placement (Simulated annealing)
-Neighbour (finding new solution)
-Cost  (Objective function)
