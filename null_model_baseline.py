#coding:utf-8
from basic_config import *


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

    lines = ['pid,c2,c5,c10,yd_div,yd_mean,yd_std']

    # 根据新混乱的进行统计
    for pid in new_pid_refs.keys():

        yds = []

        refs = new_pid_refs[pid]

        pubyear = int(pid_pubyear[pid])

        for ref in refs:
            yds.append(abs(int(pid_pubyear[ref]) - pubyear))

        yd_div = gini(yds)
        yd_mean = np.mean(yds)
        yd_std = np.std(yds)

        c2 = pid_c2.get(pid, 0)
        c5 = pid_c5.get(pid, 0)
        c10 = pid_c10.get(pid, 0)

        lines.append(f'{pid},{c2},{c5},{c10},{yd_div},{yd_mean},{yd_std}')

    open('data/new_shuffled_yd_lines.csv', 'w').write('\n'.join(lines))
    logging.info('data saved to data/new_shuffled_yd_lines.csv.')


if __name__ == "__main__":
    shuffle_year_refs()
