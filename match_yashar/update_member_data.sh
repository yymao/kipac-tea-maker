
rm data/*
while read line
do
    name=$line

    sed -e s/AUTHOR/$name/g get_from_arxiv.py > temp.py 
    python temp.py > data.xml
    python abstracts.py > ABSTRACTS_all.txt 
    ./count_member_words.sh standard_keywords.txt > data/$name.txt

done < author_list.txt


rm temp.py data.xml ABSTRACTS_all.txt 
