#coding:utf-8
'''
    calculate diversity of papers.

'''
from basic_config import *


def cal_diversity(com_ids_cc_path,com_ids_subjects_path,selected_IDs_references_path,year_differences_path):

    logging.info('loading com_ids_cc ...')
    com_ids_cc = json.loads(open(com_ids_cc_path).read())

    logging.info('loading com_ids_subjects ...')
    com_ids_subjects = json.loads(open(com_ids_subjects_path).read())

    logging.info('loading papers and references ...')
    selected_IDs_references = defaultdict(list)
    for line in open(selected_IDs_references_path):
        line = line.strip()
        pid,ref_id = line.split("\t")
        selected_IDs_references[pid].append(ref_id)


    cc_pid_diversity=defaultdict(float)
    subject_pid_diversity = defaultdict(float)

    selected_IDs = selected_IDs_references.keys()
    length = len(selected_IDs)

    for i,pid in enumerate(selected_IDs):

        if (i+1)%100000==0:
            logging.info('progress {:}/{:} ...'.format((i+1),length))


        cc_list = []
        subject_list = []

        for ref_id in selected_IDs_references[pid]:

            if '.' in ref_id:
                continue

            cc = com_ids_cc.get(ref_id,0)

            subjects = com_ids_subjects.get(ref_id,[])

            cc_list.append(cc)
            subject_list.extend(subjects)

        # print cc_list
        if len(cc_list)>0:
            cc_gini = gini(cc_list)
            cc_pid_diversity[pid] = cc_gini

        if len(subject_list)>0:
            subject_gini = gini(Counter(subject_list).values())
            subject_pid_diversity[pid] = subject_gini



    open('data/wos_cc_diversity.json','w').write(json.dumps(cc_pid_diversity))
    logging.info("saved to data/wos_cc_diversity.json.")

    open('data/wos_subject_diversity.json','w').write(json.dumps(subject_pid_diversity))
    logging.info('saved to data/wos_subject_diversity.json')

    year_differences = json.loads(open(year_differences_path).read())

    yd_pid_diversity = defaultdict(float)
    for pid in year_differences.keys():
        yd_pid_diversity[pid]=gini(year_differences[pid])

    open('data/wos_year_differences_diversity.json','w').write(json.dumps(year_differences))
    logging.info('saved to data/wos_year_differences_diversity.json')



if __name__ == '__main__':
    
    com_ids_cc_path = 'data/com_ids_cc.json'
    selected_ids_references_path ='data/selected_IDs_references.txt'
    com_ids_subjects_path = 'data/com_ids_subjects.json'
    year_differences_path = 'data/statistics/year_differences.json'
    cal_diversity(com_ids_cc_path,com_ids_subjects_path,selected_ids_references_path,year_differences_path)




