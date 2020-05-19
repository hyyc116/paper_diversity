#coding:utf-8
'''
	1. 计算每篇文章的三类diversity
	2. 每篇论文的team size分布
	3. 每篇文章的reference 数量

'''

from basic_config import *

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
		year = paper_year[paper_reference_id]

		## 第二、三个属性是c5,c10
		c5 = paper_c5.get(paper_reference_id,0)
		c10 = paper_c10.get(paper_reference_id,0)

		##第四个属性是subjects
		subjs = paper_field[paper_reference_id]

		paper_ref_attrs[paper_id] = [year,c5,c10,subjs]


	open("data/paper_ref_attrs.json",'w').write(json.dumps(paper_ref_attrs))
	logging.info('data saved to data/paper_ref_attrs.json')



if __name__ == '__main__':
	plot_refnum_dis()
	ref_attr()







