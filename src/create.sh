# 1. take the input as filename
name=$1

# 2. create a python file
echo from typing import List > "$name".py
code "$name".py

# 3. copy test file if exists otherwise create a new one
number=${name//[^0-9]/}
testfile=$(ls test_data| grep $number\. -m 1)
if [ -e $testfile ]; then
    cp -n "test_data/$testfile" "json_data/$name".json
else
    cp -n "test_data/template.json" "json_data/$name".json
fi
code "json_data/$name".json
