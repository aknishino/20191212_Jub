#! /usr/bin/env python
# coding: utf-8

# Python 2 compatibility:
from __future__ import unicode_literals

# サーバIPアドレス、ポート番号、ジョブネームを設定
host = '127.0.0.1'
port = 9199
name = ''

import jubatus

client = jubatus.Classifier(host, port, name, 300)
lab = client.get_labels()
var_name = ""
for label in lab:
    var_name += label
    var_name += str(lab[label])

client.save(var_name)
client.get_client().close()