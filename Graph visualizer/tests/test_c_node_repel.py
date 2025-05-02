import pytest
import numpy as np
import os.path as path
import graph


@pytest.mark.parametrize(
    "x1,y1,x2,y2,expected_fx,expected_fy",
    [
        (-1, -2, 3, 2, 0.00125, 0.00125),
        (-0.1, -0.1, 0.1, 0.1, 0.025, 0.025),
        (-4, -0.1, 3.0, 0.2, 1.42595e-3, 6.11122e-05),
    ],
)
def test_node_repel(x1, y1, x2, y2, expected_fx, expected_fy):
    # Create two nodes
    node1 = graph.Node()
    node1.x = x1
    node1.y = y1

    node2 = graph.Node()
    node2.x = x2
    node2.y = y2

    # Calculate the repelling force
    node1.repel(node2)
    fx1 = node1.fx
    fy1 = node1.fy
    fx2 = node2.fx
    fy2 = node2.fy

    # Check that we get to correct values
    assert abs(fx1) == pytest.approx(expected_fx, rel=1e-2)
    assert abs(fy1) == pytest.approx(expected_fy, rel=1e-2)
