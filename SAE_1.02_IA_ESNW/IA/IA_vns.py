##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################
# Import math Library

import math
import random

from moteur_esn_wars import COST_UPGRADE


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
        self.distance_missions = []
        self.rendement_missions = []
        self.rendement_missions_global = []
        self.gain_missions = []   # mt = montant total de toutes les missions
        self.distance_missions = []  # dt = distances totals de toutes les missions
        self.energie_missions = []   # et =  energie necessaire de toutes les missions
        self.note_missions = [] 
        self.energie_cl = []
        self.distance_theorique_energy_max = 0
        self.distance_theorique_coding_level =0
        self.liste_meilleur_upgrade = []
        self.liste_upgrade_energy_max  = []
        self.liste_upgrade_coding_level = []
 

    def getInfoJoueur(self):
        print("Infos joueur : " + str(self.mon_numero) + str(self.game_dic['coders'][self.mon_numero]))

    def CalculDistanceEntreJoueurEtMissions(self):
            self.distance_missions = []
            PositionJoueurActuelle = self.game_dic['coders'][self.mon_numero]['position']
            joueur_x,joueur_y = PositionJoueurActuelle
            
            for mission in self.game_dic['missions']:
                mission_x,mission_y = mission['position']
                self.distance_missions.append((mission_x - joueur_x) + (mission_y - joueur_y)) #distance de manhattan 
                #self.distance_missions.append(math.sqrt((mission_x - joueur_x)**2 + (mission_y - joueur_y)**2)) # Distance euclidienne
    
    def ChoisisMissionLaPlusProche(self):
        meilleur_mission = min(self.distance_missions)
        return meilleur_mission
    
    def GetPositionMissionLaPlusProche(self):
        index_mission_proche = self.distance_missions.index(min(self.distance_missions))
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
    


    def ArgentEstDisponible(self):
        argent_dispo = self.game_dic['coders'][self.mon_numero]['bitcoins']
        max_energy = self.game_dic['coders'][self.mon_numero]['max_energy']
        argent_dispo = self.game_dic['coders'][self.mon_numero]['bitcoins']
        level = self.game_dic['coders'][self.mon_numero]['level']

        return argent_dispo >= ((level+1)**2)* COST_UPGRADE or argent_dispo >= ((max_energy+1)**2)* COST_UPGRADE
    
    def ArgentEstDisponiblePourLevel(self):

        argent_dispo = self.game_dic['coders'][self.mon_numero]['bitcoins']
        level = self.game_dic['coders'][self.mon_numero]['level']

        return argent_dispo >= ((level+1)**2)* COST_UPGRADE 
    
    def ArgentEstDisponiblePourEM(self):

        argent_dispo = self.game_dic['coders'][self.mon_numero]['bitcoins']
        max_energy = self.game_dic['coders'][self.mon_numero]['max_energy']

        return argent_dispo >= ((max_energy+1)**2)* COST_UPGRADE

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

    # mt = montant total de toutes les missions
    # dt = distances totals de toutes les missions
    # et =  energie necessaire de toutes les missions
    # Pour une mission donnée je calcule 
    # 1/ note entre 0 et 1 : (mi / mt) * (1 - (di/dt)) * (1 - ei/et)
    # 2/ moyenne ponderé avec un facteur entre 0 et 1 exemple : 0.6 * m + 0.3*d + 0.1*e 
    # 3/ note entre 0 et 1 : faire une moyenne entre les facteurs et divisé par 3.
    
    def CalculMontantTotalMission(self):
        self.gain_missions = []
        for mission in self.game_dic['missions']:
            starting_workload = mission['starting_workload']
            difficulte = mission['difficulty']
            gain = (starting_workload * difficulte)**2
            self.gain_missions.append(gain)
        print("Liste montants totals : " + str(self.gain_missions))

    def CalculDistanceTotalDesMissions(self):
        self.distance_missions = []
        position_joueur_actuelle = self.game_dic['coders'][self.mon_numero]['position']
        joueur_x,joueur_y = position_joueur_actuelle
        for mission in self.game_dic['missions']:
            mission_x,mission_y = mission['position']
            self.distance_missions.append(abs(mission_x - joueur_x) + abs(mission_y - joueur_y)) #distance de manhattan
        print("Liste distances totales : " + str(self.distance_missions))
        
    def CalculEnergieTotaleNécessaire(self):
        self.energie_missions = []
        for mission in self.game_dic['missions']:
            energy_necessaire = mission['difficulty']
            self.energie_missions.append(energy_necessaire)
        print("Liste energies totales nécessaires : " + str(self.energie_missions))

    def CalculClTotaleNécessaire(self):
        self.energie_cl = []
        for mission in self.game_dic['missions']:
                cl_necessaire = mission['workload']
                self.energie_cl.append(cl_necessaire)
        print("Liste energies totales nécessaires : " + str(self.energie_cl))


    def CalculNote(self):
        self.note_missions = []

        for i in range (len(self.energie_missions)):
            note = (self.energie_cl[i]/sum(self.energie_cl))*1 - (0.1*(self.gain_missions[i]/sum(self.gain_missions)))*(1 - (self.distance_missions[i]/sum(self.distance_missions)))##*((1 - *self.energie_missions[i]/sum(self.energie_missions)))
            
            self.note_missions.append(note)
        print(self.note_missions)


    def CalculMissionLaPlusRentable(self):
        
        return self.note_missions.index(max(self.note_missions)) # On retourne la mission qui est la moins couteuse et la plus proche.


    def CalculMissionLaMoinsCouteuse(self):

        self.rendement_missions = []
        for mission in self.game_dic['missions']:
            remaining_workload = mission['workload']
            difficulte = mission['difficulty']
            energie_coder = self.game_dic['coders'][self.mon_numero]['energy']
        
            # Ajouter une petite valeur à l'énergie nécessaire si elle est nulle
            energie_necessaire =  difficulte
            
            gain_potentiel = (remaining_workload * difficulte)**2
            self.rendement_missions.append(gain_potentiel / energie_necessaire)
    

    def GetCoordonéesMeilleurMission(self,best_mission_index):
        best_mission = self.game_dic['missions'][best_mission_index]
        x_mission, y_mission = best_mission['position']
        return x_mission, y_mission

    def EstSurLeJC(self):

         return self.game_dic['coders'][self.mon_numero]['position'] == (10,10)

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

        coding_level = self.game_dic['coders'][self.mon_numero]['level']
        enery_max = self.game_dic['coders'][self.mon_numero]['max_energy']

        workload = self.game_dic['missions'][best_mission_index]['starting_workload']
        difficulte = self.game_dic['missions'][best_mission_index]['difficulty']
        gain = (workload * difficulte)**2

        level_cost = ((self.game_dic['coders'][self.mon_numero]['level'] + 1) ** 2) * COST_UPGRADE
        energy_cost = ((self.game_dic['coders'][self.mon_numero]['max_energy'] + 1) ** 2) * COST_UPGRADE


        # Score pour l'amélioration du niveau de codage
        energy_score = (gain - level_cost)
     
        # Score pour l'amélioration de l'énergie
        level_score = (gain - energy_cost) 

        print(energy_score)
        print(level_score)
        

        if level_score >= energy_score and self.ArgentEstDisponiblePourLevel() and coding_level <= 7:
            return 'L'
        elif energy_score >= level_score and self.ArgentEstDisponiblePourEM() and enery_max <= 4:
            return 'EM'
        elif not self.ArgentEstDisponiblePourLevel() and not self.ArgentEstDisponiblePourEM():
            return 'P'  # Action alternative si l'argent est insuffisant pour les améliorations
        elif not self.ArgentEstDisponiblePourLevel() and enery_max <= 5:
            return 'EM'  # Action alternative si l'argent est insuffisant pour améliorer le niveau de codage
        elif not self.ArgentEstDisponiblePourEM() and coding_level <= 6:
            return 'L'  # Action alternative si l'argent est insuffisant pour améliorer l'énergie maximale
            
        
        

    
    def action(self, game_dict : dict) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif de l'état de la partie

        Returns:
            str : une action 'N', 'S', 'E', 'W', 'L', 'EM', 'P'
        """
        self.CalculMontantTotalMission()
        self.CalculDistanceTotalDesMissions()
        self.CalculEnergieTotaleNécessaire()
        self.CalculClTotaleNécessaire()
       
        self.CalculNote()
        #self.CalculDistanceEntreJoueurEtMissions() # rempli la liste de distances entre les joueurs et les missions
        #self.CalculMissionLaMoinsCouteuse() # rempli la liste de rendements par rapport a le gain / le cout

        # renvoi l'index de la mission qui a la meilleur note
        index_mission_la_plus_rentable = self.CalculMissionLaPlusRentable()
        
        # renvoi les coordonées de la mission la plus rentable
        x,y = self.GetCoordonéesMeilleurMission(index_mission_la_plus_rentable)

        # Renvoi le dx,dy a faire pour diriger le joueur vers la mission la plus proche.
        direction_tuple = self.DeplacerCoder((x,y))


        # Donne la lettre du prochain coup 
        key = self.GetProchainCoup(direction_tuple)
        
        # Si l'energie est NULL Le joueur doit retourner au job center. 
        if self.checkEnergyNull():
            print("Vous n'avez plus d'energie retour au job center")
            direction_tuple = self.RetournerAuJobCenter()
            key = self.GetProchainCoup(direction_tuple)
        
    # Si le joueur est sur le JC il doit faire une upgrade s'il a l'argent disponible. 
        """
        if self.EstSurLeJC() and self.ArgentEstDisponible():
           key = self.ChoixUpgrade(index_mission_la_plus_rentable) # Le choix de l'upgrade se fait en fonction de la mission la plus rentable et du nombre de tour que l'upgrade prend pour la finir.
        """
        
        return key
        
    
    def game_over(self, game_dict: dict) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            descr (str): descriptif du dernier tour de jeu
        """
        pass


