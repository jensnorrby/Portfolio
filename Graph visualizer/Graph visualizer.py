import argparse
import math
import numpy as np
import os.path as path
import matplotlib.pyplot as plt
import matplotlib.animation as animation

KREP = 1e-2
KATR = 1e-2


class Simulation:
    def __init__(self, graph, max_iterations):
        """Object for running the simulation"""
        self.graph = graph
        self.max_iterations = max_iterations
        self.ani = None

    def run(self, frame_num: int):
        """Function that runs and update the plot"""
        # Calc forces and update locations
        # For every iteration, the graph updates itself.
        for i in range(self.max_iterations):
            self.graph.update()

        # update plot
        self.plot(frame_num)

    def line(self, edge):
        """Returns the points between two nodes"""
        return [edge.node1.x, edge.node2.x], [
            edge.node1.y,
            edge.node2.y,
        ]

    def init_plot(self):
        """Initialises the plot"""
        fig = plt.figure()
        self.ax = fig.add_subplot(1, 1, 1)
        return fig

    def plot(self, frame_num):
        """Plots the nodes and edges"""
        self.ax.clear()
        for edge in self.graph.edges:
            x, y = self.line(edge)
            self.ax.plot(x, y, "k", marker="o", markersize=10)
        self.ax.set_title(f"Frame num: {frame_num}")


def theta(x0, x1, y0, y1):
    return np.arctan2(y1 - y0, x1 - x0)


class Node:
    def __init__(self):
        """Node object, carries the location and forces"""
        self.x = 0.0  # Do not rename
        self.y = 0.0  # Do not rename
        self.fx = 0.0  # Do not rename
        self.fy = 0.0  # Do not rename

    # The add_force function takes two force values and adds them to the forces acting on the node.
    def add_force(self, fx, fy):
        self.fx += fx
        self.fy += fy
    
    # self.move() begins with adjusting the coordinates by adding the forces of the node, to subsequentely clear
    # the forces of any values.
    def move(self):
        self.x += self.fx
        self.y += self.fy
        self.fx = 0.0
        self.fy = 0.0

    def repel(self, other: "Node"):
        #We begin with using the in-built KREP and theta values to define the constants for the two nodes.
        f_rep = KREP / math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        angle = theta(self.x, other.x, self.y, other.y)
        
        # With f_rep and angle defined, we can define the forces acting towards x and y for both nodes.
        fx_self = -1 * f_rep * np.cos(angle)
        fx_other = f_rep * np.cos(angle)
        fy_self = -1 * f_rep * np.sin(angle)
        fy_other = f_rep * np.sin(angle)
        
        # Add_force allows us to add the repelling forces to the forces of each node. 
        self.add_force(fx_self, fy_self)
        other.add_force(fx_other, fy_other)


class Edge:
    def __init__(self, node1: Node, node2: Node):
        """Edge is the connection between two nodes

        Args:
            node1 (Node): Node at first end of the edge
            node2 (Node): Node at other end of the edge
        """
        self.node1 = node1  # Do not rename
        self.node2 = node2  # Do not rename

    def attract(self):
        #We begin by defining the constants.
        f_atr = KATR*((self.node1.x - self.node2.x)**2 + (self.node1.y - self.node2.y)**2)
        angle = theta(self.node1.x, self.node2.x, self.node1.y, self.node2.y)
        
        # With f_atr and angle defined for the edge, the atracting forces on each node can be calculated.
        fx_node1 = f_atr * np.cos(angle)
        fx_node2 = -1 * f_atr * np.cos(angle)
        fy_node1 = f_atr * np.sin(angle)
        fy_node2 = -1 * f_atr * np.sin(angle)

        # And add_force adds the calculated atracting forces to the total forces of the nodes.
        self.node1.add_force(fx_node1, fy_node1)
        self.node2.add_force(fx_node2, fy_node2)


class Graph:
    def __init__(self, nodes: int, edges: list[tuple[int, int]]):
        """Graph object, contains all the Nodes and Edges

        Args:
            nodes (int): Number of nodes to create
            edges (list[tuple[int, int]]): list of edge pairs (node index 1, node index 2)
        """

        self.nodes = []  # do not rename
        self.edges = []  # do not rename

        # Adds nodes number of Nodes
        for _ in range(nodes):
            self.nodes.append(Node())

        # Create all the Edges
        for edge in edges:
            self.edges.append(Edge(self.nodes[edge[0]], self.nodes[edge[1]]))

    @staticmethod
    def from_file(filename):
        #We begin by gathering a list of values from which we can derive our edges. We open the file, read it, then
        #decode it to a non-binary string and split it on linebreaks.
        opened_file = open(filename, "rb")
        binary_text = opened_file.read()
        nonbinary_text = binary_text.decode('utf-8', errors='ignore')
        edgevalues = nonbinary_text.split("\r\n")
        
        #The first value of this list denotes the number of nodes, which is converted to int and then set to {nodes}.
        #{edges} is created as a list that will be appended with tuple[int, int].
        nodes = int(edgevalues[0])
        edges = []

        #To derive the edges as tuples, we identify all the list items with a space in them (which excludes the first
        #and last item) and then split those items on spaces to receive the two nodes of each edge. These nodes are
        #then converted to int and added to a tuple which is then appended to the {edges} list.
        for edge in edgevalues:
            if edge.find(" ") >= 0:
                edgenodes = edge.split(" ")
                edgetuple = (int(edgenodes[0]), int(edgenodes[1]))
                edges.append(edgetuple)
        
        return Graph(nodes, edges)

    def update(self):
        """Calculates and applies all forces"""
        # For each node not to act upon itself, we need a loop that iterates for both item and index through enumerate().
        for index, item in enumerate(self.nodes):
            # To avoid any node acting upon itself or a node which have already asserted its repelling forces, each
            # node only repels the nodes of subsequent indexes.
            n = index + 1
            while n <= (len(self.nodes)-1):
                item.repel(self.nodes[n])
                n += 1

        # Since both the attract and move functions are self-referential to every edge or node,
        #  it can simply be executed for every element on the list.
        for edge in self.edges:
            edge.attract()
        for node in self.nodes:
            node.move()

    def init_locations(self):
        
        # The initial locations are set to approximate a circle.
        for node in self.nodes:
            node.x = np.cos(2 * np.pi * self.nodes.index(node) / len(self.nodes))
            node.y = np.sin(2 * np.pi * self.nodes.index(node) / len(self.nodes))


def main():
    # -------------------------------------
    # Command line input parser
    # Takes following positional args
    # - filename (string)
    # - max_iterations (int)
    # -------------------------------------
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("filename", type=str, help="Pathway to file.")
    arg_parser.add_argument("max_iterations", type=int, help="Number of iterations.")
    # -------------------------------------
    args = arg_parser.parse_args()
    # -------------------------------------

    # Create graph
    graph = Graph.from_file(path.join("data", args.filename))

    # Set initial circular locations
    graph.init_locations()

    # Initialise the plot
    sim = Simulation(graph, args.max_iterations)
    fig = sim.init_plot()

    # And the run the animation
    sim.ani = animation.FuncAnimation(fig, sim.run, interval=5)
    # sim.ani.save('animation.gif', writer='imagemagick', fps=30)
    plt.show()


if __name__ == "__main__":
    main()
