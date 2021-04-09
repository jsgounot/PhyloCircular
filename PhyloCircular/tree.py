import math
import numpy as np
from scipy.interpolate import interp1d

from matplotlib.patches import Wedge, Arc
from matplotlib.artist import Artist
from matplotlib.collections import LineCollection

def internal_clades_angles(clade, angles) :
    for subclade in clade:
            if subclade not in angles:
                internal_clades_angles(subclade, angles)
        
    # Closure over heights
    angles[clade] = (angles[clade.clades[0]] + angles[clade.clades[-1]]) / 2.0

def clade_angles(tree, arc, start) :
    assert arc > 0 and arc < 360
    count = tree.count_terminals()
    leaves_distances = (arc / (count - 1))
    
    angles = {
            tip: start + (leaves_distances * i)  
            for i, tip in enumerate(reversed(tree.get_terminals()))
        }

    if tree.root.clades:
        internal_clades_angles(tree.root, angles)
    
    return angles

def clade_depth(tree) :
    depths = tree.depths()
    
    if not max(depths.values()) :
        depths = tree.depths(unit_branch_lengths=True)   
        
    return depths 

def draw_label(angle, depth, clade, ax, pad, label_offset=.05) :       
    
    rotation = angle + 180 if 270 > angle > 90 else angle
    ha = "right" if 270 > angle > 90 else "left"
        
    label = clade.name

    label_offset = ax.get_ylim()[1] * label_offset
    depth = depth + label_offset + pad
     
    rad = np.deg2rad(angle)    
    ax.text(rad, depth, label, rotation=rotation, ha=ha, va="center", rotation_mode='anchor')


def draw_clade_wedge(clade, angles, depths, ax, mdepth, lratio, pad) :
    nnodes = len(clade.get_terminals())

    mdepth = mdepth + pad
       
    min_angle = min(angles[child]
            for child in clade.get_terminals())
        
    max_angle = max(angles[child]
        for child in clade.get_terminals())

    angles_diff = ((max_angle - min_angle) / (nnodes + 2)) / 2
    
    min_angle = min_angle - angles_diff
    max_angle = max_angle + angles_diff 

    kwargs = clade.wedge.copy()

    lsize = kwargs.pop("size", lratio)
    external = kwargs.pop("external", False)


    if external :
        wedge = Wedge((0, 0), mdepth + lsize, min_angle, max_angle, width=lsize,
            transform=ax.transData._b, ** kwargs)

    else :
        wedge = Wedge((0, 0), mdepth, min_angle, max_angle, transform=ax.transData._b,
            ** kwargs)

    ax.add_patch(wedge)   
    
    # Until a better solution is found

    rotation = min_angle + 180 if 270 > min_angle > 90 else min_angle
    
    if external :
        ha = "right" if 270 > min_angle > 90 else "left"
    else :
        ha = "left" if 270 > min_angle > 90 else "right"
    
    va = "top" if 270 > min_angle > 90 else "bottom"

    rad = np.deg2rad(min_angle)
    ax.text(rad, mdepth, clade.name, rotation=rotation, ha=ha, va=va, rotation_mode='anchor')
    
def draw_patch(angle, depth, ax, patch, pad) :
    rad = np.deg2rad(angle)
    depth = depth + pad
    x_coor = depth * np.cos(rad)
    y_coor = (depth * np.sin(rad))
    
    patch = patch((x_coor, y_coor))
    patch.set_transform(ax.transData._b)
    patch.set_zorder(3)
    ax.add_patch(patch)
    
def draw_baseline(node1, node2, ax, lc) :
    a1, d1 = node1
    a2, d2 = node2
    
    # we mesure the number of segments which
    # will be produced
    factor = 1
    ncount = int(abs(a1 - a2) / 5 * factor)
    if ncount < 2 : ncount = 2
        
    angles = np.deg2rad((a1, a2))
    x = np.linspace(angles[0], angles[1], ncount)
    y = interp1d(angles, (d1, d2))(x)
    segs = zip(x, y)
       
    lc.append(LineCollection([list(segs)], color="black"))
    #ax.plot(x, y, color="black")
    
    """
    a1, a2 = sorted((a1, a2))
    patch = Arc((0, 0), d1*2, d1*2, 0, a1, a2)
    patch.set_transform(ax.transData._b)
    #ax.add_patch(patch)
    lc.append(patch)
    """
    
def draw_depthline(angle, depth, cdepth, ax, lc) :
    rad = np.deg2rad(angle)
    lc.append(LineCollection([[(rad, depth), (rad, cdepth)]], color="black"))
    #ax.plot([rad,rad], [depth, cdepth], color="black")


def draw_clade(clade, ax, angles, depths, lc, mdepth, 
    depth_offset, label_external, patch_external, lratio,
    pad_label, pad_patch, pad_wedge) :
    
    # Recursively draw a tree, down from the given clade   
    angle = angles[clade]
    depth = depths[clade] + depth_offset
    
    
    try :
        patch = clade.patch
        ldepth = depth if not patch_external else mdepth
        draw_patch(angle, ldepth, ax, patch, pad_patch)
    except AttributeError:
        pass
        
    # draw label
    if clade.name and not clade.clades :
        ldepth = depth if not label_external else mdepth
        draw_label(angle, ldepth, clade, ax, pad_label)

    try :
        if clade.wedge :
            draw_clade_wedge(clade, angles, depths, ax, mdepth, lratio, pad_wedge)
    except AttributeError as e :
        pass
    
    for child in clade.clades :      
        # children
        
        cangle = angles[child]
        cdepth = depths[child] + depth_offset
        
        # draw lines
        draw_baseline((angle, depth), (cangle, depth), ax, lc)
        draw_depthline(cangle, depth, cdepth, ax, lc)
        
        draw_clade(child, ax, angles, depths, lc, mdepth,
            depth_offset, label_external, patch_external, lratio,
            pad_label, pad_patch, pad_wedge)
        
    # ax.get_figure().canvas.draw()

def polar_plot(tree, ax=None, arc=350, start=0, depth_offset=.1,
        label_external=False, patch_external=False, lratio=None,
        pad_label=0, pad_patch=0, pad_wedge=0) :

    if ax is None :
        fig = figure(figsize=(50, 50), dpi=80)
        ax = fig.add_subplot(polar=True)    

    lc = []
        
    angles = clade_angles(tree, arc, start)
    depths = clade_depth(tree)
    
    mdepth = max(depths.values()) + depth_offset
    
    if label_external or patch_external :
        lratio = lratio or mdepth / 2
        ax.set_ylim(0, mdepth + mdepth * .1 + lratio)
    else :
        ax.set_ylim(0, mdepth + mdepth * .1)
    
    # root depthline
    angle = angles[tree.root]
    draw_depthline(angle, 0, depth_offset, ax, lc)    

    # draw clades
    draw_clade(tree.root, ax, angles, depths, lc, mdepth, depth_offset, 
        label_external, patch_external, lratio, pad_label, pad_patch, pad_wedge)
    
    print ("done 1")
    
    for element in lc :
        ax.add_collection(element)
    
    print ("done 2")
    
    ax.axis("off")
    return ax