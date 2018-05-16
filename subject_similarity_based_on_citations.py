#coding:utf-8

from basic_config import *



def subject_sim():

    logging.info('load subject of papers.')
    # selected_IDs = []
    
    ## query database 
    query_op = dbop()

    sql = 'select id,subject from wos_subjects'

    pid_subjects = defaultdict(list)
    subject_count = defaultdict(int)

    progress = 0
    for pid,subject in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:} ...' .format(progress))

            
        # if field in subject.lower():
            # selected_IDs.append(str(fid))
        pid_subjects[pid].append(subject)
        subject_count[subject]+=1

    ## close db
    query_op.close_db()

    open('data/subject_count.json','w').write(json.dumps(subject_count))
    logging.info('saved to data/subject_count.json.')


    query_op = dbop()
    sql = 'select id,ref_id from wos_references'
    progress=0

    subjects_mat = defaultdict(lambda:defaultdict(int))
    subject_coocur_mat = defaultdict(lambda:defaultdict(int))

    for pid,ref_id in query_op.query_database(sql):
        progress+=1
        if progress%10000000==0:
            logging.info('total progress {:} ....'.format(progress))

        for subject in pid_subjects[pid]:
        	for ref_subject in pid_subjects[ref_id]:
        		subjects_mat[subject][ref_subject]+=1

    open('data/subjects_mat.json','w').write(subjects_mat)
    logging.info('saved to data/subjects_mat.json.')



if __name__ == '__main__':
	subject_sim()


