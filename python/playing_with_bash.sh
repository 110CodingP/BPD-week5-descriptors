output=$(openssl version -d)
dir=$(echo ${output:13:-1})
echo $dir