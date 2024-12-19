src = open('src/configs/example.config','r').read()

names = [['ResNet152', '1024'], ['ResNet152', '1536'], ['ResNet152', '1280'], ['ResNet152', '256'], ['ResNet152', '512'], ['ResNet152', '768'], ['VIT', '1024'], ['VIT', '1536'], ['VIT', '1280'], ['VIT', '256'], ['VIT', '512'], ['VIT', '768'], ['BERT', '1024'], ['BERT', '640'], ['BERT', '128'], ['BERT', '384'], ['BERT', '256'], ['BERT', '512'], ['BERT', '768'], ['SENet154', '1024'], ['SENet154', '256'], ['SENet154', '512'], ['SENet154', '768'], ['Inceptionv3', '1152'], ['Inceptionv3', '1024'], ['Inceptionv3', '1792'], ['Inceptionv3', '1536'], ['Inceptionv3', '1280'], ['Inceptionv3', '512'], ['Inceptionv3', '768']]

for i in names:
    dest = src.replace('Inceptionv3',i[0]).replace('1024',i[1]).replace('example','default')
    open('src/configs/'+'_'.join(i)+'.config','w').write(dest)
    dest = dest.replace('use_movement_hints      0','use_movement_hints      1').replace('default','hints_on')
    open('src/configs/'+'_'.join(i)+'_hints_on.config','w').write(dest)

