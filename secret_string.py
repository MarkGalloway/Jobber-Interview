from collections import defaultdict
import random

"""
Secret String

There is a secret string which is unknown to you. Given a collection of random triplets from the string, recover the original string.
A triplet here is defined as a sequence of three letters such that each letter occurs somewhere before the next in the given string. "whi" is a triplet for the string "whatisup".
As a simplification, you may assume that no letter occurs more than once in the secret string. You can assume nothing about the triplets given to you other than that they are valid
triplets and that they contain sufficient information to deduce the original string. In particular, this means that the secret string will never contain letters that do not occur in one of the triplets given to you.

secret_1 = "whatisup"
triplets_1 = [
    ['t','u','p'],
    ['w','h','i'],
    ['t','s','u'],
    ['a','t','s'],
    ['h','a','p'],
    ['t','i','s'],
    ['w','h','s']
]

To run: python secret_string.py
"""


class Graph(object):
    """A wrapper for representing an acyclic dependency graph"""

    def __init__(self, triplets):
        """Constructs a new Graph from an array of triplets."""
        self.graph = defaultdict(set)
        self.nodes = set()
        self.destination_nodes = set()

        for triplet in triplets:
            self._add_triplet(triplet)
            self.nodes.update(triplet)

        # Pruning Optimization: If (A, B) and (A, C) but also (B, C) then (A, C) is irrelevent
        for node in self.nodes:
            for child in list(self.graph[node]):
                self.graph[node] = self.graph[node] - self.graph[child]

    def _add_triplet(self, triplet):
        """Adds a triplet to the dependency graph"""
        node_1, node_2, node_3 = triplet

        # Node 1 appears before node 2
        self.destination_nodes.add(node_2)
        self.graph[node_1].add(node_2)

        # Node 2 appears before node 3
        self.graph[node_2].add(node_3)
        self.destination_nodes.add(node_3)

    @property
    def source_node(self):
        """The source node is the only node that is not a destination node"""
        return list(self.nodes - self.destination_nodes)[0]

    @property
    def longest_path_length(self):
        return len(self.nodes)

    def construct_longest_path(self, source_node, visited):
        """Construct a longest path of nodes in the graph recursively using Depth First Search"""
        visited = visited + [source_node]
        destination_nodes = self.graph[source_node]

        # Recursive case: Visit destination nodes
        for destination_node in destination_nodes:
            result = self.construct_longest_path(destination_node, visited)

            # Base case: we've found the longest path
            if len(result) == self.longest_path_length:
                return result

        # Base case: We've exhausted this path
        return visited


def parse_secret_string(triplets):
    graph = Graph(triplets)
    path_nodes = graph.construct_longest_path(graph.source_node, [])
    return ''.join(path_nodes)


def run_test(secret, triplets):
    print("Testing secret: {}".format(secret))
    assert parse_secret_string(triplets) == secret, "It should return the expected answer of `{}`".format(secret)
    print("Passed.\n")


def test_provided_case():
    secret = "whatisup"
    triplets = [
        ['t','u','p'],
        ['w','h','i'],
        ['t','s','u'],
        ['a','t','s'],
        ['h','a','p'],
        ['t','i','s'],
        ['w','h','s']
    ]

    run_test(secret, triplets)


def test_random_triplets(secret):
    """Generate many random triplets for the provided secret"""
    letters = [letter for letter in secret]

    triplets = []
    for i in range(1, 1000):
        random_indicies = random.sample(range(len(letters)), 3)
        random_triplet = [letters[i] for i in sorted(random_indicies)]
        triplets.append(random_triplet)

    run_test(secret, triplets)


if __name__ == '__main__':
    test_provided_case()
    test_random_triplets("upiswhat")
    test_random_triplets("abcdefghijklmnopqrstuvwxyz")
    test_random_triplets("zyxwvutsrqponmlkjihgfedcba")
    print("All tests passed.")
