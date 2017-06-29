from bs4 import BeautifulSoup
import bs4
from urllib import request
from collections import deque
import networkx as nx
from networkx.readwrite import json_graph
import json

# title = input('Name of the Wikipedia page:\n')
remove_leaves = True

init_link = BeautifulSoup('<a href="/wiki/Isaac_Newton" title="Isaac Newton">Isaac Newton</a>', 'html.parser').find('a')

visited = set()

queue = deque([init_link])
graph = nx.DiGraph()
graph.add_node(init_link['title'])

expanded_nodes = 0

while expanded_nodes < 50:
    link = queue.popleft()
    title = link['title']
    if title in visited:
        continue

    expanded_nodes += 1
    print(title, expanded_nodes)

    url = 'http://en.wikipedia.org' + link['href']
    page = request.urlopen(url)
    soup = BeautifulSoup(page.read(), 'html.parser')
    titleTag = soup.find(id='firstHeading').contents[0]
    title = ''
    if type(titleTag) is not bs4.NavigableString:
        title = titleTag.contents[0]
    else:
        title = titleTag

    body = soup.find(id='bodyContent')
    [x.extract() for x in body.find_all(['sup', 'span'])]
    [x.extract() for x in body.find_all(role=['note', 'navigation'])]
    # [x.extract() for x in body.find_all({'class': ['reflist', 'image']})]

    paragraphs = body.find_all('p')
    for paragraph in paragraphs:
        links = paragraph.find_all('a')

        for new_link in links:
            if new_link.get('title') is None:
                continue

            link_string = new_link['href']
            if link_string[:6] != '/wiki/':
                continue

            queue.append(new_link)
            new_title = new_link['title']

            graph.add_node(new_title)
            graph.add_edge(title, new_title)

if remove_leaves:
    # Remove leaf nodes (because they make json files huge and not that useful)
    leaves = [x for x in graph.nodes_iter() if graph.out_degree(x) == 0 or graph.in_degree(x) == 1]
    [graph.remove_node(x) for x in leaves]

graph_data = json_graph.node_link_data(graph)
# Convert format so d3 knows how to read IDs
graph_data['links'] = [
    {
        'source': graph_data['nodes'][link['source']]['id'],
        'target': graph_data['nodes'][link['target']]['id']
    }
    for link in graph_data['links']
]
with open('graph_data.json', 'w') as outfile:
    json.dump(graph_data, outfile)
