#coding:utf-8
from basic_config import *


def plot_fig2():

    logging.info('loading paper pubyear ...')
    pid_pubyear = json.loads(
        open('../WOS_data_processing/data/pid_pubyear.json').read())
    logging.info('{} papers has year label.'.format(len(pid_pubyear.keys())))

    pid_cn = json.loads(open('../WOS_data_processing/data/pid_cn.json').read())
    logging.info('{} papers has citations.'.format(len(pid_cn.keys())))

    year_num = defaultdict(int)
    year_cns = defaultdict(list)
    for pid in pid_pubyear.keys():

        pubyear = int(pid_pubyear[pid])

        year_num[pubyear] += 1

        year_cns[pubyear].append(int(pid_cn.get(pid, 0)))

    fig, ax = plt.subplots(1, 1, figsize=(5, 4))

    # 文章数量随着时间的变化
    xs = []
    ys = []
    for year in sorted(year_num.keys()):

        xs.append(year)
        ys.append(year_num[year])
    color = 'tab:blue'
    ax.plot(xs, ys, c=color)

    ax.set_xlabel('year')
    ax.set_ylabel('number of publications', color=color)
    ax.tick_params(axis='y', labelcolor=color)

    ax.set_yscale('log')

    # 平均被引次数随着时间的变化

    xs = []
    ys = []

    for year in sorted(year_cns.keys()):
        xs.append(year)
        ys.append(np.mean(year_cns[year]))

    ax2 = ax.twinx()

    color = 'tab:red'
    ax2.set_ylabel('average number of citations', color=color)
    ax2.plot(xs, ys, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.tight_layout()

    plt.savefig('fig/fig2.png', dpi=400)
    logging.info('fig saved to fig/fig2.png.')


if __name__ == '__main__':
    plot_fig2()
