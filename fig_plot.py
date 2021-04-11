#coding:utf-8
from basic_config import *
import pandas as pd
import seaborn as sns


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

    fig, ax = plt.subplots(1, 1, figsize=(7, 4))

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


# A Freshness diversity的CDF分布
# B FD 随着时间的变化
# C FD 与C5的相关关系
# D FD与C10的关系
def plot_fig3():

    all_data = pd.read_csv('data/ALL_attrs.txt')
    shuffed_data = pd.read_csv('data/new_shuffled_yd_lines.csv')

    _, axes = plt.subplots(2, 2, figsize=(10, 8))

    ax = axes[0][0]
    # CDF分布
    sns.histplot(all_data,
                 x='yd_div',
                 ax=ax,
                 kde=True,
                 cumulative=True,
                 hue='subjs',
                 fill=False,
                 stat='probability')

    # 所有的分布
    sns.histplot(all_data,
                 x='yd_div',
                 ax=ax,
                 kde=True,
                 cumulative=True,
                 fill=False,
                 stat='probability',
                 label='ALL')

    sns.histplot(shuffed_data,
                 x='yd_div',
                 ax=ax,
                 kde=True,
                 cumulative=True,
                 fill=False,
                 stat='probability',
                 label='NULLMODEL')

    ax.set_xlabel('freshness diversity')

    ax.legend()

    axb = axes[0][1]
    sns.lineplot(all_data, x='year', y='yd_div', ax=axb, ci=95, hue='subjs')
    sns.lineplot(all_data, x='year', y='yd_div', ax=axb, ci=95, label='ALL')
    sns.lineplot(shuffed_data,
                 x='year',
                 y='yd_div',
                 ax=axb,
                 ci=95,
                 label='NULLMODEL')

    axb.set_xlabel('year')
    axb.set_ylabel('freshness diversity')

    axb.legend()

    axc = axes[1][0]

    sns.lineplot(all_data, x='c10', y='yd_div', ax=axc, ci=95, hue='subjs')
    sns.lineplot(all_data, x='c10', y='yd_div', ax=axc, ci=95, label='ALL')
    sns.lineplot(shuffed_data,
                 x='c10',
                 y='yd_div',
                 ax=axc,
                 ci=95,
                 label='NULLMODEL')

    axc.set_xlabel('$c_{10}$')
    axc.set_ylabel('freshness diversity')

    axc.set_xscale('log')

    axc = axes[1][1]

    sns.lineplot(all_data, x='c5', y='yd_div', ax=axc, ci=95, hue='subjs')
    sns.lineplot(all_data, x='c5', y='yd_div', ax=axc, ci=95, label='ALL')
    sns.lineplot(shuffed_data,
                 x='c5',
                 y='yd_div',
                 ax=axc,
                 ci=95,
                 label='NULLMODEL')

    axc.set_xlabel('$c_5$')
    axc.set_ylabel('freshness diversity')

    axc.set_xscale('log')

    plt.tight_layout()

    plt.savefig('fig/fig3.png', dpi=400)
    logging.info('fig saved to fig/fig3.png.')


if __name__ == '__main__':
    # plot_fig2()

    plot_fig3()
