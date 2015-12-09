#!/usr/bin/env python

import igraph as ig
import tagspace as ts
import itertools
import operator

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


class TopicRelation:
    def __init__(self, articles):
        self.articles = articles
        self.article_paths = self.build_paths()
        self.topic_weights = {}

    def find_intersection(self, results_x, results_y):
        return set(results_x).intersection(results_y)

    def build_paths(self):
        article_paths = {}
        for article in self.articles:
            article_paths[article] = ts.IterateArticles(article).traverse()
        return article_paths

    def most_common_ancestor(self):
        ancestors = {}
        article_path_list = self.article_paths.values()

        for path in article_path_list:
            for topic_idx in range(path):
                if path[topic_idx] in ancestors:
                    ancestors[path[topic_idx]] += 1 / (1 + topic_idx)
                else:
                    ancestors[path[topic_idx]] = 1 / (1 + topic_idx)

        max_topic = max(ancestors.iteritems(), key=operator.itemgetter(1))[0]
        self.topic_weights[max_topic] = ancestors[max_topic]

        return self.topic_weights


def segment_sessions(queries, session_interval, accumulator=[]):
    end_time = queries[0][1] + session_interval
    session_list = []

    for query_idx in range(queries):
        if queries[query_idx][1] <= end_time:
            session_list.append(queries[query_idx][0])
        else:
            return segment_sessions(queries[query_idx:],
                                    session_interval,
                                    accumulator.append(session_list))

    return accumulator.append(session_list)

