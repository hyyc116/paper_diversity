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

    open('data/subjects_mat.json','w').write(json.dumps(subjects_mat))
    logging.info('saved to data/subjects_mat.json.')


def subject_similarity(subject_coocur_mat_path):
    # subject_count = json.loads(open(subject_count_path).read())
    subject_coocur_mat = json.loads(open(subject_coocur_mat_path).read())

    subjectkey_count = defaultdict(int)
    subject_cits = defaultdict(int)
    for subject in sorted(subject_coocur_mat.keys()):
        for ref_subject in sorted(subject_coocur_mat[subject].keys()):
            key = '\t'.join(sorted([subject,ref_subject]))
            num = subject_coocur_mat[subject][ref_subject]
            # print '{:}\t{:}\t{:}'.format(subject,ref_subject,num)
            subjectkey_count[key] += num

            if subject == ref_subject:
                continue

            subject_cits[subject] += num

    subjectkey_sim = {}
    for key in sorted(subjectkey_count.keys()):
        s1,s2 = key.split("\t")

        if s1==s2:
            continue

        c_s1 = subject_cits[s1]
        c_s2 = subject_cits[s2]

        sim = float(subjectkey_count[key])/(c_s1+c_s2)

        subjectkey_sim[key] = sim

        # print '{:}\t{:}\t{:}'.format(s1,s2,sim)

    open('data/subject_sim.json','w').write(json.dumps(subjectkey_sim))


def out_sim_mat(subject_sim_json):
    subject_sim = json.loads(open(subject_sim_json).read())

    print 'day\thour\tvalue'
    subjects =[]
    for key in subject_sim.keys():
        # for s2 in subjects:
        # key = '\t'.join(sorted([,rs]))
        subjects.extend(key.split('\t'))
    
    subjects = sorted(list(set(subjects)))

    # print '{:}\t{:}'.format(key,subject_sim[s1])
    for i,s1 in enumerate(subjects):
        for j,s2 in enumerate(subjects):
            key = '\t'.join(sorted([s1,s2]))
            if s1==s2:
                sim=1
            else:
                sim = subject_sim.get(sim,0) 

            print '{:}\t{:}\t{:.10f}'.format(i,j,sim)

    open('subjects.txt','w').write('\n'.join(subjects))



if __name__ == '__main__':
	# subject_sim()
    subject_count_path = 'data/subject_count.json'
    subject_coocur_mat_path = 'data/subjects_mat.json'
    # subject_similarity(subject_coocur_mat_path)

    subject_sim_path = 'data/subject_sim.json'
    out_sim_mat(subject_sim_path)







