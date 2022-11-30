# 18S-NemaBase
18S-NemaBase is a database dedicated to 18S rRNA sequences from nematodes. All sequences were obtained from SILVA v111 and v138. Taxonomic string corrections were based on the World Register of Marine Species (WoRMS) database. Below is the steps taken to create this database. 

## Taxonomic strings from WoRMS
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
paste v138_genera_full_taxonomy_expanded_sub.tsv v138_genera_full_taxonomy_expanded_genus_sp_fields.list 'sed 's/\t/:/g' >Final_names_list_v138.tsv
while read -r line; do accessionid=$(cut -f1 <(echo "$line")| sed 's/>//'); toreplace=$(grep -w "$accessionid" silva.fasta); sed -i "s|$toreplace.*|$line|" silva.fasta; done <Final_names_list_v138_with_accession.tsv 
```

