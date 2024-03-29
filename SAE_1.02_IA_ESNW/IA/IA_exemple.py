##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################
# Import math Library

import math
import random


from moteur_esn_wars import COST_UPGRADE, Mission

class Coder:
    def __init__(self):
        self.position = (None, None)
        self.level = 1
        self.energy = 1
        self.max_energy = 1
        self.bitcoins = 0

class Mission:
    def __init__(self, position, starting_workload, workload, difficulty, cooldown = 0):
        self.position = tuple(position)
        self.starting_workload = starting_workload
        if workload:
            self.workload = workload
        else:
            self.workload = starting_workload
        self.difficulty = difficulty
        self.cooldown = cooldown
        self.closestCoderDistance=1E6

    def __str__(self):
        return str(self.__dict__)
DIRECTIONS = {'N':(0,-1), 'S':(0,1), 'E':(1,0), 'W':(-1,0)}
class IA_ESNW:
    
    def __init__(self, num_joueur : int, game_dic : dict) -> None:
        

        """génère l'objet de la classe IA_ESNW

        Args:
            desc (str): descriptif de l'état initial de la partie
            num_joueur (int): numéro de joueur attribué à l'IA
        """
        self.current_mission = None
        
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
                
        self.coders = []
        self.missions = []
        self.from_dict(game_dict)
        self.me = self.coders[self.mon_numero]
        
        #grid size param
        self.PrintGame(21)
        
        # Si l'energie est NULL Le joueur doit retourner au job center. 
        if self.me.energy <= 0:
            print("Vous n'avez plus d'energie retour au job center")
            direction_tuple = self.RetournerAuJobCenter()
        else:
            if self.current_mission != None:
                print("Vous avez atteint votre mission : " + str(self.current_mission.position))
                if self.IsOnMission(self.current_mission):
                    self.current_mission = None
                else:
                    print("Vous aller vers votre mission : " + str(self.current_mission.position))
                    direction_tuple = self.GetMoveMeToPosition(self.current_mission.position)
            
            if self.current_mission == None:
                self.current_mission = self.StrategyIsSucceedAllMissions()
                print("Vous avez une mission : " + str(self.current_mission.position))
                direction_tuple = self.GetMoveMeToPosition(self.current_mission.position)
           
        key = self.GetProchainCoup(direction_tuple)
        return key
       
    def from_dict(self, game_dict):
        for coder_data in game_dict.get('coders', []):
            coder = Coder()
            coder.position = coder_data['position']
            coder.level = coder_data['level']
            coder.energy = coder_data['energy']
            coder.max_energy = coder_data['max_energy']
            coder.bitcoins = coder_data['bitcoins']
            self.coders.append(coder)

        for mission_data in game_dict.get('missions', []):
            mission = Mission(**mission_data)
            self.missions.append(mission)
        
    # Retourne la mission qui est à la fois atteignable à 100%
    # et qui a le gain max
    def StrategyIsSucceedAllMissions(self):

        for mission in self.missions:
            for coder in self.coders:
                if not (coder == self.me):
                    if self.CanEvaluateMission(mission, coder):
                        if (self.Distance(mission, coder) < mission.closestCoderDistance):
                            mission.closestCoderDistance = self.Distance(mission, coder)

        gainMax=0             
        bestMission= None
        for mission in self.missions:
            if self.CanEvaluateMission(mission, self.me) and self.IsMissionValid(mission):
                # Ma distance à la mission est la plus petite ou égale à celle des autres
                # Mais c'est mon tour...
                if (mission.closestCoderDistance >= self.Distance(mission, self.me)): 
                    if (self.GainMission(mission) > gainMax):
                        bestMission = mission
                        gainMax = self.GainMission(mission)
                        
        if (bestMission == None):
             for mission in self.missions:
                if self.CanEvaluateMission(mission, coder) and self.IsMissionValid(mission):
                    if (self.Distance(mission, coder) < mission.closestCoderDistance):
                       bestMission = mission
        
        return bestMission                

    
    def RetournerAuJobCenter(self):
        self.current_mission = None
        job_center_position = (10, 10)  # Position du job center (à adapter)
        return self.GetMoveMeToPosition(job_center_position)

    def IsCoderMyself(self, coder):
        return (self.coders[self.mon_numero] == coder)
 
    def GainMission(self, mission):
        return (mission.starting_workload * mission.difficulty)**2
        
    def CoutMission(self, mission, coder):
        return (mission.difficulty * self.Distance(mission,coder))
 
    def Distance(self, mission, coder):
        return (abs(mission.position[0] - coder.position[0]) + abs(mission.position[1] - coder.position[1]))
 
    def CanEvaluateMission(self, mission, coder):
        return (coder.energy >= mission.difficulty)
   
    def IsMissionValid(self, mission):
        return (mission.workload >= 0)
  
    def IsOnJobCenter(self, coder):
        return self.me.position == (10,10)
   
    def IsOnMission(self, mission):
        return self.me.position == mission.position

    def GetMoveMeToPosition(self, position):
            coder_dx = 0
            coder_dy = 0

            coder_x, coder_y = self.me.position
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
    
    def PrintGame(self, grid_size):

        # Initialisation de la grille vide
        grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

        # Placement des joueurs sur la grille
        for coder in self.coders:
            x,y = coder.position
            if 0 <= x < grid_size and 0 <= y < grid_size:
                grid[y][x] = 'P'
                if coder.position == self.me.position:
                    grid[y][x] = 'X'
    
        # Placement des missions sur la grille
        for mission in self.missions:
            x,y = mission.position
            if 0 <= x < grid_size and 0 <= y < grid_size:
                grid[y][x] = str(mission.workload)
                if self.current_mission != None and mission.position == self.current_mission.position:
                    grid[y][x] = 'O'

        # Affichage de la grille dans la console
        for row in grid:
            print(' '.join(row))
        

    def game_over(self, game_dict: dict) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            descr (str): descriptif du dernier tour de jeu
        """
        pass


