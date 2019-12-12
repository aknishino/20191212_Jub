#! /usr/bin/env python
# coding: utf-8

# Python 2 compatibility:
from __future__ import unicode_literals
from __future__ import print_function

import sys
import random
import re

import jubatus
from jubatus.common import Datum
import msgpackrpc
import time

from multiprocessing import Pool


# カテゴリとファイルパス（フルパス）が書かれたファイルと学習回数を読み込む
argvs = sys.argv
if (len(argvs) != 4):
    print('Usage: $ python {0} category_name file_full_path'.format(argvs[0]))
    quit()

info = argvs[1]     # learning_configファイル
m_num = int(argvs[2])    # 学習回数
l_num = int(argvs[3])

# サーバIPアドレス、ポート番号、ジョブネームを設定
host = '127.0.0.1'
port = 9199
name = ""    # 学習タイトル


def learn(cat,file_path):
    # 形成済みデータファイルをもらって1回だけ学習する
    retry_max = 10       # 再実行の回数上限
    retry_interval = 3  # 再実行の間隔（秒）

    # データ読み込み
    with open(file_path) as f:
        dic = {}
        line = f.readline()
        for line in f:
            line = line.rstrip()
            ls = line.split('\t')
            if len(ls) == 2:
                my_id = ls[0]
                my_value = float(ls[1])
                dic[my_id] = my_value
    d = Datum(dic)
    t_d = [[cat, d]]
    client = jubatus.Classifier(host, port, name, 60)

    for i in range(1, retry_max + 1):
        try:
            client.train(t_d)
            print("Finish training {0}".format(file_path))
            client.get_client().close()
            return file_path, 1
        except (msgpackrpc.error.TransportError, msgpackrpc.error.TimeoutError, msgpackrpc.error.RPCError) as e:
            client.get_client().close()
            client = jubatus.Classifier(host, port, name, 60)
            print(e)
            print("Re-try Learning time:{0} file:{1}".format(i, file_path))
            time.sleep(retry_interval)
        except (jubatus.common.client.InterfaceMismatch) as e:
            print(e)
            print("Failed Learning___{0}".format(file_path))

    client.get_client().close()
    return file_path, 0


def wrapper_learn(tuple_data):
    return learn(tuple_data[0],tuple_data[1])


def log(r1, r2, l):
    total_learned = sum(r2)
    cb = "=================== Start Log : {0} ===================\n".format(l)
    cb += "===== Finish learning sequence ====\n"
    cb += "Total Learning data count : {0}\nSucceed Learning data count (ratio) : {1} ({2}%)\n".format(len(cat), total_learned, total_learned / len(cat) * 100)
    if len(cat) > total_learned:
        cb += "======= Error Learning data =======\n"
        r = [r1[i] for i, j in enumerate(r2) if j == 0]
        cb += "\n".join(r)
    cb += "==================== End Log : {0} ====================\n\n".format(l)
    return cb


cat = []
for i in range(m_num):
    with open(info, 'r') as f:
        for j in f:
            ls = j.split("\t")
            var = [ls[0],ls[1].rstrip()]
            cat.append(var)

random.shuffle(cat)

p = Pool(8)
res1 = []
res2 = []
[(res1.append(a), res2.append(b)) for a, b in p.map(wrapper_learn, cat)]
cb = log(res1, res2, l_num)
log_name = re.sub(r'config_learning', 'log', info)
with open(log_name, 'a') as ll:
    ll.write(cb)
print(cb, end="")
