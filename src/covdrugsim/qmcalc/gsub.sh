#!/bin/bash
# Script to make job submission to PBS Pro Scheduler more convenient.
# Loop through all directories and submit all files with '*.sh' (modify FILENAME for this) in the name.

FILENAME=*.sh

returnDir () {
    echo -e "\nRETURN"
    cd ..
}

# Check whether a given file matches the description of submission script (according to FILENAME) and act accordingly
isSubmitScript () {
    if [[ $1 == $FILENAME ]]
    then
        echo "IS $FILENAME, editting..."
        dirpath=$(pwd)
        abspath="$dirpath/$1"
        dos2unix $abspath  # Remove incompatible symbols from other OS system like Windows
        echo "Submitting..."
        # qsub -A UQ-SCI-SCMB $dirpath/$1  # If RCC clusters
        qsub $dirpath/$1  # Otherwise
    else
        echo "NOT $FILENAME, skipping..." 
    fi
    echo ""
}

checkDirOrFile () {
    if [ -d $1 ]
    then
        echo "$1 IS dir, enter"
        echo -e "-----------\n"
        cd $1
        for moreEntries in $(ls)
        do
            checkDirOrFile $moreEntries
        done
        returnDir
    else
        echo "$1 NOT dir, what file?"
        isSubmitScript $1
    fi
}

loopCheck() {
    for entry in $(ls)
    do
        checkDirOrFile $entry
        echo "Checked $entry, next"
        echo -e "-----------\n"
    done
}

echo "Looking for $FILENAME files to submit to Scheduler..."
echo "------------------------------------------------------"
if [ $# -eq 0 ]
then
    loopCheck
else
    for directory in "$@"
    do
        cd $directory
        loopCheck
    done
fi
echo -e "Done!\n"
echo -e "Check queue\n"
qstat -aw1nt -u $USER

