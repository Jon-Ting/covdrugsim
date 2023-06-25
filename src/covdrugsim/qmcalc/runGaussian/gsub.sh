#!/bin/bash
# Script to make job submission to PBS Pro Scheduler more convenient.
# Loop through all directories and submit all files with 'gsub.sh' in the name.

FILE_NAME=*.sh

return_dir () {
    echo -e "\nRETURN"
    cd ..
}

is_sh_file () {
    if [[ $1 == $FILE_NAME ]]
    then
        echo "IS $FILE_NAME, edit"
        dirpath=$(pwd)
        abspath="$dirpath/$1"
        dos2unix $abspath
        echo "Submitting"
        qsub -A UQ-SCI-SCMB $dirpath/$1  # If RCC clusters
        # qsub $dirpath/$1  # Otherwise
    else
        echo "NOT $FILE_NAME, skip" 
    fi
    echo ""
}

check_dir_file () {
    if [ -d $1 ]
    then
        echo "$1 IS dir, enter"
        echo -e "-----------\n"
        cd $1
        for more_entry in $(ls)
        do
            check_dir_file $more_entry
        done
        return_dir
    else
        echo "$1 NOT dir, what file?"
        is_sh_file $1
    fi
}

loop_check() {
    for entry in $(ls)
    do
        check_dir_file $entry
        echo "Checked $entry, next"
        echo -e "-----------\n"
    done
}

echo "Looking for $FILE_NAME files to submit to Scheduler"
echo "-----------------------------------------------------"
if [ $# -eq 0 ]
then
    loop_check
else
    for directory in "$@"
    do
        cd $directory
        loop_check
    done
fi
echo -e "Done!\n"
echo -e "Check queue\n"
qstat -aw1nt -u $USER

