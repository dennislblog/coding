# 1. take the input as filename
name=$1

# 2. create a python file
echo from typing import List > "$name".py
code "$name".py

# 3. copy test file if exists otherwise create a new one
number=${name//[^0-9]/}
testfile=$(ls test_data| grep $number\. -m 1)
cd "test_data"
if [[ $testfile ]]; then
	echo "copying existing test"
    cp "./$testfile" "../json_data/$name.json"
else
	echo "creating new test"
    cp "./template.json" "../json_data/$name.json"
fi
cd ..
code "json_data/$name".json

# 4. call in the terminal: sh create.sh 902-number-greater-n