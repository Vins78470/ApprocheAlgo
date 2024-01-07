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
        self.distance_aller_retour = 0
        self.liste_distance = []
        self.liste_rendement = []
        self.liste_rendement_global = []
        self.liste_meilleur_upgrade = []
        self.distance_theorique_energy_max = 0
        self.distance_theorique_coding_level =0
        self.liste_upgrade_energy_max  = []
        self.liste_upgrade_coding_level = []

    def getInfoJoueur(self):
        print("Infos joueur : " +str(self.mon_numero) + str(self.game_dic['coders'][self.mon_numero]))

    def CalculDistanceEntreJoueurEtMissions(self):
            self.liste_distance = []
            PositionJoueurActuelle = self.game_dic['coders'][self.mon_numero]['position']
            joueur_x,joueur_y = PositionJoueurActuelle
            
            for mission in self.game_dic['missions']:
                mission_x,mission_y = mission['position']
                self.liste_distance.append(math.sqrt((mission_x - joueur_x)**2 + (mission_y - joueur_y)**2))
    
    def ChoisisMissionLaPlusProche(self):
        meilleur_mission = min(self.liste_distance)
        return meilleur_mission
    
    def GetPositionMissionLaPlusProche(self):
        index_mission_proche = self.liste_distance.index(min(self.liste_distance))
        mission_x,mission_y = self.game_dic['missions'][index_mission_proche]['position']
        print(mission_x,mission_y)
        return mission_x,mission_y

    def GetProchainePosition(self):
        PositionJoueurActuelle = self.game_dic['coders'][self.mon_numero]['position']
        joueur_x,joueur_y = PositionJoueurActuelle
        mission_x,mission_y = self.GetPositionMissionLaPlusProche()
        #mission_x,mission_y = self.GetCoordonéesMeilleurMission()
        x_deplacement = mission_x - joueur_x
        y_deplacement = mission_y - joueur_y
        
             # Vérification pour éviter la division par zéro
        if abs(x_deplacement) > abs(y_deplacement) and x_deplacement != 0:
            x_deplacement_normalise = int(x_deplacement / abs(x_deplacement))
            y_deplacement_normalise = 0
        elif y_deplacement != 0:
            x_deplacement_normalise = 0
            y_deplacement_normalise = int(y_deplacement / abs(y_deplacement))
        else:
            # Si les deux déplacements sont nuls, aucune division n'est nécessaire
            x_deplacement_normalise = 0
            y_deplacement_normalise = 0
        
        print(x_deplacement_normalise,y_deplacement_normalise)
        return x_deplacement_normalise,y_deplacement_normalise

    def GetProchainCoup(self,prochain_coup):
        for key,value in DIRECTIONS.items():
            if value == prochain_coup:
                return key
   
    def checkEnergyNull(self):
      if self.game_dic['coders'][self.mon_numero]['energy']<= 0:
          return True
    
    def RetournerAuJobCenter(self):
        job_center_position = (10, 10)  # Position du job center (à adapter)
        return self.DeplacerCoder(job_center_position)
        
    def DeplacerCoder(self, position):
        coder_dx = 0
        coder_dy = 0

        coder_x, coder_y = self.game_dic['coders'][self.mon_numero]['position']
        dest_x, dest_y = position

        # Calculer les différences sur chaque axe pour déterminer la direction du déplacement
        diff_x = dest_x - coder_x
        diff_y = dest_y - coder_y

        # Effectuer le déplacement en mettant à jour la position du coder
        if abs(diff_x) > abs(diff_y):
            # Mouvement horizontal prédominant
            if diff_x > 0:
                coder_dx = 1
            elif diff_x < 0:
                coder_dx = -1
        else:
            # Mouvement vertical prédominant
            if diff_y > 0:
                coder_dy = 1
            elif diff_y < 0:
                coder_dy = -1
        
         # Convertir les différences en tuple pour les utiliser comme clé dans le dictionnaire de directions
        direction_tuple = (coder_dx, coder_dy)

        return direction_tuple


    def CalculMissionLaPlusRentable(self):

        self.liste_rendement_global = []

        for i in range(len(self.liste_rendement)):
            self.liste_rendement_global.append(self.liste_rendement[i] - self.liste_distance[i])
            
        print(self.liste_rendement_global)
        return self.liste_rendement_global.index(max(self.liste_rendement_global)) # On retourne la mission qui est la moins couteuse et la plus proche.


    def CalculMissionLaMoinsCouteuse(self):

        self.liste_rendement = []
        for mission in self.game_dic['missions']:
            remaining_workload = mission['workload']
            difficulte = mission['difficulty']
            energie_coder = self.game_dic['coders'][self.mon_numero]['energy']
        
            # Ajouter une petite valeur à l'énergie nécessaire si elle est nulle
            energie_necessaire = max(1, energie_coder - difficulte)
            
            gain_potentiel = (remaining_workload * difficulte)**2
            self.liste_rendement.append(gain_potentiel / energie_necessaire)
    

    def GetCoordonéesMeilleurMission(self,best_mission_index):
        best_mission = self.game_dic['missions'][best_mission_index]
        x_mission, y_mission = best_mission['position']
        return x_mission, y_mission

    def EstSurLeJC(self):
       return self.game_dic['coders'][self.mon_numero]['position'] == (10,10)

    def CalculRoundNecessairePourFinirMission(self,best_mission_index):
        

        self.liste_upgrade_energy_max.append(self.ScoreEnergyMax(best_mission_index))
        self.liste_upgrade_coding_level.append(self.ScoreCodingLevel(best_mission_index))
        self.liste_meilleur_upgrade = max(len(self.liste_upgrade_energy_max ),len(self.liste_upgrade_coding_level))

        print(self.liste_meilleur_upgrade)


    def ScoreEnergyMax(self,best_mission_index):
         
         self.game_dic['coders'][self.mon_numero]['max_energy'] += 1 

         if self.game_dic['missions'][best_mission_index]['workload'] != 0:
            self.distance_theorique_energy_max += 1
         self.game_dic['coders'][self.mon_numero]['max_energy'] -= 1 
         return self.distance_theorique_energy_max

    def ScoreCodingLevel(self,best_mission_index):
        self.game_dic['coders'][self.mon_numero]['level'] += 1

        if self.game_dic['missions'][best_mission_index]['workload'] != 0:
            self.distance_theorique_coding_level += 1

        self.game_dic['coders'][self.mon_numero]['level'] -= 1
        return self.distance_theorique_coding_level

    def ChoixUpgrade(self,best_mission_index):
        coder = self.game_dic['coders'][self.mon_numero]
        level_cost = self.game_dic['coders'][self.mon_numero]['level'] ** 2 
        energy_cost = (self.game_dic['coders'][self.mon_numero]['max_energy'] + 1) ** 2 

        # Score pour l'amélioration du niveau de codage
        energy_score = level_cost/self.ScoreEnergyMax(best_mission_index)
     
        # Score pour l'amélioration de l'énergie
        level_score = energy_cost/self.ScoreCodingLevel(best_mission_index)

        if level_score >= energy_score:
            return 'L'
        else:
            return 'EM'

    
    def action(self, game_dict : dict) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif de l'état de la partie

        Returns:
            str : une action 'N', 'S', 'E', 'W', 'L', 'EM', 'P'
        """

        self.CalculDistanceEntreJoueurEtMissions() # rempli la liste de distances entre les joueurs et les missions

        self.CalculMissionLaMoinsCouteuse() # rempli la liste de rendements par rapport a le gain / le cout

        # renvoi l'index de la mission qui a la meilleur difference entre rendements moins couteux et distance la plus proche
        index_mission_la_plus_rentable = self.CalculMissionLaPlusRentable()
        
        # renvoi les coordonées de la mission la plus rentable
        x,y = self.GetCoordonéesMeilleurMission(index_mission_la_plus_rentable)

        # Renvoi le dx,dy a faire pour diriger le joueur vers la mission la plus proche.
        direction_tuple = self.DeplacerCoder((x,y))


        # Donne la lettre du prochain coup 
        key = self.GetProchainCoup(direction_tuple)
        

        if self.checkEnergyNull():
            print("Vous n'avez plus d'energie retour au job center")
            direction_tuple = self.RetournerAuJobCenter()
            key = self.GetProchainCoup(direction_tuple)
        
        if self.EstSurLeJC():
            self.CalculRoundNecessairePourFinirMission(index_mission_la_plus_rentable)
            self.ChoixUpgrade(index_mission_la_plus_rentable)
        
        return key
        
    
    def game_over(self, game_dict: dict) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            descr (str): descriptif du dernier tour de jeu
        """
        pass


