import cluster

if __name__ == "__main__":
    queries = [('Jupiter', 0),
               ('Saturn', 1),
               ('Mercury', 2),
               ('Venus', 3),
               ('Asteroid', 4),
               ('Cricket', 100),
               ('Table Tennis', 101),
               ('Rugby', 102),
               ('Football', 103),
               ('Chennai', 200),
               ('Florida', 201),
               ('France', 202),
               ('Australia', 203),
               ('California', 204),
               ('Batman', 300),
               ('The Flash', 301),
               ('Superman', 302),
               ('Jessica Jones', 303)]

    tr = cluster.TopicRelation(queries, 99)
    ct = cluster.ClusterTopics(tr.topic_weights.keys())
    print ct.cluster

