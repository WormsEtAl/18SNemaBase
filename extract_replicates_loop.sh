####Dereplication script
#file input is taxonomic tree, output is list of sequences with accession numbers and taxonomic names

#!/bin/bash 

mkdir replicates
for file in *.tre
do
        set output
        sed 's/;$//' $file | sed 's/,/\n/g' | sed 's/).*$//' | grep :0.0$ | grep -v "^(" | sed 's/(//g' | sed 's/:0.0$//' >output
        cat output >"replicates/$file".reps
done 
cat replicates/* >replicates/replicate_seqsids.list
