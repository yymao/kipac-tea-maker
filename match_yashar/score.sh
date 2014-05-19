

sed -e s/ARXIVNUMBER/$1/g get_abs1.py  > temp.py 


python temp.py > data.xml
python get_abs2.py > abstract.txt

./count_words.sh standard_keywords.txt > abstract_vector.txt

python get_score.py


rm temp.py data.xml abstract.txt abstract_vector.txt 
