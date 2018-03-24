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
            selected_IDs.append(fid)

    ## close db
    query_op.close_db()

    saved_path = 'data/selected_IDs_from_{:}.txt'.format(field)
    open(saved_path,'w').write('\n'.join(selected_IDs))
    logging.info('number of papers belong to field [{:}] is [{:}], and saved to {:}.'.format(field,len(selected_IDs),saved_path))
    return selected_IDs



def fetch_references(selected_IDs):
    logging.info('fetch reference list of {:} selected_IDs.'.format(selected_IDs))
    selected_IDs_references = defaultdict(list)
    cited_IDs = []


    saved_si_refs_path = 'data/selected_IDs_references.json'
    saved_cited_ids = 'data/cited_ids.txt'
    open(saved_si_refs_path,'w').write(json.dumps(selected_IDs_references))
    open(saved_cited_ids,'w').write('\n'.join(cited_IDs))
    logging.info('{:}/{:} papers has references saved to {:}, and {:} cited IDs saved to {:}.'.format(len(selected_IDs_references.keys()),len(selected_IDs),saved_si_refs_path,len(cited_IDs),saved_cited_ids))
    return selected_IDs_references,cited_IDs


def combine_ids(selected_IDs,cited_IDs):
    logging.info('combine ids: {:} selected_IDs and {:} cited_IDs..'.format(selected_IDs,cited_IDs))
    com_IDs = []
    com_IDs.extend(selected_IDs)
    com_IDs.extend(cited_IDs)
    com_IDs = set(com_IDs)
    saved_path = 'data/com_ids.txt'
    open(saved_path,'w').write('\n'.join(com_IDs))
    logging.info('number of combined ids is [{:}], and saved to {:}.'.format(len(com_IDs),saved_path))


def fetch_cc_of_com_ids(com_IDs):
    logging.info('fetch citation count of {:} combine ids'.format(com_IDs))
    com_ids_cc = defaultdict(int)


    return com_ids_cc

def fecth_pubyear_of_com_ids(com_IDs):
    logging.info('fetch published year of {:} combine ids'.format(com_IDs))
    com_ids_year = {}

    return com_ids_year

def fetch_subjects_of_com_ids(com_IDs):
    logging.info('fetch subjects of {:} combine ids'.format(com_IDs))
    com_ids_subjects = defaultdict(list)

    return com_ids_subjects


if __name__ == '__main__':
    label = sys.argv[1]

    if label=='t1':
        filter_out_ids_of_field(sys.argv[2])





