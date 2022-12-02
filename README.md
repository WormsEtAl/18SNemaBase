# 18S-NemaBase
18S-NemaBase is a database dedicated to 18S rRNA sequences from nematodes. All sequences were obtained from SILVA v111 and v138. Taxonomic string corrections were based on the World Register of Marine Species (WoRMS) database. Below is the steps taken to create this database. 

##  Correct Taxonomic String 
### Taxonomic strings from WoRMS
Taxonomic strings were pulled from WoRMS based on a code written by Joe Sevigny (https://github.com/Joseph7e), 
[Correct_ncbi_based_on_worms.py](https://github.com/Joseph7e/Nematode-Mitochondrial-Metagenomics/blob/main/correct_ncbi_based_on_worms.py).

```
python3 correct_ncbi_based_on_worms.py
```
### Isolate Nematode Sequences in SILVA
Download [SILVA v138 Ref NR 99](https://www.arb-silva.de/download/arb-files/). Isolate nematode sequences:

```
grep Nematoda seq_file_name.fasta > seq_ID_list.fasta
```
### Match Genus from SILVA to Corect Taxonomy from WoRMS
Extract genus names and accession numbers from SILVA v138

```
Awk -F”;” ‘{print $(NF-2), $(NF-1)}’ seq_ID_list.fasta | sed ’s/__//g’ >genus_list.fasta
```

Use custom script ([taxonToFullTaxonomy-revised.py](18SNemaBase/taxonToFullTaxonomy-revised.py)) to match WoRMS taxonomic string to genus name

```
python3 taxonToFullTaxonomy-revised.py ./genus_list.fasta >correct_taxonomic_strings.fasta
```

Check to make sure you only have nematodes. Export to excel to make sure all strings are correct. 

### Replace Taxonomy in SILVA
Isolate taxonomy

```
cut -f6- v138_genera_full_taxonomy_expanded.fasta >v138_genera_full_taxonomy_expanded_sub.fasta
```

Match the correct taxonomic string to sequence based on accession number 

```
paste v138_genera_full_taxonomy_expanded_sub.tsv v138_genera_full_taxonomy_expanded_genus_sp_fields.list 'sed 's/\t/:/g' >Final_names_list_v138.fasta
while read -r line; do accessionid=$(cut -f1 <(echo "$line")| sed 's/>//'); toreplace=$(grep -w "$accessionid" silva.fasta); sed -i "s|$toreplace.*|$line|" silva.fasta; done <Final_v138_for_NemaBase.fasta 
```

Repeat all steps with SILVA v111.
Concatenate both versions

```
cat Final_v138_for_NemaBase.fasta Final_v111_for_NemaBase.fasta >Final_all_silva_db.fasta >18SNemaBase.fasta
```

## Quality Assurance
### Dereplication
Sequences from the database were aligned, placed on a phylogenetic tree, and dereplicated to prevent redundancy in the database. 
Dereplication can be done with the alignment. We choose to use trees as they provide adjusted alignment predictions based a model. Both methods yield the same results. Alignments and phylogenetic trees were created for Enoplida and Dorylaimida. Chromadorida was further broken into sub orders for analysis. An example with Enoplida is below. 

Isolate Enoplida sequences with [seqtk](https://github.com/lh3/seqtk). 

```
grep "Enoplida" 18SNemaBase.fasta >Enoplida_names.fasta
seqtk subseq Enoplida_names.fasta Final_all_silva_db.fasta >Enoplida_seqs.txt
```

Alignment with [Muscle](https://2018-03-06-ibioic.readthedocs.io/en/latest/install_muscle.html).

```
muscle -in Enoplida_seqs.txt -out Aligned_Enoplida.fasta
```

Make a phylogenetic tree with [FastTree](https://www.metagenomics.wiki/tools/phylogenetic-tree/construction/fasttree)

```
FastTree -nt -gtr Aligned_Enoplida.fasta >Enoplida_tree.tre
```

Custom dereplication script ([extract_replicates_loop.sh](https://github.com/WormsEtAl/18SNemaBase/blob/main/extract_replicates_loop.sh))

```
extract_replicates_loop.sh Enoplida_tree.tre Enoplida_derep.fasta
```

Review output and remove sequences that are exact replicate (i.e. same sequence and same species or subspecies name).
Review tree for sequences that may be out of place. Check all misplaced sequences against 18S-NemaBase, SILVA, and NCBI Blast to ensure these are erroneous.
Remove replicates and erroneos sequence

## Customize the database
The final database is supplied as a fasta file that can be manually added to in most text editors. 
If prefered the file can also be concatenated with custom sequence file. Ex:

```
cat 18SNemaBase.fasta Sanger-sequenced_full_18S.fasta >Final_all_silva_db.fasta >18SNemaBase-supplemented.fasta
```






