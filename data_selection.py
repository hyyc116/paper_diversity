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
            open('data/{:}-papers.txt'.format(field),'w+').write('\n'.join(papers))
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

    open('data/{:}-papers.txt'.format(field),'w+').write('\n'.join(papers))
    logging.info('Number of paper in this field:{:}'.format(len(paper_ids)))

    ref_paper_ids=set(ref_paper_ids)
    logging.info('Number of references paper in this field:{:}'.format(len(ref_paper_ids)))
    open("data/{:}-ref-ids.txt".format(field),'w').write('\n'.join(ref_paper_ids))

def out_refs(path,ref_ids,field):
    ref_paper_ids = set([line.strip() for line in open(ref_ids)])
    ref_papers = []
    parsed_ids = []
    outfiles =  open('data/{:}-ref-papers.txt'.format(field),'w+')
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

                if len(parsed_ids)%10000==0:
                    logging.info('Number of reference papers in this field:{:}'.format(len(parsed_ids)))
                    outfiles.write('\n'.join(ref_papers))
                    ref_papers=[]
    
    outfiles.write('\n'.join(ref_papers))
    logging.info('Number of reference papers in this field:{:}/{:}'.format(len(parsed_ids),len(ref_paper_ids)))


def gen_paper_attrs(papers):
    '''
        draw paper distribution over year of papers.
        draw citation distribution of papers

    '''
    pid_attrs=defaultdict(dict)
    progress=0
    for line in open(papers):
        if progress%100000==0:
            logging.info('paper progress {:} ...'.format(progress))

        progress+=1

        line = line.strip()
        pObj = json.loads(line)
        pid = pObj['id']
        year = pObj.get('year',-1)
        refs =pObj.get('references',[])
        ## if there is no n_citation keywords, return 0
        n_citation = pObj.get('n_citation',0)
        ## fos
        fos = pObj.get('fos',[])
        pid_attrs[pid]['year']=year
        pid_attrs[pid]['fos']=fos
        pid_attrs[pid]['refs']=refs
        pid_attrs[pid]['n_citation']=n_citation

    open('data/paper_attrs.json','w').write(json.dumps(pid_attrs))

def gen_ref_paper_attrs(ref_papers):
    ref_pid_attrs=defaultdict(dict)
    progress=0
    attr_index=1
    outfiles = open('data/ref_paper_attrs.json','w+')
    for line in open(ref_papers):
        if progress%10000==0:
            logging.info('ref paper progress {:} ...'.format(progress))
        progress+=1

        if progress%100000==0:
            outfiles.write(json.dumps(ref_pid_attrs)+"\n")
            logging.info(' saved {:} papers to data/ref_paper_attrs.json.'.format(progress))
            ref_pid_attrs=defaultdict(dict)
            attr_index+=1

        line = line.strip().encode('utf-8',errors='ignore')
        try:
            pObj = json.loads(line)
        except:
            print line
            continue
        pid = pObj['id']
        year = pObj.get('year',-1)
        refs =pObj.get('references',[])
        ## if there is no n_citation keywords, return 0
        n_citation = pObj.get('n_citation',0)
        ## fos
        fos = pObj.get('fos',[])

        ref_pid_attrs[pid]['year']=year
        ref_pid_attrs[pid]['fos']=fos
        ref_pid_attrs[pid]['refs']=refs
        ref_pid_attrs[pid]['n_citation']=n_citation

    outfiles.write(json.dumps(ref_pid_attrs)+"\n")

if __name__ == '__main__':

    tag = sys.argv[1]

    if tag=='select_papers':

        ### extract papers of specific field
        ''' path-to-mag physics '''
        mag_dir_path = sys.argv[2]
        field = sys.argv[3]
        chose_paper_of_field(mag_dir_path,field)

    elif tag=='out_ref_papers':

        ### extract reference papers of specific field
        ''' path-to-mag data/physics-ref-ids.txt physics'''
        mag_dir_path = sys.argv[2]
        ref_ids_path = sys.argv[3]
        field = sys.argv[4]
        out_refs(mag_dir_path,ref_ids_path,field)

    elif tag=='out_paper_attrs':

        ### extract json data
        ''' path-to-physics-papers.txt '''
        path = sys.argv[2]
        gen_paper_attrs(path)

    elif tag=='out_ref_attrs':
        ### extract json data
        '''  path to physics-ref-papers.txt'''
        path = sys.argv[2]
        gen_ref_paper_attrs(path)

    else:
        logging.info('No such action tag.')


















