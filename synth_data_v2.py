import random

# maxVal = 10
# numberOfEdges = 20
# influencers = [7, 10, 95, 88]

def synth_data(maxVal, numberOfEdges, influencers):
    # Generate unique usernames
    f = open('pg69435.txt', encoding="utf8")
    conts = f.read()
    f.close()
    conts = conts.replace(',', '')
    conts = conts.replace('"', '')
    textList = list(set(conts.split()))
    newList = []
    for word in textList:
        newList.extend([word + str(x) for x in range(10)])
    
    textList.extend(newList)
    textList = list(set(textList))
    
    # Generate unique connections with weights
    """
    - Data structure: dict -> JSON
    - key is vertex, value is another dict<vertex, weight> picked randomly
    - first, populate all vertices with 100 edges randomly
    - then pick some 100 vertices and add them to each vertex with high weight
    """
    """
    - Input data comes as a dict of dicts holding usernames as vertices and each user name
        having a dict{edge, numberOfMentions}
    """
    vertexCount = len(textList[0:maxVal])
    
    # Populate the graph with random data following the real format
    graph = {}
    for user in textList[0:maxVal]:
        graph[user] = {}
        edges = list(set([random.randint(0, vertexCount - 1) for x in range(numberOfEdges)]))
        for edge in edges:
            if edge == user:
                continue
            graph[user][textList[edge]] = random.randint(1, 50)
    
    # Artificially create highly influencial user(s): 
    users = []
    for i in influencers:
        users.append(textList[i])

# =============================================================================
# Addition of extra data to check power iteration logic implementation
# =============================================================================
    # Add some vertex to every vertex except itself with large number of mentions
    for user in graph.keys():
        if user in users:
            continue
        for i in range(len(users)):
            graph[user][users[i]] = 1000
            
    # Check powerRank logic by highlighting some user with influencer mentions
    graph['mentionedByInfluencers'] = {}
    influencerNames = []
    for user, edge in graph.items():
        for edge, mentions in graph[user].items():
            if(mentions > 999 and not(edge in influencerNames)):
                influencerNames.append(edge)
    for influencer in influencerNames:
        graph[influencer]['mentionedByInfluencers'] = 50
        
    # Compare with some user who's mentioned by other non-influencial users
    graph['mentionedByAverageUsers'] = {}
    averageUsers = []
    countUsers = 0
    for user in graph.keys():
        if(user not in influencerNames and user != 'mentionedByInfluencers' and user != 'mentionedByAverageUsers'):
            averageUsers.append(user)
            countUsers = countUsers + 1
        if(countUsers > 3):
            break
    
    for user in averageUsers:
        graph[user]['mentionedByAverageUsers'] = 50
    
    return graph
















