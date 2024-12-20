cmd_a =''
cmd_b = './sim ./configs/Inceptionv3_1024.config'
lines = open('a.sh','r').read().strip().split('\n')
dest = []
for i in lines:
    name = i.split('/')[1]
    num = i.split('/')[-1]
    dest.append((name, num))

dest = sorted(dest, key=lambda x:int(x[1]))

for i in dest:
    name,num = i
    print(cmd_b.replace('Inceptionv3', name).replace('1024', num))
    print('echo '+'\"'+str(name)+'_'+str(num)+'\" > status.txt')
    print(cmd_b.replace('Inceptionv3',name).replace('1024',num+'_hints_on'))
    print('echo ' + '\"' + str(name) + '_' + str(num) + '_hints" > status.txt')