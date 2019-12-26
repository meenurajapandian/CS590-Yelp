import pandas as pd
import networkx as nx
import numpy as np
from bokeh.palettes import YlOrRd

df = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/usernetwork1.csv')
df['distance'] = 1/df['strength']
df_user = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/userdetails1.csv')
del df_user['Unnamed: 0']

G = nx.from_pandas_edgelist(df, 'user1', 'user2', ['strength','distance'])
print(nx.number_connected_components(G))
nx.set_node_attributes(G, df_user.set_index('user_id').to_dict('index'))
nx.set_node_attributes(G, dict(G.degree(weight='strength')), 'WDegree')
nx.set_node_attributes(G, nx.betweenness_centrality(G, weight='distance'), 'bwcentral')
nx.set_node_attributes(G, nx.communicability_betweenness_centrality(G), 'ccentral')

# col = ['#FFFFFF', '#93CCB9', '#4D9980', '#24745A', '#074A34', '#002217']
col = YlOrRd[8]

for u in G.nodes():
    if G.node[u]['friend'] < 730:
        G.node[u]['friend'] = col[7]
    elif G.node[u]['friend'] < (730 * 2):
        G.node[u]['friend'] = col[6]
    elif G.node[u]['friend'] < (730 * 3):
        G.node[u]['friend'] = col[5]
    elif G.node[u]['friend'] < (730 * 4):
        G.node[u]['friend'] = col[4]
    elif G.node[u]['friend'] < (730 * 5):
        G.node[u]['friend'] = col[3]
    elif G.node[u]['friend'] < (730 * 6):
        G.node[u]['friend'] = col[2]
    elif G.node[u]['friend'] < (730 * 7):
        G.node[u]['friend'] = col[1]
    else:
        G.node[u]['friend'] = col[0]

    if G.node[u]['comprank'] < 0.125:
        G.node[u]['comprank'] = col[7]
    elif G.node[u]['comprank'] < (0.125 * 2):
        G.node[u]['comprank'] = col[6]
    elif G.node[u]['comprank'] < (0.125 * 3):
        G.node[u]['comprank'] = col[5]
    elif G.node[u]['comprank'] < (0.125 * 4):
        G.node[u]['comprank'] = col[4]
    elif G.node[u]['comprank'] < (0.125 * 5):
        G.node[u]['comprank'] = col[3]
    elif G.node[u]['comprank'] < (0.125 * 6):
        G.node[u]['comprank'] = col[2]
    elif G.node[u]['comprank'] < (0.125 * 7):
        G.node[u]['comprank'] = col[1]
    else:
        G.node[u]['comprank'] = col[0]

    if G.node[u]['reviewcount'] < 106 + 110:
        G.node[u]['reviewcount'] = col[7]
    elif G.node[u]['reviewcount'] < 106 + (110 * 2):
        G.node[u]['reviewcount'] = col[6]
    elif G.node[u]['reviewcount'] < 106 + (110 * 3):
        G.node[u]['reviewcount'] = col[5]
    elif G.node[u]['reviewcount'] < 106 + (110 * 4):
        G.node[u]['reviewcount'] = col[4]
    elif G.node[u]['reviewcount'] < 106 + (110 * 5):
        G.node[u]['reviewcount'] = col[3]
    elif G.node[u]['reviewcount'] < 106 + (110 * 6):
        G.node[u]['reviewcount'] = col[2]
    elif G.node[u]['reviewcount'] < 106 + (110 * 7):
        G.node[u]['reviewcount'] = col[1]
    else:
        G.node[u]['reviewcount'] = col[0]

values = np.percentile(list(nx.get_node_attributes(G, 'WDegree').values()), [20, 50, 75, 88, 95])

for u in G.nodes():
    G.node[u]['size'] = (2 * np.log(G.node[u]['WDegree'])) - 8
    if G.node[u]['WDegree'] < values[0]:
        G.node[u]['DegCol'] = col[7]
    elif G.node[u]['WDegree'] < values[1]:
        G.node[u]['DegCol'] = col[5]
    elif G.node[u]['WDegree'] < values[2]:
        G.node[u]['DegCol'] = col[4]
    elif G.node[u]['WDegree'] < values[3]:
        G.node[u]['DegCol'] = col[3]
    elif G.node[u]['WDegree'] < values[4]:
        G.node[u]['DegCol'] = col[2]
    else:
        G.node[u]['DegCol'] = col[0]


nodep = []
nodex = []
nodey = []
values = np.percentile(list(nx.get_node_attributes(G, 'WDegree').values()), [100, 95, 85, 70, 40])
values = np.append(values, 0)
for i in range(0, 5):
    nodes = list(set(u for u in G.nodes()
                     if G.node[u]['WDegree'] >= values[i + 1] and G.node[u]['WDegree'] < values[i]))
    nodep.extend(nodes)
    s = np.random.normal(0, 0.9, len(nodes))
    t = np.random.normal(0, 0.9, len(nodes))
    h = [np.sqrt((x ** 2) + (y ** 2)) for x, y in zip(s, t)]
    s = [x * (1 + (i / z)) for x, z in zip(s, h)]
    t = [x * (1 + (i / z)) for x, z in zip(t, h)]
    nodex.extend(s)
    nodey.extend(t)
nx.set_node_attributes(G, dict(zip(nodep, zip(nodex, nodey))), 'WDegreepos')

values = np.percentile(list(nx.get_node_attributes(G, 'bwcentral').values()), [20, 50, 75, 88, 95])

for u in G.nodes():
    if G.node[u]['bwcentral'] < values[0]:
        G.node[u]['Colbw'] = col[7]
    elif G.node[u]['bwcentral'] < values[1]:
        G.node[u]['Colbw'] = col[5]
    elif G.node[u]['bwcentral'] < values[2]:
        G.node[u]['Colbw'] = col[4]
    elif G.node[u]['bwcentral'] < values[3]:
        G.node[u]['Colbw'] = col[3]
    elif G.node[u]['bwcentral'] < values[4]:
        G.node[u]['Colbw'] = col[2]
    else:
        G.node[u]['Colbw'] = col[0]

nodep = []
nodex = []
nodey = []
values = np.percentile(list(nx.get_node_attributes(G, 'bwcentral').values()), [100, 95, 85, 70, 40])
values = np.append(values, 0)
for i in range(0, 5):
    nodes = list(set(u for u in G.nodes()
                     if G.node[u]['bwcentral'] >= values[i + 1] and G.node[u]['bwcentral'] < values[i]))
    nodep.extend(nodes)
    s = np.random.normal(0, 0.9, len(nodes))
    t = np.random.normal(0, 0.9, len(nodes))
    h = [np.sqrt((x ** 2) + (y ** 2)) for x, y in zip(s, t)]
    s = [x * (1 + (i / z)) for x, z in zip(s, h)]
    t = [x * (1 + (i / z)) for x, z in zip(t, h)]
    nodex.extend(s)
    nodey.extend(t)
nx.set_node_attributes(G, dict(zip(nodep, zip(nodex, nodey))), 'bwcentralpos')

values = np.percentile(list(nx.get_node_attributes(G, 'ccentral').values()), [20, 50, 75, 88, 95])

for u in G.nodes():
    if G.node[u]['ccentral'] < values[0]:
        G.node[u]['Colcc'] = col[7]
    elif G.node[u]['ccentral'] < values[1]:
        G.node[u]['Colcc'] = col[5]
    elif G.node[u]['ccentral'] < values[2]:
        G.node[u]['Colcc'] = col[4]
    elif G.node[u]['ccentral'] < values[3]:
        G.node[u]['Colcc'] = col[3]
    elif G.node[u]['ccentral'] < values[4]:
        G.node[u]['Colcc'] = col[2]
    else:
        G.node[u]['Colcc'] = col[0]

nodep = []
nodex = []
nodey = []
values = np.percentile(list(nx.get_node_attributes(G, 'ccentral').values()), [100, 95, 85, 70, 40])
values = np.append(values, 0)
for i in range(0, 5):
    nodes = list(set(u for u in G.nodes()
                     if G.node[u]['ccentral'] >= values[i + 1] and G.node[u]['ccentral'] < values[i]))
    nodep.extend(nodes)
    s = np.random.normal(0, 0.9, len(nodes))
    t = np.random.normal(0, 0.9, len(nodes))
    h = [np.sqrt((x ** 2) + (y ** 2)) for x, y in zip(s, t)]
    s = [x * (1 + (i / z)) for x, z in zip(s, h)]
    t = [x * (1 + (i / z)) for x, z in zip(t, h)]
    nodex.extend(s)
    nodey.extend(t)
nx.set_node_attributes(G, dict(zip(nodep, zip(nodex, nodey))), 'ccentralpos')



nx.write_gml(G, "user.gml")
