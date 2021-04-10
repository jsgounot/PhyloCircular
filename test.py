# -*- coding: utf-8 -*-
# @Author: jsgounot
# @Date:   2021-04-10 10:24:48
# @Last Modified by:   jsgounot
# @Last Modified time: 2021-04-10 15:28:02

from matplotlib.pyplot import figure
from matplotlib.patches import Circle

from Bio import Phylo

from PhyloCircular import polar_plot
from PhyloCircular import Externals_labels, Externals_patchs, Externals_heatmap

from random import randint

# --------------------------------------------------------------------------

tree = list(Phylo.parse('./example.xml', 'phyloxml'))[0]
fig = figure(figsize=(8, 8), dpi=80)
fig.subplots_adjust(hspace = .3)


find_internal = lambda tree, name : next(iter(clade for clade in tree.get_nonterminals() if clade.name == name), None)

find_internal(tree, "group1").wedge = {"color" : "#90ee90", "alpha" : .5, "fill" : True}
find_internal(tree, "group2").wedge = {"color" : "#f6c85f", "alpha" : .5, "fill" : True}

for clade in tree.get_terminals() :
    clade.patch = lambda coordinates : Circle(coordinates, .05, color="black")

# heatmap data

hdata = {}
for leaf in tree.get_terminals() :
    hdata.setdefault(leaf, {})
    for row in range(3) :
        name = "Row" + str(row)
        hdata[leaf][name] = randint(0, 100)

# initialization and drawing
        
ax = fig.add_subplot(111, polar=True)

ep = Externals_patchs(bg_internal=True)
el = Externals_labels(size=2.8, bg_internal=True, offset=0.1, pad=.1)
eh = Externals_heatmap(data=hdata, offset=0.5, size=1)
externals = [ep, el, eh]

#ax = polar_plot(tree, ax=ax, arc=350, pad_wedge=1)
ax = polar_plot(tree, ax=ax, arc=300, pad_wedge=0, externals=externals,
    label_leaf=False, patch_leaf=True, wedge=False)

fig.savefig("./test.png")