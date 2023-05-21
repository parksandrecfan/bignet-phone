#!/usr/bin/env python
# coding: utf-8

# In[41]:


'''given data size like (2,5) and folder path like"iphone original", create svgs in the folder'''
import numpy as np
from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc, wsvg
import random


# In[55]:


def create_iphone_dataset(iphone_params, original_folder,                           draw_nodes=0, stroke_aug=1, stripe=0, extra=0):
    data_size=iphone_params["h"].shape
    h=iphone_params["h"]
    h2w_factor=iphone_params["h2w_factor"]
    w=iphone_params["w"]
    h2fillet_factor=iphone_params["h2fillet_factor"]
    fillet=iphone_params["fillet"]
    mute=iphone_params["mute"]
    mute2top=iphone_params["mute2top"]
    mute_h2power_factor=iphone_params["mute_h2power_factor"]
    power=iphone_params["power"]
    mute_h2power_h_factor=iphone_params["mute_h2power_h_factor"]
    power2top=iphone_params["power2top"]
    mute2vol=iphone_params["mute2vol"]
    vol=iphone_params["vol"]
    mute_h2vol_gap_factor=iphone_params["mute_h2vol_gap_factor"]
    vol_gap=iphone_params["vol_gap"]
    notch_r1=iphone_params["notch_r1"]
    vshift=iphone_params["vshift"]
    notch_r2=iphone_params["notch_r2"]
    notch_h=iphone_params["notch_h"]
    notch_w=iphone_params["notch_w"]
    button_t=iphone_params["button_t"]
    scr2pl=iphone_params["scr2pl"]
    scr_gap2edge_gap_factor=iphone_params["scr_gap2edge_gap_factor"]
    pl2edge=iphone_params["pl2edge"]
    stripe_w=iphone_params["stripe_w"]
    stripe2top=iphone_params["stripe2top"]
    stripe_top2low_factor=iphone_params["stripe_top2low_factor"]
    stripe2low=iphone_params["stripe2low"]
    stripe_ur=iphone_params["stripe_ur"]
    stripe_top2ll_factor=iphone_params["stripe_top2ll_factor"]
    stripe_ll=iphone_params["stripe_ll"]
    ringr=iphone_params["ringr"]
    ringd=iphone_params["ringd"]
    ringd2=iphone_params["ringd2"]
    lens1=iphone_params["lens1"]
    lens2=iphone_params["lens2"]
    lens3=iphone_params["lens3"]
    lens4=iphone_params["lens4"]
    lens1p=iphone_params["lens1p"]
    lens2p=iphone_params["lens2p"]
    lens3p=iphone_params["lens3p"]
    lens4p=iphone_params["lens4p"]
    lens2p2=0.4185
    lens3p2=0.6323
    lens_random=iphone_params["lens_random"]
    notch_random=iphone_params["notch_random"]    
    
    for i in range(data_size[0]):#2
        for j in range(data_size[1]):#5
            r0=fillet[i][j]
            w0=w[i][j]
            h0=h[i][j]
            gap0=pl2edge[i][j]
            gap1=scr2pl[i][j]
            r1=notch_r1[i][j]
            vs=vshift[i][j]
            r2=notch_r2[i][j]
            n_w=notch_w[i][j]
            mute_pos=mute2top[i][j]
            mute_size=mute[i][j]
            t=button_t[i][j]
            mute_vol=mute2vol[i][j]
            vol_size=vol[i][j]
            vgap=vol_gap[i][j]
            power_pos=power2top[i][j]
            power_size=power[i][j]
            stripe_upos=stripe2top[i][j]
            stripe_size=stripe_w[i][j]
            stripe_dpos=stripe2low[i][j]
            stripe_rpos=stripe_ur[i][j]
            stripe_lpos=stripe_ll[i][j]
            ring_r=ringr[i][j]
            ring_d=ringd[i][j]
            ring_d2=ringd2[i][j]
            lens_1=lens1[i][j]
            lens_2=lens2[i][j]
            lens_3=lens3[i][j]
            lens_4=lens4[i][j]
            lens_1p=lens1p[i][j]
            lens_2p=lens2p[i][j]
            lens_3p=lens3p[i][j]
            lens_4p=lens4p[i][j]
            lens_rand=lens_random[i][j]
            notch_rand=notch_random[i][j]

            path1=draw_contour(r0,w0,h0,0)
            path2=draw_contour(r0-gap0,w0-2*gap0,h0-2*gap0,gap0*(1+-1j))
            path3=draw_notch(r0-gap0-gap1,w0-2*(gap0+gap1),h0-2*(gap0+gap1),(gap0+gap1)*(1+-1j),r1,vs,r2,n_w)
            ulcorner=0+h0*-1j
            paths4=draw_buttons(ulcorner,mute_pos,mute_size,t,mute_vol,vol_size,vgap,w0,power_pos,power_size)
            if stripe==1:
                paths5=draw_stripes(ulcorner,stripe_upos,stripe_size,gap0,w0,stripe_dpos,h0,stripe_rpos,stripe_lpos)
            
            mid_plane=w0/2 + (h0-gap0) * -1j
            n_h=r1+vs+r2+gap1#notch_h
            paths6=draw_lens(notch_rand, lens_rand, mid_plane,                              n_w, n_h, ring_r, ring_d, ring_d2,                              lens_1, lens_2, lens_3, lens_4,
                             lens_1p, lens_2p, lens_3p, lens_4p, \
                             lens2p2, lens3p2, r2)
            if stripe==1:
                path=[path1,path2,path3]+paths4+paths5+paths6
            elif stripe==0:
                path=[path1,path2,path3]+paths4+paths6
            svg_name=original_folder+"/iphone%s-%s.svg"%(i,j)
            
            if draw_nodes==1:
                nodes=[]
                #this will plot nodes
                for a in path:
                    for b in a:
                        nodes.append(b.start)
                wsvg(path,stroke_widths=list(np.ones(len(path))*0.2),
                nodes=nodes, node_radii=list(np.ones(len(nodes))*0.5),
                viewbox=(-10,-120,90,130),dimensions=(360,900),filename=svg_name)
            # path.extend(path2)
            else:
                stroke_params=np.ones(len(path))*0.2
                if stroke_aug==1:
                    stroke_params=np.random.uniform(low=0.2, high=1.8, size=len(path))
                if extra==0:
                    wsvg(path,stroke_widths=stroke_params,viewbox=(-10,-120,90,130),dimensions=(360,900),                filename=svg_name)
                elif extra==1:
                    wsvg(path,filename=svg_name)


# In[ ]:


def create_iphone_params(data_size):
    h_min=131.5
    h_max=160.8
    w_min=64.2
    w_max=78.1
    #1.68~2.5047
    fillet_min=9.5
    fillet_max=12
    mute_min=5.19
    mute_max=5.65
    mute2top_min=21.96
    mute2top_max=33.27
    power_min=15.56
    power_max=18.05
    power2top_min=30.91
    power2top_max=53.66
    mute2vol_min=12.11
    mute2vol_max=13.3
    vol_min=9.76
    vol_max=10.91
    vol_gap_min=12.26
    vol_gap_max=14.01
    notch_r1_min=0.82
    notch_r1_max=1.14
    vshift_min=0
    vshift_max=1
    notch_r2_min=2.56
    notch_r2_max=4
    notch_h_min=7.29
    notch_h_max=9.2
    notch_w_min=26.86
    notch_w_max=36.79
    button_t_min=0.4
    button_t_max=0.59
    scr2pl_min=2.17
    scr2pl_max=4.2
    pl2edge_min=1
    pl2edge_max=1.5
    stripe_w_min=1
    stripe_w_max=1.51
    stripe2top_min=12.81
    stripe2top_max=16.51
    stripe2low_min=12.81
    stripe2low_max=16.51
    stripe_ur_min=13.13
    stripe_ur_max=16.38
    stripe_ll_min=13.13
    stripe_ll_max=16.38
    
    ringr_min, ringr_max = 0.5, 0.77
    ringd_min, ringd_max = 5.79, 8.1 #when speaker is middle
    ringd2_min, ringd2_max = 5.79, 10.34#when speaker is upper
    lens_min, lens_max = 0.9, 1.88 #min/max of holes1234r
    lens1p_min, lens1p_max = 0.101838, 0.14264432
    lens2p_min1, lens2p_max1= 0.265, 0.29 #when speaker at middle
#     lens2p2=0.4185 #when speaker is upper, take avg of the 2 cases, used in line 60

    lens3p_min1, lens3p_max1= 0.7, 0.733 #when speaker at middle
#     lens3p2=0.6323 #when speaker is upper, take avg of the 2 cases, used in line 61
    lens4p_min, lens4p_max = 0.85443, 0.88854
    
    #strong correlation
    h2w=0.98423
    h2fillet=0.642522
    h2stripe_ur=0.996595
    mute_h2power=0.687735
    mute_h2power_h=0.868564
    mute_h2vol_gap=0.678879
    scr_gap2edge_gap=0.610561
    stripe_top2low=0.991767
    stripe_top2ll=0.956417
    
    #create a batch
    
    h=np.random.uniform(h_min,h_max,data_size)

    h2w_factor=(h-h_min)/(h_max-h_min)*(w_max-w_min)+w_min

    w=np.random.uniform(w_min,w_max,data_size) * (1-h2w) + h2w_factor*h2w

    h2fillet_factor=(h-h_min)/(h_max-h_min)*(fillet_max-fillet_min)+fillet_min

    fillet=np.random.uniform(fillet_min,fillet_max,data_size)*(1-h2fillet) + h2fillet_factor*h2fillet
    mute=np.random.uniform(mute_min,mute_max,data_size)
    mute2top=np.random.uniform(mute2top_min,mute2top_max,data_size)

    mute_h2power_factor=(mute2top-mute2top_min)/(mute2top_max-mute2top_min)*(power_max-power_min)+power_min

    power=np.random.uniform(power_min,power_max,data_size)*(1-mute_h2power) + mute_h2power_factor*mute_h2power

    mute_h2power_h_factor=(mute2top-mute2top_min)/(mute2top_max-mute2top_min)*(power2top_max-power2top_min)+power2top_min

    power2top=np.random.uniform(power2top_min,power2top_max,data_size)*(1-mute_h2power_h)+mute_h2power_h_factor*mute_h2power_h
    mute2vol=np.random.uniform(mute2vol_min,mute2vol_max,data_size)
    vol=np.random.uniform(vol_min,vol_max,data_size)

    mute_h2vol_gap_factor=(mute-mute_min)/(mute_max-mute_min)*(vol_gap_max-vol_gap_min)+vol_gap_min

    vol_gap=np.random.uniform(vol_gap_min,vol_gap_max,data_size)*(1-mute_h2vol_gap)+mute_h2vol_gap_factor*mute_h2vol_gap
    notch_r1=np.random.uniform(notch_r1_min,notch_r1_max,data_size)
    vshift=np.random.uniform(vshift_min,vshift_max,data_size)
    notch_r2=np.random.uniform(notch_r2_min,notch_r2_max,data_size)
    notch_h=np.random.uniform(notch_h_min,notch_h_max,data_size)
    notch_w=np.random.uniform(notch_w_min,notch_w_max,data_size)
    button_t=np.random.uniform(button_t_min,button_t_max,data_size)
    scr2pl=np.random.uniform(scr2pl_min,scr2pl_max,data_size)

    scr_gap2edge_gap_factor=(scr2pl-scr2pl_min)/(scr2pl_max-scr2pl_min)*(pl2edge_max-pl2edge_min)+pl2edge_min

    pl2edge=np.random.uniform(pl2edge_min,pl2edge_max,data_size)*(1-scr_gap2edge_gap)+scr_gap2edge_gap_factor*scr_gap2edge_gap
    stripe_w=np.random.uniform(stripe_w_min,stripe_w_max,data_size)
    stripe2top=np.random.uniform(stripe2top_min,stripe2top_max,data_size)

    stripe_top2low_factor=(stripe2top-stripe2top_min)/(stripe2top_max-stripe2top_min)*(stripe2low_max-stripe2low_min)+stripe2low_min

    stripe2low=np.random.uniform(stripe2low_min,stripe2low_max,data_size)*(1-stripe_top2low)+stripe_top2low_factor*stripe_top2low
    stripe_ur=np.random.uniform(stripe_ur_min,stripe_ur_max,data_size)

    stripe_top2ll_factor=(stripe2top-stripe2top_min)/(stripe2top_max-stripe2top_min)*(stripe_ll_max-stripe_ll_min)+stripe_ll_min

    stripe_ll=np.random.uniform(stripe_ll_min,stripe_ll_max,data_size)*(1-stripe_top2ll)+stripe_top2ll_factor*stripe_top2ll
    
    ringr=np.random.uniform(ringr_min,ringr_max,data_size)
    ringd=np.random.uniform(ringd_min,ringd_max,data_size)
    ringd2=np.random.uniform(ringd2_min,ringd2_max,data_size)
    lens1=np.random.uniform(lens_min,lens_max,data_size)
    lens2=np.random.uniform(lens_min,lens_max,data_size)
    lens3=np.random.uniform(lens_min,lens_max,data_size)
    lens4=np.random.uniform(lens_min,lens_max,data_size)
    lens1p=np.random.uniform(lens1p_min, lens1p_max, data_size)
    lens2p=np.random.uniform(lens2p_min1,lens2p_max1,data_size)
    lens3p=np.random.uniform(lens3p_min1,lens3p_max1,data_size)
    lens4p=np.random.uniform(lens4p_min, lens4p_max, data_size)
    lens_random=np.random.randint(0,2,(data_size[0],data_size[1],4))
    notch_random=np.random.randint(0,2,data_size)
    
    iphone_params={}
    iphone_params["h"]=h
    iphone_params["h2w_factor"]=h2w_factor
    iphone_params["w"]=w
    iphone_params["h2fillet_factor"]=h2fillet_factor
    iphone_params["fillet"]=fillet
    iphone_params["mute"]=mute
    iphone_params["mute2top"]=mute2top
    iphone_params["mute_h2power_factor"]=mute_h2power_factor
    iphone_params["power"]=power
    iphone_params["mute_h2power_h_factor"]=mute_h2power_h_factor
    iphone_params["power2top"]=power2top
    iphone_params["mute2vol"]=mute2vol
    iphone_params["vol"]=vol
    iphone_params["mute_h2vol_gap_factor"]=mute_h2vol_gap_factor
    iphone_params["vol_gap"]=vol_gap
    iphone_params["notch_r1"]=notch_r1
    iphone_params["vshift"]=vshift
    iphone_params["notch_r2"]=notch_r2
    iphone_params["notch_h"]=notch_h
    iphone_params["notch_w"]=notch_w
    iphone_params["button_t"]=button_t
    iphone_params["scr2pl"]=scr2pl
    iphone_params["scr_gap2edge_gap_factor"]=scr_gap2edge_gap_factor
    iphone_params["pl2edge"]=pl2edge
    iphone_params["stripe_w"]=stripe_w
    iphone_params["stripe2top"]=stripe2top
    iphone_params["stripe_top2low_factor"]=stripe_top2low_factor
    iphone_params["stripe2low"]=stripe2low
    iphone_params["stripe_ur"]=stripe_ur
    iphone_params["stripe_top2ll_factor"]=stripe_top2ll_factor
    iphone_params["stripe_ll"]=stripe_ll
    iphone_params["ringr"]=ringr
    iphone_params["ringd"]=ringd
    iphone_params["ringd2"]=ringd2
    iphone_params["lens1"]=lens1
    iphone_params["lens2"]=lens2
    iphone_params["lens3"]=lens3
    iphone_params["lens4"]=lens4
    iphone_params["lens1p"]=lens1p
    iphone_params["lens2p"]=lens2p
    iphone_params["lens3p"]=lens3p
    iphone_params["lens4p"]=lens4p
    iphone_params["lens_random"]=lens_random
    iphone_params["notch_random"]=notch_random
    return iphone_params


# In[44]:


def draw_lens(notch_rand, lens_rand, mid_plane, n_w, n_h, ring_r, ring_d, ring_d2, lens_1, lens_2, lens_3, lens_4,
                             lens_1p, lens_2p, lens_3p, lens_4p, lens2p2, lens3p2, r2):
    return_paths=[]
    l1=lens_1
    l2=lens_2
    l3=lens_3
    l4=lens_4
    left_most=mid_plane-n_w/2-n_h/2*-1j
    
    lp1=left_most + lens_1p * n_w
    lp4=left_most + lens_4p * n_w
    
    if notch_rand==1:#upper speaker
        p=mid_plane+ring_d2/2-ring_r*-1j
        path_ring=draw_ring(p, ring_d2, ring_r)
        lp2=left_most + lens2p2 * n_w
        lp3=left_most + lens3p2 * n_w

    else:
        p=mid_plane+ring_d/2-(n_h/2)*-1j
        path_ring=draw_ring(p, ring_d, ring_r)
        lp2=left_most + lens_2p * n_w
        lp3=left_most + lens_3p * n_w
    
    return_paths.append(path_ring)
    
    if lens_rand[0]==1:
        new_path=draw_circle(lp2,l2)
        return_paths.append(new_path)
    if lens_rand[1]==1:
        new_path=draw_circle(lp3,l3)
        return_paths.append(new_path)
    if lens_rand[2]==1:
        new_path=draw_circle(lp4,l4)
        return_paths.append(new_path)
    if lens_rand[3]==1:#if there is nothing here yet, draw the leftmost
        new_path=draw_circle(lp1,l1)
        return_paths.append(new_path)
        
    return return_paths


# In[45]:


def draw_circle(p,r):
    pL=p-r
    pR=p+r
    seg1=Arc(pL,r*(-1+-1j),rotation=0,large_arc=0,sweep=0,end=pR)
    seg2=Arc(pL,r*(-1+-1j),rotation=0,large_arc=0,sweep=1,end=pR)
    return Path(seg1,seg2)


# In[46]:


def draw_ring(p,d,ring): #p is the right
    p_ur=p+ring*-1j
    p_lr=p-ring*-1j
    seg1=Arc(p_ur,ring*(-1+-1j),rotation=0,large_arc=0,sweep=1,end=p_lr)
    p_ll=p_lr-d
    seg2=Line(p_lr,p_ll)
    p_ul=p_ur-d
    seg3=Arc(p_ll,ring*(-1+-1j),rotation=0,large_arc=0,sweep=1,end=p_ul)
    seg4=Line(p_ul,p_ur)
    return Path(seg1, seg2, seg3, seg4)


# In[47]:


def draw_contour(r,w,h,start):
    r0=r
    p1=start+0+r0*-1j
    p2=p1+(h-2*r0)*-1j
    seg1=Line(p1,p2)
    p3=p2+r0*(1+-1j)
    seg2=Arc(p2,r0+r0*-1j,rotation=0,large_arc=0,sweep=1,end=p3)
    p4=p3+w-2*r0
    seg3=Line(p3,p4)
    p5=p4+r0*(1--1j)
    seg4=Arc(p4,r0+r0*-1j,rotation=0,large_arc=0,sweep=1,end=p5)
    p6=p5-(h-2*r0)*-1j
    seg5=Line(p5,p6)
    p7=p6+r0*(-1--1j)
    seg6=Arc(p6,r0+r0*-1j,rotation=0,large_arc=0,sweep=1,end=p7)
    p8=p7-(w-2*r0)
    seg7=Line(p7,p8)
    p9=p1
    seg8=Arc(p8,r0+r0*-1j,rotation=0,large_arc=0,sweep=1,end=p9)
    path_out=Path(seg1,seg2,seg3,seg4,seg5,seg6,seg7,seg8)
#     path_out=[Path(seg1),Path(seg2),Path(seg3),Path(seg4),Path(seg5),Path(seg6),Path(seg7),Path(seg8)]
    return path_out


# In[48]:


def draw_notch(r,w,h,start,r1,vshift,r2,notch_w):
    r0=r
    p1=start+0+r0*-1j
    p2=p1+(h-2*r0)*-1j
    seg1=Line(p1,p2)
    p3=p2+r0*(1+-1j)
    seg2=Arc(p2,r0+r0*-1j,rotation=0,large_arc=0,sweep=1,end=p3)
    p4=p3+(w-2*r0-notch_w-2*r1)/2
    seg3=Line(p3,p4)
    p5=p4+r1*(1--1j)
    seg4=Arc(p4,r1*(1+-1j),rotation=0,large_arc=0,sweep=1,end=p5)
    p6=p5-vshift*-1j
    seg5=Line(p5,p6)
    p7=p6+r2*(1--1j)
    seg6=Arc(p6,r2*(-1+-1j),rotation=0,large_arc=0,sweep=0,end=p7)
    p8=p7+notch_w-2*r2
    seg7=Line(p7,p8)
    p9=p8+r2*(1+-1j)
    seg8=Arc(p8,r2*(-1+-1j),rotation=0,large_arc=0,sweep=0,end=p9)
    p10=p9+vshift*-1j
    seg9=Line(p9,p10)
    p11=p10+r1*(1+-1j)
    seg10=Arc(p10,r1*(-1+-1j),rotation=0,large_arc=0,sweep=1,end=p11)
    p12=p11+(w-2*r0-notch_w-2*r1)/2
    seg11=Line(p11,p12)
    p13=p12+r0*(1--1j)
    seg12=Arc(p12,r0*(-1+-1j),rotation=0,large_arc=0,sweep=1,end=p13)
    p14=p13-(h-2*r0)*-1j
    seg13=Line(p13,p14)
    p15=p14+r0*(-1--1j)
    seg14=Arc(p14,r0+r0*-1j,rotation=0,large_arc=0,sweep=1,end=p15)
    p16=p15-(w-2*r0)
    seg15=Line(p15,p16)
    p17=p1
    seg16=Arc(p16,r0+r0*-1j,rotation=0,large_arc=0,sweep=1,end=p17)    
    if vshift!=0:
        path_out=Path(seg1,seg2,seg3,seg4,seg5,seg6,seg7,seg8,seg9,seg10,seg11,seg12,seg13,seg14,seg15,seg16)
    return path_out


# In[49]:


def draw_rect(width,height,start):
    p1=start#upper right corner is where i start
    p2=p1-height*-1j
    p3=p2-width
    p4=p3+height*-1j
    seg1=Line(p1,p2)
    seg2=Line(p2,p3)
    seg3=Line(p3,p4)
    seg4=Line(p4,p1)
    path_out=Path(seg1,seg2,seg3,seg4,stroke_widths=1)
    return path_out


# In[50]:


def draw_buttons(ulcorner,mute2top,mute,button_t,mute2vol,vol,vol_gap,w,power2top,power):
    anchor1=ulcorner-(mute2top-mute/2)*-1j
    path1=draw_rect(button_t,mute,anchor1)
    anchor2=anchor1-(mute/2+mute2vol-vol/2)*-1j
    path2=draw_rect(button_t,vol,anchor2)
    anchor3=anchor2-(vol/2+vol_gap)*-1j
    path3=draw_rect(button_t,vol,anchor3)
    anchor4=ulcorner+w+button_t-(power2top-power/2)*-1j
    path4=draw_rect(button_t,power,anchor4)
    paths_out=[path1,path2,path3,path4]
    return paths_out


# In[51]:


def draw_stripes(ulcorner,stripe2top,stripe_w,pl2edge,w,stripe2low,h,stripe_ur,stripe_ll):
    anchor1=ulcorner-(stripe2top-stripe_w/2)*-1j+pl2edge
    path1=draw_rect(pl2edge,stripe_w,anchor1)
    anchor2=anchor1+w-pl2edge
    path2=draw_rect(pl2edge,stripe_w,anchor2)
    
    anchor3=ulcorner-(h-stripe2low-stripe_w/2)*-1j+pl2edge
    path3=draw_rect(pl2edge,stripe_w,anchor3)
    anchor4=anchor3+w-pl2edge
    path4=draw_rect(pl2edge,stripe_w,anchor4)
    paths_out=[path1,path2,path3,path4]
    if random.randint(0,1)==1:#add 2 strips
        anchor5=ulcorner+w-stripe_ur+stripe_w/2
        path5=draw_rect(stripe_w,pl2edge,anchor5)
        anchor6=ulcorner-h*-1j+stripe_ll+stripe_w/2+pl2edge*-1j
        path6=draw_rect(stripe_w,pl2edge,anchor6)
        paths_out=[path1,path2,path3,path4,path5,path6]
    return paths_out


# In[52]:


def draw_circle(p,r):
    pL=p-r
    pR=p+r
    seg1=Arc(pL,r*(-1+-1j),rotation=0,large_arc=0,sweep=0,end=pR)
    seg2=Arc(pL,r*(-1+-1j),rotation=0,large_arc=0,sweep=1,end=pR)
    return Path(seg1,seg2)


# In[56]:


# data_size=(1,5)
# original_folder="iphone original"

# rec = create_iphone_dataset_rec(data_size, original_folder, stroke_aug=0)

