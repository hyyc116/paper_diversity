#coding:utf-8


from basic_config import *

## 几种diversity随时间的变化
def year_div():

	paper_year= json.loads(open('data/paper_year.json').read())
	logging.info('year data loaded ....')

	paper_ts= json.loads(open('data/paper_teamsize.json').read())
	logging.info('team size data loaded ....')

	paper_fos= json.loads(open('data/paper_field0.json').read())
	logging.info('paper field data loaded ....')

	year_div_dis = defaultdict(list)
	c10_div_dis = defaultdict(list)
	subj_div_dis = defaultdict(list)

	## team size
	ts_year_dis = defaultdict(list)
	ts_c10_dis = defaultdict(list)
	ts_subj_dis = defaultdict(list)

	## field of study
	fos_year_dis = defaultdict(list)
	fos_c10_dis = defaultdict(list)
	fos_subj_dis = defaultdict(list)


	progress = 0 
	total_papers = 0
	for line in open('data/pid_divs.txt'):

		progress+=1

		logging.info("progress {}, total papers {} ....".format(progress,total_papers))

		line = line.strip()
		pid_div_vs = json.loads(line)
		for pid in pid_div_vs.keys():

			year = int(paper_year.get(pid,9999))

			ts = int(paper_ts.get(pid,-1))

			subjs = paper_fos.get(pid,None)

			if year>2008 or ts==-1:
				continue

			total_papers+=1

			year_div,c5_div,c10_div,subj_div = pid_div_vs[pid]

			year_div_dis[year].append(year_div)
			c10_div_dis[year].append(c10_div)
			subj_div_dis[year].append(subj_div)

			ts_year_dis[ts].append(year_div)
			ts_subj_dis[ts].append(subj_div)
			ts_c10_dis[ts].append(c10_div)

			if subjs is None:
				continue

			for subj in subjs:
				fos_year_dis[subj].append(year_div)
				fos_subj_dis[subj].append(subj_div)
				fos_c10_dis[subj].append(c10_div)


	plot_dis_over_attr('publication year',(year_div_dis,subj_div_dis,c10_div_dis))

	plot_dis_over_attr('team size',(ts_year_dis,ts_subj_dis,ts_c10_dis))

	# plot_dis_over_attr('field',(fos_year_dis,fos_subj_dis,fos_c10_dis))

def plot_dis_over_attr(attrName,data):

	logging.info("start to plotting {}, length of data {} ....".format(attrName,len(data)))

	print(data.keys())

	year_div_dis,subj_div_dis,c10_div_dis = data

	fig,axes = plt.subplots(3,1,figsize=(5,12))

	ax = axes[0]
	xs = []
	ys_mean = []
	ys_median = []
	for year in sorted(year_div_dis.keys()):
		xs.append(year)
		ys_mean.append(np.mean(year_div_dis[year]))
		ys_median.append(np.median(year_div_dis[year]))

	ax.plot(xs,ys_mean,'-.',label = 'mean')
	ax.plot(xs,ys_median,'-.',label ='median')

	ax.set_xlabel('{}'.format(attrName))
	ax.set_ylabel('year diversity')
	ax.set_title('year diversity')


	ax = axes[1]
	xs = []
	ys_mean = []
	ys_median = []
	for year in sorted(subj_div_dis.keys()):
		xs.append(year)
		ys_mean.append(np.mean(subj_div_dis[year]))
		ys_median.append(np.median(subj_div_dis[year]))


	ax.plot(xs,ys_mean,'-.',label = 'mean')
	ax.plot(xs,ys_median,'-.',label = 'median')

	ax.set_xlabel('{}'.format(attrName))
	ax.set_ylabel('subject diversity')

	ax.set_title('subject diversity')


	ax = axes[2]
	xs = []
	ys_mean = []
	ys_median = []
	for year in sorted(c10_div_dis.keys()):
		xs.append(year)
		ys_mean.append(np.mean(c10_div_dis[year]))
		ys_median.append(np.median(c10_div_dis[year]))


	ax.plot(xs,ys_mean,'-.',label = 'mean')
	ax.plot(xs,ys_median,'-.',label = 'median')

	ax.set_xlabel('{}'.format(attrName))
	ax.set_ylabel('impact diversity')

	ax.set_title('impact diversity')


	plt.tight_layout()

	plt.savefig('fig/diversity_over_{}.png'.format(attrName.replace(' ','_')),dpi=400)
	logging.info("fig saved to fig/diversity_over_{}.png.".format(attrName.replace(' ','_')))



## 随team size的分布
def team_div():
	paper_ts= json.loads(open('data/paper_teamsize.json').read())
	logging.info('team size data loaded ....')

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

			year = int(paper_ts.get(pid,-1))

			if year>2005:
				continue

			year_div,c5_div,c10_div,subj_div = pid_div_vs[pid]

			year_div_dis[year].append(year_div)
			c10_div_dis[year].append(c10_div)
			subj_div_dis[year].append(subj_div)

	logging.info("start to plotting ....")

	fig,axes = plt.subplots(3,1,figsize=(5,12))

	ax = axes[0]
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


	ax = axes[1]
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


	ax = axes[2]
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


## 随领域的分布
def subject_div():

	pass


## 与citation count之间的关系
def impact_div():

	pass



if __name__ == '__main__':
	year_div()