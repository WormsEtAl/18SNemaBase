#!/mnt/lustre/software/linuxbrew/colsa/bin/python3

#Author: Joseph Sevigny (github: https://github.com/Joseph7e)

## give a list of taxonomic names, provides NCBIs complete taxonomy, and reduced taxonomy of all.
## Tab seperated of known taxonomy, starts at the right and tries to identify taxonomy, then moves one column left and tries again.
## -retain_right_taxon, uses the right most taxon for the species name.

import sys
from subprocess import check_output
import subprocess


def store_taxonomy(expanded_taxonomy_file):
    ''' convert taxonomy into dictionary, should add node-db'''
    tax_dict = {}
    for line in open(expanded_taxonomy_file):
        data = line.rstrip().split('\t')
        tax_dict[data[0]] = data[1:]

field_seperator = ' ' # input table field seperator, if any.
retain_species = True
skip_species = False
taxonomy_categories = ['superkingdom', 'Kingdom', 'phylum', 'subphylum', 'superclass', 'class', 'subclass', 'superorder',
         'order', 'suborder', 'infraorder', 'superfamily',
         'family', 'subfamily', 'genus', 'species', 'subspecies']
#taxonomy_categories = ['superkingdom', 'kingdom', 'phylum', 'subphylum', 'superclass', 'class', 'subclass', 'superorder', 'order', 'superfamily', 'family', 'subfamily', 'genus', 'species']
#qiime_all_level_12_categories = [superkingdom, subkingdom, sub_subkingdom, kingdom, tmp1, tmp2, phylum, subphylum, class, order, family, genus, species]
seven_levels = [1,2,5,8,12,14,15]


input_table = sys.argv[1] # tab seperated list of taxon names, broad -> specific.
output_full = open(input_table.split('.')[0]+'_full_taxonomy_expanded.tsv','w')
output_reduced = open(input_table.split('.')[0]+'_eight-levels_taxonomy_expanded.tsv','w')

ncbi_taxonomy = "/home/genome/shared/mito-sequence-reference/taxonomy-corrected-database/combined_ncbi_and_worms_taxonomy.tsv" # sys.argv[2]


def grep_search(search_term, file):
    if search_term == '\tBacteria\t':
        search_term = 'Bacteria\t'
    ''' given a search term, grep into the file and return first line matched)'''
    term = '"' + search_term + '"'
    command = ['grep','-m', '1', '-i', '-P', search_term, file]
    #print (' '.join(command))
    #output = check_output(command)
    try:
        output,error  = subprocess.Popen(
                        command, universal_newlines=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()        # print ("output:", output)
        # print ("error", error)
        return output
    except subprocess.CalledProcessError:
        print ("ERROR:ERROR")
        sys.exit()
    #output = p.stdout.read()

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x.strip() for x in seq if not (x.strip() in seen or seen_add(x.strip()))]


for line in open(input_table):
    print (line)
    if line.strip(): # ignore blank lines
        elements = line.lstrip().rstrip().split(field_seperator)
        complete_input = ':'.join(elements)
        species = elements[-1]
        print (elements)
        best_match = ''
        if skip_species:
            del elements[-1]
        for tax in reversed(elements):
            tax = tax.rstrip().lstrip()
            if best_match != '':
                break
            tax = tax.strip()
            search_terms = []
            ####### deal with weird sp names
            if '_' in tax:
                genus, sp = tax.split('_')
                fixed = sp.replace('.','').replace("sp","").rstrip()
                search_terms.append(genus + " " + fixed)
                search_terms.append(genus)
            elif '-' in tax:
                genus, sp = tax.split('-')
                fixed = sp.replace('.','').replace("sp","").rstrip()
                search_terms.append(genus + " " + fixed)
                search_terms.append(genus)
            elif ' ' in tax:
                genus, sp = tax.split(' ')[:2]
                fixed = sp.replace('.','').replace("sp","").rstrip()
                search_terms.append(genus + " " + fixed)
                search_terms.append(genus)
            else:
                search_terms.append(tax)
            #print (search_terms)
            search_terms = f7(search_terms)
            #print (search_terms)
            ##################################
            for search_term in search_terms: # perfrom the search
                print ("searching for", search_term)
                search_term = search_term
                if " " in search_term:
                    search_term = "\t" + search_term
                else:
                    search_term = "\t" + search_term + "\t"
                #print ("search term:", search_term)
                match = grep_search(search_term,ncbi_taxonomy)
                if match.strip():
                    best_match = match.rstrip()
                    break
        #print ("Best Match: ", best_match)
        output_full_line = complete_input + '\t' + search_term + '\t'
        output_seven_line = complete_input + '\t' + search_term + '\t'
        print (best_match)
        if best_match:
            best_match_data = best_match.rstrip().split('\t')
            code = best_match_data[0]
            best_taxonomy = best_match_data[1:]
            if retain_species:
                best_taxonomy[-1] = species
            output_full_line += code + '\t' + '\t'.join(best_taxonomy)
            output_seven_line += code + '\t' + '\t'.join([best_taxonomy[i] for i in seven_levels])
        else:
            output_full_line +=  'NULL\tUNKNOWN'
            output_seven_line += 'NULL\tUNKNOWN'
        output_full.writelines(output_full_line + '\n')
        output_reduced.writelines(output_seven_line + '\n')
        #print (output_full_line)
        #print (output_seven_line)
