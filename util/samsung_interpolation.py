#!/usr/bin/env python
# coding: utf-8

# In[1]:


def ratio_value(ratio, minimum, maximum):
    return ratio * maximum + (1-ratio) * minimum


# In[2]:

import util as u
import os
par_dir = "samsung_par.pkl"
if os.path.isfile(par_dir):
    samsung_par=u.load_item(par_dir)
    a,b="min","max"
    h_min, h_max=samsung_par["h_par"][a],samsung_par["h_par"][b]
    w_min, w_max=samsung_par["w_par"][a],samsung_par["w_par"][b]
    rl_min, rl_max=samsung_par["rl_par"][a],samsung_par["rl_par"][b]
    rm_min, rm_max=samsung_par["rm_par"][a],samsung_par["rm_par"][b]
    m_ushift_min, m_ushift_max=samsung_par["m_ushift_par"][a],samsung_par["m_ushift_par"][b]
    m_lshift_min, m_lshift_max=samsung_par["m_lshift_par"][a],samsung_par["m_lshift_par"][b]
    rs_min, rs_max=samsung_par["rs_par"][a],samsung_par["rs_par"][b]
    sux_min, sux_max=samsung_par["sux_par"][a],samsung_par["sux_par"][b]
    suh_min, suh_max=samsung_par["suh_par"][a],samsung_par["suh_par"][b]
    slh_min, slh_max=samsung_par["slh_par"][a],samsung_par["slh_par"][b]
    camera_r_h_min, camera_r_h_max=samsung_par["camera_r_h_par"][a],samsung_par["camera_r_h_par"][b]
    camera2r_min, camera2r_max=samsung_par["camera2r_par"][a],samsung_par["camera2r_par"][b]
    camera_d_min, camera_d_max=samsung_par["camera_d_par"][a],samsung_par["camera_d_par"][b]
    camera_r1_min, camera_r1_max=samsung_par["camera_r1_par"][a],samsung_par["camera_r1_par"][b]
    camera_r2_min, camera_r2_max=samsung_par["camera_r2_par"][a],samsung_par["camera_r2_par"][b]
    ring_min, ring_max=samsung_par["ring_par"][a],samsung_par["ring_par"][b]
    camera_m_h_min, camera_m_h_max=samsung_par["camera_m_h_par"][a],samsung_par["camera_m_h_par"][b]
    camera_m_r_min, camera_m_r_max=samsung_par["camera_m_r_par"][a],samsung_par["camera_m_r_par"][b]
    trap_u_min, trap_u_max=samsung_par["trap_u_par"][a],samsung_par["trap_u_par"][b]
    trap_l_min, trap_l_max=samsung_par["trap_l_par"][a],samsung_par["trap_l_par"][b]
    trap_h_ratio_min, trap_h_ratio_max=samsung_par["trap_h_ratio_par"][a],samsung_par["trap_h_ratio_par"][b]
    vol_l_min, vol_l_max=samsung_par["vol_l_par"][a],samsung_par["vol_l_par"][b]
    vol_h_min, vol_h_max=samsung_par["vol_h_par"][a],samsung_par["vol_h_par"][b]
    bixby_l_min, bixby_l_max=samsung_par["bixby_l_par"][a],samsung_par["bixby_l_par"][b]
    bixby_h_min, bixby_h_max=samsung_par["bixby_h_par"][a],samsung_par["bixby_h_par"][b]
    power_free_h_min, power_free_h_max=samsung_par["power_free_h_par"][a],samsung_par["power_free_h_par"][b]
    power_unfree_h_min, power_unfree_h_max=samsung_par["power_unfree_h_par"][a],samsung_par["power_unfree_h_par"][b]
    power_l_min, power_l_max=samsung_par["power_l_par"][a],samsung_par["power_l_par"][b]
    button_h=samsung_par["button_h_par"]

import numpy as np
# ratio=0.5 #the most average
def samsung_interpolation(ratio,ct=0):

    # ratio=0.5 #the most average

    data_size=(1,1) #I only want the average

    h=ratio_value(ratio,h_min,h_max)
    w=ratio_value(ratio,w_min, w_max)
    rl=ratio_value(ratio,rl_min, rl_max)
    rm=ratio_value(ratio,rm_min, rm_max)
    rs=ratio_value(ratio,rs_min, rs_max)
    m_ushift=ratio_value(ratio, m_ushift_min, m_ushift_max)
    m_lshift=ratio_value(ratio, m_lshift_min, m_lshift_max)
    sux=ratio_value(ratio, sux_min, sux_max)
    suh=ratio_value(ratio, suh_min, suh_max)
    slh=ratio_value(ratio, slh_min, slh_max)
    camera_r_h=ratio_value(ratio, camera_r_h_min, camera_r_h_max)
    camera_ct=ct#now only consider middle
    camera_d=ratio_value(ratio, camera_d_min, camera_d_max)
    camera_r1=ratio_value(ratio, camera_r1_min, camera_r1_max)
    camera_r2=ratio_value(ratio, camera_r2_min, camera_r2_max)
    camera2r=ratio_value(ratio, camera2r_min, camera2r_max)
    ring_r=ratio_value(ratio, ring_min, ring_max)
    camera_m_h=ratio_value(ratio, camera_m_h_min, camera_m_h_max)
    camera_m_r=ratio_value(ratio, camera_m_r_min, camera_m_r_max)
    trap_u=ratio_value(ratio, trap_u_min, trap_u_max)
    trap_l=ratio_value(ratio, trap_l_min, trap_l_max)
    trap_h_ratio=ratio_value(ratio, trap_h_ratio_min, trap_h_ratio_max)
    button_h=0.75
    vol_l=ratio_value(ratio, vol_l_min, vol_l_max)
    vol_h=ratio_value(ratio, vol_h_min, vol_h_max)
    bixby_l=ratio_value(ratio, bixby_l_min, bixby_l_max)
    bixby_h=ratio_value(ratio, bixby_h_min, bixby_h_max)
    power_l=ratio_value(ratio, power_l_min, power_l_max)
    power_free_h=ratio_value(ratio, power_free_h_min, power_free_h_max)
    power_unfree_h=ratio_value(ratio, power_unfree_h_min, power_unfree_h_max)

    #overwrite one variable, to a larger/smaller one
#     extra_ratio

    source_rec={}
    source_rec["h"]=h
    source_rec["w"]=w
    source_rec["rl"]=rl
    source_rec["rm"]=rm
    source_rec["rs"]=rs
    source_rec["m_ushift"]=m_ushift
    source_rec["m_lshift"]=m_lshift
    source_rec["sux"]=sux
    source_rec["suh"]=suh
    source_rec["slh"]=slh
    source_rec["camera_r_h"]=camera_r_h
    source_rec["camera_ct"]=camera_ct
    source_rec["camera_d"]=camera_d
    source_rec["camera_r1"]=camera_r1
    source_rec["camera_r2"]=camera_r2
    source_rec["camera2r"]=camera2r
    source_rec["ring_r"]=ring_r
    source_rec["camera_m_h"]=camera_m_h
    source_rec["camera_m_r"]=camera_m_r
    source_rec["trap_u"]=trap_u
    source_rec["trap_l"]=trap_l
    source_rec["trap_h_ratio"]=trap_h_ratio
    source_rec["button_h"]=button_h
    source_rec["vol_l"]=vol_l
    source_rec["vol_h"]=vol_h
    source_rec["bixby_l"]=bixby_l
    source_rec["bixby_h"]=bixby_h
    source_rec["power_l"]=power_l
    source_rec["power_free_h"]=power_free_h
    source_rec["power_unfree_h"]=power_unfree_h
    

    for idx,i in enumerate(source_rec):
    #     print(i)
        if type(i).__name__!='ndarray' and i!="button_h": #not button_h
            source_rec[i]=np.array(source_rec[i]).reshape(data_size)
    return source_rec

# source_rec=samsung_interpolation(0.5,ct=1)