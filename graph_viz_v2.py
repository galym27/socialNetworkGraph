import plotly.graph_objects as go
import networkx as nx
import plotly.io as pio
pio.renderers.default = 'browser'
# from networkx.drawing.nx_pydot import write_dot

def draw_graph(graph, powerRank):
    # Transfer data from graph to networkx graph object
    G = nx.Graph()
    for node in graph.keys():
        G.add_node(node)
        for edge in graph[node].keys():
            if(node != edge):
                G.add_edge(node, edge)
    
    # Generate positions for vertices for a layout for vizualization
    pos = nx.nx_agraph.graphviz_layout(G)
    
    # Prepare data for lines (edges) using positions generated above
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Prepare data for nodes (vertices) using positions generated above
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Power rank',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    
    node_adjacencies = []
    node_text = []
    # for node, adjacencies in enumerate(G.adjacency()):
    #     node_adjacencies.append(len(adjacencies[1]))
    #     node_text.append('# of connections: '+str(len(adjacencies[1])))
    
    # Extract powers of vertices
    for node in G.nodes():
        power = powerRank[node]
        node_adjacencies.append(power)
        node_text.append(node + ', power: '+str(round(power, 3)))
    
    # Set the color according to the power of the node
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    
    # Draw the graph
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    # fig.show()
    return fig
