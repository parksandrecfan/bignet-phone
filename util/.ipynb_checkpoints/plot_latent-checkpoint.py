#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#the step to extract letent vector should be outside the plot
from .bignet1 import *
import util as u
def get_latent(data_set, data_curve_label, data_dist_mat, model_path, mode="norm"):
    
    batch_size=len(data_set)

    evaluation_net= bignet1(batch_size=batch_size)
    
    
    evaluation_net.load_state_dict(torch.load(model_path))
    evaluation_net.eval()
    latent_vec, _=evaluation_net(data_set,data_curve_label,data_dist_mat)
    return latent_vec.detach().numpy()


# In[6]:


from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def vec2plot(latent_vec, mode="tsne", dimension=2):
    if mode=="tsne":
        model = TSNE(n_components=dimension, random_state=0)
    if mode=="pca":
        model = PCA(n_components=dimension)

    vector2plot=model.fit_transform(latent_vec) 
    return vector2plot


# In[ ]:


def plot_vec(vector, threshold=None, feature=None, angles=(160,9,70)):
    dimension=vector.shape[1]
    if dimension==2:
        plt.scatter(vector[:threshold,0], vector[:threshold,1],                    color='red', s=8)
        plt.scatter(vector[threshold:,0], vector[threshold:,1],                    color='blue', s=8)
    elif dimension==3:
        azim, dist, elev=angles
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(projection='3d')
#         ax.title.set_text(mode)
        ax.scatter(vector[:threshold,0], vector[:threshold,1]                   , vector[:threshold,2], color='red', s=8)
        ax.scatter(vector[threshold:,0], vector[threshold:,1]                   , vector[threshold:,2], color='blue', s=8)
        ax.azim = azim
        ax.dist = dist
        ax.elev = elev


# In[ ]:


def latent2plot(latent_vec, mode="tsne", dimension=2, threshold=None, angles=(160,9,70)):
    vector=vec2plot(latent_vec, mode=mode, dimension=dimension)
    if threshold==None:
        threshold=int(vector.shape[0]/2)
    plot_vec(vector=vector, threshold=threshold, angles=angles)


# In[ ]:


import numpy as np
def plot_separation(latent_vec, phone_rec, names, dimension=2, phone="iphone", mode="tsne", folder="tsne/normalized_separation/2d", normalized=0, angles=(160,9,70)):
    plt_vec=vec2plot(latent_vec, mode=mode, dimension=dimension)
    
    if phone=="iphone":
        shift=0
    if phone=="samsung":
        shift=10000

    azim, dist, elev=angles
    for count,feature in enumerate(phone_rec):
        if type(feature).__name__!='float':
            if normalized==1 and             names[count]!='iphone_lens_random' and            names[count]!='iphone_notch_random' and            names[count]!='samsung_camera_ct':
                feature=feature/phone_rec[0]

            feat_min=feature.min()
            feat_max=feature.max()
            feat_range=feat_max-feat_min

            feat_0=feat_min
            feat_1=feat_min+feat_range*0.25
            feat_2=feat_min+feat_range*0.50
            feat_3=feat_min+feat_range*0.75
            feat_4=feat_max

            color_list=[]

            for idx,i in enumerate(latent_vec):
                if idx in np.where((feature>=feat_0)*(feature<=feat_1))[1]-shift-9000:
                    color_list.append([1, 1, 0])
                elif idx in np.where((feature>=feat_1)*(feature<=feat_2))[1]-shift-9000:
                    color_list.append([1,0.5, 0])
                elif idx in np.where((feature>=feat_2)*(feature<=feat_3))[1]-shift-9000:
                    color_list.append([0.7,0.5, 0.4])
                elif idx in np.where((feature>=feat_3)*(feature<=feat_4))[1]-shift-9000:
                    color_list.append([0,0, 0])
                else:
                    color_list.append([0,0, 1])

            if dimension==2:
                
                plt.figure(figsize=(12, 12))
                plt.title(names[count])
                plt.scatter(plt_vec[:,0], plt_vec[:,1],                            color=color_list, s=8)
            if dimension==3:
                
                fig = plt.figure(figsize=(12, 12))

                ax = fig.add_subplot(projection='3d')
                ax.title.set_text(names[count])
                ax.scatter(plt_vec[:,0], plt_vec[:,1]                           , plt_vec[:,2], color=color_list, s=8)
                ax.azim = azim
                ax.dist = dist
                ax.elev = elev

            plt.savefig("%s/%s"%(folder,names[count]))
            plt.close()

