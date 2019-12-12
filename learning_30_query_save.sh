# 同じデータセットを使って、合計300回の学習をする。
# 10回の学習を終える毎に、多値分類と学習モデルの保存を行う。

for i in `seq 30`
do
    python /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/learning.py /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/config_learning.txt 10 $i
    a=`expr $i \* 10`
    python /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/query.py /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/config_query.txt $a
    python /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/save.py
done

bash /home/jubatusserver/Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/dump.sh