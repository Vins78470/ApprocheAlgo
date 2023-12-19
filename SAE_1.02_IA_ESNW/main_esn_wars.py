##############################################################################
# main ESN WARS                                                              #
##############################################################################

# Dans ce fichier que vous pouvez compléter vous lancez vos expérimentations

from moteur_esn_wars import partie

#spécifiez le nom d'un fichier contenant une IA se trouvant dans le dossier IA
#spécifiez le nom d'une map se trouvant dans le dossier map

if __name__ == '__main__':
    partie(['IA_aleatoire', 'IA_aleatoire', 'IA_aleatoire', 'IA_aleatoire'], "map1.txt")
