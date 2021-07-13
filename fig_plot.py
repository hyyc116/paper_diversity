#coding:utf-8
from matplotlib.pyplot import legend
from basic_config import *
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
lowess = sm.nonparametric.lowess


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


def replace_subj(filepath):

    data = []
    for line in open(filepath):
        data.append(line.strip().replace('Clinical, Pre-Clinical & Health',
                                         'Clinical Pre-Clinical & Health'))

    open(filepath, 'w').write('\n'.join(data))


# 根据属性 画 多个领域的折线图，并平滑
def plot_cdf_with_norm(data, attrname, ax, smooth=False):

    labels = [
        'Arts & Humanities', 'Clinical Pre-Clinical & Health',
        'Engineering & Technology', 'Life Sciences', 'Physical Sciences',
        'Social Sciences'
    ]

    # CDF分布
    sns.kdeplot(data=data,
                x=attrname,
                ax=ax,
                cumulative=True,
                hue='subj',
                hue_order=labels,
                fill=False,
                common_norm=False,
                legend=False)

    if smooth:
        xs = []
        ys = []
        for line in ax.get_lines():

            x = line.get_xdata()
            y = line.get_ydata()

            xs.append(x)
            ys.append(y)
        # 把之前的消除了

        ax.clear()

        for i, x in enumerate(xs):

            y = ys[i]

            xi, yi = zip(*lowess(y, x, frac=1. / 3, it=0))

            ax.plot(xi, yi, label=labels[i])


def plot_line_with_norm(data, x, y, ax, smooth=False):

    labels = [
        'Arts & Humanities', 'Clinical Pre-Clinical & Health',
        'Engineering & Technology', 'Life Sciences', 'Physical Sciences',
        'Social Sciences'
    ]

    # CDF分布
    sns.lineplot(data=data,
                 x=x,
                 y=y,
                 ax=ax,
                 ci=None,
                 hue_order=[
                     'Arts & Humanities', 'Clinical Pre-Clinical & Health',
                     'Engineering & Technology', 'Life Sciences',
                     'Physical Sciences', 'Social Sciences'
                 ],
                 hue='subj')

    if smooth:
        xs = []
        ys = []
        for line in ax.get_lines():

            x = line.get_xdata()
            y = line.get_ydata()

            xs.append(x)
            ys.append(y)
        # 把之前的消除了

        # print(xs)
        # print(ys)

        ax.clear()

        for i, x in enumerate(xs):

            y = ys[i]

            if len(x) == 0:
                continue

            xi, yi = zip(*lowess(y, x, frac=0.25, it=0))

            ax.plot(xi, yi, label=labels[i])


# A Freshness diversity的CDF分布
# B FD 随着时间的变化
# C FD 与C5的相关关系
# D FD与C10的关系
def plot_fig3(attrName='yd_div', shuffed_data=None):
    # data = shuffed_data = pd.read_csv('data/ALL_attrs.txt', error_bad_lines=False)

    _, axes = plt.subplots(2, 2, figsize=(25, 20))

    sns.set_theme(style="ticks")

    ax = axes[0][0]
    # CDF分布
    sns.kdeplot(data=shuffed_data,
                x='_{:}'.format(attrName),
                ax=ax,
                cumulative=True,
                hue='subj',
                hue_order=[
                    'Arts & Humanities', 'Clinical Pre-Clinical & Health',
                    'Engineering & Technology', 'Life Sciences',
                    'Physical Sciences', 'Social Sciences'
                ],
                fill=False,
                common_norm=False,
                legend=False)

    # 所有的分布
    sns.kdeplot(data=shuffed_data,
                x='_{:}'.format(attrName),
                ax=ax,
                cumulative=True,
                fill=False,
                label='ALL',
                color='blue',
                lw=3)

    sns.kdeplot(data=shuffed_data,
                x='{:}'.format(attrName),
                ax=ax,
                cumulative=True,
                fill=False,
                label='NULLMODEL',
                color='r',
                lw=4)

    if attrName == 'yd_div':
        ax.set_xlabel('freshness diversity')
    elif attrName == 'subj_div':
        ax.set_xlabel('subject diversity')
    elif attrName == 'c10_div':
        ax.set_xlabel('impact diversity')

    ax.set_ylabel('probability')

    ax.legend()

    axb = axes[0][1]
    sns.lineplot(data=shuffed_data,
                 x='year',
                 y='_{:}'.format(attrName),
                 ax=axb,
                 ci=None,
                 hue_order=[
                     'Arts & Humanities', 'Clinical Pre-Clinical & Health',
                     'Engineering & Technology', 'Life Sciences',
                     'Physical Sciences', 'Social Sciences'
                 ],
                 hue='subj')
    # plot_line_with_norm(shuffed_data, 'year', '_{:}'.format(attrName), axb, True)

    sns.lineplot(data=shuffed_data,
                 x='year',
                 y='_{:}'.format(attrName),
                 ax=axb,
                 ci=None,
                 label='ALL',
                 color='blue',
                 lw=3)
    sns.lineplot(data=shuffed_data,
                 x='year',
                 y='{:}'.format(attrName),
                 ax=axb,
                 ci=None,
                 label='NULLMODEL',
                 color='r',
                 lw=4)

    axb.set_xlabel('year')
    if attrName == 'yd_div':
        axb.set_ylabel('freshness diversity')
        axb.set_ylim(0.2, 0.6)

    elif attrName == 'subj_div':
        axb.set_ylabel('subject diversity')
        axb.set_ylim(0, 0.04)

    elif attrName == 'c10_div':
        axb.set_ylabel('impact diversity')
        axb.set_ylim(0.2, 0.7)

    axb.legend()

    axc = axes[1][0]

    plot_line_with_norm(shuffed_data, 'c10', '_{:}'.format(attrName), axc,
                        True)

    # sns.lineplot(data=shuffed_data,
    #              x='c10',
    #              y='_{:}'.format(attrName),
    #              ax=axc,
    #              ci=None,
    #              label='ALL',
    #              c='blue',
    #              lw=3)
    # sns.lineplot(data=shuffed_data,
    #              x='c10',
    #              y='{:}'.format(attrName),
    #              ax=axc,
    #              ci=None,
    #              label='NULLMODEL',
    #              color='c',
    #              lw=3,
    #              ls='--')
    xi, yi = zip(*lowess(shuffed_data['_{:}'.format(attrName)],
                         shuffed_data['c10'],
                         frac=0.3,
                         it=0))
    axc.plot(xi, yi, label='ALL', c='blue', lw=2)
    xi, yi = zip(*lowess(shuffed_data['{:}'.format(attrName)],
                         shuffed_data['c10'],
                         frac=0.3,
                         it=0))
    axc.plot(xi, yi, label='NULLMODEL', c='r', lw=4)

    axc.set_xlim(1, 5 * 10**4)

    axc.legend()

    axc.set_xlabel('$c_{10}$')
    if attrName == 'yd_div':
        axc.set_ylabel('freshness diversity')
        axc.set_ylim(0.2, 0.6)
    elif attrName == 'subj_div':
        axc.set_ylabel('subject diversity')
        axc.set_ylim(0, 0.04)

    elif attrName == 'c10_div':
        axc.set_ylabel('impact diversity')
        axc.set_ylim(0.2, 0.7)

    axc.set_xscale('log')

    axc = axes[1][1]

    # sns.lineplot(data=shuffed_data,
    #              x='c5',
    #              y='_{:}'.format(attrName),
    #              ax=axc,
    #              hue='subj',
    #              ci=None,
    #              hue_order=[
    #                  'Arts & Humanities', 'Clinical Pre-Clinical & Health',
    #                  'Engineering & Technology', 'Life Sciences',
    #                  'Physical Sciences', 'Social Sciences'
    #              ])
    plot_line_with_norm(shuffed_data, 'c5', '_{:}'.format(attrName), axc, True)

    xi, yi = zip(*lowess(shuffed_data['_{:}'.format(attrName)],
                         shuffed_data['c5'],
                         frac=0.3,
                         it=0))
    axc.plot(xi, yi, label='ALL', c='blue', lw=2)
    xi, yi = zip(*lowess(shuffed_data['{:}'.format(attrName)],
                         shuffed_data['c5'],
                         frac=0.3,
                         it=0))
    axc.plot(xi, yi, label='NULLMODEL', c='r', lw=4)

    axc.set_xlim(2, 10**4)

    # sns.lineplot(data=shuffed_data,
    #              x='c5',
    #              y='_{:}'.format(attrName),
    #              ax=axc,
    #              ci=None,
    #              label='ALL',
    #              color='blue',
    #              lw=3)
    # sns.lineplot(data=shuffed_data,
    #              x='c5',
    #              y='{:}'.format(attrName),
    #              ax=axc,
    #              ci=None,
    #              label='NULLMODEL',
    #              lw=3,
    #              ls='--',
    #              color='c')

    axc.set_xlabel('$c_5$')
    if attrName == 'yd_div':
        axc.set_ylabel('freshness diversity')
        axc.set_ylim(0.2, 0.6)
    elif attrName == 'subj_div':
        axc.set_ylabel('subject diversity')
        axc.set_ylim(0, 0.04)
    elif attrName == 'c10_div':
        axc.set_ylabel('impact diversity')
        axc.set_ylim(0.2, 0.7)

    axc.set_xscale('log')

    axc.legend()

    plt.tight_layout()

    plt.savefig('fig/fig_{:}.png'.format(attrName), dpi=400)
    logging.info(f'fig saved to fig/fig_{attrName}.png.')


if __name__ == '__main__':
    # plot_fig2()

    shuffed_data = pd.read_csv('data/new_shuffled_yd_lines.csv')

    # plot_fig3('yd_div', shuffed_data)
    plot_fig3('c10_div', shuffed_data)
    # plot_fig3('subj_div', shuffed_data)

    # replace_subj(sys.argv[1])
