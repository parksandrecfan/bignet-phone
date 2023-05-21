from .bignet1 import bignet1, binary_acc, timeSince
import torch
import torch.nn as nn
import util as u
import numpy as np
import random
import os
import shutil
pkl_folder="pkl"

# mode: "avg", "cor", "frame", "norm"

def eval1folder(model_path, in_folder, out_folder="ablation_svg",
               brand="iphone", resample=0, mode="avg"):

    pixel_format=".bmp"
    if resample==1:
        original_folder=in_folder
        pixel_folder="eval_pixel"
        resample_folder="eval_resample"
        u.initialize([pixel_folder,resample_folder])
        u.resample(original_folder, pixel_folder,\
          pixel_format, resample_folder)
        phones = u.get_filelist(dir, resample_folder)
        
    elif resample==0:
        phones = u.get_filelist(dir, in_folder)
        
    if brand=="iphone":
        this_set, this_label, this_dist_mat, this_name_list=\
        u.get_normalized_data(phones, [], h_aug=0, v_aug=0)
    elif brand=="samsung":
        this_set, this_label, this_dist_mat, this_name_list=\
        u.get_normalized_data([], phones, h_aug=0, v_aug=0)
    
    for name_idx, name in enumerate(this_name_list):
        this_name_list[name_idx]=name.split("/")[-1].split(".")[0]
    
    this_curve_label=u.curve_labeling(this_set)    
    eval1set(model_path, this_set, this_label,\
             this_curve_label, this_dist_mat,\
             this_name_list, out_folder, mode)

def eval1set(model_path, this_set, this_label,\
             this_curve_label, this_dist_mat,\
             names, out_folder="ablation_svg", mode="avg"):
    
    temp_folder="%s/temp"%pkl_folder
    os.mkdir(temp_folder)
    

    eval_net= u.bignet1(batch_size=1)

        
    eval_net.load_state_dict(torch.load(model_path))
    eval_net.eval()
    eval_net.batch_size=1

    eval_set=this_set
    eval_label=this_label
    eval_curve_label=this_curve_label
    eval_dist_mat=this_dist_mat

    eval_loss_rec=[]
    eval_acc_rec=[]
    eval_feat_rec=[]
    #for each picture:
    for idx, label in enumerate(eval_label):#a picture

        this_loss_rec=[]
        this_acc_rec=[]
        svg_list=[eval_set[idx]]
        #confirm there is more than 1 group
        if len(svg_list[0])!=1:
    #         print(len(svg_list[0]))
            curve_feature=[]
            cor=eval_dist_mat[idx]
            label=[eval_label[idx]]
            curve_label=[eval_curve_label[idx]]

            #calculate ref loss, acc
            _, test_pred=eval_net(svg_list, curve_label, [cor])
    #         print(test_pred.detach().numpy())
            loss_func=nn.BCELoss()
            torch_label=torch.FloatTensor(label)
            test_loss=loss_func(test_pred, torch_label)
            '''serve as reference'''
            this_loss_rec.append(test_loss.detach().numpy())
            this_acc_rec.append(test_pred.detach().numpy())

        #     test_acc=binary_acc(test_pred, torch_label)
            #to avoid traffic, dump to a random file, and delete at last

            file_random=random.random()
            temp_svg_list="%s/%s.pkl"%(temp_folder,file_random)
            u.dump_item(svg_list, temp_svg_list)

            for group2del,this_group in enumerate(svg_list[0]):
                '''first, delete a curve'''
                # deep copy svg_list
                svg_list=u.load_item(temp_svg_list) #everytime
                curve_loss_rec=[]
                '''serve as reference'''
                curve_loss_rec.append(this_loss_rec[0])
                for curve2del,_ in enumerate(this_group):
                    svg_list=u.load_item(temp_svg_list) #everytime
    #                 print(len(svg_list[0][group2del]))
                    del svg_list[0][group2del][curve2del]
    #                 print(len(svg_list[0][group2del]))
                    #we assume deleting one curve will not change bbox
                    curve_label=u.curve_labeling(svg_list)
                    _, curve_pred=eval_net(svg_list, curve_label, [cor])
                    loss_func=nn.BCELoss()
                    torch_label=torch.FloatTensor(label)
                    curve_loss=loss_func(curve_pred, torch_label)
                    curve_loss_rec.append(curve_loss.detach().numpy())
                curve_loss_increase=len(curve_loss_rec)
                curve_test_increase=np.zeros(curve_loss_increase)
    #             print(curve_loss_rec)
                for curve_num in range(curve_loss_increase):
                    this_loss=curve_loss_rec[curve_num]
                    ref_loss=curve_loss_rec[0]
                    curve_test_increase[curve_num]=(this_loss-ref_loss)*1e5
    #             print(curve_test_increase)
                feature_curve=curve_test_increase.argmax()-1
                feature_curve=None if feature_curve<0 else feature_curve
                #means no matter erase which curve acc goes up
                curve_test_increase2=np.expand_dims(curve_test_increase, axis=0)
                feature_curve2=np.argsort(np.max(curve_test_increase2, axis=0))[-2]-1
                feature_curve2=None if feature_curve2<0 or feature_curve==None else feature_curve2
                feature_curve3=np.argsort(np.max(curve_test_increase2, axis=0))[-3]-1
                feature_curve3=None if feature_curve3<0 or feature_curve2==None else feature_curve3
                feature_curve4=np.argsort(np.max(curve_test_increase2, axis=0))[-4]-1
                feature_curve4=None if feature_curve4<0 or feature_curve3==None else feature_curve4
                feature_curve5=np.argsort(np.max(curve_test_increase2, axis=0))[-5]-1
                feature_curve5=None if feature_curve5<0 or feature_curve4==None else feature_curve5


                curve_feature.append([feature_curve,feature_curve2,\
                                      feature_curve3, feature_curve4, feature_curve5])
    #             print(curve_feature)
                '''then, delete a group'''
                svg_list=u.load_item(temp_svg_list) #everytime
                del svg_list[0][group2del] #delete the svg
        #         print(len(svg_list[0]))
                #save this svg to see what it looks like?

                cor_del=np.delete(np.delete(cor, group2del, 0), group2del, 1)#delete the cor mat
                curve_label=u.curve_labeling(svg_list)
                #calculate ref loss, acc
                rec, test_pred=eval_net(svg_list, curve_label, [cor_del])
                loss_func=nn.BCELoss()
                torch_label=torch.FloatTensor(label)
                test_loss=loss_func(test_pred, torch_label)

                this_loss_rec.append(test_loss.detach().numpy())
                this_acc_rec.append(test_pred.detach().numpy())
            svg_list=u.load_item(temp_svg_list) #everytime
            eval_loss_rec.append(this_loss_rec)
            eval_acc_rec.append(this_acc_rec)
            #find the most important group
            loss_increase=len(this_loss_rec)
            test_increase=np.zeros(loss_increase)
            for group_num in range(loss_increase):
                this_loss=this_loss_rec[group_num]
                ref_loss=this_loss_rec[0]
                test_increase[group_num]=this_loss-ref_loss
            feature_group=test_increase.argmax()-1#index of the max group
            feature_group=None if feature_group<0 else feature_group

            test_increase2=np.expand_dims(test_increase, axis=0)
            feature_group2=np.argsort(np.max(test_increase2, axis=0))[-2]-1

            feature_group2=None if feature_group2<0 or feature_group==None else feature_group2
            feature_group3=np.argsort(np.max(test_increase2, axis=0))[-3]-1
            feature_group3=None if feature_group3<0 or feature_group2==None else feature_group3
            if len(test_increase2[0])<5:#5-1=only 4 groups
                feature_group4=None
            else:
                feature_group4=np.argsort(np.max(test_increase2, axis=0))[-4]-1
                feature_group4=None if feature_group4<0 or feature_group3==None else feature_group4

    #         print(idx, feature_group, feature_group2, len(svg_list[0]))
            #shift by one because the list all minus the first loss,
            #the first one [0] is always 0, means nothing

            group_feat=[feature_group, feature_group2, feature_group3, feature_group4]
            eval_feat_rec.append(feature_group)
            #reload svg_list
            svg_list=u.load_item(temp_svg_list) #everytime
            set2svg(names[idx], svg_list, group_feat, curve_feature, mode="group", ablation_folder=out_folder)
            set2svg(names[idx], svg_list, group_feat, curve_feature, mode="curve", ablation_folder=out_folder)        #after finding the most important 
    shutil.rmtree(temp_folder)
    
    
from svgpathtools import Path, Line, QuadraticBezier, \
CubicBezier, Arc,svg2paths2,wsvg,disvg,svg2paths

# len(test_label)
# print(len(test_set2[0]))#how many groups
# print(len(test_set2[0][0]))#how many curves
# print(len(test_set2[0][0][0]))#8
def set2svg(name, svg_list, group_feat=None, \
            curve_feature=None, mode="group", ablation_folder="ablation_svg"):

    ablation_folder=ablation_folder
    pic=svg_list[0]
    svg_path=[]
    color=[]
    feat_w=0.006
    feat_w2=0.0055
    feat_w3=0.0055
    feat_w4=0.005
    feat_w5=0.005
    norm_w=0.002

    curve_feature=curve_feature
    
    if mode=="group":
        stroke_params=list(np.ones(len(pic))*norm_w)  
        for idx, group in enumerate(pic):
            group_path=0
            for idy, curve in enumerate(group):
        #         print(curve)
                c0_x, c0_y, c1_x, c1_y, c2_x, c2_y, c3_x, c3_y=\
                curve
                c0=complex(c0_x, -c0_y)
                c1=complex(c1_x, -c1_y)
                c2=complex(c2_x, -c2_y)
                c3=complex(c3_x, -c3_y)
                seg= CubicBezier(c0,c1,c2,c3)
                if group_path==0:
                    group_path=Path(seg)
                else:
                    group_path.append(seg)
            if idx==group_feat[0]:
                color.append((255,0,0))
            elif idx==group_feat[1]:
                color.append((255,100,100))
            elif idx==group_feat[2]:
                color.append((255,150,150))    
            elif idx==group_feat[3]:
                color.append((255,190,190)) 
            else:
                color.append((0,0,0))
            svg_path.append(group_path)

        if group_feat[0]!=None:
            stroke_params[group_feat[0]]=feat_w 
        if group_feat[1]!=None:
            stroke_params[group_feat[1]]=feat_w 
        if group_feat[2]!=None:
            stroke_params[group_feat[2]]=feat_w 
        if group_feat[3]!=None:
            stroke_params[group_feat[3]]=feat_w             
    if mode=="curve":
        stroke_params=[]
        for idx, group in enumerate(pic):
            for idy, curve in enumerate(group):
        #         print(curve)
                c0_x, c0_y, c1_x, c1_y, c2_x, c2_y, c3_x, c3_y=\
                curve
                c0=complex(c0_x, -c0_y)
                c1=complex(c1_x, -c1_y)
                c2=complex(c2_x, -c2_y)
                c3=complex(c3_x, -c3_y)
                seg= CubicBezier(c0,c1,c2,c3)
                svg_path.append(seg)

                if idx==group_feat[0]:
                    color.append((255,0,0))
                elif idx==group_feat[1]:
                    color.append((255,100,100))
                elif idx==group_feat[2]:
                    color.append((255,150,150))    
                elif idx==group_feat[3]:
                    color.append((255,190,190)) 
                else:
                    color.append((0,0,0))
#                 print(curve_feature[idx])
                if curve_feature[idx][0]==idy:
                    stroke_params.append(feat_w)
                    color[-1]=(0,0,255)
#                     print("0")
                elif curve_feature[idx][1]==idy:
                    stroke_params.append(feat_w2)
#                     color[-1]=(0,0,210)
                    color[-1]=(70,70,255)
#                     print("1")
                elif curve_feature[idx][2]==idy:
                    stroke_params.append(feat_w3)
#                     color[-1]=(0,0,170)
                    color[-1]=(110,110,255)
#                     print("2")
                elif curve_feature[idx][3]==idy:
                    stroke_params.append(feat_w4)
#                     color[-1]=(0,0,120)
                    color[-1]=(150,150,255)
#                     print("3")
                elif curve_feature[idx][4]==idy:
                    stroke_params.append(feat_w5)
#                     color[-1]=(0,0,70)
                    color[-1]=(190,190,255)
#                     print("4")
                else:
                    stroke_params.append(norm_w) 

    wsvg(svg_path,color,stroke_widths=stroke_params,\
         filename="%s/%s %s.svg"%(ablation_folder,mode,name))



def test1svg(model_path, svg_path, brand="iphone", resample=0,\
            prediction=1, ablation=None, mode="avg", temp_seed=0):
    if brand=="iphone":
        label=[[1,0]]
    elif brand=="samsung":
        label=[[0,1]]
        
    eval_net= u.bignet1(batch_size=1)

        
    eval_net.load_state_dict(torch.load(model_path))
    eval_net.eval()
    eval_net.batch_size=1
    
    eval_svg="eval%s.svg"%temp_seed
    if resample==1:
        u.resample1svg(svg_path, eval_svg, remove=0, temp_seed=temp_seed)
        
    elif resample==0:
        eval_svg=svg_path
        
    if brand=="iphone":
        this_set, this_label, this_dist_mat, this_name_list=\
        u.get_normalized_data([eval_svg], [], h_aug=0, v_aug=0)
    elif brand=="samsung":
        this_set, this_label, this_dist_mat, this_name_list=\
        u.get_normalized_data([], [eval_svg], h_aug=0, v_aug=0)
    

    this_curve_label=u.curve_labeling(this_set, temp_seed=temp_seed)    
    test_acc=None
    test_prediction=None
    if prediction==1:
        rec, test_pred=eval_net(this_set, this_curve_label, this_dist_mat)
        loss_func=nn.BCELoss()
        torch_label=torch.FloatTensor(label)
        test_acc=binary_acc(test_pred, torch_label)
        test_prediction=test_pred.detach().numpy()
    if ablation!=None:
        svg_name=svg_path.split("/")[-1].split(".")[0]
        eval1svg(eval_net, svg_name, this_set, label,\
                 this_curve_label, this_dist_mat, ablation_folder=ablation,\
                 temp_seed=temp_seed)
    return test_acc, test_prediction

def eval1svg(model, svg_name, this_set, this_label, this_curve_label, this_dist_mat, ablation_folder, temp_seed=0):
    eval_net= model

    eval_set=this_set
    eval_label=this_label
    eval_curve_label=this_curve_label
    eval_dist_mat=this_dist_mat

    eval_loss_rec=[]
    eval_acc_rec=[]
    eval_feat_rec=[]
    #for each picture:
    for idx, label in enumerate(eval_label):#a picture

        this_loss_rec=[]
        this_acc_rec=[]
        svg_list=[eval_set[idx]]
        #confirm there is more than 1 group
        if len(svg_list[0])!=1:
    #         print(len(svg_list[0]))
            curve_feature=[]
            cor=eval_dist_mat[idx]
            label=[eval_label[idx]]
            curve_label=[eval_curve_label[idx]]

            #calculate ref loss, acc
            _, test_pred=eval_net(svg_list, curve_label, [cor])
    #         print(test_pred.detach().numpy())
            loss_func=nn.BCELoss()
            torch_label=torch.FloatTensor(label)
            test_loss=loss_func(test_pred, torch_label)
            '''serve as reference'''
            this_loss_rec.append(test_loss.detach().numpy())
            this_acc_rec.append(test_pred.detach().numpy())

        #     test_acc=binary_acc(test_pred, torch_label)
            temp_folder="%s/temp%s"%(pkl_folder,temp_seed)
            os.mkdir(temp_folder)
            file_random=random.random()
            temp_svg_list="%s/%s.pkl"%(temp_folder,file_random)
            u.dump_item(svg_list, temp_svg_list) # dump only one time

            for group2del,this_group in enumerate(svg_list[0]):
                '''first, delete a curve'''
                # deep copy svg_list
                svg_list=u.load_item(temp_svg_list) #everytime
                curve_loss_rec=[]
                '''serve as reference'''
                curve_loss_rec.append(this_loss_rec[0])
                for curve2del,_ in enumerate(this_group):
                    svg_list=u.load_item(temp_svg_list) #everytime
    #                 print(len(svg_list[0][group2del]))
                    del svg_list[0][group2del][curve2del]
    #                 print(len(svg_list[0][group2del]))
                    #we assume deleting one curve will not change bbox
                    curve_label=u.curve_labeling(svg_list, temp_seed=temp_seed)
                    _, curve_pred=eval_net(svg_list, curve_label, [cor])
                    loss_func=nn.BCELoss()
                    torch_label=torch.FloatTensor(label)
                    curve_loss=loss_func(curve_pred, torch_label)
                    curve_loss_rec.append(curve_loss.detach().numpy())
                curve_loss_increase=len(curve_loss_rec)
                curve_test_increase=np.zeros(curve_loss_increase)
    #             print(curve_loss_rec)
                for curve_num in range(curve_loss_increase):
                    this_loss=curve_loss_rec[curve_num]
                    ref_loss=curve_loss_rec[0]
                    curve_test_increase[curve_num]=(this_loss-ref_loss)*1e5
    #             print(curve_test_increase)
                feature_curve=curve_test_increase.argmax()-1
                feature_curve=None if feature_curve<0 else feature_curve
                #means no matter erase which curve acc goes up
                curve_test_increase2=np.expand_dims(curve_test_increase, axis=0)
                feature_curve2=np.argsort(np.max(curve_test_increase2, axis=0))[-2]-1
                feature_curve2=None if feature_curve2<0 or feature_curve==None else feature_curve2
                feature_curve3=np.argsort(np.max(curve_test_increase2, axis=0))[-3]-1
                feature_curve3=None if feature_curve3<0 or feature_curve2==None else feature_curve3
                feature_curve4=np.argsort(np.max(curve_test_increase2, axis=0))[-4]-1
                feature_curve4=None if feature_curve4<0 or feature_curve3==None else feature_curve4
                feature_curve5=np.argsort(np.max(curve_test_increase2, axis=0))[-5]-1
                feature_curve5=None if feature_curve5<0 or feature_curve4==None else feature_curve5


                curve_feature.append([feature_curve,feature_curve2,                                      feature_curve3, feature_curve4, feature_curve5])
                '''then, delete a group'''
                svg_list=u.load_item(temp_svg_list) #everytime
                del svg_list[0][group2del] #delete the svg

                cor_del=np.delete(np.delete(cor, group2del, 0), group2del, 1)#delete the cor mat
                curve_label=u.curve_labeling(svg_list, temp_seed=temp_seed)

                #calculate ref loss, acc
                rec, test_pred=eval_net(svg_list, curve_label, [cor_del])
                loss_func=nn.BCELoss()
                torch_label=torch.FloatTensor(label)
                test_loss=loss_func(test_pred, torch_label)

                this_loss_rec.append(test_loss.detach().numpy())
                this_acc_rec.append(test_pred.detach().numpy())
            svg_list=u.load_item(temp_svg_list) #everytime
            eval_loss_rec.append(this_loss_rec)
            eval_acc_rec.append(this_acc_rec)
            #find the most important group
            loss_increase=len(this_loss_rec)
            test_increase=np.zeros(loss_increase)
            for group_num in range(loss_increase):
                this_loss=this_loss_rec[group_num]
                ref_loss=this_loss_rec[0]
                test_increase[group_num]=this_loss-ref_loss
            feature_group=test_increase.argmax()-1#index of the max group
            feature_group=None if feature_group<0 else feature_group

            test_increase2=np.expand_dims(test_increase, axis=0)
            feature_group2=np.argsort(np.max(test_increase2, axis=0))[-2]-1

            feature_group2=None if feature_group2<0 or feature_group==None else feature_group2
            feature_group3=np.argsort(np.max(test_increase2, axis=0))[-3]-1
            feature_group3=None if feature_group3<0 or feature_group2==None else feature_group3
            if len(test_increase2[0])<5:#5-1=only 4 groups
                feature_group4=None
            else:
                feature_group4=np.argsort(np.max(test_increase2, axis=0))[-4]-1
                feature_group4=None if feature_group4<0 or feature_group3==None else feature_group4


            group_feat=[feature_group, feature_group2, feature_group3, feature_group4]
            eval_feat_rec.append(feature_group)
            #reload svg_list
            svg_list=u.load_item(temp_svg_list) #everytime
            shutil.rmtree(temp_folder)
            set2svg(svg_name, svg_list, group_feat, curve_feature, mode="curve", ablation_folder=ablation_folder)
            set2svg(svg_name, svg_list, group_feat, curve_feature, mode="group", ablation_folder=ablation_folder)