import json
import numpy as np
import matplotlib.pyplot as plt

import basegantt as bg
import argparse

parser = argparse.ArgumentParser(
                    prog='Python Gantt chart',
                    description='Produces a figure of the Gantt chart, to be saved. Suggested formats are PNG and SVG, the latter being editable.',
                    epilog='-- good luck with your project!')

parser.add_argument('filename')
args = parser.parse_args()
#open json file
f = open(args.filename,'r')
all = json.load(f)
f.close()
all = all[0]

#these parameters influence the rendering
left_delta = 0.5
right_delta = 1.0
barheight = 1.0

gantt = bg.gantt(all)

plt.rcParams.update({'font.size': gantt.fontsize})

#prepare the canvas
base = gantt.aspectratio
factor = gantt.scalefactor
fig,ax = plt.subplots(figsize=(base[0]*factor,base[1]*factor))

ax.grid(True,'both')
ax.set_title(gantt.title)
#ax2=ax.twinx()



vpos = 0
hbar = 1

for wp in gantt._wps:
    vpos-=hbar
    #matplotlib.pyplot.barh(y, width, height=0.8, left=None, *, align='center', **kwargs)
    ax.barh(vpos-hbar/2,wp.stop-wp.start+1,left=wp.start-1,height = barheight,align='center',color=wp.color)
    ax.text(-left_delta,vpos-hbar/2,wp.id,horizontalalignment='right',verticalalignment='center',color=wp.id_color)
    ax.text(gantt.nmonths+right_delta,vpos-hbar/2,wp.title,horizontalalignment='left',verticalalignment='center',color=wp.title_color)
    vpos-=hbar
    for task in wp._tasks:
        vpos-=hbar
        ax.barh(vpos-hbar/2,task.stop-task.start+1,left=task.start-1,height = barheight,align='center',color=task.color)
        ax.text(-left_delta,vpos-hbar/2,task.id,horizontalalignment='right',verticalalignment='center',color=task.id_color)
        ax.text(gantt.nmonths+right_delta,vpos-hbar/2,task.title,horizontalalignment='left',verticalalignment='center',color=task.title_color)
        for dv in task._deliverables:
            ax.text(dv.month,vpos-hbar/2,dv.id,fontsize=dv.font_size,color='w',horizontalalignment='center',verticalalignment='center',bbox=dict(boxstyle='Round',facecolor=dv.color,alpha=1))
        vpos-=hbar
vpos-=hbar


for dataset in gantt._sets:
    vpos-=hbar
    months = dataset.data
    ax.text(-left_delta,vpos-hbar/2,dataset.id,horizontalalignment='right',verticalalignment='center',color=dataset.id_color)
    if dataset.labels is not None:
        labels = dataset.labels
        for i in range(len(months)):
            m = months[i]
            l = labels[i]
            ax.text(m,vpos-hbar/2,l,fontsize=6,color=dataset.text_color,horizontalalignment='center',verticalalignment='center',bbox=dict(boxstyle='Round',facecolor=dataset.color,alpha=1))    
    else:
        ax.plot(months,vpos-hbar/2*np.ones(len(months)),marker=dataset.symbol,markersize=dataset.size,color=dataset.color,ls='')
    vpos-=hbar
vpos-=hbar
ax.set_yticks(np.arange(-0.5,vpos,-2),minor=False,labels='')
ax.set_xticks(range(0,gantt.nmonths+1),minor=True)
ax.set_xticks(range(0,gantt.nmonths+1,2),minor=False)
ax.set_ylim((vpos+0.5,-0.5))
ax.set_xlim((0,gantt.nmonths))

plt.tight_layout()
plt.show()