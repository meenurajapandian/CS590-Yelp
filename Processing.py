import pandas as pd
import networkx as nx
import numpy as np

df = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/usernetwork1.csv')
df['distance'] = 1/df['strength']
df_user = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/userdetails1.csv')
del df_user['Unnamed: 0']

G = nx.from_pandas_edgelist(df, 'user1', 'user2', ['strength','distance'])
print(nx.number_connected_components(G))
nx.set_node_attributes(G, df_user.set_index('user_id').to_dict('index'))
nx.set_node_attributes(G, dict(G.degree(weight='strength')), 'WDegree')
nx.set_node_attributes(G, nx.betweenness_centrality(G, weight='distance'), 'bwcentral')
#nx.set_node_attributes(G, dict(G.degree()), 'ccentral')
nx.set_node_attributes(G, nx.communicability_betweenness_centrality(G), 'ccentral')

values = np.percentile(list(nx.get_node_attributes(G, 'WDegree').values()), [20, 50, 75, 88, 95])

for u in G.nodes():
    G.node[u]['size'] = (2*np.log(G.node[u]['WDegree'])) - 8
    if G.node[u]['WDegree'] < values[0]:
        G.node[u]['DegCol'] = '#FFAAAA'
    elif G.node[u]['WDegree'] < values[1]:
        G.node[u]['DegCol'] = '#D46A6A'
    elif G.node[u]['WDegree'] < values[2]:
        G.node[u]['DegCol'] = '#AA3939'
    elif G.node[u]['WDegree'] < values[3]:
        G.node[u]['DegCol'] = '#801515'
    elif G.node[u]['WDegree'] < values[4]:
        G.node[u]['DegCol'] = '#550000'
    else:
        G.node[u]['DegCol'] = '#FFFFFF'


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
        G.node[u]['Colbw'] = '#FFAAAA'
    elif G.node[u]['bwcentral'] < values[1]:
        G.node[u]['Colbw'] = '#D46A6A'
    elif G.node[u]['bwcentral'] < values[2]:
        G.node[u]['Colbw'] = '#AA3939'
    elif G.node[u]['bwcentral'] < values[3]:
        G.node[u]['Colbw'] = '#801515'
    elif G.node[u]['bwcentral'] < values[4]:
        G.node[u]['Colbw'] = '#550000'
    else:
        G.node[u]['Colbw'] = '#FFFFFF'

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
        G.node[u]['Colcc'] = '#FFAAAA'
    elif G.node[u]['ccentral'] < values[1]:
        G.node[u]['Colcc'] = '#D46A6A'
    elif G.node[u]['ccentral'] < values[2]:
        G.node[u]['Colcc'] = '#AA3939'
    elif G.node[u]['ccentral'] < values[3]:
        G.node[u]['Colcc'] = '#801515'
    elif G.node[u]['ccentral'] < values[4]:
        G.node[u]['Colcc'] = '#550000'
    else:
        G.node[u]['Colcc'] = '#FFFFFF'

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
