#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch
import torch.nn as nn
from torch.optim import Adam
from sklearn.metrics import accuracy_score

class bignet1(nn.Module):
    def __init__(self, batch_size=1):
        super(bignet1, self).__init__()
        self.neigh=4
        self.embed_len=8+(self.neigh)*6
        self.batch_size=batch_size
        self.curve_lv1=nn.Linear(self.embed_len,24)#32x24
        self.curve_lv2=nn.Linear(24,12)
        self.norm_curve=nn.BatchNorm1d(12)
        
        self.dist_mlp_lv1=nn.Linear(5,12)#for distance matrix
        self.dist_mlp_lv1.weight.data.fill_(1)#initialize to be 1
        self.dist_mlp_lv1.bias.data.fill_(1)#initialize to be 1
        
        self.group_level_layers=3
        
        self.norm_group=nn.BatchNorm1d(36)
        self.picture_lv1=nn.Linear(36,18)
        self.picture_lv2=nn.Linear(18,8)
        self.picture_lv3=nn.Linear(8,2)
        
        
        self.activation=nn.LeakyReLU()
        
    def forward(self, this_set, curve_label, dist_mat):

        set_flat=[]
        label_flat=[]
        for idx,i in enumerate(this_set):
            for jdx,j in enumerate(i):
                for kdx,k in enumerate(j):
                    label_flat.append(curve_label[idx][jdx][kdx])
                    set_flat.append(k[:])
                    #get next two neighbors
                    for m in range(self.neigh):
                        index=(kdx+m+1)%len(j)
                        set_flat[-1].extend(j[index][2:])
                        #just ignore the ctrl pts
        #same linear on all the curves
        #make train_flat torch tensor
        

        torch_set_flat=torch.FloatTensor(set_flat)#[340, 32]
        embed_len=8+(self.neigh)*6 #32
#         test=nn.Linear(embed_len,24)#32x24
        curve_layer1=self.curve_lv1(torch_set_flat)#340x24
        curve_layer1_act=self.activation(curve_layer1)#340x24
        
#         test2=nn.Linear(24,12)
        curve_layer2=self.curve_lv2(curve_layer1_act)#340x12
        curve_layer2_act=self.activation(curve_layer2)#340x12
        ''''''
        curve_layer2_norm=self.norm_curve(curve_layer2_act)
        ''''''
        #mean pool curves in same pool

        group_count=0
        group_sizes=[] #[[0:3],[3:10]]
        group_range=[] #[[0,111],[111,141]...[311,340]]
        idx_start=0
        for idx in range(len(label_flat)-1):
            if label_flat[idx][0]!=label_flat[idx+1][0]:#change picture
                group_sizes.append([group_count,group_count+label_flat[idx][1]+1])
                group_count+=label_flat[idx][1]+1

            if label_flat[idx][1]!=label_flat[idx+1][1]:#change group
                group_range.append([idx_start,idx])

                idx_start=idx

        #and the last picture
        group_sizes.append([group_count,group_count+label_flat[-1][1]+1])
        group_count+=label_flat[-1][1]+1 #10
        group_range.append([idx_start,len(label_flat)])
  
        groups_layer1=torch.zeros(group_count,12)

        for idx,i in enumerate(group_range):
            start_idx=group_range[idx][0]
            end_idx=group_range[idx][1]

            groups_layer1[idx]=torch.mean(curve_layer2_norm[start_idx:end_idx],axis=0)#340x12->10x12
            
        # group_layer1:10x12

        #apply distance matrix, and cat the result.
        # make sum group 10x12->(mxnx5)->2x12

        #just look the first group 2x12
        sum_pic=torch.zeros(self.batch_size,self.group_level_layers*12)
        for idx,i in enumerate(sum_pic):#a picture
            start=group_sizes[idx][0]
            end=group_sizes[idx][1]

            dist_now=torch.FloatTensor(dist_mat[idx])

            cor_now=dist_now[:,0,:]#3x5, 7x5
            cor_adapt=self.activation(self.dist_mlp_lv1(cor_now))

            group_layer1=groups_layer1[start:end]
            picture_level1=torch.mean(group_layer1,axis=0)
            group_layer2=cor_adapt*group_layer1#3x12, 3x12->3x12
            picture_level2=torch.mean(group_layer2,axis=0)#3x12->1x12
            group_layer3=cor_adapt*group_layer2#3x12, 3x12->3x12
            picture_level3=torch.mean(group_layer3,axis=0)#3x12->1x12


            L1=torch.unsqueeze(picture_level1,dim=0)
            L2=torch.unsqueeze(picture_level2,dim=0)
            L3=torch.unsqueeze(picture_level3,dim=0)
            sum_pic[idx]=torch.cat((L1,L2,L3),1)#1x12->1x36    
        
        sum_norm=self.norm_group(sum_pic)
        #go through the last linear then the label!
        pred_level1=self.activation(self.picture_lv1(sum_norm))#2x36->2x18
        pred_level2=self.activation(self.picture_lv2(pred_level1))#2x18->2x8
        pred_level3=nn.Softmax(dim=1)(self.picture_lv3(pred_level2))#2x8->2x2
        
        return pred_level2, pred_level3
    
def onehot2class (label,max=2):
    onehot_label=np.zeros((len(label),max))
    i=0
    while i<len(label):
        onehot_label[i][int(label[i])]=1
        i+=1
    return onehot_label

def binary_acc(batch_pred, label):
    pred=batch_pred.max(axis=1).indices.detach().numpy()
    true=torch.FloatTensor(label).max(axis=1).indices.detach().numpy()
    acc=accuracy_score(true, pred, normalize=True)
    return acc
import time
import math
def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

