#coding:utf-8
'''
    calculate diversity of papers.

'''
from basic_config import *


def cal_diversity(com_ids_cc_path,com_ids_subjects_path,selected_IDs_references_path):

    logging.info('loading papers and references ...')
    selected_IDs_references = defaultdict(list)
    for line in open(selected_IDs_references_path):
        line = line.strip()
        pid,ref_id = line.split("\t")
        selected_IDs_references[pid].append(ref_id)


    for pid in selected_IDs_references.keys():
        for ref_id in selected_IDs_references[pid].keys():



    year_difference_diversity()

    field_diversity()

    impact_diversity()


def impact_diversity():

    pass


def field_diversity():

    pass


def year_difference_diversity():

    pass