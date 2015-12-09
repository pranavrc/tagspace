#!/usr/bin/env python

import igraph as ig
import tagspace as ts
import itertools

class ClusterTopics:
    def __init__(self, topics):
        self.topics = topics
        self.graph = None

    def make_complete_graph(self):
        self.graph = ig.Graph.Full(len(self.topics))
        self.graph.vs["name"] = self.topics
        self.graph.es["weight"] = 1.0
        return self.graph

    def assign_edge_weights(self):
        vertices = self.graph.vs["name"]
        vertex_pairs = list(itertools.combinations(vertices, 2))
        
        for pair in vertex_pairs:
            self.graph[pair[0], pair[1]] = topic_sim(pair[0], pair[1])
        
        return self.graph

    def cluster(self):
        return self.graph.community_fastgreedy()

