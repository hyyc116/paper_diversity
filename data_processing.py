#coding:utf-8
'''
数据处理包括：

1. paper_references 引用关系,计算citation count
2. paper_fields_of_study 文章对应的领域
3. 文章对应的年份

'''
from basic_config import *

def read_dataset():

    # 文章对应的年份
    paper_year = {}

    ## 文章的citation count
    paper_citnum = defaultdict(int)
    paper_c5 = defaultdict(int)
    paper_c10 = defaultdict(int)



    

    query_op = dbop()

    # sql = 'select paper_id,year from mag_core.papers'
    # year_process  = 0    
    # for paper_id,year in query_op.query_database(sql):
    #     year_process +=1

    #     if year_process%100000==0:

    #         logging.info('read year progress :{} ...'.format(year_process))

    #     paper_year[paper_id] = year


    # open('data/paper_year.json','w').write(json.dumps(paper_year))
    # logging.info('paper year saved to data/paper_year.json')

    paper_year = json.loads(open('data/paper_year.json').read())


    # ## 文章对应的field
    # paper_fields = defaultdict(list)
    # # 文章对应的subject
    # sql = 'select paper_id,A.field_of_study_id from mag_core.paper_fields_of_study as A, mag_core.fields_of_study as B where A.field_of_study_id = B.field_of_study_id and B.level=1'
    # field_progress =  0
    # for paper_id,field_of_study in query_op.query_database(sql):

    #     field_progress+=1

    #     if field_progress%100000==0:

    #         logging.info('paper field progress:{} ...'.format(field_progress))

    #     paper_fields[paper_id].append(field_of_study)

    # open('data/paper_field1.json','w').write(json.dumps(paper_fields))
    # logging.info('paper fields saved to data/paper_field1.json')

    paper_field = json.loads(open('data/paper_field1.json').read())

    paper_refnum = defaultdict(int)

    subj12_num = defaultdict(lambda:defaultdict(int))

    ### paper references
    sql = 'select paper_id,paper_reference_id from mag_core.paper_references'
    reference_progress= 0 
    for paper_id,paper_reference_id in query_op.query_database(sql):

        pyear = paper_year[paper_id]
        ref_year = paper_year[paper_reference_id]

        paper_refnum[paper_id]+=1

        paper_citnum[paper_reference_id]+=1


        subj1 = paper_field.get(paper_id,[])
        subj2 = paper_field.get(paper_reference_id,[])
        ##统计学科之间的引用次数，计算学科的相似性
        for s1 in subj1:
            for s2 in subj2:
                subj12_num[s1][s2]+=1

        if int(pyear)-int(ref_year)<=5:
            paper_c5[paper_reference_id]+=1

        if int(pyear) - int(ref_year)<=10:
            paper_c10[paper_reference_id]+=1

        reference_progress+=1

        if reference_progress%10000000==0:

            logging.info('reference progress {} ..'.format(reference_progress))

    open("data/paper_citnum.json",'w').write(json.dumps(paper_citnum))
    logging.info("paper citnum saved to data/paper_citnum.json")

    open("data/paper_refnum.json",'w').write(json.dumps(paper_refnum))
    logging.info("paper citnum saved to data/paper_refnum.json")

    open("data/paper_c5.json",'w').write(json.dumps(paper_c5))
    logging.info("paper citnum saved to data/paper_c5.json")

    open("data/paper_c10.json",'w').write(json.dumps(paper_c10))
    logging.info("paper citnum saved to data/paper_c10.json")

    open('data/subj_refnum.json','w').write(json.dumps(subj12_num))

    query_op.close_db()



if __name__ == '__main__':
    read_dataset()
