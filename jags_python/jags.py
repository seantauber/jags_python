import pandas as pd
import numpy as np


def parseJagsNode(node):
	vals = node.strip(']').split('[')

	out = {'name':vals[0]}

	if len(vals) == 2:
		vals[1] = vals[1].split(',')
		vals[1] = np.array(vals[1], dtype=int).tolist()
		out['index'] = vals[1]
	else:
		out['index'] = [1]

	return out


def readJagsPosterior(jagschain='CODAindex.txt'):

	jagsIndex = pd.read_table(jagschain, sep=' ', header=None, 
		names=['node','firstIndex','lastIndex'])
	jagsIndex = np.array(jagsIndex)

	num_samples = jagsIndex[0][2]

	node_shapes = {}

	for node in jagsIndex[:,0]:
		
		parsed_node = parseJagsNode(node)
		
		if parsed_node['name'] not in node_shapes:
			node_shapes[parsed_node['name']] = parsed_node['index']
		
		else:
			for i,j in enumerate(parsed_node['index']):
				node_shapes[parsed_node['name']][i] = max(node_shapes[parsed_node['name']][i], j)

	
	post = {}
	for node, shape in node_shapes.items():
		shape.append(num_samples)
		post[node] = np.empty(shape)


	jagsPost = pd.read_table('CODAchain1.txt', sep='  ', header=None, names=['sample','value'])
	samples = np.array(jagsPost)[:,1]

	for ind in jagsIndex:
		parsedNode = parseJagsNode(ind[0])
		index = tuple( np.array( parsedNode['index'] ) - 1 )
		post[parsedNode['name']][index] = samples[ind[1]-1:ind[2]]

	return post





