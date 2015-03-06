from __future__ import division
import random, csv, operator, math
import database, graph, measures, data, config
import networkx as nx
from pprint import pprint
import matplotlib.pyplot as plt

# Calculate the accuracy of a measure
# Used for comparing the different network models
def compare_networks():
	conf = config.Data()

	users = data.Data()
	sample_users = users.get_sample_users()

	db = database.Database()
	db.open()
	time_start, time_end = db.get_time_min_max()

	# Get edges between sample_users between time 48 and 72
	edges = db.get_links(time_start+37*conf.delta_t, time_start+72*conf.delta_t, sample_users, True)
	
	# Make edges as a list
	edges_list = []
	for n in edges:
		for m in edges[n]:
			edges_list.append((n.encode('ascii','ignore'),m.encode('ascii','ignore')))
	
	files = {	'1' : 'exp-data/2015-02-16/common_neighbor_1.csv',
				'2' : 'exp-data/2015-02-16/common_neighbor_2.csv',
				'3' : 'exp-data/2015-02-16/common_neighbor_3.csv',}

	for n in files:
		if n not in ['1','2','3']:
			continue
		file_data = {}
		# Read data
		with open(files[n], 'rb') as csvfile:
			datareader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for row in datareader:
				file_data[(row[0], row[1])] = row[-1]
		scores = sorted(file_data.items(), key=operator.itemgetter(1), reverse=True)
		
		# Provide a rank for scores
		rank = {}
		prev = None
		i = 1
		j = 0
		for e in scores:
			# score(a,b) = score(b,a) for neighbor based measures
			# no need to include both
			if (e[1][1], e[1][0]) not in rank:
				if e[1] != prev:
					i += j
					prev = e[1]
				else:
					j += 1
				rank[e[0]] = i

		# Calculate the average rank of actual edges in the predicted list
		counter = []
		for e in edges:
			for f in edges[e]:
				if (e,f) in rank:
					counter.append(rank[(e,f)])
				else:
					counter.append(rank[(f,e)])

		if len(edges_list)%2 == 0:
			mid = int(len(edges_list)/2)
		else:
			mid = int(math.ceil(len(edges_list)/2))

		median = counter[mid]

		# Print the median positions
		pprint((n, counter[mid]))




def main():

	pass


if __name__ == '__main__':
	compare_networks()
	#pagerank()
	#main()