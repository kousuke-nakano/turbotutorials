#! /bin/bash

echo "test"

dir_list=`ls -d */`
tutorial_root=`pwd`

for dir in $dir_list
do
    cd $dir
    if [ -e ./file ]; then
    rm file.tar.gz
    find ./file -name ".DS_Store" | xargs rm
    find ./file -name "fort.11" | xargs rm
    find ./file -name "fort.12*" | xargs rm
    find ./file -name "fort.21*" | xargs rm
    find ./file -name "kelcont*" | xargs rm
    find ./file -name "randseed*" | xargs rm
    find ./file -name "turborvb.scratch" | xargs rm -r
    tar -zcvf file.tar.gz file
    fi
    cd $tutorial_root
done

