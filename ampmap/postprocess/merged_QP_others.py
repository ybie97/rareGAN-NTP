import pandas as pd
import numpy as np
import itertools,os
import networkx as nx
from itertools import permutations 
import seaborn as sns
# from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics import pairwise_distances
from sklearn.cluster import AgglomerativeClustering
from ast import literal_eval

def reduced_QPspace(proto_name,flag=0):
    df=pd.read_csv(proto_name+'/all_QPS.csv')

    df.sort_values(by=['amp_fac'], ascending=False,inplace=True)
    print(df)
    if(flag==1):
        df = df.query('max_amp >=10')
        app='_max'
    else:
        df = df.query('amp_fac >=10')
        app='_median'

    print("PRINTING: ",df)
    if 'host' in df.columns.values:
        # df = df.applymap(str)

        del df['host']
    # del df['url']
    newdf=df.copy()
    del newdf['amp_fac']
    del newdf['min_amp']
    del newdf['max_amp']
    del newdf['count_amp']
    amps=df['amp_fac'].values
    print("amps",amps.shape)
    newdf = newdf.applymap(str)
    arr =newdf.values
    print(arr.shape,arr)
    uniques = np.unique(arr)
    X = np.searchsorted(uniques, arr)

    avg_dist = pairwise_distances(X, X, metric='hamming')
    print(avg_dist.shape)
    print(avg_dist[0,:])
    print(arr[0,:])
    print(arr[1,:])
    merge_thr = 1 / arr.shape[1]
    print("merge thresh",merge_thr)
    # n_clusters=10
    # model = AgglomerativeClustering(n_clusters=n_clusters,linkage="average", affinity='hamming')
    # model.fit(arr)
    # print(model)
    neigh_AFthresh= 10000
    new_signatures=[]
    ign_list=[]
    for i in range(avg_dist.shape[0]):
        if i in ign_list:
            continue
        currow= avg_dist[i,:]
        my_AF=amps[i]
        p1=np.where(currow<=merge_thr)[0]
        neigh_AF=amps[p1]
        possible_inds=np.where(np.abs(neigh_AF-my_AF)<=neigh_AFthresh)[0]
        valid_inds = p1[possible_inds]
        valid_inds =np.setdiff1d(valid_inds,ign_list)
        ign_list.extend(list(valid_inds))
        valid_AFS=neigh_AF[possible_inds]
        rows= arr[valid_inds,:]    
        newrow=[]
        for k in range(rows.shape[1]):
            curvals=list(np.unique(rows[:,k]))
            newrow.append(curvals)
        newrow.append(np.mean(valid_AFS))
        new_signatures.append(newrow)
    print(len(new_signatures),new_signatures[0])
    cols=df.columns.values[0:-3]
    print(cols)
    new_sigs=np.array(new_signatures)
    new_sigDF=pd.DataFrame(new_sigs,columns=cols)
    # new_sigDF
    new_sigDF.sort_values(by=['amp_fac'], ascending=False,inplace=True)
    print(new_sigDF.shape)
    new_sigDF.to_csv(proto_name+'/QPS_merged'+app+'.csv',index=False)
    print(new_sigDF)
    # print()


def DAG_setcover(proto_name,flag=0):

    df=pd.read_csv(proto_name+'/all_QPS.csv')
    df.sort_values(by=['amp_fac'], ascending=False,inplace=True)
    print(df.head(),df.shape,flag)
    # ()+1
    # df = df.query('amp_fac >=10')
    if(flag==1):
        df = df.query('max_amp >=10')
        app='_max'
    else:
        df = df.query('amp_fac >=10')
        app='_median'
    # del df['url']
    print(df.head(),df.shape,flag)
    print(df)
    save_file = proto_name+'/DAG_QPS_depth'+app +'.npy'
    if os.path.exists(save_file):
        return 0
    if df.shape[0]==0:
        return 0
    # ()+1
    del df['min_amp']
    del df['max_amp']
    del df['count_amp']


    ## Manually removing 
    # del df['err']
    # del df['mbz']
    # del df['seq']
    # del df['data_item_size']
    # del df['response']
    # del df['data']
    # del df['more']
    # del df['mode']


    ##
    # del df['rcode']
    print(df.head(),df.shape)
    df = df.drop_duplicates(subset=df.columns.difference(['amp_fac']))
    print(df.head(),df.shape)
    cols=df.columns.values
    amps = df['amp_fac'].values
    del df['amp_fac']

    leafs = df.values
    print(leafs.shape)
    print(leafs.shape,leafs,cols,amps.shape)

    C = leafs

    # amps = leafs[:,11]




    print(leafs[0,:],C[0,:],amps)
    # ()+1

    # ()+1
    # for item in leafs.iter
    all_nodes  = []
    node_info={}
    def get_node(ll):
        return str(list(ll))
    to_iterate = C

    G = nx.DiGraph()
    bigconnect_list={}
    # bignames_list=[]
    lknodes={}
    for k2 in range(leafs.shape[1]):
        newlist=[]
        strlist=[]
        print("TO ITer",to_iterate.shape,len(list(G._node)))
        for i in range(to_iterate.shape[0]):
            curleaf=to_iterate[i,:]
            p_node = get_node(curleaf)
            if  not (p_node in G):
                G.add_node(p_node,connect = str(i),name=list(curleaf))            
            childrens  = []
            for k in range(to_iterate.shape[1]):
                newrow=curleaf.copy()
                newrow[k]=-1
                curnode=get_node(newrow)
                if curnode in G:
                    G.add_edge(curnode,p_node)
                    G._node[curnode]['connect']+=','+G._node[p_node]['connect']

                else:
                    newlist.append(newrow)
                    strlist.append(curnode)
                    G.add_node(curnode,connect=G._node[p_node]['connect'],name=list(newrow))
                    G.add_edge(curnode,p_node)
                bigconnect_list[curnode] =  G._node[curnode]['connect']
        lknodes[k2] = strlist
        newlist=np.array(newlist)
        to_iterate=newlist
        print("Next Level: ",k2,len(node_info.keys()),newlist.shape)
        if k2 >0:
            for val in strlist:
                curconn=G._node[val]['connect']
                llb=curconn.split(",")
                newllb=list(set(llb))
                newllb.sort()
                s = ",".join(newllb)             
                G._node[val]['connect'] = s
        if not strlist:
            break

    nodes=list(G._node)
    cnt =1
    for val in nodes:
        curconn=G._node[val]['connect']
        llb=curconn.split(",")
        newllb=list(set(llb))
        newllb.sort()
        s = ",".join(newllb)             
        G._node[val]['connect'] = s
        cnt+=1
    roots = (v for v, d in G.in_degree() if d == 0)
    leaves = (v for v, d in G.out_degree() if d == 0)
    leaf_count=len(list(leaves))
    print(lknodes.keys(),C.shape)
    maxDepth=C.shape[1]
    DAG_QPS={}
    temp=[]
    for currow in C:
        nr=[]
        for k1 in range(C.shape[1]):
            nr.append([currow[k1]])
        temp.append(nr)
        # print(currow,nr)
        # ()+1
    d1=pd.DataFrame(temp,columns=cols[:-1])
    d1 = d1.applymap(str)
    DAG_QPS[0]=d1
    # ()+1
    for depth,values in lknodes.items():
    #     print(depth)
        subsets=[]
        subset_map=[]
        name_nodes=[]
        for eachnode in values:
            c_name=eachnode
            current_child = G._node[c_name]['connect'].split(',')
            current_num = set([ int(x) for x in current_child ])
            name_nodes.append(c_name)
            subsets.append(current_num)

        universe = set(range(0, leaf_count))
        covered = set()
        cover = []
        set_KCover=[]
        idx_covered=[]
        if len(values)==0:
            continue
        while covered != universe:
            print("HERE : ",len(subsets),len(covered),len(values))
            subset = max(subsets, key=lambda s: len(s - covered))
            index=subsets.index(subset)
            cover.append(subset)
            covered |= subset

            print(name_nodes[index])
            set_KCover.append(literal_eval(name_nodes[index]))
            diff = universe-covered
            idx_covered.append(subset)
        print("\n\n\n\n\n\t",depth , leaf_count,len(cover),"\n")
        print(depth,subsets,values)
        # ()+1
        set_KCover=np.array(set_KCover)
    #     print(set_KCover,set_KCover.shape)
        new_SetK=[]
        for i in range(set_KCover.shape[0]):
            print(i,set_KCover)

            newrow=[[i] for i in set_KCover[i,:]]
            new_SetK.append(newrow)
    #         break

    #     ()+1
        df=pd.DataFrame(new_SetK,columns=cols[:-1])
        df = df.applymap(str)
        DAG_QPS[depth+1]=df
        print(df)

    np.save(save_file,DAG_QPS)
 

# proto_name='out_DNS_10k_query_searchout_May11dns_sec'
# dnssec = 1

# reduced_QPspace(proto_name,0)
# reduced_QPspace(proto_name,1)
# DAG_setcover(proto_name,1)

# DAG_setcover(proto_name,0)




