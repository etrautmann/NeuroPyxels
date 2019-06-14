# -*- coding: utf-8 -*-
"""
2018-07-20
@author: Maxime Beau, Neural Computations Lab, University College London
"""
import os
import os.path as op

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from rtn.utils import phyColorsDic, seabornColorsDic, DistinctColors20, DistinctColors15, mark_dict,\
                    npa, sign, minus_is_1, thresh, smooth, \
                    _as_array, _unique, _index_of
                    
from rtn.npix.gl import get_good_units
from rtn.npix.spk_wvf import get_channels
from rtn.npix.corr import acg, ccg, gen_sfc, find_significant_hist_peak, make_cm
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D

#%% regular histogram
def hist_MB(arr, a, b, s, title='MB hist', xlabel='', ylabel=''):
    hist=np.histogram(arr, bins=np.arange(a,b,s))
    y=hist[0]
    x=hist[1][:-1]
    fig, ax = plt.subplots()
    ax.bar(x=x, height=y, width=s)
    ax.set_title(title)
    ax.set_xlabel(xlabel) if len(xlabel)>0 else ax.set_xlabel('Window:[{},{}] - binsize:{}'.format(a,b,s))
    ax.set_ylabel(ylabel) if len(ylabel)>0 else ax.set_ylabel('Counts')
    return fig

#%% Save matplotlib animations
# https://towardsdatascience.com/how-to-create-animated-graphs-in-python-bb619cc2dec1
##### TO CREATE A SERIES OF PICTURES
 
def make_views(ax,angles,width, height, elevation=None,
                prefix='tmprot_',**kwargs):
    """
    Makes jpeg pictures of the given 3d ax, with different angles.
    Args:
        ax (3D axis): te ax
        angles (list): the list of angles (in degree) under which to
                       take the picture.
        width,height (float): size, in inches, of the output images.
        prefix (str): prefix for the files created. 
     
    Returns: the list of files created (for later removal)
    """
     
    files = []
    ax.figure.set_size_inches(width,height)
     
    for i,angle in enumerate(angles):
        
        ax.view_init(elev = elevation, azim=angle)
        ax.set_xlim3d([206, 212])
        ax.set_ylim3d([208, 213])
        ax.set_zlim3d([207, 213])
        fname = '%s%03d.png'%(prefix,i)
        ax.figure.savefig(fname)
        files.append(fname)
     
    return files
 
 
 
##### TO TRANSFORM THE SERIES OF PICTURE INTO AN ANIMATION
 
def make_movie(files,output, fps=10,bitrate=1800,**kwargs):
    """
    Uses mencoder, produces a .mp4/.ogv/... movie from a list of
    picture files.
    """
     
    output_name, output_ext = os.path.splitext(output)
    command = { '.mp4' : 'mencoder "mf://%s" -mf fps=%d -o %s.mp4 -ovc lavc\
                         -lavcopts vcodec=msmpeg4v2:vbitrate=%d'
                         %(",".join(files),fps,output_name,bitrate)}
                          
    command['.ogv'] = command['.mp4'] + '; ffmpeg -i %s.mp4 -r %d %s'%(output_name,fps,output)
     
    print(command[output_ext])
    output_ext = os.path.splitext(output)[1]
    os.system(command[output_ext])
 
 
 
def make_gif(files,output,delay=100, repeat=True,**kwargs):
    """
    Uses imageMagick to produce an animated .gif from a list of
    picture files.
    """
     
    loop = -1 if repeat else 0
    os.system('convert -delay %d -loop %d %s %s'
              %(delay,loop," ".join(files),output))
 
 
 
 
def make_strip(files,output,**kwargs):
    """
    Uses imageMagick to produce a .jpeg strip from a list of
    picture files.
    """
     
    os.system('montage -tile 1x -geometry +0+0 %s %s'%(" ".join(files),output))
     
     
     
##### MAIN FUNCTION
 
def rotanimate(ax, width, height, angles, output, **kwargs):
    """
    Produces an animation (.mp4,.ogv,.gif,.jpeg,.png) from a 3D plot on
    a 3D ax
     
    Args:
        ax (3D axis): the ax containing the plot of interest
        angles (list): the list of angles (in degree) under which to
                       show the plot.
        output : name of the output file. The extension determines the
                 kind of animation used.
        **kwargs:
            - width : in inches
            - heigth: in inches
            - framerate : frames per second
            - delay : delay between frames in milliseconds
            - repeat : True or False (.gif only)
    """
         
    output_ext = os.path.splitext(output)[1]
 
    files = make_views(ax,angles, width, height, **kwargs)
     
    D = { '.mp4' : make_movie,
          '.ogv' : make_movie,
          '.gif': make_gif ,
          '.jpeg': make_strip,
          '.png':make_strip}
           
    D[output_ext](files,output,**kwargs)
     
    for f in files:
        os.remove(f)

def make_mpl_animation(ax, Nangles, delay, width=10, height=10, saveDir='~/Downloads', title='movie', frmt='gif', axis=True):
    '''
    ax is the figure axes that you will make rotate along its vertical axis,
    on Nangles angles (default 300),
    separated by delay time units (default 2),
    at a resolution of widthxheight pixels (default 10x10),
    saved in saveDir directory (default Downloads) with the title title (default movie) and format frmt (gif).
    '''
    assert frmt in ['gif', 'mp4', 'ogv']
    if not axis: plt.axis('off') # remove axes for visual appeal
    oldDir=os.getcwd()
    saveDir=op.expanduser(saveDir)
    os.chdir(saveDir)
    angles = np.linspace(0,360,Nangles)[:-1] # Take 20 angles between 0 and 360
    ttl='{}.{}'.format(title, frmt)
    rotanimate(ax, width, height, angles,ttl, delay=delay)
    
    os.chdir(oldDir)

#%% Waveforms
def plot_wvf_16(datam):
    datam = np.squeeze(datam)
    if datam.shape == (82, 16):
        datam = datam.T
    assert datam.shape == (16, 82)
    fig, ax = plt.subplots(int(datam.shape[0]*1./2), 2)
    ylim1, ylim2 = np.squeeze(np.min(datam))-10, np.squeeze(np.max(datam))+10
    for i in range(datam.shafind_significant_ccg_peakpe[0]):
        print(i//2, i%2)
        ax[i//2,i%2].plot(datam[i,:])
        ax[i//2,i%2].set_ylim([ylim1, ylim2])
    fig.tight_layout()
    
    return fig

def plot_wvf_setCh(data, chStart=179, title = 'Mother unit.', Nchannels=8, \
                   color=(0./255, 0./255, 0./255), ampFactor=500, fs=30000, 
                   labels=True, saveDir='~/Downloads', saveFig=False, saveData=False, ylim=0):
    assert data.shape == (100, 82, 384)
    saveDir=op.expanduser(saveDir)
    chStart = int(min(chStart-1, data.shape[2]-Nchannels-1))
    chEnd = int(chStart+Nchannels)
    fig, ax = plt.subplots(int(Nchannels*1./2), 2, figsize=(8, 16), dpi=80)
    data = data*(1.2e6/2**10/ampFactor) # Correct voltage
    datam = np.rollaxis(data.mean(0),1)
    datastd = np.rollaxis(data.std(0),1)
    data = data[:, :, chStart:chEnd]
    datam = datam[chStart:chEnd, :]
    datastd = datastd[chStart:chEnd, :]
    x = np.linspace(0, data.shape[1]*1./(fs/1000), data.shape[1]) # Plot 82 datapoints between 0 and 82/30 ms
    if ylim==0:
        ylim1, ylim2 = np.squeeze(np.min(datam)-np.max(datastd)-20), np.squeeze(np.max(datam)+np.max(datastd)+20)
    else:
        ylim1, ylim2 = ylim[0], ylim[1]
    for i in range(data.shape[2]):
        i1, i2 = data.shape[2]//2-1-i//2, i%2
        for j in range(data.shape[1]):
            ax[i1, i2].set_ylim([ylim1, ylim2])
            ax[i1, i2].plot(x, data[j,:, i], linewidth=0.5, alpha=0.3, color=color)
        #r, c = int(Nchannels*1./2)-1-(i//2),i%2
        color_dark=(max(color[0]-0.08,0), max(color[1]-0.08,0), max(color[2]-0.08,0))
        ax[i1, i2].plot(x, datam[i, :], linewidth=2, color=color_dark, alpha=1)
        ax[i1, i2].plot(x, datam[i, :]+datastd[i,:], linewidth=1, color=color, alpha=0.5)
        ax[i1, i2].plot(x, datam[i, :]-datastd[i,:], linewidth=1, color=color, alpha=0.5)
        ax[i1, i2].fill_between(x, datam[i, :]-datastd[i,:], datam[i, :]+datastd[i,:], facecolor=color, interpolate=True, alpha=0.2)
        if labels:
            ax[i1, i2].set_title(chStart+(2*(i//2)+i%2), size=12, loc='right', weight='bold')
            if i2==0:
                ax[i1, i2].set_ylabel('EC V (uV)', size=14)
            if i1==int(Nchannels/2)-1:#start plotting from top
                ax[i1, i2].set_xlabel('t (ms)', size=20)
            ax[i1, i2].tick_params(labelsize=16)
        else:
            ax[i1, i2].axis('off')
#            for axis in ['x', 'y']:
#                ax[r, c].tick_params(axis=axis,          # changes apply to the x-axis
#                                which='both',      # both major and minor ticks are affected
#                                bottom=False,      # ticks along the bottom edge are off
#                                top=False,         # ticks along the top edge are off
#                                labelbottom=False) # labels along the bottom edge are off
        # Hide the right and top spines
        ax[i1, i2].spines['right'].set_visible(False)
        ax[i1, i2].spines['top'].set_visible(False)
        ax[i1, i2].spines['left'].set_visible(False)
        ax[i1, i2].spines['bottom'].set_visible(False)

    if labels:
        fig.suptitle(title, size=20, weight='bold')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.subplots_adjust(left=0.2, bottom=0.05, right=0.8, top=0.95, wspace=0.1, hspace=0.05)
    
    return fig
    
def plot_wvf_mainCh(data, title = 'Merged units 19, 452, 555', color=(0./255, 0./255, 0./255), 
                    ampFactor=500, fs=30000, plotRaw=False, channel=None, saveDir='~/Downloads', 
                    saveFig=False, saveData=False, ylim=0):
    assert data.ndim == 3# (100, 82, 384) or  data.shape == (100, 82, 373)
    saveDir=op.expanduser(saveDir)
    data = data*(1.2e6/2**10/ampFactor) # Correct voltage
    fig, ax = plt.subplots()
    datam = np.rollaxis(data.mean(0),1)
    datastd = np.rollaxis(data.std(0),1)
    if not channel:
        mainChannel = np.argwhere(np.max(abs(datam),1) == np.max(np.max(abs(datam),1)))
    else:
        mainChannel = [[channel]]
    print(mainChannel)
    data = data[:, :, mainChannel]
    datam = np.squeeze(datam[mainChannel, :])
    datastd = np.squeeze(datastd[mainChannel, :])
    x = np.linspace(0, data.shape[1]*1./(fs/1000), data.shape[1]) # Plot 82 datapoints between 0 and 82/30 ms
    #ylim1, ylim2 = np.squeeze(np.min(datam))-10, np.squeeze(np.max(datam))+10
    if plotRaw:
        for j in range(data.shape[1]):
            #ax.set_ylim([ylim1, ylim2])
            ax.plot(x, data[j,:, 0], linewidth=0.5, alpha=0.5, color=color)

    ax.plot(x, datam, linewidth=2.5, color=color)
    ax.plot(x, datam+datastd, linewidth=1, color=color, alpha=0.7)
    ax.plot(x, datam-datastd, linewidth=1, color=color, alpha=0.7)
    ax.fill_between(x, datam-datastd, datam+datastd, facecolor=color, interpolate=True, alpha=0.3)
    if type(ylim)==list or type(ylim)==tuple:
        ax.set_ylim(ylim)
    ax.set_title(title)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Extracellular Potential (uV)')
    fig.tight_layout()
    
    return fig
    

#%% Correlograms

def plt_ccg(uls, CCG, cbin=0.04, cwin=5, bChs=None, fs=30000, saveDir='~/Downloads', saveFig=True, 
            show=True, pdf=True, png=False, rec_section='all', labels=True, std_lines=True, title=None, color=-1, 
            saveData=False, ylim=0, normalize='Hertz'):
    '''Plots acg and saves it given the acg array.
    unit: int.
    ACG: acg array in non normalized counts.
    cwin and cbin: full window and bin in ms.
    phycolor: index (0 to 5) of the phy colorchart.
    savedir: plot saving destination.
    save: boolean, to save the figure or not.
    '''
    global phyColorsDic
    # CCGsides=np.append(CCG[:int(1*len(CCG)*1./3)], CCG[int(2*len(CCG)*1./3):])
    mn = np.mean(np.append(CCG[:int(len(CCG)*2./5)], CCG[int(len(CCG)*3./5):]))
    std = np.std(np.append(CCG[:int(len(CCG)*2./5)], CCG[int(len(CCG)*3./5):]))
    cbin = np.clip(cbin, 1000*1./fs, 1e8)
    if type(color)==int: # else, an actual color is passed
        color=phyColorsDic[color]
    fig, ax = plt.subplots(figsize=(10,8))
    x=np.linspace(-cwin*1./2, cwin*1./2, CCG.shape[0])
    assert x.shape==CCG.shape
    ax.bar(x=x, height=CCG, width=cbin, color=color, edgecolor=color)
    if ylim==0:
        if normalize=='Hertz':
            yl=max(CCG); ylim=int(yl)+5-(yl%5);
        elif normalize=='Pearson':
            yl=max(CCG); ylim=yl+0.01-(yl%0.01);
    ax.set_ylim([0, ylim])
    ax.plot([0,0], ax.get_ylim(), ls="--", c=[0,0,0], lw=2)
    if labels:
        if std_lines:
            ax.plot([x[0], x[-1]], [mn,mn], ls="--", c=[0,0,0], lw=2)
            for st in [1,2,3]:
                ax.plot([x[0], x[-1]], [mn+st*std,mn+st*std], ls="--", c=[0.5,0,0], lw=0.5)
                ax.plot([x[0], x[-1]], [mn-st*std,mn-st*std], ls="--", c=[0,0,0.5], lw=0.5)
        ax.set_ylabel("Crosscorrelation (Hz)", size=20)
        ax.set_xlabel('Time (ms)', size=20)
        ax.set_xlim([-cwin*1./2, cwin*1./2])
        if type(title)!=str:
            if type(bChs)!=list:
                title="Units {}->{} ({})s".format(uls[0], uls[1], str(rec_section)[0:50].replace(' ',  ''))
            else:
                title="Units {}@{}->{}@{} ({})s".format(uls[0], bChs[0], uls[1], bChs[1], str(rec_section)[0:50].replace(' ',  ''))
        ax.set_title(title, size=22)
        ax.tick_params(labelsize=20)
    fig.tight_layout()
    plt.close() if not show else plt.show()
    if saveFig or saveData:
        saveDir=op.expanduser(saveDir)
        if not os.path.isdir(saveDir): os.mkdir(saveDir)
        if saveFig:
            if pdf: fig.savefig(saveDir+'/ccg%d-%d_%d_%.2f.pdf'%(uls[0], uls[1], cwin, cbin))
            if png: fig.savefig(saveDir+'/ccg%d-%d_%d_%.2f.png'%(uls[0], uls[1], cwin, cbin))
        if saveData:
            np.save(saveDir+'/ccg%d-%d_%d_%.2f_x.npy'%(uls[0], uls[1], cwin, cbin), x)
            np.save(saveDir+'/ccg%d-%d_%d_%.2f_y.npy'%(uls[0], uls[1], cwin, cbin), CCG)
        
    return fig
        
def plt_acg(unit, ACG, cbin=0.2, cwin=80, bChs=None, color=0, fs=30000, saveDir='~/Downloads', saveFig=True, 
            show=True, pdf=True, png=False, rec_section='all', labels=True, title=None, ref_per=True, saveData=False, ylim=0, normalize='Hertz'):
    '''Plots acg and saves it given the acg array.
    unit: int.
    ACG: acg array in non normalized counts.
    cwin and cbin: full window and bin in ms.
    phycolor: index (0 to 5) of the phy colorchart.
    savedir: plot saving destination.
    saveFig: boolean, to save the figure or not.
    '''
    global phyColorsDic
    cbin = np.clip(cbin, 1000*1./fs, 1e8)
    if type(color)==int: # else, an actual color is passed
        color=phyColorsDic[color]
    fig, ax = plt.subplots(figsize=(10,8))
    x=np.linspace(-cwin*1./2, cwin*1./2, ACG.shape[0])
    assert x.shape==ACG.shape
    ax.bar(x=x, height=ACG, width=cbin, color=color, edgecolor=color)
    if ylim==0:
        if normalize=='Hertz':
            yl=max(ACG); ylim=int(yl)+5-(yl%5);
        elif normalize=='Pearson':
            yl=max(ACG); ylim=yl+0.01-(yl%0.01);
    ax.set_ylim([0, ylim])
    if labels:
        ax.set_ylabel("Autocorrelation (Hz)", size=20)
        ax.set_xlabel('Time (ms)', size=20)
        ax.set_xlim([-cwin*1./2, cwin*1./2])
        if type(title)!=str:
            if type(bChs)!=list:
                title="Unit {} ({})s".format(unit, str(rec_section)[0:50].replace(' ',  ''))
            else:
                title="Unit {}@{} ({})s".format(unit, bChs[0], str(rec_section)[0:50].replace(' ',  ''))
        ax.set_title(title, size=22)
        ax.tick_params(labelsize=20)
        if ref_per:
            ax.plot([-1, -1], [0, max(ACG)], color='black', linestyle='--', linewidth=1)
            ax.plot([1, 1], [0, max(ACG)], color='black', linestyle='--', linewidth=1)
    fig.tight_layout()
    plt.close() if not show else plt.show()
    if saveFig or saveData:
        saveDir=op.expanduser(saveDir)
        if not os.path.isdir(saveDir): os.mkdir(saveDir)
        if saveFig:
            if pdf: fig.savefig(saveDir+'/acg%d_%d_%.2f.pdf'%(unit, cwin, cbin))
            if png: fig.savefig(saveDir+'/acg%d_%d_%.2f.png'%(unit, cwin, cbin))
        if saveData:
            np.save(saveDir+'/acg%d_%d_%.2f_x.npy'%(unit, cwin, cbin), x)
            np.save(saveDir+'/acg%d_%d_%.2f_y.npy'%(unit, cwin, cbin), ACG)
    return fig
        
    
def plt_ccg_subplots(units, CCGs, cbin=0.2, cwin=80, bChs=None, Title=None, saveDir='~/Downloads', 
                     saveFig=False, prnt=False, show=True, pdf=True, png=False, rec_section='all', 
                     labels=True, title=None, std_lines=True, ylim=0, normalize='Hertz'):
    colorsDic = {
    0:(53./255, 127./255, 255./255),
    1:(255./255, 0./255, 0./255),
    2:(255./255,215./255,0./255),
    3:(238./255, 53./255, 255./255),
    4:(84./255, 255./255, 28./255),
    5:(255./255,165./255,0./255),
    -1:(0., 0., 0.),
    }
    #print(cwin*1./CCGs.shape[2])
    #assert cbin==cwin*1./CCGs.shape[2]

    fig, ax = plt.subplots(len(units), len(units), figsize=(16, 10), dpi=80)
    for i in range(len(units)):
        for j in range(len(units)):
            r, c = i, j
            if (i==j):
                color=colorsDic[i]#'#A785BD'#
            else:
                color=colorsDic[-1]
            x=np.linspace(-cwin*1./2, cwin*1./2, CCGs.shape[2])
            y=CCGs[i,j,:]
            ax[r, c].bar(x=x, height=y, width=cbin, color=color, edgecolor=color)
            if ylim==0:
                if normalize=='Hertz':
                    yl=max(y); ylim=int(yl)+5-(yl%5);
                elif normalize=='Pearson':
                    yl=max(y); ylim=yl+0.01-(yl%0.01);
            ax[r, c].set_ylim([0, ylim])
            if labels:
                if j==0:
                    ax[r, c].set_ylabel("Crosscorr. (Hz)", size=12)
                if i==len(units)-1:
                    ax[r, c].set_xlabel('Time (ms)', size=12)
                ax[r, c].set_xlim([-cwin*1./2, cwin*1./2])
                if type(bChs)!=list:
                    title="{}->{} ({})s".format(units[i], units[j], str(rec_section)[0:50].replace(' ',  ''))
                else:
                    title="{}@{}->{}@{} ({})s".format(units[i], bChs[i], units[j], bChs[j], str(rec_section)[0:50].replace(' ',  ''))
                ax[r, c].set_title(title, size=12)
                ax[r, c].tick_params(labelsize=20)
                if i!=j:
                    mn = np.mean(np.append(y[:int(len(y)*2./5)], y[int(len(y)*3./5):]))
                    std = np.std(np.append(y[:int(len(y)*2./5)], y[int(len(y)*3./5):]))
                    if std_lines:
                        ax[r, c].plot([x[0], x[-1]], [mn,mn], ls="--", c=[0,0,0], lw=1)
                        for st in [1,2,3]:
                            ax[r, c].plot([x[0], x[-1]], [mn+st*std,mn+st*std], ls="--", c=[0.5,0,0], lw=0.5)
                            ax[r, c].plot([x[0], x[-1]], [mn-st*std,mn-st*std], ls="--", c=[0,0,0.5], lw=0.5)
    
    
    if Title:
        fig.suptitle(Title, size=20, weight='bold')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.close() if not show else plt.show()
    if saveFig:
        saveDir=op.expanduser(saveDir)
        if not os.path.isdir(saveDir): os.mkdir(saveDir)
        if pdf: fig.savefig(saveDir+'/ccg%s-%d_%.2f.pdf'%(str(units).replace(' ', ''), cwin, cbin))
        if png: fig.savefig(saveDir+'/ccg%s_%d_%.2f.png'%(str(units).replace(' ', ''), cwin, cbin))
        
    return fig

def plot_acg(dp, unit, cbin=0.2, cwin=80, normalize='Hertz', color=0, saveDir='~/Downloads', saveFig=True, prnt=False, show=True, 
             pdf=True, png=False, rec_section='all', labels=True, title=None, ref_per=True, saveData=False, ylim=0):
    assert type(unit)==int
    saveDir=op.expanduser(saveDir)
    bChs=None
    gu = get_good_units(dp) # get good units
    # sort them by depth
    if (unit in gu) and os.path.isfile(dp+'/FeaturesTable/FeaturesTable_good.csv'):
        ft = pd.read_csv(dp+'/FeaturesTable/FeaturesTable_good.csv', sep=',', index_col=0)
        bestChs=np.array(ft["WVF-MainChannel"])
        bChs=[bestChs[np.isin(gu, unit)][0]]
    ACG=acg(dp, unit, cbin, cwin, fs=30000, normalize='Hertz', prnt=prnt, rec_section=rec_section)
    plt_acg(unit, ACG, cbin, cwin, bChs, color, 30000, saveDir, saveFig, pdf=pdf, png=png, 
            rec_section=rec_section, labels=labels, title=title, ref_per=ref_per, saveData=saveData, ylim=ylim)
    
def plot_ccg(dp, units, cbin=0.2, cwin=80, normalize='Hertz', saveDir='~/Downloads', saveFig=False, prnt=False, show=True, 
             pdf=False, png=False, rec_section='all', labels=True, std_lines=True, title=None, color=-1, CCG=None, saveData=False, ylim=0):
    assert type(units)==list
    saveDir=op.expanduser(saveDir)
    bChs=None
    gu = get_good_units(dp) # get good units
    # sort them by depth
    if np.all(np.isin(units, gu)) and os.path.isfile(dp+'/FeaturesTable/FeaturesTable_good.csv'):
        ft = pd.read_csv(dp+'/FeaturesTable/FeaturesTable_good.csv', sep=',', index_col=0)
        bestChs=np.array(ft["WVF-MainChannel"])
        bChs=[bestChs[np.isin(gu, u)][0] for u in units]

    if CCG is None:
        CCG=ccg(dp, units, cbin, cwin, fs=30000, normalize=normalize, prnt=prnt, rec_section=rec_section)
    if CCG.shape[0]==2:
        fig = plt_ccg(units, CCG[0,1,:], cbin, cwin, bChs, 30000, saveDir, saveFig, show, pdf, png, rec_section=rec_section, 
                      labels=labels, std_lines=std_lines, title=title, color=color, saveData=saveData, ylim=ylim, normalize=normalize)
    else:
        fig = plt_ccg_subplots(units, CCG, cbin, cwin, bChs, None, saveDir, saveFig, prnt, show, pdf, png, rec_section=rec_section, labels=labels, title=title, std_lines=std_lines, ylim=ylim, normalize=normalize)
        
    return fig

# Plot correlation matrix of variables x ovservations 2D arrray
    
def plot_cm(dp, units, b=5, cwin=100, cbin=1, corrEvaluator='CCG', vmax=5, vmin=0, cmap='viridis', rec_section='all', ret_cm=False, saveDir='~/Downloads', saveFig=False, pdf=1, png=0):
    '''Plot correlation matrix.
    dp: datapath
    units: units list of the same dataset
    b: bin, in milliseconds'''
    
    # Sanity checks
    allowedCorEvals = ['CCG', 'covar', 'corrcoeff', 'corrcoeff_MB']
    try:
        assert corrEvaluator in allowedCorEvals
    except:
        print('WARNING: {} should be in {}. Exiting now.'.format(corrEvaluator, allowedCorEvals))
        return
    
    # Sort units by depth
    units, channels = get_channels(dp, units)
    
    # make correlation matrix of units sorted by depth
    cm = make_cm(dp, units, b, cwin, cbin, corrEvaluator, vmax, vmin, rec_section)
    
    # Plot correlation matrix
    cm[np.eye(cm.shape[0], dtype=bool)]=0 # set diag values to 0
    plt.figure()
    hm = sns.heatmap(cm, vmin=vmin, vmax=vmax, cmap=cmap)
    hm.axes.plot(hm.axes.get_xlim(), hm.axes.get_ylim()[::-1], ls="--", c=[0.5,0.5,0.5], lw=1)
    hm.axes.set_yticklabels(['{}@{}'.format(units[i], channels[i]) for i in range(len(units))], rotation=0)
    hm.axes.set_xticklabels(['{}@{}'.format(units[i], channels[i]) for i in range(len(units))], rotation=45, horizontalalignment='right')
    hm.axes.set_title('Dataset: {}'.format(dp.split('/')[-1]))
    hm.axes.set_aspect('equal','box-forced')
    fig = plt.gcf()
    plt.tight_layout()
    print(units)
    
    if saveFig:
        saveDir=op.expanduser(saveDir)
        if not os.path.isdir(saveDir): os.mkdir(saveDir)
        if pdf: fig.savefig(saveDir+'/ccg%s-%d_%.2f.pdf'%(str(units).replace(' ', ''), cwin, cbin))
        if png: fig.savefig(saveDir+'/ccg%s_%d_%.2f.png'%(str(units).replace(' ', ''), cwin, cbin))
    
    if ret_cm:
        return cm
    else:
        return fig

#%% Connectivity inferred from correlograms
    
def plot_sfcdf(dp, cbin=0.1, cwin=10, threshold=2, n_consec_bins=3, text=True, markers=False, rec_section='all', ticks=True, again = False, saveFig=True):
    '''
    Visually represents the connectivity datafrane otuputted by 'gen_cdf'.
    Each line/row is a good unit.
    Each intersection is a square split in a varying amount of columns,
    each column representing a positive or negatively significant peak collored accordingly to its size s.
    '''
    df, hmm, gu, bestChs, hmmT = gen_sfc(dp, cbin, cwin, threshold, n_consec_bins, rec_section=rec_section, _format='peaks_infos', again=again)
    plt.figure()
    hm = sns.heatmap(hmm, yticklabels=True, xticklabels=True, cmap="RdBu_r", center=0, vmin=-5, vmax=5, cbar_kws={'label': 'Crosscorrelogram peak (s.d.)'})
    #hm = sns.heatmap(hmmT, yticklabels=False, xticklabels=False, alpha=0.0)
    
    hm.axes.plot(hm.axes.get_xlim(), hm.axes.get_ylim()[::-1], ls="--", c=[0.5,0.5,0.5], lw=1)
    hm.axes.set_yticklabels(['{}@{}'.format(gu[i], bestChs[i]) for i in range(len(gu))])
    hm.axes.set_xticklabels(np.array([['{}@{}'.format(gu[i], bestChs[i])]*12 for i in range(len(gu))]).flatten())
    for i in range(hmm.shape[1]):
        if (i-5)%12!=0: hm.axes.xaxis.get_major_ticks()[i].set_visible(False)
        else: hm.axes.xaxis.get_major_ticks()[i].set_visible(True)
    if not ticks:
        [tick.set_visible(False) for tick in hm.axes.xaxis.get_major_ticks()]
        [tick.set_visible(False) for tick in hm.axes.yaxis.get_major_ticks()]

    if markers:
        for i in range(hmm.shape[0]):
            for j in range(hmm.shape[0]):
                if i!=j:
                    pkT = hmmT[i,j*12]
                    if pkT>0:
                        hm.axes.scatter(j*12+5, i, marker='^', s=20, c="black")
                    elif pkT<0:
                        hm.axes.scatter(j*12+5, i, marker='v', s=20, c="black")
                    elif pkT==0:
                        hm.axes.scatter(j*12+5, i, marker='*', s=20, c="black")
    if text:
        for i in range(hmm.shape[0]):
            for j in range(hmm.shape[0]):
                pkT = np.unique(hmmT[i,j*12:j*12+12])
                if i!=j and (min(pkT)<=0 or max(pkT)>0):
                    hm.axes.text(x=j*12+2, y=i, s=str(pkT), size=6)
    fig = hm.get_figure()
    if saveFig: fig.savefig(dp+'/heatmap_{}_{}_{}_{}.pdf'.format(cbin, cwin, threshold, n_consec_bins))
    
    return fig

def plot_dataset_CCGs(dp, cbin=0.1, cwin=10, threshold=2, n_consec_bins=3, rec_section='all'):
    gu = get_good_units(dp) # get good units
    prct=0; sig=0;
    for i1, u1 in enumerate(gu):
        for i2, u2 in enumerate(gu):
            end = '\r' if (i1*len(gu)+i2)<(len(gu)**2-1) else ''
            if prct!=int(100*((i1*len(gu)+i2+1)*1./(len(gu)**2))):
                prct=int(100*((i1*len(gu)+i2+1)*1./(len(gu)**2)))
                #print('{}%...'.format(prct), end=end)
            if i1<i2:
                print('Assessing CCG {}x{}... {}%'.format(u1, u2, prct))
                hist=ccg(dp, [u1,u2], cbin, cwin, fs=30000, normalize='Hertz', prnt=False, rec_section=rec_section)[0,1,:]
                pks = find_significant_hist_peak(hist, cbin, threshold, n_consec_bins, ext_mn=None, ext_std=None, pkSgn='all')
                if np.array(pks).any():
                    sig+=1
                    print("{}th significant CCG...".format(sig))
                    plot_ccg(dp, [u1,u2], cbin, cwin, savedir=dp+'/significantCCGs_{}_{}_{}_{}'.format(cbin, cwin, threshold, n_consec_bins), \
                             saveFig=True, prnt=False, show=False, pdf=False, png=True, rec_section=rec_section, CCG=hist)
    return

def plot_dataset_ACGs(dp, cbin=0.5, cwin=80):
    gu = get_good_units(dp) # get good units
    prct=0
    for i1, u1 in enumerate(gu):
        prct=i1*100./len(gu)
        print('{}%...'.format(prct))
        plot_acg(dp, u1, cbin, cwin, savedir=dp+'/allACGs', saveFig=True, prnt=False, show=False, pdf=False, png=True)
    return


#%% Graphs
    
def network_plot_3D(G, angle, save=False):
    '''https://www.idtools.com.au/3d-network-graphs-python-mplot3d-toolkit'''
    # Get node positions
    pos = nx.get_node_attributes(G, 'pos')
    
    # Get number of nodes
    n = G.number_of_nodes()

    # Get the maximum number of edges adjacent to a single node
    edge_max = max([G.degree(i) for i in range(n)])

    # Define color range proportional to number of edges adjacent to a single node
    colors = [plt.cm.plasma(G.degree(i)/edge_max) for i in range(n)] 

    # 3D network plot
    with plt.style.context(('ggplot')):
        
        fig = plt.figure(figsize=(10,7))
        ax = Axes3D(fig)
        
        # Loop on the pos dictionary to extract the x,y,z coordinates of each node
        for key, value in pos.items():
            xi = value[0]
            yi = value[1]
            zi = value[2]
            
            # Scatter plot
            ax.scatter(xi, yi, zi, c=colors[key], s=20+20*G.degree(key), edgecolors='k', alpha=0.7)
        
        # Loop on the list of edges to get the x,y,z, coordinates of the connected nodes
        # Those two points are the extrema of the line to be plotted
        for i,j in enumerate(G.edges()):

            x = np.array((pos[j[0]][0], pos[j[1]][0]))
            y = np.array((pos[j[0]][1], pos[j[1]][1]))
            z = np.array((pos[j[0]][2], pos[j[1]][2]))
        
        # Plot the connecting lines
            ax.plot(x, y, z, c='black', alpha=0.5)
    
    # Set the initial view
    ax.view_init(30, angle)

    # Hide the axes
    ax.set_axis_off()

     if save is not False:
         plt.savefig("C:\scratch\\data\"+str(angle).zfill(3)+".png")
         plt.close('all')
     else:
          plt.show()
    
    return