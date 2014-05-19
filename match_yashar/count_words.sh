while read line
do
    name=$line
    grep -c -i "$name" abstract.txt
done < $1

