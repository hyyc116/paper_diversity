#coding:utf-8
'''
	1. 计算每篇文章的三类diversity
	2. 每篇论文的team size分布
	3. 每篇文章的reference 数量

'''

from basic_config import *
from gini import gini

## 画出reference num的数量分布

def plot_refnum_dis():

	paper_refnum = json.loads(open('data/paper_refnum.json').read())

	refnums = Counter([int(i) for i in paper_refnum.values()])

	xs = []
	ys = []
	for key in sorted(refnums.keys()):
		xs.append(key)
		ys.append(refnums[key])

	ys = np.array(ys)/float(np.sum(ys))


	plt.figure(figsize=(5,4))

	plt.plot(xs,ys)

	plt.xlabel("number of references")
	plt.ylabel('percentage')

	plt.tight_layout()

	plt.savefig('fig/paper_refnum_dis.png',dpi=400)


## 计算每篇论文需要的diversity的attr
def ref_attr():

	## 加载统计数据

	paper_year = json.loads(open('data/paper_year.json').read())

	paper_field = json.loads(open('data/paper_field1.json').read())

	paper_c5 = json.loads(open('data/paper_c5.json').read())

	paper_c10 = json.loads(open('data/paper_c10.json').read())

	query_op  = dbop()


	paper_ref_attrs = defaultdict(list)

	sql = 'select paper_id,paper_reference_id from mag_core.paper_references'
	reference_progress= 0 
	for paper_id,paper_reference_id in query_op.query_database(sql):

		reference_progress+=1

		if reference_progress%10000000==0:

			logging.info('reference progress {} ...'.format(reference_progress))


		##第一个属性是year
		year = paper_year.get(paper_reference_id,None)

		if year is None:
			continue

		## 第二、三个属性是c5,c10
		c5 = paper_c5.get(paper_reference_id,0)
		c10 = paper_c10.get(paper_reference_id,0)

		##第四个属性是subjects
		subjs = paper_field.get(paper_reference_id,None)

		if subjs is None:
			continue

		paper_ref_attrs[paper_id].append([year,c5,c10,subjs])

	logging.info('{} paper ref done, slicing dict'.format(len(paper_ref_attrs)))


	total = len(paper_ref_attrs)
	keys = paper_ref_attrs.keys()
	of = open("data/paper_ref_attrs.json",'w')
	sub_dict = {}
	progress = 0
	for i in range(total):
		key = keys[i]
		sub_dict[key] = paper_ref_attrs[key]

		if i!=0 and i%1000000==0:

			of.write(json.dumps(sub_dict)+'\n')
			sub_dict={}

			logging.info("writting progress {}/{} ...".format(i,total))

	if sub_dict!={}:
		of.write(json.dumps(sub_dict)+'\n')
		logging.info("writting progress {}/{} ...".format(i,total))
	
	logging.info('data saved to data/paper_ref_attrs.json')


##计算所有论文的各种diversity
def cal_diversity():

	subj_refnum = json.loads(open('data/subj_refnum.json').read())
	subj_totalnum = subj_refnum.keys()

	citnum_total = defaultdict(int)
	for subj in subj_refnum.keys():
		for subj2 in subj_refnum[subj].keys():
			citnum_total[subj2]+=subj_refnum[subj][subj2]



	of = open('data/pid_divs.txt','w')
	progress = 0

	for line in open('data/paper_ref_attrs.json'):

		progress+=1

		logging.info('progress {} ...'.format(progress))
		
		pid_div_vs = {}


		line = line.strip()

		paper_ref_attrs = json.loads(line)

		for pid in paper_ref_attrs.keys():

			years = []
			c5s = []
			c10s = []

			all_subjs = []

			for ref_attr in paper_ref_attrs[pid]:

				year,c5,c10,subjs = ref_attr

				years.append(year)
				c5s.append(c5)
				c10s.append(c10)

				all_subjs.append(subjs)

			year_div = gini(years)
			c5_div = gini(c5s)
			c10_div = gini(c10s)
			subj_div = cal_subj_div(all_subjs,subj_refnum,subj_totalnum,citnum_total)

			pid_div_vs[pid] = [year_div,c5_div,c10_div,subj_div]

		of.write(json.dumps(pid_div_vs)+"\n")

	logging.info('paper attr done.')


## 计算subject的diversity
def cal_subj_div(all_subjs,subj_refnum,subj_totalnum,citnum_total):
	subj_set = []
	subj_num = []
	for subjs in all_subjs:
		subj_num.append(len(subjs))

		subj_set.extend(subjs)

	subj_set = list(set(subj_set))

	## nc/N
	variety = len(subj_set)/subj_totalnum

	balance = gini(subj_num)

	dispasity = cal_dispasity(subj_set,subj_refnum,citnum_total)

	return variety*balance*dispasity


def cal_dispasity(subj_set,subj_refnum,citnum_total):

	all_dij = []
	for i in range(len(subj_set)):

		for j in range(i+1,len(subj_set)):

			if i==j:
				continue

			subj1 = subj_set[i]
			subj2 = subj_set[j]

			dij = 1-Sij(subj1,subj2,subj_refnum,citnum_total)

			all_dij.append(dij)

	return np.mean(all_dij)




def Rij(subj1,subj2,subj_refnum):

	return int(subj_refnum[subj1].get(subj2,0))

def Sij(subj1,subj2,subj_refnum,citnum_total):

	return (Rij(subj1,subj2,subj_refnum)+Rij(subj2,subj1,subj_refnum))/np.sqrt((total_refnum_of_subj(subj1,subj_refnum)+total_citnum_of_subj(subj1,citnum_total))*(total_refnum_of_subj(subj2,subj_refnum)+total_citnum_of_subj(subj2,citnum_total)))


def total_refnum_of_subj(subj,subj_refnum):

	return np.sum([int(i) for i in subj_refnum[subj].values()])

def total_citnum_of_subj(subj,citnum_total):
	return citnum_total[subj]










if __name__ == '__main__':
	# plot_refnum_dis()
	# ref_attr()
	cal_diversity()
