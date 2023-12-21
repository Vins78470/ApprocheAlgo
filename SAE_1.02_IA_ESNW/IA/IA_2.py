##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################
import math
import random

class IA_ESNW:
    def __init__(self, num_joueur : int, game_dic : dict) -> None:
        """génère l'objet de la classe IA_ESNW

        Args:
            desc (str): descriptif de l'état initial de la partie
            num_joueur (int): numéro de joueur attribué à l'IA
        """

        print("IA num", num_joueur,"chargée : OK" )
        pass

   

    def reperer_mission_la_plus_proche(self, game_dict):
        """Repérer les missions stratégiques dans game_dict"""

        # Accès aux informations des missions depuis game_dict
        missions = game_dict['missions']
        coders = game_dict['coders']

        # Récupération de la position de votre IA
        x_self, y_self = coders[self.num_joueur - 1]['position']

        # Calcul des distances pour toutes les missions
        distances = {}
        for idx, mission_info in enumerate(missions):
            x_mission, y_mission = mission_info['position']
            distance = math.sqrt((x_mission - x_self)**2 + (y_mission - y_self)**2)
            distances[idx] = distance

        # Tri des missions par distance
        sorted_missions = sorted(distances.items(), key=lambda x: x[1])

        # Sélection des missions les plus proches
        closest_missions = []
        for mission_idx, distance in sorted_missions:
            closest_missions.append(mission_idx)

        return closest_missions


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
