#coding:utf-8
from basic_config import *

import pandas as pd
import seaborn as sns
from wos_diversity import cal_subj_div


# 保持引用的学科不变，改变引用节点的时间
def shuffle_year_refs():

    logging.info('loading paper pubyear ...')
    pid_pubyear = json.loads(
        open('../WOS_data_processing/data/pid_pubyear.json').read())
    logging.info('{} papers has year label.'.format(len(pid_pubyear.keys())))

    pid_c2 = json.loads(open('../WOS_data_processing/data/pid_c2.json').read())
    logging.info('{} papers has c2.'.format(len(pid_c2.keys())))

    pid_c5 = json.loads(open('../WOS_data_processing/data/pid_c5.json').read())
    logging.info('{} papers has c5.'.format(len(pid_c5.keys())))

    pid_c10 = json.loads(
        open('../WOS_data_processing/data/pid_c10.json').read())
    logging.info('{} papers has c10.'.format(len(pid_c10.keys())))

    logging.info('loading paper top subjects ...')
    pid_topsubjs = json.loads(
        open('../WOS_data_processing/data/pid_topsubjs.json').read())
    logging.info('{} papers has top subject label.'.format(
        len(pid_topsubjs.keys())))

    logging.info('loading paper subjects ...')
    pid_subjects = json.loads(
        open('../WOS_data_processing/data/pid_subjects.json').read())
    logging.info('{} papers has subject label.'.format(len(
        pid_subjects.keys())))

    subj_subj_sim = json.loads(
        open('../WOS_data_processing/data/subj_subj_sim.json').read())

    subj_totalnum = float(len(subj_subj_sim.keys()))

    # 已经有的
    pid_divs = json.loads(open('data/pid_divs.json').read())

    progress = 0

    sub_progress = 0

    year_refs = defaultdict(list)

    logging.info('start to stat refs ...')

    for line in open('../WOS_data_processing/data/pid_refs.txt'):

        line = line.strip()

        progress += 1

        pid_refs = json.loads(line)

        for pid in pid_refs.keys():

            sub_progress += 1

            if sub_progress % 1000000 == 0:
                logging.info('progress:{},sub progress {} ...'.format(
                    progress, sub_progress))

            pubyear = int(pid_pubyear.get(pid, 9999))

            ## 1980年 到 如果年份大于2004则舍弃
            if pubyear > 2004 or pubyear < 1980:
                continue

            if len(pid_refs[pid]) < 4 or len(pid_refs[pid]) > 100:
                continue

            for ref in pid_refs[pid]:
                year_refs[pubyear].append([pid, ref])

    logging.info('starting to shuffle ...')

    new_pid_refs = defaultdict(list)
    # 每一年对应的论文和参考文献
    for year in year_refs.keys():

        pids, refs = list(zip(*year_refs[year]))

        pids = list(pids)
        refs = list(refs)

        # 只需要将refs进行shuffle，就基本上不会进行
        np.random.shuffle(refs)

        for i, pid in enumerate(pids):
            ref = refs[i]
            new_pid_refs[pid].append(ref)

    lines = [
        'pid,year,subj,c2,c5,c10,yd_div,yd_mean,yd_std,c5_div,c10_div,subj_div,_yd_div,_subj_div,_c5_div,_c10_div'
    ]

    # 根据新混乱的进行统计
    for pid in new_pid_refs.keys():

        refs = new_pid_refs[pid]
        pubyear = int(pid_pubyear[pid])

        yds = []
        c5s = []
        c10s = []
        ref_subjs = []
        subj_nums = []

        for ref in refs:
            yds.append(float(abs(int(pid_pubyear[ref]) - pubyear)))

            c5s.append(pid_c5.get(ref, 0))
            c10s.append(pid_c10.get(ref, 0))

            ref_subjs.extend(pid_subjects.get(ref, []))
            subj_nums.append(len(pid_subjects.get(pid, [])))

        yd_div = gini(yds)
        yd_mean = np.mean(yds)
        yd_std = np.std(yds)

        c5_div = gini(c5s)
        c10_div = gini(c10s)

        ref_subjs = list(set(ref_subjs))

        if len(ref_subjs) <= 1:
            subj_div = 0

        else:
            subj_div = cal_subj_div(subj_totalnum, subj_nums, ref_subjs,
                                    subj_subj_sim)

        c2 = pid_c2.get(pid, 0)
        c5 = pid_c5.get(pid, 0)
        c10 = pid_c10.get(pid, 0)

        subjs = pid_topsubjs.get(pid, [])

        if len(subjs) == 0:
            continue

        subj = np.random.choice(subjs, size=1)[0]

        # 非shuffle的数据值
        _yd_div, _subj_div, _c2_div, _c5_div, _c10_div, _yd_mean, _yd_std, c2_mean, c2_std, c5_mean, c5_std, c10_mean, c10_std, c2p_div, c5p_div, c10p_div, c2p_mean, c2p_std, c5p_mean, c5p_std, c10p_mean, c10p_std = pid_divs[
            pid]

        lines.append(
            f'{pid},{pubyear},{subj},{c2},{c5},{c10},{yd_div},{yd_mean},{yd_std},{c5_div},{c10_div},{subj_div},{_yd_div},{_subj_div},{_c5_div},{_c10_div}'
        )

    open('data/new_shuffled_yd_lines.csv', 'w').write('\n'.join(lines))
    logging.info('data saved to data/new_shuffled_yd_lines.csv.')


def plot_attrs():

    data = pd.read_csv('data/new_shuffled_yd_lines.csv')

    # sns.lineplot(data=data, x=x, y=y, ax=ax, ci='sd')
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    ax = axes[0]
    sns.histplot(data,
                 x='yd_mean',
                 ax=ax,
                 kde=True,
                 cumulative=True,
                 stat='probability')
    ax = axes[1]
    sns.histplot(data,
                 x='yd_std',
                 ax=ax,
                 kde=True,
                 cumulative=True,
                 stat='probability')

    plt.tight_layout()

    plt.savefig('fig/fig3.png', dpi=400)
    logging.info('fig saved to fig/fig3.png.')


if __name__ == "__main__":
    shuffle_year_refs()

    # plot_attrs()
