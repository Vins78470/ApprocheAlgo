##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################
import math
import random


class IA_ESNW:

    def __init__(self, num_joueur : int, game_dic : dict) -> None:
        self.num_joueur = num_joueur
        self.game_dic = game_dic
        self.mission_distances = {} 
        """génère l'objet de la classe IA_ESNW

        Args:
            desc (str): descriptif de l'état initial de la partie
            num_joueur (int): numéro de joueur attribué à l'IA
        """

        print("IA num", num_joueur,"chargée : OK" )

        
    def get_mission_distance(self):
        """Repérer les missions stratégiques dans game_dict"""

        # Accès aux informations des missions depuis game_dict
        missions = self.game_dic['missions']
        coders = self.game_dic['coders']

        # Récupération de la position de l'IA
        x_self, y_self = coders[self.num_joueur - 1]['position']

        # Initialisation du dictionnaire de distances
        distances = {}

        # Calcul des distances pour toutes les missions et stockage dans le dictionnaire
        for mission_info in missions:
            x_mission, y_mission = mission_info['position']
            distance = math.sqrt((x_mission - x_self)**2 + (y_mission - y_self)**2)
            distances[mission_info['symbol']] = distance

        self.mission_distances = distances
        print(self.mission_distances)

    def chooseNextPosition(self):
        distance_min = min(self.mission_distances.values())
        # Chercher la clé correspondante à la valeur recherchée
        for cle, valeur in self.mission_distances.items():
            if valeur == distance_min:
                print("La mission la plus proche est la est la :", cle)
                break  # Arrêter la recherche une fois la clé trouvée
    
    def GetPosition():
        for key,value in  
        # Calcul du décalage en soustrayant les coordonnées de la mission par rapport à celles du joueur
        decalage_x = position_mission[0] - position_joueur[0]
        decalage_y = position_mission[1] - position_joueur[1]

    def GetClosestPos():
        pass

    def action(self, game_dict : dict) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif de l'état de la partie

        Returns:
            str : une action 'N', 'S', 'E', 'W', 'L', 'E', 'P'
        """

        ####################################################
        #ICI il FAUT compléter et faire votre versions !   #
        ####################################################
        
        return ['N', 'S', 'E', 'W', 'L', 'E', 'P'][random.randint(0,6)]



    def game_over(self, game_dict: dict) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            descr (str): descriptif du dernier tour de jeu
        """
        pass
