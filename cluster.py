#!/usr/bin/env python

import igraph as ig
import tagspace as ts
import itertools
import operator
from math import log10

class ClusterTopics:
    def __init__(self, topics):
        self.topics = topics
        self.graph = self.make_complete_graph()
        self.assign_edge_weights()
        self.cluster = self.cluster()

    def make_complete_graph(self):
        graph = ig.Graph.Full(len(self.topics))
        graph.vs["name"] = self.topics
        graph.es["weight"] = 1.0
        return graph

    def assign_edge_weights(self):
        vertices = self.graph.vs["name"]
        vertex_pairs = list(itertools.combinations(vertices, 2))

        for pair in vertex_pairs:
            self.graph[pair[0], pair[1]] = len(find_intersection(pair[0], pair[1]))

        return self.graph

    def cluster(self):
        return self.graph.community_fastgreedy()


class TopicRelation:
    def __init__(self, queries, session_interval):
        self.queries = segment_sessions(queries, session_interval)

        self.article_paths = []
        for session in self.queries:
            self.article_paths.append(self.build_paths(session))

        self.topic_weights = {}
        for path in self.article_paths:
            self.topic_weights.update(self.most_common_ancestor(path))


    def build_paths(self, articles):
        article_paths = {}
        for article in articles:
            article_paths[article] = ts.IterateArticles(article).traverse()
        return article_paths

    def most_common_ancestor(self, article_paths):
        ancestors = {}
        article_path_list = article_paths.values()

        for path in article_path_list:
            for topic_idx in range(1, len(path)):
                if path[topic_idx] in ancestors:
                    ancestors[path[topic_idx]] += 3.0 / topic_idx
                else:
                    ancestors[path[topic_idx]] = 3.0 / topic_idx

        max_topic = max(ancestors.iteritems(), key=operator.itemgetter(1))[0]
        return {max_topic: ancestors[max_topic]}


def segment_sessions(queries, session_interval, accumulator=[]):
    end_time = queries[0][1] + session_interval
    session_list = []

    for query_idx in range(len(queries)):
        if queries[query_idx][1] <= end_time:
            session_list.append(queries[query_idx][0])
        else:
            return segment_sessions(queries[query_idx:],
                                    session_interval,
                                    accumulator=accumulator + [session_list])

    return accumulator + [session_list]

def find_intersection(topic_x, topic_y):
    results_x = ts.IterateArticles(topic_x).traverse()
    results_y = ts.IterateArticles(topic_y).traverse()
    return set(results_x).intersection(results_y)

