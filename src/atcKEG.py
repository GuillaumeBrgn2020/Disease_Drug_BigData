def get_atc_stitch_ids_labels_dico():
    """Reads br08303.keg ATC Stitch.

    Returns:
        dico : {ATC Stitch ids : drug labels}
    """
    dico = {}

    with open("bd/br08303.keg") as f:
        line = f.readline()
        while (line != "!\n" or not line):
            line = f.readline()
        line = f.readline()[:-1]
        while (line != "!" or not line):
            line = line.split()
            
            label = ""
            for item in line[2:]:
                label = label + ' ' + str(item)
            label = label[1:]
            
            dico[line[1]] = label
            
            line = f.readline()[:-1]
            if (line == "#"):
                line = f.readline()[:-1]
            if (len(line.split()[0]) == 2):
                line = f.readline()[:-1]

    return dico

#print(get_atc_stitch_ids_labels_dico())
