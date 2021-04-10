# PhyloCircular

An attempt to produce circular phylogenetic tree with matplotlib. Based on the [biopython]("https://biopython.org/") Phylo [library](https://biopython.org/wiki/Phylo). 

![Example image](https://github.com/jsgounot/PhyloCircular/blob/main/test.png)

### Usage

```
def polar_plot(tree, ax=None, arc=350, start=0, root_distance=.1,
        label_leaf=True, patch_leaf=True, wedge=True, pad_label=0, 
        pad_patch=0, pad_wedge=0, externals=[])
```

* `tree` : The Phylo tree object.
* `ax` : An ax, if not provided, one will be created
* `arc` : Angle (degree) of your tree
* `start` : Starting angle
* `root_distance` : Distance between the center of graph and your first clade (root)
* `label_leaf` : Draw leaf label next to leaves location
* `patch_leaf` : Draw leaf patch directly on leaves location
* `wedge` : Draw wedges inside the tree
* `pad_label` : Text depth distance global padding
* `pad_patch` : Patch depth distance global padding
* `pad_wedge` : Wedge depth distance global padding
* `externals` : External rings to the tree

### Example

```python3
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
```