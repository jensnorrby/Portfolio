import pytest
import sys
import graph


def test_a_iteration_argument(mocker):
    # Mock all other calls
    mocker.patch("graph.Graph")
    mocker.patch("graph.Simulation")
    mocker.patch("matplotlib.animation.FuncAnimation")

    sys.argv = ["imdb.py", "2line", "100"]
    graph.main()

    args = graph.Simulation.call_args[0]
    assert type(args[1]) == int, "max_iterations should be an integer"
    assert args[1] == 100

    sys.argv = ["imdb.py", "2line", "178"]
    graph.main()

    args = graph.Simulation.call_args[0]
    assert args[1] == 178
