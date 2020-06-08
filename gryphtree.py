import pygraphviz as pgv
import pydot as pd

try:
    G = pgv.AGraph('testgraph.dot')
    G.layout(prog='dot')
    G.add_node('b')
    G.write('output.gv')

    graphs = pd.graph_from_dot_file('output.gv')
    graphs[0].write_svg('output.svg')
except Exception as e:
    print(e)
    exit()
