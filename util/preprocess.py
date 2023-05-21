#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import random
from .get_filelist import get_filelist
def split(folder, ratio):
    resample_phones = get_filelist(dir, folder)
    train_num=int(len(resample_phones) * ratio)
    train_phones =resample_phones[:train_num]
    test_phones  =resample_phones[train_num:]
    return train_phones, test_phones

#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import numpy as np
from .svgpic2path import svg_pic2pathsum
#normalization? get bounding box info, correlation matrix and normalized svg, turn into a list
def normalize(picpath, print_option=0, h_aug=0, v_aug=0):
    svg_orig=svg_pic2pathsum(path=picpath)
    #check if there is only one group, if it is and []
    if str(type(svg_orig[0]))=="<class 'svgpathtools.path.CubicBezier'>":
        svg_orig=[svg_orig]
    xmin=0
    xmax=0
    ymin=0
    ymax=0
    bbox=[]
    for idx,i in enumerate(svg_orig):#and idx is a group
#         print(idx+1,"group has",len(i),"curves")
        for jdx,j in enumerate(i):#a jdx is a curve
            for kdx,k in enumerate(j):#a kdx is an x or y component
                if(jdx==0 and kdx==0):#if it is the first curve in a group
                    xmin=k.real
                    xmax=k.real
                    ymin=k.imag
                    ymax=k.imag
                else:
                    xmin=k.real if float(k.real)<xmin else xmin
                    xmax=k.real if float(k.real)>xmax else xmax
                    ymin=k.imag if float(k.imag)<ymin else ymin
                    ymax=k.imag if float(k.imag)>ymax else ymax
        bbox.append([xmin,ymin,xmax,ymax])
#         curves+=len(i)

    xmin=0
    ymin=0
    xmax=0
    ymax=0
    for idx,i in enumerate(bbox):
        xmin=i[0] if idx==0 else i[0] if i[0]<xmin else xmin
        ymin=i[1] if idx==0 else i[1] if i[1]<ymin else ymin
        xmax=i[2] if idx==0 else i[2] if i[2]>xmax else xmax
        ymax=i[3] if idx==0 else i[3] if i[3]>ymax else ymax

#     print(xmin,ymin,xmax,ymax)
    h=ymax-ymin#need to keep this! add back at final representation
    absh=h
    cx=(xmin+xmax)/2
    cy=(ymin+ymax)/2

    for idx,i in enumerate(bbox):
        for jdx,j in enumerate(i):
            i[jdx]=(i[jdx]-cx)/h if jdx%2==0 else i[jdx] #odd,  x
            i[jdx]=(i[jdx]-cy)/h if jdx%2==1 else i[jdx] #even, y
#     bbox

    #2. shift to origin and make svg to list 1*8
    svg_list=[]
    group_list=[]
    curve_list=[]
    
    #augmentation
    h_shift=0
    v_shift=0
    if h_aug==1:
        h_shift=random.uniform(-0.05,0.05)
    if v_aug==1:
        v_shift=random.uniform(-0.05,0.05)    
        
    random.uniform(0,1)
    for idx,i in enumerate(svg_orig):#a idx is a group
        for jdx,j in enumerate(i):#a jdx is a curve
            for kdx,k in enumerate(j):#a k is a point
                curve_list.append((k.real-cx)/h+h_shift)
                curve_list.append((k.imag-cy)/h+v_shift)
            group_list.append(curve_list)
            curve_list=[]
        svg_list.append(group_list)
        group_list=[]

    bbox_par=[]

    for idx,i in enumerate(bbox):#every box(xmin,ymin,xmax,ymax)
        [xmin,ymin,xmax,ymax]=i
        area=(xmax-xmin)*(ymax-ymin)
        cx=(xmin+xmax)/2
        cy=(ymin+ymax)/2
        w=xmax-xmin
        h=ymax-ymin
        bbox_par.append([area,cx,cy,w,h])
# print bounding box info
#     print("[a, cx, cy, w, h]")
#     for i in bbox_par:
#         print("[",end='')
#         for j in i:
#             print(round(j,2),end=', ')
#         print("]")
        
#print the first bounding box: is it the frame?
    if print_option==1:
        print("[a,   cx,   cy,   w,   h]")
        for j in bbox_par[0]:
            print(round(j,2),end=', ')
        print()
        print()

    cor=np.zeros((len(bbox_par),len(bbox_par),len(bbox_par[0])))
    for n,corn in enumerate(cor):
        for m,corm in enumerate(corn):
            cor[n][m][0]=bbox_par[n][0]/bbox_par[m][0]
            cor[n][m][1]=bbox_par[n][1]-bbox_par[m][1]
            cor[n][m][2]=bbox_par[n][2]-bbox_par[m][2]
            cor[n][m][3]=bbox_par[n][3]/bbox_par[m][3]
            cor[n][m][4]=bbox_par[n][4]/bbox_par[m][4]
    return svg_list, cor


# In[1]:


def get_normalized_data(iphones, samsungs, h_aug=0, v_aug=0):
    this_list=[]
    label=[]
    cor_list=[]
    name_list=iphones+samsungs
    
    for iphone in iphones:
        svg_list, cor = normalize(iphone, h_aug=h_aug, v_aug=v_aug)
        this_list.append(svg_list)
        label.append([1,0])
        cor_list.append(cor)

    for samsung in samsungs:
        svg_list, cor = normalize(samsung, h_aug=h_aug, v_aug=v_aug)
        this_list.append(svg_list)
        label.append([0,1])
        cor_list.append(cor)
        
    return this_list, label, cor_list, name_list

