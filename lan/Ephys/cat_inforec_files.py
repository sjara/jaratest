import os
import re
#import fileinput

animal = 'adap012'
directory = '/home/languo/src/jaratest/lan/Ephys/'
outfilePath = os.path.join(directory, '{}_inforec.py'.format(animal))

if not os.path.exists(outfilePath):
    fileNames = sorted([filename for filename in os.listdir(directory) if (filename.endswith('.py') and (animal in filename))])

    outFile = open(outfilePath, 'a')

    for file in fileNames:
        with open(file, 'r') as f:
            indList=[]
            expList=[]
            content = f.readlines()
            cat = [line for line in content if (('exp' in line) or ('add_session' in line))]
            for ind, line in enumerate(cat):
                m = re.search('^exp[0-9]*', line)
                if m:   
                    indList.append(ind)
                    expList.append(m.group(0))
            for inc,ind in enumerate(indList):
                cat.insert(ind+1+inc, 'experiments.append({})\n'.format(expList[inc]))

            cat = ''.join(cat)
            outFile.write(cat)
            outFile.write('\n')
    outFile.close()

else:
    #with open(outFile, 'r+') as outFileNew:
    #fileinput.FileInput(outfilePath, mode='r+',inplace=True, backup='.bak') 
    with open(outfilePath, 'r') as file:
        filedata = file.read()
    
    filedata = filedata.replace("animalName='{}'".formate(animal), "subject")
    filedata = filedata.replace("experimenter='lan'", "brainarea='rightAStr'")
    filedata = filedata.replace("defaultParadigm='laser_tuning_curve'", "info=''")
    filedata = filedata.replace("sessionTypes['nb']","'noiseburst'")
    filedata = filedata.replace("sessionTypes['tc']","'tc'")
    filedata = filedata.replace("sessionTypes['2afc']", "'behavior'")
    #if line.endswith("'noiseburst')") or line.endswith("'tc')") :
    filedata = filedata.replace("'noiseburst')", "'noiseburst', 'laser_tuning_curve')")
    filedata = filedata.replace("'tc')", "'tc', 'laser_tuning_curve')")

    filedata = "from jaratoolbox import celldatabase as cellDB\nsubject = '{}'\nexperiments = []\n".format(animal) + '\n' + filedata

    with open(outfilePath, 'w') as file:
        file.write(filedata)
