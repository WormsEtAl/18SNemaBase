# 18S-NemaBase
18S-NemaBase is a database dedicated to 18S rRNA sequences from nematodes. All sequences were obtained from SILVA v111 and v138. Taxonomic string corrections were based on the World Register of Marine Species (WoRMS) database. Below is the steps taken to create this database. 

## Taxonomic strings from WoRMS
Taxonomic strings were pulled from WoRMS based on a code written by Joe Sevigny (https://github.com/Joseph7e)

```
python3 correct_ncbi_based_on_worms.py
```

[Correct_ncbi_based_on_worms.py](Joseph7e/Nematode-Mitochondrial-Metagenomics/correct_ncbi_based_on_worms.py) is a custome script that pulls taxonomic 
