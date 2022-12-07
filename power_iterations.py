import numpy as np

def power_it(graph, powerIterations):
    # =============================================================================
    # Prepare the graph data for power iterations
    # =============================================================================
    # Normalize the weights of edges for each vertex
    for user in graph.keys():
        total = 0
        for edge in graph[user].keys():
            total = total + graph[user][edge]
        for edge in graph[user].keys():
            graph[user][edge] = graph[user][edge] / total / len(graph)
    
    # Create a dict for incoming connections weighted by contributing vertex's power
    incomingConns = {}
    # Create a dict that holds current powers of each vertex
    powerRanks = {}
    for user in graph.keys():
        incomingConns[user] = 0
        powerRanks[user] = 1/len(graph)
    
    # =============================================================================
    # Power iterations
    # =============================================================================
    
    """
    1) Setup a loop
        2) Traverse all graph edges and collect incoming contributions for each graph into incomContr dict
        3) Iterate over each graph vertex in power ranks and update power ranks as per incoming connections
        4) Iterate over each vertex in graph and distribute its power among edges by normalizing to total power of vertex
    """
    # Pick a number of power iterations
    # powerIterations = 10
    for i in range(powerIterations):
        # Reset all incoming connections to zero
        for key in incomingConns.keys():
            incomingConns[key] = 0.0
        
        # Traverse all graph edges and collect incoming contributions for each graph into incomContr dict
        for user in graph.keys():
            for edge in graph[user].keys():
                incomingConns[edge] = incomingConns[edge] + graph[user][edge]
        
        # Iterate over each graph vertex in power ranks and update power ranks as per incoming connections
        for user in powerRanks.keys():
            powerRanks[user] = incomingConns[user]
        
        # Iterate over each vertex in graph and distribute its power among edges by normalizing to total power of vertex
        for user in graph.keys():
            total = 0
            for edge in graph[user].keys():
                total = total + graph[user][edge]
            for edge in graph[user].keys():
                graph[user][edge] = graph[user][edge] / total * powerRanks[user]
    
    powerRanksSorted = {k: v for k, v in sorted(powerRanks.items(), key=lambda item: item[1], reverse=True)}
    
    return powerRanksSorted

# =============================================================================
# Power rank iterations with 2D matrix representation of graph
# =============================================================================
def power_it_m(graph, powerIterations):
    # Create 1D vector that will be holding powerRanks of each vertex
    powerRanks = np.ones(shape=[len(graph),1])
    
    # Create a 2D matrix that will be multiplied by power rank vector during
    # power iterations
    matrix = np.ones(shape=[len(graph), len(graph)])
    
    for i in range(powerIterations):
        powerRanks = np.dot(matrix, powerRanks)
    
    return powerRanks
    
    
    
# =============================================================================
# RENDERING RESULTS
# =============================================================================

"""
- Results in tabular format can be shown for a large number of vertices
- Results in graph network format can be shown only for certain amount 
    of vertices
"""