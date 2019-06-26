#!/bin/bash
GENEID=$1
TEST=(`~/edirect/efetch -db gene -id $GENEID -format docsum -mode xml | ~/edirect/xtract -pattern Status -element Status`)
GENEINFO=''

# get number of elements in the array
ELEMENTS=${#TEST[@]}

# echo each element in array 
# for loop

for (( i=0;i<$ELEMENTS;i++)); do

    GENEINFO+=' '${TEST[${i}]}
    
done 

echo $GENEINFO
