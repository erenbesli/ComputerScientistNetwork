# AMD-HW4
This is the last project we did during the course **Algorithm of data mining** where we practiced on dealing with networks.

The data we had available concerned the publications made by the computer scientists, so we had to create a computer scientists Network and carry out some informations from this one. 

The file *modules.py* contains the code.

We decided to split it in a four parts:

* Introduction
* first point
* second point
* third point

## Introduction
In order to run our code import module.py.

import modules

In the introduction what we did is quite simple.

We import data from a Json file saving it in a variable called **data**, we start to observe the data (their structure) and wondering how to approach on it? are there any missing data? 

At this point, once we decided how to store, manipulate and parse the data, we start creating a dictionary which contains for each *computer scientists* all the publications that he did.

* Convert dictionary to ![equation](http://latex.codecogs.com/gif.latex?%5Crightarrow) *author: {list of publication}*

This part is our one of the main part in our implementation. 
Before convert data structure like {authors:{}, publication} to calculate Jaccard similarity, we need to reach list of publication for specific author in efficiency way. 

We planned to use this structure in intersection function.
	
	Example:
		input:	dict_author_pub[93126]
		output is list of publication for author which id = 93126
		out:	[{162021: 'perturbo: a new classification algorithm based on the spectrum perturbations of the laplace-beltrami operator.'},
				{730272: 'optimal spectral transportation with application to music transcription.'},
				{731280: 'mapping estimation for discrete optimal transport.'}]
	
In order to do this part above run this:

modules.buildDataStructure()

and this if you want to check:

modules.dict_author_pub


## First point
In this first part, after importing the library *Networkxx*, we implemented the code to create our Graph.

Once studied the structure of our json file:

where :

+ keys are the ‘authors’ and the values are lists of dictionaries containing the authors name and id whose participated in the same publication.

the other keys of the dictionary are:

* the title of the publication
* the id of the publication
* the id of the conference.

Before creating the graph we defined the **jaccard** function, which calculated the distance, precisely of **jaccard**, between two authors, on the basis of their publications.

* Jaccard distance: ![equation](http://latex.codecogs.com/gif.latex?J_%7B%5Cdelta%7D%28A%2CB%29%3D%5Cfrac%7B%7CA%20%5Ccup%20B%7C%20-%20%7CA%20%5Ccap%20B%7C%7D%7B%7CA%20%5Ccup%20B%7C%7D)

So if two authors have made the same publications, or rather have always collaborated together, their distance of **jaccard** will be 0.

* Calculating Jaccard Distance

	function: def Jaccard(p1,p2):{

	It is taking two lists as input which represent list of publication belongs two different author.

	We will use this lists in intersection function.

	We implemented Jaccard distance in order to this formula, 1-J(A,B)}

	
	
* In Jaccard function, we also used one help function to convert our input into appropriate format for intersection function.

		We define "listToDict(pubList):{}" function

		[{162021: 'perturbo: a new classification algorithm based on the spectrum perturbations of the laplace-beltrami operator.'},
		{730272: 'optimal spectral transportation with application to music transcription.'},
		{731280: 'mapping estimation for discrete optimal transport.'}]
		
		We convert our data; list of dictionary to Dictionary; Above structure to Below structure
		
		{162021: 'perturbo: a new classification algorithm based on the spectrum perturbations of the laplace-beltrami operator.',
		730272: 'optimal spectral transportation with application to music transcription.',
		731280: 'mapping estimation for discrete optimal transport.'}


Then we built up our graph adding as nodes all the authors and the edges are between the computer scientist who collaborated for the same publications with weight equal to the distance of jaccard between them.

But how we built this?:

* Building Graph:
	
We have three for loop in our function;	

First for loop is loop in publications and every step chooses one publication.

Second for loop chooses author in this publication.

Third for loop chooses other author in this publication.

In last part of the third for loop, It is calculating Jaccard distance of these two author.
											
In order to build our graph you just need to run this code:

import networkx as nx
G = nx.Graph()
G = modules.buildGraph()

if you want info about this Graph, run this:

print(nx.info(G))

## Second point

In the second part after creating the network of computer scientists, we create a function called ‘searchConfid’ that wants in input a conference id and returns all the authors who participated in it.
So with this function we are now able to draw a subgraph of authors from the entire graph.

In order to search by ‘ConfId’ you have to run this code:

#given a conference ID return the subgraph induced by the set of authors who published at the input conference at least once
conf=int(input())
H = G.subgraph(module.searchConfId(conf))

and this to plot the subgraph:

module.plot_subgraph(H)

Up until now we carried out informations from the subgraph we’ve generated previously with some statistics technique; 

so we calculate:

+ [*Degree*](https://en.wikipedia.org/wiki/Degree_(graph_theory))
+ [*Betweenness centrality*](https://en.wikipedia.org/wiki/Betweenness_centrality)
+ [*Closeness centrality*](https://en.wikipedia.org/wiki/Closeness_centrality)

of nodes.

The function named *most_important* return the nodes in the subgraph with high betweenness centrality.

At the same time the function called *get_top_keys* returns the nodes with highest closeness centrality.

In order to plot and check our statistics about subgraph run this code:

module.loglog_plot(H)
Gt= module.most_important(H)
modules.plot_betwenness(Gt)
modules.top_clos_node(H)

This second part also deals with **HOP DISTANCE**.

We created a function called [hopDistance](https://www.lifewire.com/what-are-hops-hop-counts-2625905) which wants in input a source (author-id) and an integer ‘d’.

The function first of all computes the shortest path from a node source to all the nodes in the graph and we assign the length of this path to a variable named ‘edge’;
in each iteration if edge is at most equal to the integer d, keep it and append it in an empty list.

At the end we will have all node with the required skills and we plotted them and visualize the graph.

Hop Distance:

	We wrote function "def hopDistance(author,d):"

	It takes two in input, first is author that we calculate distance of second one in d that represent our distance threshold.
	
	We calculate it with using one for loop in order to loop in all node in graph.

	After choose node in graph, calculated distance into our author and filter that is it has smaller distance than our threshold distance.

	And we are adding these filter nodes into our subgraph and plot them.
	
	
	We also implement it with recursive way. 

In order to run HopDistance_one run the code below:

modules.hopDistance_one(G, 93126,23)

## Third point

This third point concerns the last part of the homework.
First we implemented the Dijkstra algorithm as it was the key to resolving the two points that followed.

![Alt Text](https://media.giphy.com/media/ZkIkk3Y8E6hgc/giphy.gif)

We have implemented two functions that calculated the shortest path from a source node to a destination node.

During the execution we realized that the first function that we implemented had a fairly high computation complexity and therefore took a long time, and in most cases when we compared two quite distant nodes it gave as *maximum depth recursion error*.

Shortest Path:
	We wrote shortest path from starch with recursive way.

	We use this data structure in my implementation.

		dictionary; Source node is A and all nodes with weight is value of A
		{A:{B:weight, 
			C:weight, 
			D:weight, 
			E: weight}}	
	
		function "def shorthestPath(unvisitedNode):{}"
		It takes one argument which takes node that has not visited yet.
			In first time I am giving source node as unvisited node, In that time, It is enogh to store weigths of node neighbors in our dictinary.
			
			For other nodes I chceking that before, I calculated distance to this node or not;
				If I calculated before then compare weigths with reacing nodes with that nodes
				If I did not calculate update weigth into that node with sum of dict[sourceNode][unvisitedNode] + G[unvisitedNode][node]['weight']
				
In order to run this shortest path algorithm run this code:

shortPath = modules.shortestPath(G,93126,93126)

				
We know that:

the running time of **Dijkstra's algorithm** depends on the combination of the underlying data structure and the graph shape (edges and vertices).

For example, using a linked list would require ![equation](http://latex.codecogs.com/gif.latex?O%28V%5E2%29) time, i.e. it only depends on the number of vertices. 

Using a heap would require ![equation](http://latex.codecogs.com/gif.latex?O%28%28V%20&plus;%20E%29%20%5Ccdot%20log%20V%29), i.e. it depends on both the number of vertices and the number of edges.
For this reason, also documenting on the web, we have seen that using the heap algorithm becomes more efficient.

In order to run the shortest path with heap to calculate distance from Aris and an other target node run this:

module.shortestPath_heap(G,256176, 256177)

In the second part of this third point we created a function that takes in input a subset of nodes (cardinality smaller than 21) and returns, for each node of the graph, its GroupNumber:
![equation](http://latex.codecogs.com/gif.latex?GroupNumber%28v%29%20%3D%20min_%7Bu%20%5Cin%20l%7D%20%28ShortestPath%28v%2Cu%29%29)

* Grouping nodes that has shorthest path to the our node.

We implemented this function with using for loop in all nodes in Graph. 

After choosing that node we used for loop in nodes in group.
	
After choosing group node we calculate shorthest path between these two node and compare with minimum weight.

If this weight is minumum we are updating our minimum weight after finished second for loop.

Also in this part, in order to run this algorithm, run the code below:
 
group=[93126,256176]
groupedList = modules.findGroupNodes(group,G)

then if you want to print Aris group run this:

modules.printArisGroup(G)

## Authors

*  Alfonso D’Amelio [(damelioalfonso@hotmail.com)](mailto:damelioalfonso@hotmail.com)

*  Eren Beşli [(eren5li@gmail.com)](mailto:eren5li@gmail.com)





