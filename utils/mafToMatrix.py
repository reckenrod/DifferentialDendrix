from collections import defaultdict

#Parses protNames.txt to get list of genes considered
#Excludes any genes in the excludes list.
def parse_genes(exclude):
    full_list = []
    with open("../Data/protNames.txt", "r") as genes_file:
        genes = genes_file.readlines()
        for gene in genes:
            gene = gene.strip()
            if gene not in exclude:
                full_list.append(gene)
    print("Collected %d genes." % len(full_list))
    return full_list

#Parses a given maf file to return mutation matrix file for Dendrix
#Excludes any genes from the exclude list.
def parse_maf(filename, genes, exclude):
    #first get mapping from each patient to their mutated genes
    mutation_sets = defaultdict(set)
    with open(filename, "r") as maf:
        for line in maf.readlines()[6:]:
            fields = line.split("\t")
            gene = fields[0]
            patient = fields[15]
            mType = fields[8]
            #print(gene, patient, mType)
            if gene in genes and mType in ["Missense_Mutation", "Nonsense_Mutation"]:
                mutation_sets[patient].add(gene)
    print("Collected %d patients in mutation matrix." % len(mutation_sets))
    
    #write mutations to a file Dendrix can use
    if len(exclude):
        filename = filename + ".exclude" + str(len(exclude))
    with open(filename + ".matrix", "w") as output:
        for k, genes in mutation_sets.iteritems():
            output.write(k)
            for gene in genes:
                output.write("\t" + gene)
            output.write("\n")

    #create mutation matrix to return to Dendrix
    #didn't end up using this
    #matrix = []
    #i = 0
    #for mutations in mutation_sets.values():
    #    matrix.append([])
    #    for gene in genes:
    #        if gene not in exclude:
    #            matrix[i].append(gene in mutations)
    #    i += 1
    #return matrix

if __name__ == "__main__":
    exclude = []
    genes = parse_genes(exclude)
    parse_maf("../Data/mafs/GBM.maf", genes, exclude)
