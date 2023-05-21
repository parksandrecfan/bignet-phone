#!/usr/bin/env python
# coding: utf-8

# In[1]:


# from ipynb.fs.full.array2svg import *
# from ipynb.fs.full.svg2rnn import *
# from ipynb.fs.full.color2rnn import *
import svgpathtools
from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc, svg2paths2
import numpy as np

# In[2]:


def svg_pic2pathsum(path):
    paths, attributes,svg_attributes=svg2paths2(path)
    svgpath=0
    svgpathsum=0
    for i in paths:

#         print("new group",len(i))
        for j in i:
            if isinstance(j, Arc):
                
#                 print("arc",j)
                xc=j.center.real
                yc=j.center.imag
                x1=j.start.real
                y1=j.start.imag
                x4=j.end.real
                y4=j.end.imag

                ax = x1 - xc
                ay = y1 - yc
                bx = x4 - xc
                by = y4 - yc
                q1 = ax * ax + ay * ay
                q2 = q1 + ax * bx + ay * by
                k2 = (4/3) * (np.sqrt(2 * q1 * q2) - q2) / (ax * by - ay * bx)

                x2 = xc + ax - k2 * ay
                y2 = yc + ay + k2 * ax
                x3 = xc + bx + k2 * by                                 
                y3 = yc + by - k2 * bx
                c0=complex(x1,y1)
                c1=complex(x2,y2)
                c2=complex(x3,y3)
                c3=complex(x4,y4)
                seg=CubicBezier(c0,c1,c2,c3)
                k=j

            if isinstance(j, Line):
#                 print("line",j)
                seg=CubicBezier(j.start, j.start*2/3+j.end/3, j.start/3+j.end*2/3, j.end)
#                 print(seg)
            if isinstance(j, QuadraticBezier):
#                 print("quad",j)
                seg=CubicBezier(j.start, j.start/3+j.control*2/3, j.control*2/3+j.end/3, j.end)
            if isinstance(j, CubicBezier):
#                 print("cub",j)
                seg=CubicBezier(j.start, j.control1, j.control2, j.end)

            if svgpath==0:
                svgpath=Path(seg)
            else:
                svgpath.append(seg)
#         print(len(svgpath))
        if svgpathsum==0:
            svgpathsum=svgpath
            oldsvgpath=svgpath
#             print("first")
        else:
            if svgpathsum==oldsvgpath:
                svgpathsum=[svgpathsum,svgpath]
#                 print("second")
            else:
                svgpathsum.extend(Path(svgpath))
#                 print("third")
        svgpath=0
#         disvg(svgpathsum,filename="test.svg")
    return svgpathsum


# In[5]:


# path="train svg/hatch_win.svg"
# paths, attributes,svg_attributes=svg2paths2(path)
# len(paths[0])

# path='/Users/idig/Desktop/cars/research venv/20210124venv/test/audi 2017 side5 edge pixel (6).svg'
# paths, attributes,svg_attributes=svg2paths2(path)
# len(paths[0])
# path=svg_pic2pathsum(path)


# In[29]:


# file="self made svg/hatch_win.svg"
# path=svg_pic2pathsum(file)
# path[0]==path[1]

