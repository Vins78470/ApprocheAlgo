##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################
# Import math Library

import math
import random

DIRECTIONS = {'N':(0,-1), 'S':(0,1), 'E':(1,0), 'W':(-1,0)}
class IA_ESNW:
    def __init__(self, num_joueur : int, game_dic : dict) -> None:
        """génère l'objet de la classe IA_ESNW

        Args:
            desc (str): descriptif de l'état initial de la partie
            num_joueur (int): numéro de joueur attribué à l'IA
        """

        print("IA num", num_joueur,"chargée : OK" )
        self.mon_numero = num_joueur
        self.game_dic = game_dic
        self.liste_distance = []


    def getInfoJoueur(self):
        print("Infos joueur : " +str(self.mon_numero) + str(self.game_dic['coders'][self.mon_numero]))

    def CalculDistanceEntreJoueurEtMissions(self):
            
            self.liste_distance = []
            PositionJoueurActuelle = self.game_dic['coders'][self.mon_numero]['position']
            joueur_x,joueur_y = PositionJoueurActuelle
            
            for mission in self.game_dic['missions']:
                mission_x,mission_y = mission['position']
                self.liste_distance.append(math.sqrt((mission_x - joueur_x)**2 + (mission_y - joueur_y)**2))
    
    def ChoisisMeilleurMission(self):
        meilleur_mission = min(self.liste_distance)
        print(meilleur_mission)
    
    def GetPositionMissionLaPlusProche(self):
        index_mission_proche = self.liste_distance.index(min(self.liste_distance))
        mission_x,mission_y = self.game_dic['missions'][index_mission_proche]['position']
        print(mission_x,mission_y)
        return mission_x,mission_y

    def GetProchainePosition(self):
        PositionJoueurActuelle = self.game_dic['coders'][self.mon_numero]['position']
        joueur_x,joueur_y = PositionJoueurActuelle
        mission_x,mission_y = self.GetPositionMissionLaPlusProche()
        x_deplacement = mission_x - joueur_x
        y_deplacement = mission_y - joueur_y
        norme_vecteur = math.sqrt(x_deplacement**2 + y_deplacement**2) # On normalise le vecteur pour avoir un deplacement de 1 en 1.
        norme_vecteur=int(norme_vecteur)

        x_deplacement_normalise = int(x_deplacement / norme_vecteur)
        y_deplacement_normalise =int(y_deplacement / norme_vecteur)
        print(x_deplacement_normalise,y_deplacement_normalise)
        return x_deplacement_normalise,y_deplacement_normalise

    def GetProchainCoup(self,prochain_coup):
        for key,value in DIRECTIONS.items():
            if value == prochain_coup:
                return key

    def action(self, game_dict : dict) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif de l'état de la partie

        Returns:
            str : une action 'N', 'S', 'E', 'W', 'L', 'EM', 'P'
        """
        
        self.getInfoJoueur()
        self.CalculDistanceEntreJoueurEtMissions()
        print(self.liste_distance)
        self.ChoisisMeilleurMission()
        self.GetPositionMissionLaPlusProche()
        prochain_position_coup = self.GetProchainePosition()
        key = self.GetProchainCoup(prochain_position_coup)
        return key
        



    def game_over(self, game_dict: dict) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            descr (str): descriptif du dernier tour de jeu
        """
        pass


