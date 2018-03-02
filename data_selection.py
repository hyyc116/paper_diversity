#coding:utf-8
'''
    
    select papers of a specific domain from mag.
    
    Input: All papers of  MAG

    Output: papers of specific papers

'''
import sys
import os
import json
from basic_config import *

def chose_paper_of_field(path,field):
    if not path.endswith('/'):
        path = path+"/"
    papers = []
    paper_ids = []
    ref_paper_ids = []
    ## 1. get all ids of this field
    ## 2. get the references of these papers
    log_progress=0
    files = os.listdir(path)
    for f in files:
        fpath = path+f
        log_progress+=1
        logging.info('progress {:}/{:}, Number of paper in {:}:{:} ....'.format(log_progress,len(files),field,len(paper_ids)))

        if len(paper_ids)%10000==1:
            open('{:}-papers.txt'.format(field),'w+').write('\n'.join(papers))
            papers = []

        for line in open(fpath):
            line = line.strip()
            pObj = json.loads(line)

            if 'fos' not in pObj.keys() or 'lang' not in pObj.keys() or 'references' not in pObj.keys():
                continue
            fos = ','.join(pObj['fos']).lower()

            if field not in fos:
                continue
            lang = pObj['lang']
            if lang!='en':
                continue

            references = pObj['references']
            pid = pObj['id']

            papers.append(line)
            paper_ids.append(pid)
            for ref_id in references:
                ref_paper_ids.append(ref_id)

    open('{:}-papers.txt'.format(field),'w+').write('\n'.join(papers))
    logging.info('Number of paper in this field:{:}'.format(len(paper_ids)))

    ref_paper_ids=set(ref_paper_ids)
    logging.info('Number of references paper in this field:{:}'.format(len(ref_paper_ids)))
    open("{:}-ref-ids.txt".format(field),'w').write('\n'.join(ref_paper_ids))

def out_refs(path,ref_ids,field):
    ref_paper_ids = set([line.strip() for line in open(ref_ids)])
    ref_papers = []
    parsed_ids = []
    outfiles =  open('{:}-ref-papers.txt'.format(field),'w+')
    for i,f in enumerate(os.listdir(path)):
        fpath = path+f
        logging.info('progress: {:}/167 ...'.format(i))
        
        for line in open(fpath):
            line = line.strip()
            pObj = json.loads(line)
            pid = pObj['id']
            if pid in ref_paper_ids:
                ref_papers.append(line)
                parsed_ids.append(pid)

                if len(parsed_ids)%100000==0:
                    logging.info('Number of reference papers in this field:{:}'.format(len(parsed_ids)))
                    outfiles.write('\n'.join(ref_papers))
                    ref_papers=[]
    
    outfiles.write('\n'.join(ref_papers))
    logging.info('Number of reference papers in this field:{:}/{:}'.format(len(parsed_ids),len(ref_paper_ids)))



if __name__ == '__main__':
    # chose_paper_of_field(sys.argv[1],sys.argv[2])
    out_refs(sys.argv[1],sys.argv[2],sys.argv[3])
