#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from .get_filelist import get_filelist
from .svg_to_rasterize import svg_to_rasterize
import os

def rasterize(in_folder, out_folder, pixel_format):
    original_svg = get_filelist(dir,in_folder)
    for svg_path in original_svg:
        rasterized_img=svg_to_rasterize(res=250,path=svg_path)
        pixel_name=out_folder+"/"+svg_path.split("/")[-1].split(".")[0]+pixel_format
        rasterized_img.save(filename=pixel_name)

def vectorize(in_folder, out_folder):
    pixel_phone = get_filelist(dir,in_folder)
    for idx,picture_path in enumerate(pixel_phone):
        name=picture_path.split("/")[-1].split(".")[0]
        resample_path=out_folder+"/"+name+".svg"
        get_ipython().system('potrace "{picture_path}" -o {resample_path} -b svg')

def resample(original_folder, pixel_folder, pixel_format, resample_folder):
    rasterize(original_folder, pixel_folder, pixel_format)
    vectorize(pixel_folder, resample_folder)
    
def rasterize1svg(svg_path, out_img="temp.bmp", temp_seed=0):
    rasterized_img=svg_to_rasterize(res=250,path=svg_path, temp_seed=temp_seed)
    rasterized_img.save(filename=out_img)

def vectorize1svg(in_img, out_svg):
    get_ipython().system('potrace "{in_img}" -o {out_svg} -b svg')

def resample1svg(in_svg, out_svg, remove=1, temp_seed=0):
    
    temp_img="temp%s.bmp"%temp_seed
    rasterize1svg(in_svg, temp_img, temp_seed)
    vectorize1svg(temp_img, out_svg)
    if remove==1:
        os.remove(temp_img)