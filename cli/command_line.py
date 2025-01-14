#!/usr/bin/python

import sys
import os
from os import path
import numpy as np
import networkx as nx
from algorithms.wd import wd
from io_utils.plot_utils import *
from algorithms.retiming.strategies import *
from algorithms.common import apply_retiming

if len(sys.argv) < 3:
    print("arguments must be: <input_graph> <output_folder>")
    sys.exit(-1)

file_in_graph = sys.argv[1]
out_folder = sys.argv[2].replace(' ', '')

if out_folder[-1] != '/':
    out_folder += '/'

if not path.exists(out_folder):
    os.makedirs(out_folder)

w_out = out_folder + "w"
d_out = out_folder + "d"
out_graph_opt1 = out_folder + "opt1"
out_graph_opt2 = out_folder + "opt2"

print(f'Reading graph from {file_in_graph}')
graph = read_graph_from_file(file_in_graph)
print(f'Graph has been read from file.')

print("Calculating WD")
W, D = wd(graph)
print("WD has been calculated")

print(f'Writing WD to file {w_out}')
np.savetxt(w_out, W)
print(f'WD has been written to file {d_out}')
np.savetxt(d_out, D)
print('Running OPT1')
min_clock_opt1, retiming_opt_1 = opt1(graph, W, D)
print('Done running OPT1')

print('Running OPT2')
min_clock_opt2, retiming_opt_2 = opt2(graph, W, D)
print('Done running OPT2\n\n')

print(f'OPT1 --> min_clock={min_clock_opt1}')
print(f'OPT1 --> retiming={retiming_opt_1}\n\n')
print(f'OPT2 --> min_clock={min_clock_opt2}')
print(f'OPT2 --> retiming={retiming_opt_2}\n\n')

print('Applying OPT1 retiming to graph')
graph_opt1 = apply_retiming(graph, retiming_opt_1)

print('Applying OPT" retiming to graph')
graph_opt2 = apply_retiming(graph, retiming_opt_2)

print('Saving OPT1 retimed graph')
nx.nx_agraph.write_dot(graph_opt1, out_graph_opt1)

print('Saving OPT2 retimed graph')
nx.nx_agraph.write_dot(graph_opt2, out_graph_opt2)

print('Done')
