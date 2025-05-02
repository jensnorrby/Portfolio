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


def test_part_edge_length():
    # Given the triangle pattern with initialized position
    filename = "triangle"
    g = graph.Graph.from_file(path.join("data", filename))
    g.init_locations()

    # Expect all initial edge distances to be 1.732 +/- 0.1
    actual_lengths = np.array([elen(edge) for edge in g.edges])
    expected_lengths = np.array([1.7] * 3)
    assert np.isclose(
        actual_lengths, expected_lengths, atol=0.2
    ).all(), "the distances between nodes in the triangle should be approx 1.732"


def test_init_locations_simple_line():
    filename = "2line"
    g = graph.Graph.from_file(path.join("data", filename))
    g.init_locations()

    actual_coords = get_locations(g)
    expected_coords = np.array(
        [
            [1.0, 0.0],
            [-1.0, 0.0],
        ]
    )
    assert np.isclose(actual_coords, expected_coords, atol=0.2).all()


def test_init_locations_8wheel():
    filename = "8wheel"
    g = graph.Graph.from_file(path.join("data", filename))
    g.init_locations()

    actual_coords = get_locations(g)
    expected_coords = np.array(
        [
            [1.0, 0.0],
            [0.766044443118978, 0.6427876096865393],
            [0.17364817766693041, 0.984807753012208],
            [-0.4999999999999998, 0.8660254037844387],
            [-0.9396926207859083, 0.3420201433256689],
            [-0.9396926207859084, -0.34202014332566866],
            [-0.5000000000000004, -0.8660254037844384],
            [0.17364817766692997, -0.9848077530122081],
            [0.7660444431189778, -0.6427876096865396],
        ]
    )
    assert np.isclose(actual_coords, expected_coords, atol=0.2).all()
