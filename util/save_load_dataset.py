#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
def dump_item(this_item, path):
    open_file = open(path, "wb")
    pickle.dump(this_item, open_file)
    open_file.close()
    
def load_item(path):
    open_file = open(path, "rb")
    this_item=pickle.load(open_file)
    open_file.close()
    return this_item


# In[ ]:


# create label of the item, but save as a different file
import os
def curve_labeling(this_item, temp_seed=0):
    #deep copy a item
    temp_path="temp%s.pkl"%temp_seed
    dump_item(this_item,temp_path)
    curve_label=load_item(temp_path)
    
    for idx,i in enumerate(this_item):#pic_num
        for jdx,j in enumerate(i):#group_num
            for kdx,k in enumerate(j):#curve_num
                curve_label[idx][jdx][kdx]=[idx, jdx, kdx]
    os.remove(temp_path)
    return curve_label
#     dump_item(curve_labels, curve_label_path)
#     os.remove("temp.pkl")


# In[ ]:


#label the item
import os
def labeling(this_item, labeled_item_path):
    #deep copy a item
    temp_path="temp.pkl"
    dump_item(this_item,temp_path)
    labeled_item=load_item(temp_path)
    
    for idx,i in enumerate(this_item):#pic_num
        for jdx,j in enumerate(i):#group_num
            for kdx,k in enumerate(j):#curve_num
                labeled_item[idx][jdx][kdx].insert(0,kdx)
                labeled_item[idx][jdx][kdx].insert(0,jdx)
                labeled_item[idx][jdx][kdx].insert(0,idx)
    dump_item(labeled_item, labeled_item_path)
    os.remove("temp.pkl")


# In[ ]:


def save_set(set_name, curve_label_name, label_name, dist_mat_name,
            set_item, set_label, set_cor_item):
#     labeling(set_item, set_name)
    curve_label=curve_labeling(set_item)
    dump_item(curve_label, curve_label_name)
    dump_item(set_item, set_name)
    dump_item(set_label, label_name)
    dump_item(set_cor_item, dist_mat_name)


# In[ ]:


def save_dataset(train_set_name, train_curve_label_name, train_label_name, train_dist_mat_name,
                 test_set_name, test_curve_label_name, test_label_name, test_dist_mat_name,
                 train_item, train_label, train_cor_item,
                 test_item, test_label, test_cor_item):
    
    save_set(train_set_name, train_curve_label_name, train_label_name, train_dist_mat_name,
             train_item, train_label, train_cor_item)
    save_set(test_set_name, test_curve_label_name, test_label_name, test_dist_mat_name,
             test_item, test_label, test_cor_item)
    
#     labeling(train_item, train_set_name)
#     dump_item(train_label, train_label_name)
#     dump_item(train_cor_item, train_dist_mat_name)
#     labeling(test_item, test_set_name)
#     dump_item(test_label, test_label_name)
#     dump_item(test_cor_item, test_dist_mat_name)


# In[ ]:


def load_set(set_name, curve_label_name, label_name, dist_mat_name):
    this_set=load_item(set_name)
    curve_label=load_item(curve_label_name)
    label=load_item(label_name)
    dist_mat=load_item(dist_mat_name)
    return this_set, curve_label, label, dist_mat


# In[ ]:


def load_dataset(train_set_name, train_curve_label_name, train_label_name, train_dist_mat_name,
                 test_set_name, test_curve_label_name, test_label_name, test_dist_mat_name):
    train_set, train_curve_label, train_label, train_dist_mat=    load_set(train_set_name, train_curve_label_name, train_label_name, train_dist_mat_name)
    test_set, test_curve_label, test_label, test_dist_mat=    load_set(test_set_name, test_curve_label_name, test_label_name, test_dist_mat_name)
#     train_set=load_item(train_set_name)
#     train_label=load_item(train_label_name)
#     train_dist_mat=load_item(train_dist_mat_name)
#     test_set=load_item(test_set_name)
#     test_label=load_item(test_label_name)
#     test_dist_mat=load_item(test_dist_mat_name)
    return train_set, train_curve_label, train_label, train_dist_mat,           test_set, test_curve_label, test_label, test_dist_mat

