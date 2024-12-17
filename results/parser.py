import sys
if(len(sys.argv)>1):
    file_base = sys.argv[-1]
else:
    file_base ='./Inceptionv3/sim_input/1024'

ts = open(file_base+'Tensor.info','r').read().strip().split('\n')
ks = open(file_base+'Kernel.info').read().strip().split('\n')

t_info = {}
k_info = {}

for i in ts:
    tid, tmem, tglob = i.split()
    t_info[(tid)] = {'mem':int(tmem),'tglob':tglob,'live':{'start':None,'end':None}}

for i in ks:
    temp =''
    if(i[-1]!=']'):
        temp = i.split()[-1]
        i= ' '.join(i.split()[:-1])
    num, name, exec_time, ins, outs = i.split()
    num = int(num)
    if(ins != '[]'):
        ins = ins[1:-1].split(',')
    else:
        ins = []
    outs = outs[1:-1].split(',')
    in_outs = ins+outs
    if(temp):
        if(t_info[temp]['live']['start'] == None):
            t_info[temp]['live']['start'] = num
        t_info[temp]['live']['end'] = num
    for o1 in in_outs:
        if (t_info[o1]['live']['start'] == None):
            t_info[o1]['live']['start'] = num
    if(in_outs):
        for i1 in in_outs:
            t_info[i1]['live']['end'] = num

    k_info[num]={'time':exec_time}

max_mem = 0
for k in k_info:
    p_mem = 0
    for t in t_info:
        if(t_info[t]['tglob']=='true'):
            p_mem+=t_info[t]['mem']
        # if(t_info[t]['live']['end'] ==None):
        #     continue
        # if (t_info[t]['live']['start'] == None):
        #     continue
        if(k in range(t_info[t]['live']['start'],(t_info[t]['live']['end']+1))):
            p_mem+=t_info[t]['mem']
    k_info[k]['mem'] = p_mem
    max_mem = max(max_mem,p_mem)
    # if(max_mem == p_mem):
    #     print(k)
print(file_base,max_mem/pow(2,30))
# Generating prefetch information...
prefetch_={}
for t in t_info:
    k = t_info[t]['live']['start']
    if((k in prefetch_)==0):
        prefetch_[k]=[]
    if(t_info[t]['tglob']=='false'):
        prefetch_[k].append(t)

with open('x.prefetch','w') as wf:
    for i in sorted(prefetch_):
        wf.write((str(i)+ ' '+prefetch_[i][0])+'\n')

