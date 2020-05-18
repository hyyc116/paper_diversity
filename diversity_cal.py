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


## 计算refnum在N以上的论文
def cal_diversity(N):

	## 加载统计数据

	paper_year = json.loads(open('data/paper_year.json').read())

	paper_field = json.loads(open('data/paper_field0.json').read())


	query_op  = dbop()

	sql = ' '




