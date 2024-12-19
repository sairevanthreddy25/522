cmd_a =''
cmd_b = './sim ./configs/Inceptionv3/sim-1024-ideal.config'
lines = open('a.sh','r').read().strip().split('\n')
for i in lines:
    name = i.split('/')[1]
    num = i.split('/')[-1]
    print(i)
    print(cmd_b.replace('Inceptionv3',name).replace('1024',num))