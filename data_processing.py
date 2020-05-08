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



	## 文章对应的field
	paper_fields = defaultdict(list)

	query_op = dbop()

	# sql = 'select paper_id,year from mag_core.papers'
	# year_process  = 0	
	# for paper_id,year in query_op.query_database(sql):
	# 	year_process +=1

	# 	if year_process%100000==0:

	# 		logging.info('read year progress :{} ...'.format(year_process))

	# 	paper_year[paper_id] = year


	# open('data/paper_year.json','w').write(json.dumps(paper_year))
	# logging.info('paper year saved to data/paper_year.json')

	paper_year = json.loads(open('data/paper_year.json').read())


	## 文章对应的subject
	# sql = 'select paper_id,field_of_study_id from mag_core.paper_fields_of_study'
	# field_progress =  0
	# for paper_id,field_of_study in query_op.query_database(sql):

	# 	field_progress+=1

	# 	if field_progress%100000==0:

	# 		logging.info('paper field progress:{} ...'.format(field_progress))

	# 	paper_fields[paper_id].append(field_of_study)

	# open('data/paper_fields.json','w').write(json.dumps(paper_fields))
	# logging.info('paper fields saved to data/paper_fields.json')


	### paper references
	sql = 'select paper_id,paper_reference_id from mag_core.paper_references'
	reference_progress= 0 
	for paper_id,paper_reference_id in query_op.query_database(sql):

		pyear = paper_year[paper_id]
		ref_year = paper_year[paper_reference_id]

		paper_citnum[paper_reference_id]+=1

		if int(pyear)-int(ref_year)<=5:
			paper_c5[paper_reference_id]+=1

		if int(pyear) - int(ref_year)<=10:
			paper_c10[paper_id]+=1

		reference_progress+=1

		if reference_progress%10000000==0:

			logging.info('reference progress {} ..'.format(reference_progress))

	open("data/paper_citnum.json",'w').write(json.dumps(paper_citnum))
	logging.info("paper citnum saved to data/paper_citnum.json")

	open("data/paper_c5.json",'w').write(json.dumps(paper_c5))
	logging.info("paper citnum saved to data/paper_c5.json")

	open("data/paper_c10.json",'w').write(json.dumps(paper_c10))
	logging.info("paper citnum saved to data/paper_c10.json")

	query_op.close_db()


if __name__ == '__main__':
	read_dataset()
