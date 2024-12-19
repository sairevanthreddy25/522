import sys
if(len(sys.argv)>1):
    file_base = sys.argv[-1]
else:
    file_base ='./Inceptionv3/sim_input/512'

import matplotlib.pyplot as plt



ts = open(file_base+'Tensor.info','r').read().strip().split('\n')
ks = open(file_base+'Kernel.info').read().strip().split('\n')

t_info = {}
k_info = {}

for i in ts:
    tid, tmem, tglob = i.split()
    t_info[(tid)] = {'mem':int(tmem),'tglob':tglob,'live':{'start':None,'end':None,'active':0}}


accum_time = 0
ideal_max=0
for i in ks:
    temp =''
    if(i[-1]!=']'):
        temp = i.split()[-1]
        i= ' '.join(i.split()[:-1])
    num, name, exec_time, ins, outs = i.split()
    exec_time=float(exec_time)
    num = int(num)
    if(ins != '[]'):
        ins = ins[1:-1].split(',')
    else:
        ins = []
    outs = outs[1:-1].split(',')
    in_outs = ins+outs
    k_mem = 0
    if(temp):
        if(t_info[temp]['live']['start'] == None):
            t_info[temp]['live']['start'] = accum_time
        t_info[temp]['live']['end'] = accum_time+exec_time
        t_info[temp]['live']['active'] = t_info[temp]['live']['active']+exec_time
        k_mem+=t_info[temp]['mem']
    for o1 in in_outs:
        if (t_info[o1]['live']['start'] == None):
            t_info[o1]['live']['start'] = accum_time
            t_info[o1]['live']['active'] = t_info[o1]['live']['active'] + exec_time
            k_mem += t_info[o1]['mem']
    if(in_outs):
        for i1 in in_outs:
            t_info[i1]['live']['end'] = accum_time+exec_time
    ideal_max= max(ideal_max,k_mem)
    accum_time+=exec_time
    k_info[num]={'time':exec_time}
max_mem = 0
accum_time=0
for k in k_info:
    p_mem = 0
    for t in t_info:
        if(t_info[t]['tglob']=='true'):
            p_mem+=t_info[t]['mem']
        # if(t_info[t]['live']['end'] ==None):
        #     continue
        # if (t_info[t]['live']['start'] == None):
        #     continue
        if((accum_time >=t_info[t]['live']['start']) and (accum_time<=t_info[t]['live']['end'])):
            p_mem+=t_info[t]['mem']
    k_info[k]['mem'] = p_mem
    max_mem = max(max_mem,p_mem)
    accum_time+=k_info[k]['time']


# Generating prefetch information...
prefetch_={}
for t in t_info:
    k = t_info[t]['live']['start']
    if((k in prefetch_)==0):
        prefetch_[k]=[]
    if(t_info[t]['tglob']=='false'):
        prefetch_[k].append(t)

with open(file_base+'.hint','w') as wf:
    for i in sorted(prefetch_):
        wf.write((str(i)+ ' '+prefetch_[i][0])+'\n')

