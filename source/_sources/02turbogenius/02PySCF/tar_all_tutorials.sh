#! /bin/bash

echo "test"

dir_list=`ls -d */`
tutorial_root=`pwd`

for dir in $dir_list
do
    cd $dir
    if [ -e ./file ]; then
    rm file.tar.gz
    find ./file -name "commands.story" | xargs rm
    find ./file -name "structure.xsf" | xargs rm
    find ./file -name "*.dat" | xargs rm
    find ./file -name "parminimized.d" | xargs rm
    find ./file -name "forces.dat" | xargs rm
    find ./file -name "Average_parameters.dat" | xargs rm
    find ./file -name "pip*" | xargs rm
    find ./file -name "out*" | xargs rm
    find ./file -name "*.out" | xargs rm
    find ./file -name "*_out" | xargs rm
    find ./file -name "*.png" | xargs rm
    find ./file -name ".DS_Store" | xargs rm
    find ./file -name "*.sh" | xargs rm
    find ./file -name "fort.10_averaged" | xargs rm
    find ./file -name "fort.10_bak" | xargs rm
    find ./file -name "fort.10_org" | xargs rm
    find ./file -name "fort.10_in" | xargs rm
    find ./file -name "fort.10_dft" | xargs rm
    find ./file -name "fort.10_pyscf" | xargs rm
    find ./file -name "fort.10_new" | xargs rm
    find ./file -name "fort.11" | xargs rm
    find ./file -name "fort.12*" | xargs rm
    find ./file -name "fort.2*" | xargs rm
    find ./file -name "kelcont*" | xargs rm
    find ./file -name "randseed*" | xargs rm
    find ./file -name "vmcopt.o*" | xargs rm
    find ./file -name "vmcopt.e*" | xargs rm
    find ./file -name "vmc.o*" | xargs rm
    find ./file -name "vmc.e*" | xargs rm
    find ./file -name "prep.o*" | xargs rm
    find ./file -name "prep.e*" | xargs rm
    find ./file -name "average_story.d" | xargs rm
    find ./file -name "story.d" | xargs rm
    find ./file -name "nodelist" | xargs rm
    find ./file -name "all_story.d" | xargs rm
    find ./file -name "lrdmc.o*" | xargs rm
    find ./file -name "lrdmc.e*" | xargs rm
    find ./file -name "job*" | xargs rm
    find ./file -name "*.pkl" | xargs rm
    find ./file -name "ave_temp" | xargs rm -r
    find ./file -name "turborvb.scratch" | xargs rm -r
    find ./file -name "parameters_graphs" | xargs rm -r
    find ./file -name ".*" | xargs rm -r
    tar -zcvf file.tar.gz file
    fi
    cd $tutorial_root
done
