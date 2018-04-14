#coding:utf-8
'''
    filtering data from web of science through following steps"
    1. from wos_subjects filter out IDs of specified field as selected_IDs
    2. from wos_references get reference list of these selected_IDs and get list of cited papers as cited_IDs
    3. combine selected_IDs and cited_IDs and get set COM_IDs
    4. use COM_IDs to stats the citation count of each paper from wos_references and saved as com_ids_cc.json {(id:number of cc)}, cc = citation count
    5. use COM_IDs to get pubyear from wos_summray saved as com_ids_year.json {(id:pubyear)}
    6. use COM_IDs to get subjects from wos_subjects saved as com_ids_subjects.json {id:[list of subjects]}

'''

from basic_config import *

def filter_out_ids_of_field(field):
    logging.info('filter out paper ids from wos_subjects of field:[{:}].'.format(field))
    selected_IDs = []
    
    ## query database 
    query_op = dbop()

    sql = 'select id,subject from wos_subjects'

    progress = 0
    for fid,subject in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:}/167,000,000 ...' .format(progress))

            
        if field in subject.lower():
            selected_IDs.append(str(fid))

    ## close db
    query_op.close_db()

    selected_IDs = list(set(selected_IDs))
    saved_path = 'data/selected_IDs_from_{:}.txt'.format(field)
    open(saved_path,'w').write('\n'.join(selected_IDs))
    logging.info('number of papers belong to field [{:}] is [{:}], and saved to {:}.'.format(field,len(selected_IDs),saved_path))
    return selected_IDs



def fetch_references(selected_IDs_path):
    selected_IDs = set([line.strip() for line in open(selected_IDs_path)])
    logging.info('fetch reference list of {:} selected_IDs.'.format(len(selected_IDs)))
    # selected_IDs_references = defaultdict(list)
    cited_IDs = []
    length = len(selected_IDs)
    ## query database
    query_op = dbop()
    sql = 'select id,ref_id from wos_references'
    progress=0
    pid_refs = []
    for pid,ref_id in query_op.query_database(sql):
        progress+=1
        if progress%10000000==0:
            logging.info('total progress {:}, sub_progress:{:}/{:}'.format(progress,len(pid_refs),length))
        if pid in selected_IDs:

            # selected_IDs_references[pid].append(ref_id)

            if ref_id is None:
                continue

            cited_IDs.append(ref_id)
            pid_refs.append('{:}\t{:}'.format(pid,ref_id))

    query_op.close_db()
    cited_IDs = list(set(cited_IDs))
    saved_si_refs_path = 'data/selected_IDs_references.txt'
    saved_cited_ids = 'data/cited_ids.txt'
    open(saved_si_refs_path,'w').write('\n'.join(pid_refs))
    open(saved_cited_ids,'w').write('\n'.join(cited_IDs))
    logging.info('{:}/{:} papers has references saved to {:}, and {:} cited IDs saved to {:}.'.format(len(pid_refs),len(selected_IDs),saved_si_refs_path,len(cited_IDs),saved_cited_ids))
    # return selected_IDs_references,cited_IDs


def combine_ids(selected_IDs_path,cited_IDs_path):

    selected_IDs = list(set([line.strip() for line in open(selected_IDs_path)]))
    cited_IDs = list(set([line.strip() for line in open(cited_IDs_path)]))
    logging.info('combine ids: {:} selected_IDs and {:} cited_IDs..'.format(len(selected_IDs),len(cited_IDs)))
    com_IDs = []
    com_IDs.extend(selected_IDs)
    com_IDs.extend(cited_IDs)
    com_IDs = set(com_IDs)
    saved_path = 'data/com_ids.txt'
    open(saved_path,'w').write('\n'.join(com_IDs))
    logging.info('number of combined ids is [{:}], and saved to {:}.'.format(len(com_IDs),saved_path))


def fetch_cc_of_com_ids(com_IDs_path,selected_IDs_path):
    com_IDs = set([line.strip() for line in open(com_IDs_path)])
    selected_IDs = set([line.strip() for line in open(selected_IDs_path)])
    logging.info('fetch citation count of {:} combine ids, {:} selected IDs.'.format(len(com_IDs),len(selected_IDs)))
    com_ids_cc = defaultdict(int)
    selected_IDs_citations = []

    ##query table wos_refrences
    query_op = dbop()
    sql = 'select id,ref_id from wos_references'
    progress=0
    for pid,ref_id in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:} ...'.format(progress))
        if ref_id in com_IDs:
            com_ids_cc[ref_id]+=1

        if ref_id in selected_IDs:
            selected_IDs_citations.append('{:}\t{:}'.format(ref_id,pid))

    query_op.close_db()
    logging.info('{:} cited ids have citations'.format(len(com_ids_cc.keys())))
    open('data/com_ids_cc.json','w').write(json.dumps(com_ids_cc))

    open('data/selected_IDs_citations.txt','w').write('\n'.join(selected_IDs_citations))
    logging.info('selected IDs and citations saved to data/selected_IDs_citations.txt.')
    return com_ids_cc

def fecth_pubyear_of_com_ids(com_IDs_path):
    com_IDs = set([line.strip() for line in open(com_IDs_path)])
    logging.info('fetch published year of {:} combine ids'.format(len(com_IDs)))
    com_ids_year = {}

    ## query database wos_summary
    query_op = dbop()
    sql = 'select id,pubyear from wos_summary'
    progress=0
    for pid,pubyear in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:} ...'.format(progress))
        if pid in com_IDs:
            com_ids_year[pid] = pubyear

    query_op.close_db()
    logging.info('{:} cited ids have citations'.format(len(com_ids_year.keys())))
    open('data/com_ids_year.json','w').write(json.dumps(com_ids_year))
    return com_ids_year

def fetch_subjects_of_com_ids(com_IDs_path):
    com_IDs = set([line.strip() for line in open(com_IDs_path)])
    logging.info('fetch subjects of {:} combine ids'.format(len(com_IDs)))
    com_ids_subjects = defaultdict(list)

    ## query table wos_subjects
    query_op = dbop()
    sql = 'select id,subject from wos_subjects'
    progress=0
    for pid,subject in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:} ...'.format(progress))
        if pid in com_IDs:
            com_ids_subjects[pid].append(subject)

    query_op.close_db()

    logging.info('{:} cited ids have subjects'.format(len(com_ids_subjects.keys())))
    open('data/com_ids_subjects.json','w').write(json.dumps(com_ids_subjects))
    return com_ids_subjects


if __name__ == '__main__':
    label = sys.argv[1]

    if label=='t1':
        filter_out_ids_of_field(sys.argv[2])

    elif label == 't2':
        fetch_references(sys.argv[2])

    elif label == 't3':
        combine_ids(sys.argv[2],sys.argv[3])

    elif label =='t4':
        fetch_cc_of_com_ids(sys.argv[2])

    elif label =='t5':
        fecth_pubyear_of_com_ids(sys.argv[2])

    elif label =='t6':
        fetch_subjects_of_com_ids(sys.argv[2])

        





