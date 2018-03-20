import json
from pprint import pprint

#data = json.load(open('reduced_dblp.json'))
data = json.load(open('full_dblp.json'))

#############################################################################

def searchConfId(confId):
    author_list = []
    for item in data:
        conferenceId = item["id_conference_int"]
        if(confId == conferenceId):
            authors = item["authors"]
            for author in authors:
                authorId = author["author_id"]
                author_list.append(authorId)
    return author_list

#############################################################################


## Conver dictionary to author:{list of publication}

#author:{list of publication}

dict_author_pub = {}
dict_author_conf = {}
dict_publication = {}
author_publication_list = []

def buildDataStructure():
    for item in data:
        publicationId = item["id_publication_int"]
        publicationTitle = item["title"]
        dict_publication = {}
        dict_publication[publicationId] = publicationTitle

        authors = item["authors"]  
        for author in authors:
            author_publication_list = []

            authorId= author["author_id"]
            authorName = author["author"]

            if authorId in dict_author_pub.keys():
                author_publication_list = dict_author_pub[authorId]
                author_publication_list.append(dict_publication)
                dict_author_pub[authorId] = author_publication_list

            else:
                author_publication_list.append(dict_publication)
                dict_author_pub[authorId] = author_publication_list
				
				
				
#############################################################################


#givena conference ID return the subgraph induced by the set of authors who published at the input conference at least once

#conf=int(input())

#H = G.subgraph(searchConfId(conf))



def plot_subgraph(H):
	import warnings
	warnings.filterwarnings('ignore')
	import matplotlib.pyplot as plt
	#g1 = nx.petersen_graph()
	pos = nx.spring_layout(H)
	nx.draw(H,pos,with_labels= True,node_size=100,node_color='r')
	plt.show()

	


###########################

#plot degree in a loglog plot

def loglog_plot(H):
	import matplotlib.pyplot as plt
	degree_sequence=sorted(nx.degree(H).values(),reverse=True) # degree sequence
	#print "Degree sequence", degree_sequence
	dmax=max(degree_sequence)
	plt.loglog(degree_sequence,'b-',marker='o')
	plt.title("log-log plot (Degree-rank )")
	plt.ylabel("log(degree)")
	plt.xlabel("log(rank)")
	plt.show()


###########################

#most important node 

def most_important(G):
	ranking = nx.betweenness_centrality(G).items()
	r = [x[1] for x in ranking]
	m = sum(r)/len(r) # mean centrality
	t = m*3 # threshold, we keep only the nodes with 3 times the mean
	Gt = G.copy()
	for k, v in ranking:
		if v < t:
			Gt.remove_node(k)
		return Gt

############################

def plot_betwenness(Gt):
	#Gt=most_important(H)# draw the most important nodes with a different style
	pos = nx.spring_layout(Gt)
	nx.draw_networkx_nodes(Gt,pos,node_color='r',alpha=0.4,node_size=254)
	# also the labels this time
	nx.draw_networkx_labels(Gt,pos,font_size=12,font_color='b')
	plt.show()


def get_top_keys(dictionary, top):
	items = sorted(dictionary.items(),reverse=True, key=lambda x: x[1])
	return list(map(lambda x: x[0], items[:top]))

	
def top_clos_node(H):
	clos=nx.closeness_centrality(H)
	top_clo_cen = get_top_keys(clos,10)
	clos_graph=H.subgraph(top_clo_cen)
	nx.draw_networkx(clos_graph, with_labels= True)
	plt.show()	


##########################

def top_close_node(subgraph):
	clos=nx.closeness_centrality(subgraph)
	top_clo_cen = get_top_keys(clos,10)
	clos_graph=subgraph.subgraph(top_clo_cen)
	nx.draw_networkx(clos_graph, with_labels= True)
	plt.show()
	
###########################

def listToDict(pubList):
    dictt={}
    for item in pubList:
        key = list(item.keys())[0]
        value = list(item.values())[0]
        dictt[key] =value
    return dictt

def jaccard(p1,p2):
    p1= listToDict(p1)
    p2= listToDict(p2)
    p1_int_p2=len(set(p1).intersection(p2))
    result = 1 - (p1_int_p2 / (len(p1) + len(p2) - p1_int_p2))

    return result
	
#############################################################################

# create garph

import networkx as nx

def buildGraph():
	G = nx.Graph()
	for item in data:
		authors = item["authors"]  
		for author in authors:
			for author2 in authors:
				aId= author["author_id"]
				a2Id= author2["author_id"]
				G.add_node(aId)
				G.add_node(a2Id)
				if( (aId != a2Id) and not(G.has_edge(aId,a2Id))  ):
					r_weight= jaccard(dict_author_pub[aId],dict_author_pub[a2Id])
					G.add_edge(aId,a2Id, key='info', weight=r_weight)
					
	return G
					
#############################################################################

## It can done using neighboorhood
#len(G.nodes())
import matplotlib.pyplot as plt
def hopDistance_one(Graph,author,d):
	degreeList =[]
	for node in Graph.nodes():
		if nx.has_path(Graph,author,node):
			edges = len(nx.shortest_path(Graph, source=author, target=node, weight=None)) - 1
			if(edges <= d):
				degreeList.append(node)			
	print(degreeList)
	H = Graph.subgraph(degreeList)
	nx.draw(H, with_labels= True)
	plt.show()
	
	
#############################################################################

#Hop Distance

def hopDistance_two(Graph,node, degree):
	if(degree == 0):
		return resultList
		if (degree == 1):
			resultList.append(Graph.neighbors(node))
		else:
			for node in Graph.neighbors(node):
				resultList.append([node])
				hopDistance_two(Graph,node,degree-1)
			
			
			
	resultList = []
	hopDistance_two(Graph, node,1)
	hopResult = [item for sublist in resultList for item in sublist]
	len(set(hopResult))
					
	H = G.subgraph(hopResult)
	import matplotlib.pyplot as plt
	#g1 = nx.petersen_graph()
	nx.draw(H, with_labels= True)
	plt.show()


#############################################################################

def hopDistance_nx(graph, source, degree):
	c = nx.ego_graph(graph, source, degree)
	nx.draw(c)
	plt.show()

#############################################################################
sourceNode = 93126
dictt = {}
visitedNodes={}

visitedNodes[sourceNode]={}
dictt[sourceNode]={}

def shortestPath(graph,sourceNode,unvisitedNode):
    for node in graph.neighbors(unvisitedNode):
        if(sourceNode == unvisitedNode):
            dictt[sourceNode][node] = graph[unvisitedNode][node]['weight']
        else:
            if(node in dictt[sourceNode].keys()):
                if(graph[unvisitedNode][node]['weight'] +  dictt[sourceNode][unvisitedNode] < dictt[sourceNode][node] ):
                    dictt[sourceNode][node] = graph[unvisitedNode][node]['weight'] + dictt[sourceNode][unvisitedNode]
            else:
                dictt[sourceNode][node] = dictt[sourceNode][unvisitedNode] + graph[unvisitedNode][node]['weight']
    
    exractedVisitedNodes = { k : dictt[sourceNode][k] for k in set(dictt[sourceNode]) - set(visitedNodes[sourceNode]) }
    #print("exractedVisitedNodes: ")
    #print(exractedVisitedNodes)
    if (len(exractedVisitedNodes) == 0):
        return dictt[sourceNode]
    minNode = min(exractedVisitedNodes.items(), key=lambda x: x[1])
    visitedNodes[sourceNode][minNode[0]]="visited"
    #print(visitedNodes[sourceNode])
    #print(minNode[0])
    shorthestPath(graph,sourceNode,minNode[0])
	
	
####################

#very fast
import heapq

def shortestPath_heap(graph,start, end):
	dictOfNode={}
	for i in graph.nodes():
		for j in graph[i]:
			if i not in dictOfNode.keys():
				dictOfNode[i]={}
				dictOfNode[i][j]=graph[i][j]['weight']
			else:
				dictOfNode[i][j]=graph[i][j]['weight']
	queue = [(0, start, [])]
	seen= set()
	while queue:
		(cost, v, path) = heapq.heappop(queue)
		if v not in seen:
			path = path + [v]
			seen.add(v)
			if v == end:
				return cost
			for (next, c) in dictOfNode[v].items():
				heapq.heappush(queue, (cost + c, next, path))
    
	return float('no path')	


#############################################################################

#check if two nodes are connected
def Check(connect,src,dest,graph):
	connect=sorted(nx.connected_components(graph), key=len, reverse=True) #connected nodes
	c=''
	for i in connect:
		if src in i: 
			if dest in i:
				c='True'
			else:
				c='False'
	return c
	
	
#####################
	


def findGroupNodes(group,graph):
	dictOfNode={}
	for i in graph.nodes():
		for j in graph[i]:
			if i not in dictOfNode.keys():
				dictOfNode[i]={}
				dictOfNode[i][j]=graph[i][j]['weight']
			else:
				dictOfNode[i][j]=graph[i][j]['weight']
	connect=sorted(nx.connected_components(graph), key=len, reverse=True) #connected nodes
	newlist=[]
	newdict={}
	authordict ={}
	for node in dictOfNode:
		minim=10000
		newdict={}
		for groupNode in group:

			if Check(connect,node,groupNode,graph)=='True':
				c=shortestPath_heap(graph,node,groupNode)
				if c<minim:
					minim=c
					newdict[node]=groupNode

			if (bool(newdict)):
				#print(newdict)
				if(groupNode in authordict.keys()):
					newlist= authordict[groupNode]
					#newdict[i] it will return closest author
					newlist.append(newdict.keys())
					authordict[groupNode]=newlist
						#newlist[(i,j)]=c
				else:
					newlist.append(newdict.keys())
					authordict[groupNode]=newlist

	return authordict
	
	
	
def printArisGroup(graph):
	Aris_id = 256176
	# i create dict with key and his node

	node_Aris=[256176]
		
	result_of_group_nodes = findGroupNodes(node_Aris,graph)
	#Print Group nodes for Prof. Aris            
	resultList=[]
	for author in result_of_group_nodes[Aris_id]:
		for key in author:
			resultList.append(key)
	print(resultList)


#############################################################################



