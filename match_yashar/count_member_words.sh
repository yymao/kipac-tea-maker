

numpapers=`grep '<summary>' data.xml | wc -l`

while read line
do
    name=$line
    #echo $name
    a=`grep -c -i "$name" ABSTRACTS_all.txt`
    bc <<< "scale=2; $a/$numpapers"
done < $1

