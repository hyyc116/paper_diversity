#coding:utf-8


from basic_config import *

## 几种diversity随时间的变化
def year_div():

	paper_year= json.loads(open('data/paper_year.json').read())

	year_div_dis = defaultdict(list)
	c10_div_dis = defaultdict(list)
	subj_div_dis = defaultdict(list)

	progress = 0 
	for line in open('data/pid_divs.txt'):

		progress+=1

		logging.info("progress {} ....".format(progress))

		
		line = line.strip()

		pid_div_vs = json.loads(line)

		for pid in pid_div_vs.keys():

			year = int(paper_year.get(pid,9999))

			if year>2005:
				continue

			year_div,c5_div,c10_div,subj_div = pid_div_vs[pid]

			year_div_dis[year].append(year_div)
			c10_div_dis[year].append(c10_div)
			subj_div_dis[year].append(subj_div)

	logging.info("start to plotting ....")

	fig,axes = plt.subplots(3,1,figsize=(5,12))

	ax0 = axes[0]
	xs = []
	ys_mean = []
	ys_median = []
	for year in sorted(year_div_dis.keys()):
		xs.append(year)
		ys_mean.append(np.mean(year_div_dis[year]))
		ys_median.append(np.median(year_div_dis[year]))


	ax.plot(xs,ys_mean,'mean')
	ax.plot(xs,ys_median,'median')

	ax.set_xlabel('publication year')
	ax.set_ylabel('year diversity')

	ax.set_title('year diversity')


	ax0 = axes[1]
	xs = []
	ys_mean = []
	ys_median = []
	for year in sorted(subj_div_dis.keys()):
		xs.append(year)
		ys_mean.append(np.mean(subj_div_dis[year]))
		ys_median.append(np.median(subj_div_dis[year]))


	ax.plot(xs,ys_mean,'mean')
	ax.plot(xs,ys_median,'median')

	ax.set_xlabel('publication year')
	ax.set_ylabel('subject diversity')

	ax.set_title('subject diversity')


	ax0 = axes[2]
	xs = []
	ys_mean = []
	ys_median = []
	for year in sorted(c10_div_dis.keys()):
		xs.append(year)
		ys_mean.append(np.mean(c10_div_dis[year]))
		ys_median.append(np.median(c10_div_dis[year]))


	ax.plot(xs,ys_mean,'mean')
	ax.plot(xs,ys_median,'median')

	ax.set_xlabel('publication year')
	ax.set_ylabel('impact diversity')

	ax.set_title('impact diversity')


	plt.tight_layout()

	plt.savefig('fig/diversity_over_year.png',dpi=400)
	logging.info("fig saved to fig/diversity_over_year.png.")


## 随team size的分布
def team_div():

	pass

## 随领域的分布
def subject_div():

	pass


## 与citation count之间的关系
def impact_div():

	pass



if __name__ == '__main__':
	year_div()