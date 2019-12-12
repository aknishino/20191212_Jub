#! /usr/bin/env python
# coding: utf-8

import sys
import os
import re

argvs = sys.argv    # 2つの引数必要。total学習回数（数字）、何回学習毎にclassifyとsaveを実行するか（数字）

if (len(argvs) != 3):
    print 'Usage: $ python {0} total_learning_number number_of_classification_every_X_times_of_learning'.format(argvs[0].decode('utf-8'))
    quit()

num = str(int(float(argvs[1]) / float(argvs[2])))
num2 = argvs[2]
dir = os.path.split(os.path.abspath(__file__))[0]
path = os.path.split(os.path.dirname(argvs[0]))[1]
sh = dir + "/learning_" + num + "_query_save.sh"
dm = dir + "/dump.sh"
rscr = dir + "/make_Report.R"


f = open(sh,'w')
string = """\
# 同じデータセットを使って、合計{my_num3}回の学習をする。
# {my_num2}回の学習を終える毎に、多値分類と学習モデルの保存を行う。

for i in `seq {my_num}`
do
    python /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/{my_path}/learning.py /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/{my_path}/config_learning.txt {my_num2} $i
    a=`expr $i \* {my_num2}`
    python /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/{my_path}/query.py /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/{my_path}/config_query.txt $a
    python /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/{my_path}/save.py
done

bash /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/{my_path}/dump.sh\
""".format(my_path=path, my_num=num, my_num2=num2, my_num3=argvs[1])

f.write(string)
f.close()

f = open(dm,'w')
string = """\
for file in `\\find Desktop/Jubatus/Learning_and_Classification/{my_path}/LearningModel -maxdepth 1 -type f`
do
    a=`basename $file`
    a=${{a/\\.jubatus/\\.json}}
    jubadump -i $file > Desktop/Jubatus/Learning_and_Classification/{my_path}/Dump/$a
    python Desktop/Jubatus/Learning_and_Classification/{my_path}/json2txt.py Desktop/Jubatus/Learning_and_Classification/{my_path}/Dump/$a
    rm Desktop/Jubatus/Learning_and_Classification/{my_path}/Dump/$a
done\
""".format(my_path=path)

f.write(string)
f.close()

f = open(rscr, 'w')
string = """\
library(ggplot2)

dat <- read.delim("/Users/juuikinouseikagaku/Documents/Jubatus/Analysis/{my_path}/result.txt",header = F)
head <- c("Category","Score","Name","Group")
names(dat) <- head
g <- ggplot(dat,aes(x = Group,y = Score,fill=Category))
g + geom_bar(stat = "identity",position = "dodge") + facet_wrap(~Name,ncol = 1)\
""".format(my_path=path)

f.write(string)
f.close()
