from flask import Flask, redirect, render_template, request
from synth_data_v2 import synth_data
from power_iterations import power_it
from graph_viz_v2 import draw_graph
import json
import plotly

app = Flask(__name__)
GRAPH = {}
powerRank = {}

@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'GET'):
        
        # Provide fields for user input for data generation
        inputs = ['maxVal', 'numberOfEdges']
        titles = {'maxVal': "Number of users",
                  'numberOfEdges': "Number of edges per user"}
        return render_template("index.html", inputs=inputs, titles=titles)
    
    elif(request.method == 'POST'):
        
        global GRAPH
        global powerRank
        
        # Get user data 
        maxVal = int(request.form.get('maxVal'))
        numberOfEdges = int(request.form.get('numberOfEdges'))
        
        # Define top influencers
        influencers = [1, 3, 5, 8]

        # Generate synthetic data with user specified criteria and perform 1 power iter
        GRAPH = synth_data(maxVal, numberOfEdges, influencers)
        powerRank = power_it(GRAPH, 1)
        
        return redirect("/table")

@app.route("/powerIter", methods=['GET', 'POST'])
def power_iterations():
    if(request.method == 'GET'):
        
        # Provide a form for user input
        inputs = ['numberOfIterations']
        titles = {'numberOfIterations': "Number of power iterations"}
        return render_template("powerIter.html", inputs=inputs, titles=titles)
    
    elif(request.method == 'POST'):
        
        global GRAPH
        global powerRank
        
        # Get user input data 
        numberOfIterations = int(request.form.get('numberOfIterations'))
        
        # Perform power iterations
        powerRank = power_it(GRAPH, numberOfIterations)
        
        # Redirect to the updated table with ranks
        return redirect("/table")

@app.route("/table", methods=['GET'])
def table():
    global GRAPH
    global powerRank

    # If graph is empty, redirect to data generation page
    if(len(GRAPH)==0):
        return redirect("/")
    
    else:
        # Show top 20 influencers by power rank
        graphForViz = [[]]
        counter = 0
        for user in powerRank.keys():
            counter = counter + 1
            graphForViz.append([counter, user, round(powerRank[user], 6)])
            if counter > 20:
                break        
    
    return render_template("tableGraph.html", graphForViz=graphForViz)
    
@app.route("/viz", methods=['GET'])
def show_network():
    global GRAPH
    global powerRank
    
    # If graph is empty, redirect to data generation page
    if(len(GRAPH) == 0):
        return redirect('/')

    # Show top 100 influencers by power rank
    graphForViz = {}
    # powerRankForViz = {}
    counter = 0
    for user in powerRank.keys():
        graphForViz[user] = GRAPH[user]
        # powerRankForViz[user] = powerRank[user]
        counter = counter + 1
        if counter > 99:
            break      
        
    # Create vizualisation figure
    fig = draw_graph(graphForViz, powerRank)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)    
    print("length is: ", len(graphForViz))
    return render_template("graphViz_v2.html", fig_json=fig_json)


if __name__ == '__main__':
    app.run(debug=False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    