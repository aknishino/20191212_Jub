for file in `\find Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/LearningModel -maxdepth 1 -type f`
do
    a=`basename $file`
    a=${a/\.jubatus/\.json}
    jubadump -i $file > Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/Dump/$a
    python Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/json2txt.py Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/Dump/$a
    rm Desktop/Jubatus/Learning_and_Classification/190114_HM450K_iPSvsES_D/Dump/$a
done