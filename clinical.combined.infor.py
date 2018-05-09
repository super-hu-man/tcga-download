import xml.etree.ElementTree as ET
import os,sys

path = '/public/ptbus/home/huchao/data/clinical.files.all'
files = os.listdir(path)

def run(element):
    if len(element)==0 :
        #print element.tag,'----',element.text
        index = re.match('{.*}(.*)',element.tag).group(1)
        if index in info.keys() :
            info[index].append(element.text)
        if 'gender' in index :
            info['gender'] = element.text
    else :
        for i in range(len(element)) :
            child = element[i]
            run(child)

out = open('infomation.txt',w)
out.write('sample\tdays\tvital_status\tgender\n')

for file in files :
    tree = ET.parse('/'.join((path,file)))
    root = tree.getroot()
    barcode = re.match('.*(TCGA.*).xml',file).group(1)
    info = {}
    info['days_to_last_followup'] = []
    info['days_to_death'] = []
    info['vital_status'] = []
    run(root)
    gender = info['gender']
    if 'Dead' in info['vital_status'] : status = 'Dead'
    else : status = 'Alive'
    list = dict['days_to_last_followup']+dict['days_to_death']
    days = 0
    for i in list :
        if str(i).isdigit() : days = max(days,int(i))
    out.write('\t'.join(barcode,days,status,gender)+'\n')

print 'done'
