import pytest
import numpy as np
import os.path as path
import graph


def get_locations(g: graph.Graph) -> np.ndarray:
    return np.array([[node.x, node.y] for node in g.nodes])


@pytest.mark.parametrize(
    "filename,nodes,edges",
    [
        ("2line", 2, 1),
        ("3grid", 9, 12),
        ("127binary-tree", 127, 126),
    ],
)
def test_part_read_graph(filename, nodes, edges):
    # Given a graph filename, read it
    g = graph.Graph.from_file(path.join("data", filename))
    # Then check if the expected number of edges and nodes exists
    assert len(g.nodes) == nodes, f"file '{filename}' shoud have {nodes}"
    assert len(g.edges) == edges, f"file '{filename}' shoud have {edges}"
