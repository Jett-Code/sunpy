"""
===========================================
Base and Running Difference in MapSequences
===========================================

This example illustrates how to do base and running differencing with a MapSequence.
Base differencing uses a fixed map when compared to running difference.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

import sunpy.map
import sunpy.physics.differential_rotation as diffrot
from sunpy.data.sample import AIA_193_CUTOUT01_IMAGE, AIA_193_CUTOUT02_IMAGE, AIA_193_CUTOUT03_IMAGE

###############################################################################
# We create the MapSequence using the AIA_193_CUTOUT sample data.
# To create a MapSequence, we can call Map directly and add in a keyword to output a MapSequence instead.
aiamapseq = sunpy.map.Map(AIA_193_CUTOUT01_IMAGE, AIA_193_CUTOUT02_IMAGE,
                           AIA_193_CUTOUT03_IMAGE, sequence=True)

############################################################################
# In case of running difference, we loop through all the maps in the
# aiamapseq and differentially rotate each map in the MapSequence
# with respect to the previous map
# while in case of base difference we differentially
# rotate each map in the MapSequence to the time of the base map.
# We then store all the difference maps in a list.
base_diffmap = []
running_diffmap = []
for i, map_i in enumerate(aiamapseq[1:]):
    aiamap_rot = diffrot.diffrot_map(map_i, time=aiamapseq[0].date)
    aiamapseq_rot = diffrot.diffrot_map(aiamapseq[i+1], time=aiamapseq[i].date)
    diffdata = map_i.data - aiamap_rot.data
    smap_base = sunpy.map.Map(diffdata, map_i.meta)
    diffdata = aiamapseq_rot.data - map_i.data
    smap_run = sunpy.map.Map(diffdata, map_i.meta)
    smap_base.plot_settings['cmap'] = plt.get_cmap('Greys_r')
    smap_base.plot_settings['norm'] = colors.LogNorm(100, smap_base.max())
    smap_run.plot_settings['cmap'] = plt.get_cmap('Greys_r')
    smap_run.plot_settings['norm'] = colors.LogNorm(100, smap_run.max())
    base_diffmap.append(smap_base)
    running_diffmap.append(smap_run)

############################################################################
# This plots the original MapSequence
aiamapseq.peek()

##############################################################################
# This plots the final MapSequence obtained after implementing the base difference
result_mapseq = sunpy.map.MapSequence(base_diffmap)
result_mapseq.peek()

############################################################################
# This plots the final MapSequence after implementing the running difference
result_mapseq = sunpy.map.MapSequence(running_diffmap)
result_mapseq.peek()
plt.show()
