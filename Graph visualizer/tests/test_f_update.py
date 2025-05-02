import pytest
import numpy as np
import os.path as path
import graph


def get_locations(g: graph.Graph) -> np.ndarray:
    return np.array([[node.x, node.y] for node in g.nodes])


def elen(edge):
    return np.sqrt(
        (edge.node1.x - edge.node2.x) ** 2 + (edge.node1.y - edge.node2.y) ** 2.0
    )


def test_converge_simulation():
    # Sets the simulation parameters for fast convergence
    graph.KREP = 1e-2
    graph.KATR = 1e-2

    # Given the star pattern with initialized position
    filename = "star"
    g = graph.Graph.from_file(path.join("data", filename))
    g.init_locations()

    # Then run the simulation for 100 steps
    for i in range(100):
        g.update()

    # And expect all edge lengths to have converged on 1.71 +/- 0.2
    actual_lengths = np.array([elen(edge) for edge in g.edges])
    expected_lengths = np.array([1.71] * 9)
    assert np.isclose(actual_lengths, expected_lengths, atol=0.2).all()
