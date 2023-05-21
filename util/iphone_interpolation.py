#!/usr/bin/env python
# coding: utf-8

# In[1]:


def ratio_value(ratio, minimum, maximum):
    return ratio * maximum + (1-ratio) * minimum


# In[2]:


import util as u
import os
par_dir = "iphone_par.pkl"
if os.path.isfile(par_dir):
    iphone_par=u.load_item(par_dir)
    a,b="min","max"
    h_min,h_max=iphone_par["h_par"][a],iphone_par["h_par"][b]
    w_min,w_max=iphone_par["w_par"][a],iphone_par["w_par"][b]
    fillet_min,fillet_max=iphone_par["fillet_par"][a],iphone_par["fillet_par"][b]
    mute_min,mute_max=iphone_par["mute_par"][a],iphone_par["mute_par"][b]
    mute2top_min,mute2top_max=iphone_par["mute2top_par"][a],iphone_par["mute2top_par"][b]
    power_min,power_max=iphone_par["power_par"][a],iphone_par["power_par"][b]
    power2top_min,power2top_max=iphone_par["power2top_par"][a],iphone_par["power2top_par"][b]
    mute2vol_min,mute2vol_max=iphone_par["mute2vol_par"][a],iphone_par["mute2vol_par"][b]
    vol_min,vol_max=iphone_par["vol_par"][a],iphone_par["vol_par"][b]
    vol_gap_min,vol_gap_max=iphone_par["vol_gap_par"][a],iphone_par["vol_gap_par"][b]
    notch_r1_min,notch_r1_max=iphone_par["notch_r1_par"][a],iphone_par["notch_r1_par"][b]
    vshift_min,vshift_max=iphone_par["vshift_par"][a],iphone_par["vshift_par"][b]
    notch_r2_min,notch_r2_max=iphone_par["notch_r2_par"][a],iphone_par["notch_r2_par"][b]
    notch_h_min,notch_h_max=iphone_par["notch_h_par"][a],iphone_par["notch_h_par"][b]
    notch_w_min,notch_w_max=iphone_par["notch_w_par"][a],iphone_par["notch_w_par"][b]
    button_t_min,button_t_max=iphone_par["button_t_par"][a],iphone_par["button_t_par"][b]
    scr2pl_min,scr2pl_max=iphone_par["scr2pl_par"][a],iphone_par["scr2pl_par"][b]
    pl2edge_min,pl2edge_max=iphone_par["pl2edge_par"][a],iphone_par["pl2edge_par"][b]
    stripe_w_min,stripe_w_max=iphone_par["stripe_w_par"][a],iphone_par["stripe_w_par"][b]
    stripe2top_min,stripe2top_max=iphone_par["stripe2top_par"][a],iphone_par["stripe2top_par"][b]
    stripe2low_min,stripe2low_max=iphone_par["stripe2low_par"][a],iphone_par["stripe2low_par"][b]
    stripe_ur_min,stripe_ur_max=iphone_par["stripe_ur_par"][a],iphone_par["stripe_ur_par"][b]
    stripe_ll_min,stripe_ll_max=iphone_par["stripe_ll_par"][a],iphone_par["stripe_ll_par"][b]
    ringr_min,ringr_max=iphone_par["ringr_par"][a],iphone_par["ringr_par"][b]
    ringd_min,ringd_max=iphone_par["ringd_par"][a],iphone_par["ringd_par"][b]
    ringd2_min,ringd2_max=iphone_par["ringd2_par"][a],iphone_par["ringd2_par"][b]
    lens_min,lens_max=iphone_par["lens_par"][a],iphone_par["lens_par"][b]
    lens1p_min,lens1p_max=iphone_par["lens1p_par"][a],iphone_par["lens1p_par"][b]
    lens2p_min1,lens2p_max1=iphone_par["lens2p_par"][a],iphone_par["lens2p_par"][b]
    lens3p_min1,lens3p_max1=iphone_par["lens3p_par"][a],iphone_par["lens3p_par"][b]
    lens4p_min,lens4p_max=iphone_par["lens4p_par"][a],iphone_par["lens4p_par"][b]

    lens2p2=iphone_par["lens2p2"]
    lens3p2=iphone_par["lens3p2"]

    h2w=iphone_par["h2w"]
    h2fillet=iphone_par["h2fillet"]
    h2stripe_ur=iphone_par["h2stripe_ur"]
    mute_h2power=iphone_par["mute_h2power"]
    mute_h2power_h=iphone_par["mute_h2power_h"]
    mute_h2vol_gap=iphone_par["mute_h2vol_gap"]
    scr_gap2edge_gap=iphone_par["scr_gap2edge_gap"]
    stripe_top2low=iphone_par["stripe_top2low"]
    stripe_top2ll=iphone_par["stripe_top2ll"]


# In[14]:


#create average iphone
import numpy as np
# ratio=0.5 #the most average
def iphone_interpolation(ratio, notch_random=0, lens_random=None):
    # ratio=0.5 #the most average

    data_size=(1,1) #I only want the average

    h=ratio_value(ratio,h_min,h_max)
    h2w_factor=None
    w=ratio_value(ratio,w_min, w_max)
    h2fillet_factor=None
    fillet=ratio_value(ratio,fillet_min, fillet_max)
    mute=ratio_value(ratio,mute_min, mute_max)
    mute2top=ratio_value(ratio,mute2top_min, mute2top_max)
    mute_h2power_factor=None
    power=ratio_value(ratio,power_min, power_max)
    mute_h2power_h_factor=None
    power2top=ratio_value(ratio,power2top_min, power2top_max)
    mute2vol=ratio_value(ratio,mute2vol_min, mute2vol_max)
    vol=ratio_value(ratio,vol_min, vol_max)
    mute_h2vol_gap_factor=None
    vol_gap=ratio_value(ratio,vol_gap_min, vol_gap_max)
    notch_r1=ratio_value(ratio,notch_r1_min, notch_r1_max)
    vshift=ratio_value(ratio,vshift_min, vshift_max)
    notch_r2=ratio_value(ratio,notch_r2_min, notch_r2_max)
    notch_h=ratio_value(ratio,notch_h_min, notch_h_max)
    notch_w=ratio_value(ratio,notch_w_min, notch_w_max)
    button_t=ratio_value(ratio,button_t_min, button_t_max)
    scr2pl=ratio_value(ratio,scr2pl_min, scr2pl_max)
    scr_gap2edge_gap_factor=None
    pl2edge=ratio_value(ratio,pl2edge_min, pl2edge_max)
    stripe_w=ratio_value(ratio,stripe_w_min, stripe_w_max)
    stripe2top=ratio_value(ratio,stripe2top_min, stripe2top_max)
    stripe_top2low_factor=None
    stripe2low=ratio_value(ratio,stripe2low_min, stripe2low_max)
    stripe_ur=ratio_value(ratio,stripe_ur_min, stripe_ur_max)
    stripe_top2ll_factor=None
    stripe_ll=ratio_value(ratio,stripe_ll_min, stripe_ll_max)
    ringr=ratio_value(ratio,ringr_min, ringr_max)
    ringd=ratio_value(ratio,ringd_min, ringd_max)
    ringd2=ratio_value(ratio,ringd2_min, ringd2_max)
    lens1=ratio_value(ratio,lens_min, lens_max)
    lens2=ratio_value(ratio,lens_min, lens_max)
    lens3=ratio_value(ratio,lens_min, lens_max)
    lens4=ratio_value(ratio,lens_min, lens_max)
    lens1p=ratio_value(ratio,lens1p_min, lens1p_max)
    lens2p=ratio_value(ratio,lens2p_min1, lens2p_max1)
    lens3p=ratio_value(ratio,lens3p_min1, lens3p_max1)
    lens4p=ratio_value(ratio,lens4p_min, lens4p_max)
    
#     lens_random_init=np.ones((data_size[0], data_size[1], 4)) #all cameras present
    lens_random=lens_random
    notch_random=notch_random #lower speaker, use lens2p, lens3p instead of lens2p2, lens3p2

    #overwrite one variable, to a larger/smaller one
#     extra_ratio

    source_rec={}
    source_rec["h"]=h
    source_rec["h2w_factor"]=h2w_factor
    source_rec["w"]=w
    source_rec["h2fillet_factor"]=h2fillet_factor
    source_rec["fillet"]=fillet
    source_rec["mute"]=mute
    source_rec["mute2top"]=mute2top
    source_rec["mute_h2power_factor"]=mute_h2power_factor
    source_rec["power"]=power
    source_rec["mute_h2power_h_factor"]=mute_h2power_h_factor
    source_rec["power2top"]=power2top
    source_rec["mute2vol"]=mute2vol
    source_rec["vol"]=vol
    source_rec["mute_h2vol_gap_factor"]=mute_h2vol_gap_factor
    source_rec["vol_gap"]=vol_gap
    source_rec["notch_r1"]=notch_r1
    source_rec["vshift"]=vshift
    source_rec["notch_r2"]=notch_r2
    source_rec["notch_h"]=notch_h
    source_rec["notch_w"]=notch_w
    source_rec["button_t"]=button_t
    source_rec["scr2pl"]=scr2pl
    source_rec["scr_gap2edge_gap_factor"]=scr_gap2edge_gap_factor
    source_rec["pl2edge"]=pl2edge
    source_rec["stripe_w"]=stripe_w
    source_rec["stripe2top"]=stripe2top
    source_rec["stripe_top2low_factor"]=stripe_top2low_factor
    source_rec["stripe2low"]=stripe2low
    source_rec["stripe_ur"]=stripe_ur
    source_rec["stripe_top2ll_factor"]=stripe_top2ll_factor
    source_rec["stripe_ll"]=stripe_ll
    source_rec["ringr"]=ringr
    source_rec["ringd"]=ringd
    source_rec["ringd2"]=ringd2
    source_rec["lens1"]=lens1
    source_rec["lens2"]=lens2
    source_rec["lens3"]=lens3
    source_rec["lens4"]=lens4
    source_rec["lens1p"]=lens1p
    source_rec["lens2p"]=lens2p
    source_rec["lens3p"]=lens3p
    source_rec["lens4p"]=lens4p
    source_rec["lens_random"]=lens_random
    source_rec["notch_random"]=notch_random

    for idx,i in enumerate(source_rec):
    #     print(i)
        if type(source_rec[i]).__name__!='ndarray': #not lens_random
            source_rec[i]=np.array(source_rec[i]).reshape(data_size)
    return source_rec

# source_rec=iphone_interpolation(0.5, notch_random=1,\
#                                 lens_random=np.array([[[0,0,0,1]]]))


# In[16]:


# source_rec

