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

    ## 1. get all ids of papers in this field
    ## 2. get the all ids in these papers' reference list

    if not path.endswith('/'):
        path = path+"/"

    paper_ids = []
    ref_paper_ids = []
    
    log_progress=0
    files = os.listdir(path)
    # doc_type_dict=defaultdict(int)
    for f in files:
        fpath = path+f
        log_progress+=1
        logging.info('progress {:}/{:}, Number of paper in {:}:{:} ....'.format(log_progress,len(files),field,len(paper_ids)))

        for line in open(fpath):
            line = line.strip()
            pObj = json.loads(line)

            if 'fos' not in pObj.keys() or 'lang' not in pObj.keys() or 'references' not in pObj.keys():
                continue

            fos = ','.join(pObj['fos']).lower()

            if field not in fos:
                continue

            lang = pObj['lang']

            doc_type = pObj.get('doc_type','Other')

            print doc_type

            if lang!='en':
                continue

            if doc_type!='Conference' or doc_type!='Journal':
                continue

            references = pObj['references']
            pid = pObj['id']

            paper_ids.append(pid)
            for ref_id in references:
                ref_paper_ids.append(ref_id)

    logging.info('Number of paper in this field:{:}'.format(len(paper_ids)))
    open('data/{:}-paper-ids.txt'.format(field),'w').write('\n'.join(paper_ids))

    ref_paper_ids=set(ref_paper_ids)
    logging.info('Number of references paper in this field:{:}'.format(len(ref_paper_ids)))
    open("data/{:}-ref-ids.txt".format(field),'w').write('\n'.join(ref_paper_ids))



def citing_relation(path,paper_ids_path):

    paper_ids = set([line.strip() for line in open(paper_ids_path)])
    logging.info('length of paper ids:{:}'.format(len(paper_ids)))
    paper_citations=defaultdict(list)

    if not path.endswith('/'):
        path = path+"/"
    papers = []
    ref_paper_ids = []
    ## 1. get all ids of this field
    ## 2. get the references of these papers
    log_progress=0
    files = os.listdir(path)
    for f in files:
        fpath = path+f
        log_progress+=1
        logging.info('progress {:}/{:},length of paper citation:{:} ....'.format(log_progress,len(files),len(paper_citations.keys())))

        for line in open(fpath):
            line = line.strip()
            pObj = json.loads(line)

            if 'fos' not in pObj.keys() or 'lang' not in pObj.keys() or 'references' not in pObj.keys():
                continue

            for ref in pObj['references']:
                # print ref
                if ref in paper_ids:
                    paper_citations[ref].append('{:},{:}'.format(pObj['id'],pObj.get('year',-1)))


    open('data/paper_citation.json','w').write(json.dumps(paper_citations));

def out_papers(path,paper_ids_path,ref_ids_path,field):
    paper_ids = set([line.strip() for line in open(paper_ids_path)])
    ref_paper_ids = set([line.strip() for line in open(ref_ids_path)])
    paper_ids.extend(ref_paper_ids)
    all_ids = set(paper_ids)

    ref_papers = []
    parsed_ids = []
    outfiles =  open('data/{:}-all-papers.txt'.format(field),'w+')
    for i,f in enumerate(os.listdir(path)):
        fpath = path+f
        logging.info('progress: {:}/167 ...'.format(i))
        
        for line in open(fpath):
            line = line.strip()
            pObj = json.loads(line)
            pid = pObj['id']
            if pid in all_ids:
                ref_papers.append(line)
                parsed_ids.append(pid)

                if len(parsed_ids)%10000==0:
                    logging.info('Number of reference papers in this field:{:}'.format(len(parsed_ids)))
                    outfiles.write('\n'.join(ref_papers))
                    ref_papers=[]
    
    outfiles.write('\n'.join(ref_papers))
    logging.info('Number of reference papers in this field:{:}/{:}'.format(len(parsed_ids),len(ref_paper_ids)))


def export_paper_attrs(papers,paper_ids_path,ref_ids_path):
    '''
        draw paper distribution over year of papers.
        draw citation distribution of papers

    '''
    paper_ids = set([line.strip() for line in open(paper_ids_path)])
    ref_paper_ids = set([line.strip() for line in open(ref_ids_path)])

    pid_attrs=defaultdict(dict)
    ref_pid_attrs=defaultdict(dict)

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


        if pid in paper_ids:
            pid_attrs[pid]['year']=year
            pid_attrs[pid]['fos']=fos
            pid_attrs[pid]['refs']=refs
            pid_attrs[pid]['n_citation']=n_citation

        if pid in ref_paper_ids:
            ref_pid_attrs[pid]['year']=year
            ref_pid_attrs[pid]['fos']=fos
            ref_pid_attrs[pid]['n_citation']=n_citation

    open('data/paper_attrs.json','w').write(json.dumps(pid_attrs))
    open('data/ref_paper_attrs.json','w').write(json.dumps(ref_pid_attrs))


if __name__ == '__main__':

    tag = sys.argv[1]

    if tag=='select_papers':

        ### extract papers of specific field
        ''' path-to-mag physics '''
        mag_dir_path = sys.argv[2]
        field = sys.argv[3]
        chose_paper_of_field(mag_dir_path,field)

    elif tag=='citing_relation':
        mag_dir_path = sys.argv[2]
        paper_ids_path = sys.argv[3]
        citing_relation(mag_dir_path,paper_ids_path)

    elif tag=='out_papers':

        ### extract reference papers of specific field
        ''' path-to-mag data/physics-paper-ids.txt data/physics-ref-ids.txt physics'''
        mag_dir_path = sys.argv[2]
        paper_ids_path = sys.argv[3]
        ref_ids_path = sys.argv[4]
        field = sys.argv[5]
        out_papers(mag_dir_path,paper_ids_path,ref_ids_path,field)

    elif tag=='export_paper_attrs':

        ### extract json data
        ''' path-to-physics-papers.txt '''
        path = sys.argv[2]
        paper_ids_path = sys.argv[3]
        ref_ids_path = sys.argv[4]
        export_paper_attrs(path,paper_ids_path,ref_ids_path)

    else:
        logging.info('No such action tag.')


















