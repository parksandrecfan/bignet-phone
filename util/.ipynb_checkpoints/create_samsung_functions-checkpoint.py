#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''given data size like (2,5) and folder path like"samsung original", create svgs in the folder'''
import numpy as np
from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc, wsvg
def create_samsung_dataset(samsung_params, original_folder,                            draw_nodes=0, stroke_aug=0, stripe=0, extra=0):

    data_size=samsung_params["h"].shape
    h=samsung_params["h"]
    w=samsung_params["w"]
    rl=samsung_params["rl"]
    rm=samsung_params["rm"]
    rs=samsung_params["rs"]
    m_ushift=samsung_params["m_ushift"]
    m_lshift=samsung_params["m_lshift"]
    sux=samsung_params["sux"]
    suh=samsung_params["suh"]
    slh=samsung_params["slh"]
    camera_r_h=samsung_params["camera_r_h"]
    camera_ct=samsung_params["camera_ct"]
    camera_d=samsung_params["camera_d"]
    camera_r1=samsung_params["camera_r1"]
    camera_r2=samsung_params["camera_r2"]
    camera2r=samsung_params["camera2r"]
    ring_r=samsung_params["ring_r"]
    camera_m_h=samsung_params["camera_m_h"]
    camera_m_r=samsung_params["camera_m_r"]
    trap_u=samsung_params["trap_u"]
    trap_l=samsung_params["trap_l"]
    trap_h_ratio=samsung_params["trap_h_ratio"]
    button_h=samsung_params["button_h"]
    vol_l=samsung_params["vol_l"]
    vol_h=samsung_params["vol_h"]
    bixby_l=samsung_params["bixby_l"]
    bixby_h=samsung_params["bixby_h"]
    power_l=samsung_params["power_l"]
    power_free_h=samsung_params["power_free_h"]
    power_unfree_h=samsung_params["power_unfree_h"]

    #create svgs in folder
    for i in range(data_size[0]):#2
        for j in range(data_size[1]):#5
            r0=rl[i][j]
            w0=w[i][j]
            h0=h[i][j]
            r1=rm[i][j]
            if r1>r0:
                r1=r0
            mu=m_ushift[i][j]
            ml=m_lshift[i][j]
            w1=w0-2*(r0-r1)
            h1=h0-2*(r0-r1)-mu-ml
            r2=rs[i][j]
            sux0=sux[i][j]
            suh0=suh[i][j]
            slh0=slh[i][j]
            w2=w1-2*(sux0+(r1-r2))
            h2=h1-2*(r1-r2)+suh0-slh0

            p0=0
            path1=draw_contour(r0,w0,h0,p0)
            p1=(w0-w1)/2+-1j*ml+p0+(r0-r1)*-1j

            p2=(w1-w2)/2+slh0*-1j+p1+(r1-r2)*-1j
            path3=draw_contour(r2,w2,h2,p2)
            trapu=trap_u[i][j]
            trapl=trap_l[i][j]
#             traph=trap_h[i][j]
            traph_ratio=trap_h_ratio[i][j]
            ms_gap=r1-r2-suh0
            traph=ms_gap * traph_ratio
            ur_corner=p0+w0+h0*-1j
            cam_h=camera_r_h[i][j]
            cam2r=camera2r[i][j]
            ct=camera_ct[i][j]
            vh=vol_h[i][j]
            vl=vol_l[i][j]
            pl=power_l[i][j]
            #determine screen has notch or not from camera position
            if ct==0:
#                 path2=draw_contour(r1,w1,h1,p1)#no notch
#                 path3=draw_contour(r2,w2,h2,p2)#no notch
                path2=draw_notch(r1,w1,h1,p1,trapu,trapl,traph) #also have notch
                #draw buttons
                vol_ur=ur_corner+button_h+(-vh+vl/2)*-1j
                vol_path=draw_rect(button_h,vl,vol_ur)

                ph=power_unfree_h[i][j]#unfree because volume on top
                power_ur=ur_corner+button_h+(-ph+pl/2)*-1j
                power_path=draw_rect(button_h,pl,power_ur)
                buttons=[vol_path,power_path]
            else:
                path2=draw_notch(r1,w1,h1,p1,trapu,trapl,traph)#has notch, vol on left, has bixby
#                 path3=draw_notch(r2,w2,h2,p2,trapu,trapl,traph)#has notch, vol on left, has bixby
                #draw buttons
                vol_ur=p0+(h0-vh+vl/2)*-1j
                vol_path=draw_rect(button_h,vl,vol_ur)

                ph=power_free_h[i][j]#unfree because volume on top
                power_ur=ur_corner+button_h+(-ph+pl/2)*-1j
                power_path=draw_rect(button_h,pl,power_ur)

                bh=bixby_h[i][j]
                bl=bixby_l[i][j]
                bixby_ur=p0+(h0-bh+bl/2)*-1j
                bixby_path=draw_rect(button_h,bl,bixby_ur)            
                buttons=[vol_path,power_path,bixby_path]

            cam_r1=camera_r1[i][j]
            cam_r2=camera_r2[i][j]
            d=camera_d[i][j]
            ring=ring_r[i][j]
            cam_mh=camera_m_h[i][j]
            cam_mr=camera_m_r[i][j]
            paths4=draw_camera(p0,ur_corner,cam_h,cam2r,ct,cam_r1,cam_r2,d,ring,cam_mh,cam_mr)
            path=[path1,path2,path3]+paths4+buttons
            svg_name=original_folder+"/samsung%s-%s.svg"%(i,j)
            
            if draw_nodes==1:
                nodes=[]
                #this will plot nodes
                for a in path:
                    for b in a:
                        nodes.append(b.start)
                wsvg(path,stroke_widths=list(np.ones(len(path))*0.2),
                nodes=nodes, node_radii=list(np.ones(len(nodes))*0.5),
                viewbox=(-10,-120,90,130),dimensions=(360,900),filename=svg_name)
            else:   
                stroke_params=np.ones(len(path))*0.2
                if stroke_aug==1:
                    stroke_params=np.random.uniform(low=0.2, high=1.8, size=len(path))
            
                if extra==0:
                    wsvg(path,stroke_widths=stroke_params,viewbox=(-10,-120,90,130),dimensions=(360,900),                filename=svg_name)
                elif extra==1:
                    wsvg(path,filename=svg_name)

# In[ ]:


def create_samsung_params(data_size):
    '''set the range of variables and important correlations'''
    h_min=142.2
    h_max=166.9
    w_min=69.1
    w_max=77.1
    #1.844-2.415
    rl_min, rl_max=6.52, 8.31
    rm_min, rm_max=6.52, 8.03
    m_ushift_min, m_ushift_max=0,1.76
    m_lshift_min, m_lshift_max=0,2.44
    rs_min, rs_max=4.89, 6.97
    sux_min, sux_max=-0.37, 1.33
    suh_min, suh_max=-0.76, 0.86
    slh_min, slh_max=0.41, 1.97
    camera_r_h_min, camera_r_h_max=7.82, 8.01 #right height
    camera2r_min, camera2r_max=7.79, 9.96 #cam2right for cameras on the right
    camera_d_min, camera_d_max=7.29, 11.03 #if exist
    camera_r1_min, camera_r1_max=2.47, 2.49 #camera radius at right corner
    camera_r2_min, camera_r2_max=1.59, 1.63 #camera radius at middle
    ring_min, ring_max=2.36, 2.65

    camera_m_h_min, camera_m_h_max=5.23, 5.37 #middle height
    camera_m_r_min, camera_m_r_max=1.81, 1.98 #middle radius

    trap_u_min, trap_u_max=12.45, 13.56
    trap_l_min, trap_l_max=8.51, 10.5
#     trap_h_min, trap_h_max=0.89, 1.7
#     trap_h_ratio_min, trap_h_ratio_max=0.447236, 1
    trap_h_ratio_min, trap_h_ratio_max=0.1, 1 #use ratio between suh, to make sure it scales
    button_h=0.75
    vol_l_min, vol_l_max=19.25, 20.04
    vol_h_min, vol_h_max=28.76, 41.8
    bixby_l_min, bixby_l_max=7.86, 10.22
    bixby_h_min, bixby_h_max=50.16,65.69
    power_free_h_min, power_free_h_max=26.76, 51.57# has bixby
    power_unfree_h_min, power_unfree_h_max=61.52, 66.38 #no bixby
    power_l_min, power_l_max=10.03, 14.88 
    
    '''correlations'''
    h2w=0.87219
    h2mu=0.6385
    h2ml=0.75174
    h2rs=0.58661
    h2sux=0.64597
#     h2traph=-0.959
    h2vol_h=0.89517
    v2bixby_l=0.994885
    v2bixby_h=0.989886
    v2p=0.9 #technically 0.912
    rl2rm=0.816426
    rm2rs=0.642392
    suh2slh=-0.84589
    
    
    '''make a matrix of random variables'''
    h=np.random.uniform(h_min,h_max,data_size)
    w=weighted_random(w_min,w_max,h_min,h_max,h,h2w,data_size)
    rl=np.random.uniform(rl_min, rl_max,data_size)
    rm=weighted_random(rm_min,rm_max,rl_min,rl_max,rl,rl2rm,data_size)
    rs1=weighted_random(rs_min,rs_max,h_min,h_max,h,h2rs,data_size)
    rs2=weighted_random(rs_min,rs_max,rm_min,rm_max,rm,rm2rs,data_size)
    rs=0.5*(rs1+rs2)

    m_ushift=weighted_random(m_ushift_min, m_ushift_max, h_min, h_max, h, h2mu, data_size)
    m_lshift=weighted_random(m_lshift_min, m_lshift_max, h_min, h_max, h, h2ml, data_size)
    sux=weighted_random(sux_min, sux_max, h_min, h_max, h, h2mu, data_size)
    suh=np.random.uniform(suh_min, suh_max,data_size)

    slh=weighted_random(slh_min, slh_max, suh_min, suh_max, suh, suh2slh, data_size)

    camera_r_h=np.random.uniform(camera_r_h_min, camera_r_h_max,data_size)
    camera_ct=np.random.randint(0,3,data_size)
    camera_d=np.random.uniform(camera_d_min, camera_d_max,data_size)#if here
    camera_r1=np.random.uniform(camera_r1_min, camera_r1_max,data_size)#if 1 cam
    camera_r2=np.random.uniform(camera_r2_min, camera_r2_max,data_size)#if 2 cams
    camera2r=np.random.uniform(camera2r_min, camera2r_max,data_size)
    ring_r=np.random.uniform(ring_min, ring_max,data_size)

    camera_m_h=np.random.uniform(camera_m_h_min, camera_m_h_max, data_size)
    camera_m_r=np.random.uniform(camera_m_r_min, camera_m_r_max, data_size)

    trap_u=np.random.uniform(trap_u_min, trap_u_max,data_size)
    trap_l=np.random.uniform(trap_l_min, trap_l_max,data_size)
#     trap_h=weighted_random(trap_h_min, trap_h_max, h_min, h_max, h, h2traph, data_size)
    trap_h_ratio=np.random.uniform(trap_h_ratio_min, trap_h_ratio_max,data_size)
    button_h=button_h


    vol_l=np.random.uniform(vol_l_min, vol_l_max,data_size)
    vol_h=weighted_random(vol_h_min, vol_h_max, h_min, h_max, h, h2vol_h, data_size)
    bixby_l=weighted_random(bixby_l_min, bixby_l_max, vol_l_min, vol_l_max, vol_l, v2bixby_l, data_size)
    bixby_h=weighted_random(bixby_h_min, bixby_h_max, vol_h_min, vol_h_max, vol_h, v2bixby_h, data_size)
    power_l=np.random.uniform(power_l_min, power_l_max,data_size)
    power_free_h=weighted_random(power_free_h_min, power_free_h_max, vol_h_min, vol_h_max, vol_h, v2p, data_size)
    power_unfree_h=weighted_random(power_unfree_h_min, power_unfree_h_max, vol_h_min, vol_h_max, vol_h, v2p, data_size)

    samsung_params={}
    samsung_params["h"]=h
    samsung_params["w"]=w
    samsung_params["rl"]=rl
    samsung_params["rm"]=rm
    samsung_params["rs"]=rs
    samsung_params["m_ushift"]=m_ushift
    samsung_params["m_lshift"]=m_lshift
    samsung_params["sux"]=sux
    samsung_params["suh"]=suh
    samsung_params["slh"]=slh
    samsung_params["camera_r_h"]=camera_r_h
    samsung_params["camera_ct"]=camera_ct
    samsung_params["camera_d"]=camera_d
    samsung_params["camera_r1"]=camera_r1
    samsung_params["camera_r2"]=camera_r2
    samsung_params["camera2r"]=camera2r
    samsung_params["ring_r"]=ring_r
    samsung_params["camera_m_h"]=camera_m_h
    samsung_params["camera_m_r"]=camera_m_r
    samsung_params["trap_u"]=trap_u
    samsung_params["trap_l"]=trap_l
    samsung_params["trap_h_ratio"]=trap_h_ratio
    samsung_params["button_h"]=button_h
    samsung_params["vol_l"]=vol_l
    samsung_params["vol_h"]=vol_h
    samsung_params["bixby_l"]=bixby_l
    samsung_params["bixby_h"]=bixby_h
    samsung_params["power_l"]=power_l
    samsung_params["power_free_h"]=power_free_h
    samsung_params["power_unfree_h"]=power_unfree_h
    return samsung_params


# In[3]:


def draw_notch(r,w,h,start,trap_u,trap_l,trap_h):
    r0=r
    p1=start+0+r0*-1j
    p2=p1+(h-2*r0)*-1j
    seg1=Line(p1,p2)
    p3=p2+r0*(1+-1j)
    seg2=Arc(p2,r0*(1+-1j),rotation=0,large_arc=0,sweep=1,end=p3)
    p4=p3+(w-2*r0-trap_u)/2
    seg3=Line(p3,p4)
    p5=p4+(trap_u-trap_l)/2-trap_h*-1j
    seg4=Line(p4,p5)
    p6=p5+trap_l
    seg5=Line(p5,p6)
    p7=p6+(trap_u-trap_l)/2+trap_h*-1j
    seg6=Line(p6,p7)
    p8=p7+(w-2*r0-trap_u)/2
    seg7=Line(p7,p8)
    p9=p8+r0*(1--1j)
    seg8=Arc(p8,r0*(-1--1j),rotation=0,large_arc=0,sweep=1,end=p9)
    p10=p9-(h-2*r0)*-1j
    seg9=Line(p9,p10)
    p11=p10+r0*(-1--1j)
    seg10=Arc(p10,r0*(-1--1j),rotation=0,large_arc=0,sweep=1,end=p11)
    p12=p11-(w-2*r0)
    seg11=Line(p11,p12)
    p13=p1
    seg12=Arc(p12,r0*(-1+-1j),rotation=0,large_arc=0,sweep=1,end=p13)  
    #this notch is connected
    seg13=Line(p4,p7)
    path_out=Path(seg1,seg2,seg3,seg4,seg5,seg6,seg7,seg8,seg9,seg10,seg11,seg12,seg13)
    return path_out


# In[4]:


def weighted_random(target_min, target_max, 
                    influence_min, influence_max, influence_value, influence_weight, 
                    data_size):
    
    weight_factor=(influence_value-influence_min)/(influence_max-influence_min)*(target_max-target_min)+target_min
    unweighted_randoms=np.random.uniform(target_min,target_max,data_size)
    weighted_randoms=unweighted_randoms*(1-influence_weight)+weight_factor*influence_weight
        
    return weighted_randoms


# In[5]:


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


# In[6]:


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


# In[7]:


def draw_camera(start,ur_corner,h,to_r,ct,r1,r2,d,ring,cam_mh,cam_mr):
    if ct==0:
        #if start is always 0,0, then middle is easy
        p0=(start.real+ur_corner.real)/2+ur_corner.imag*1j-cam_mh*-1j
        r=cam_mr
        path=draw_circle(p0,r)
        return [path]
    if ct!=0:
        p0=ur_corner-to_r-h*-1j
        if ct==1: #1 cam
            r=r1
            path=draw_circle(p0,r)
            return [path]
        if ct==2: #1 cam
            r=r2
            path1=draw_circle(p0,r)
            path2=draw_circle(p0-d,r)
            path3=draw_ring(p0,d,ring)
            return [path1, path2, path3]


# In[8]:


def draw_circle(p,r):
    pL=p-r
    pR=p+r
    seg1=Arc(pL,r*(-1+-1j),rotation=0,large_arc=0,sweep=0,end=pR)
    seg2=Arc(pL,r*(-1+-1j),rotation=0,large_arc=0,sweep=1,end=pR)
    return Path(seg1,seg2)


# In[9]:


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


# In[10]:


# data_size=(2,5)
# original_folder="samsung original"

# rec=create_samsung_dataset_rec(data_size, original_folder, stroke_aug=0)

