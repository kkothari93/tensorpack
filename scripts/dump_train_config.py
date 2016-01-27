#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: dump_train_config.py
# Author: Yuxin Wu <ppwwyyxx@gmail.com>

import argparse
import cv2
import tensorflow as tf
import imp
import tqdm
import os

from tensorpack.utils import logger
from tensorpack.utils.utils import mkdir_p

parser = argparse.ArgumentParser()
parser.add_argument(dest='config')
parser.add_argument('-o', '--output', help='output directory to dump dataset image')
parser.add_argument('-n', '--number', help='number of images to dump',
                    default=10, type=int)
args = parser.parse_args()



get_config_func = imp.load_source('config_script', args.config).get_config
config = get_config_func()

if args.output:
    mkdir_p(args.output)
    cnt = 0
    index = 0   # TODO: as an argument?
    for dp in config.dataset.get_data():
        imgbatch = dp[index]
        if cnt > args.number:
            break
        for bi, img in enumerate(imgbatch):
            cnt += 1
            fname = os.path.join(args.output, '{:03d}-{}.png'.format(cnt, bi))
            cv2.imwrite(fname, img)

NR_DP_TEST = 100
logger.info("Testing dataflow speed:")
with tqdm.tqdm(total=NR_DP_TEST, leave=True, unit='data points') as pbar:
    for idx, dp in enumerate(config.dataset.get_data()):
        if idx > NR_DP_TEST:
            break
        pbar.update()


