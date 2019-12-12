#! /usr/bin/env python
# coding: utf-8

# Python 2 compatibility:
from __future__ import unicode_literals

import jubatus
from jubatus.common import Datum

import sys
import re
import os.path
import msgpackrpc
import time

from multiprocessing import Pool
from multiprocessing import Process

# カテゴリとファイルパス（フルパス）が書かれたファイルを読み込む
argvs = sys.argv
info = argvs[1]

if (len(argvs) != 3):
    print('Usage: $ python {0} category_name file_full_path'.format(argvs[0]))
    quit()

# サーバIPアドレス、ポート番号、ジョブネームを設定
host = '127.0.0.1'
port = 9199
name = ''


def query(file_path):
    retry_max = 3  # 再実行の上限回数
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
    var_nam = os.path.basename(file_path)
    client = jubatus.Classifier(host, port, name, 300)

    for i in range(1, retry_max + 1):
        try:
            # RPC実行
            res = client.classify([d])
            ret = ""
            for j in range(len(res[0])):
                ret += "{0}\t{1}\t{2}\t{3}\n".format(res[0][j].label, res[0][j].score, var_nam, argvs[2])
            client.get_client().close()
            return ret
        except (msgpackrpc.error.TransportError, msgpackrpc.error.TimeoutError, msgpackrpc.error.RPCError) as e:
            client.get_client().close()
            client = jubatus.Classifier(host, port, name, 60)
            print(e)
            print("Re-try Querying time:{0} file:{1}".format(i, file_path))
            time.sleep(retry_interval)
        except (jubatus.common.client.InterfaceMismatch) as e:
            print(e)
            print("Failed Querying___{0}".format(file_path))
    client.get_client().close()
    ret = "Failed Querying {0}\n".format(file_path)
    return ret



def wrapper_query(tuple_data):
    return tuple_data[0](tuple_data[1])


with open(info,'r') as f:
    category = []
    file_name = []
    for line in f:
        line = line.rstrip()
        var = line.split('\t')
        category.append(var[0])
        file_name.append(var[1])

p = Pool()
callback = p.map(query, file_name)

res_name = re.sub(r'config_query','result',info)
with open(res_name,'a') as out:
    out.write(u"Category\tScore\tQuery_File_Name\tClassificationGroup\n")
    for cb in callback:
        out.write(cb)
        print(cb)
