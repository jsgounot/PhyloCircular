# -*- coding: utf-8 -*-
# @Author: jsgounot
# @Date:   2021-04-09 17:00:12
# @Last Modified by:   jsgounot
# @Last Modified time: 2021-04-09 23:50:19

from matplotlib.pyplot import figure
from matplotlib.patches import Circle

from Bio import Phylo

from PhyloCircular import polar_plot

# --------------------------------------------------------------------------

tree = list(Phylo.parse('./example.xml', 'phyloxml'))[0]
fig = figure(figsize=(20, 20), dpi=80)
fig.subplots_adjust(hspace = .3)

# --------------------------------------------------------------
# produce tree n 1

ax = fig.add_subplot(221, polar=True)
ax = polar_plot(tree, ax=ax)

# --------------------------------------------------------------
# produce tree n 2

# Generate aesthetic

find_internal = lambda tree, name : next(iter(clade for clade in tree.get_nonterminals() if clade.name == name), None)

find_internal(tree, "group1").wedge = {"color" : "#90ee90", "alpha" : .5, "fill" : True, 
            "external" : False, "size" : 1.5}

find_internal(tree, "group2").wedge = {"color" : "#f6c85f", "alpha" : .5, "fill" : True, 
            "external" : False, "size" : 1.5}

        
for clade in tree.get_terminals() :
    if clade.name.endswith("BRAFL") :
        clade.patch = lambda coordinates : Circle(coordinates, .05, color="black")
    else :
        clade.patch = lambda coordinates : Circle(coordinates, .05, color="blue")

ax = fig.add_subplot(222, polar=True)

ax = polar_plot(tree, ax=ax, arc=180)


# --------------------------------------------------------------
# produce tree n 3

ax = fig.add_subplot(223, polar=True)

ax = polar_plot(tree, ax=ax, arc=350, start=0, depth_offset=.1,
        label_external=True, patch_external=True, lratio=None,
        pad_label=0.1, pad_patch=0.1, pad_wedge=0)


# --------------------------------------------------------------
# produce tree n 4

find_internal(tree, "group1").wedge["external"] = True
find_internal(tree, "group2").wedge["external"] = True

find_internal(tree, "group1").wedge["size"] = 1.5
find_internal(tree, "group2").wedge["size"] = 3

ax = fig.add_subplot(224, polar=True)

ax = polar_plot(tree, ax=ax, arc=350, start=0, depth_offset=.1,
        label_external=True, patch_external=True, lratio=1.5,
        pad_label=0.2, pad_patch=0.2, pad_wedge=0)

fig.savefig("./test.png")