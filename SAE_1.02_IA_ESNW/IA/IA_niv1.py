##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

import random
from moteur_esn_wars import * 
from math import * 




#############################################################################################################################
#IMPORTANT : 'game_dic' est un dictionnaire fixe (qui ne se met pas à jour lors de la partie                                #     
#             ex: il va garder (10,10) comme position pour tout les joueurs tout le long de la partie                       #
#            'game_dict' est undictionnaire flexible (qui se met à jour lors de la partie)                                  #
#             ex: il va mettre à jour les nouvelles position des joueurs lors de la partie                                  #
#############################################################################################################################




class IA_ESNW:

    def __init__(self, num_joueur : int, game_dic : dict) -> None:
    
        #####################################################################################################################
        #génère l'objet de la classe IA_ESNW                                                                                #
        #                                                                                                                   #
        #Args:                                                                                                              #
        #    desc (str): descriptif de l'état initial de la partie                                                          #
        #    num_joueur (int): numéro de joueur attribué à l'IA                                                             #
        #####################################################################################################################
        
        
        
        
        print("IA num", num_joueur,"chargée : OK" )
        
        
        """
        pour récuperer le numéro de notre IA, et donc son indice dans la liste de la clé "coders" (définie plus tard dans le code)
        """
        self.numero_joueurIA = num_joueur
       

        """
        récupération des coordonnées x et y du JC
        """
        self.JC_x = JC[0]
        self.JC_y = JC[1]
   
   
        """
        définition d'une liste 'liste_missions',
        va dans le dictionnaire 'game_dic' à la clé "missions" (dont la valeur est une liste)
        PS : la liste est définitive et ne se met pas à jour (liste fixe)
        """
        self.liste_missions = game_dic['missions']
            

   
   
    def mission_plus_proche(self):
    
        ######################################################################################################################
        #Cette méthode va comparer la distance entre les missions et l'IA (qui se situe au JC);                              #
        #puis va retourner la plus proche (sous forme de tuple de coordonnées) ainsi que son workload (un float)             #                                            
        ######################################################################################################################
        
        
        

        """
        initialisation de la première mission dans la liste 'liste_missions' comme celle étant la plus proche 'self.mission_proche_position'
        """
        self.mission_proche_position = self.liste_missions[0]['position']
        
        
        """
        initialisation du workload 'self.mission_proche_Sworkload' appartenant à la mission la plus proche initialisée au dessus ('self.mission_proche_position')
        PS: ce workload n'est pas mis à jour, il est fixe (car il est issu de la liste 'self.liste_missions')
        """
        self.mission_proche_Sworkload = self.liste_missions[0]['starting_workload']
        
        
        
        """
        comparaison des distances des missions présentes dans la liste 'liste_missions' par rapport au JC,
        avec l'utilisation de la formule en Math qui sert à calculer la distance entre 2 points,
        on fait à partir de 1 car la mission qui se trouve à l'indice 0 à déjà été initialisée au dessus ('self.mission_proche_position') 
        """
        for i in range(1,len(self.liste_missions)):    
            """
            si la distance entre notre IA et une mission présente dans la liste 'self.liste_missions' est inférieur à celle entre notre IA et celle initilaisée,
            alors elle devient la nouvelle mission la plus proche 'self.mission_proche_position'
            """        
            if sqrt((self.liste_missions[i]['position'][0] - self.JC_x)**2 + (self.liste_missions[i]['position'][1] - self.JC_y)**2) < sqrt((self.mission_proche_position[0] - self.JC_x)**2 + (self.mission_proche_position[1] - self.JC_y)**2):
                self.mission_proche_position = self.liste_missions[i]['position']
                self.mission_proche_Sworkload = self.liste_missions[i]['starting_workload']             
        return self.mission_proche_position, self.mission_proche_Sworkload
    
    
    
    
    def mission_gros_gain(self):
    
        ######################################################################################################################
        #Cette méthode va comparer la difficultés des missions;                                                              #
        #puis va retourner celle qui possède la plus haute (sa position), sa difficulté et son workload                      #
        ######################################################################################################################
        
        
        
        
        """
        initialisation de la position de la première mission de la liste 'self.liste_missions' comme celle étant la plus prospère ('self.mission_fortune_position')
        """
        self.mission_fortune_position = self.liste_missions[0]['position']
        
        """
        initialisation de la première mission dans la liste 'self.liste_missions' comme celle étant la plus prospère ('self.mission_fortune')
        """
        self.mission_fortune = self.liste_missions[0]['difficulty']
        
        
        """
        initialisation du workload 'self.mission_fortune_workload' appartenant à la mission la plus prospère initialisée au dessus ('self.mission_fortune')
        """
        self.mission_fortune_Sworkload = self.liste_missions[0]['workload']
        
        
        
        """
        comparaison des difficultés des missions présentes dans la liste 'self.liste_missions',
        on fait à partir de 1 car la mission qui se trouve à l'indice 0 à déjà été initialisée au dessus 
        """
        for i in range(1,len(self.liste_missions)):     
            """
            si la difficulté d'une mission présente dans la liste 'self.liste_missions' est supérieur à celle initialisée,
            alors elle devient la nouvelle mission la plus prospère 'self.mission_fortune_position' et 'self.mission_fortune'
            PS: on récupère son workload et sa position mais pas sa difficulté car elle nous intéressait seulement pour le comparaison
            """  
            if self.liste_missions[i]['difficulty'] > self.mission_fortune:
                self.mission_fortune_position = self.liste_missions[i]['position']
                self.mission_fortune = self.liste_missions[i]['difficulty']
                self.mission_fortune_Sworkload = self.liste_missions[i]['starting_workload']               
        return self.mission_fortune_position, self.mission_fortune_Sworkload
    
    
    
    
    def distance_joueur(self, ia_x, ia_y, dico_g):
    
        ######################################################################################################################
        #Cette méthode va comparer la distance des autres joueurs par rapport à la mission la plus proche;                   #
        #si la distance entre notre IA et la mission est supérieur à 2 fois le distance entre un un joueur et cette même     #
        #mission, l'IA ne va pas la faire;                                                                                   #
        #retourne un booléen                                                                                                 #
        ######################################################################################################################
        
        
        
        
        """
        définition d'une liste 'self.liste_position_joueurs',
        va dans le dictionnaire 'game_dict' à la clé "coders" (dont la valeur est une liste)
        PS : cette liste se met à jour en fonction des nouvelles positions des autres joueurs
        """
        self.liste_position_joueurs = dico_g['coders']
        
        
        """
        on attribue la valeur False à la variable joueur_plus_proche
        """
        joueur_plus_proche = False 
        
        
        
        for i in range(len(self.liste_position_joueurs)):        
            """
            si la comparaison décrite au début de la méthode (dans l'encadré) est vérifiée,
            alors la variable 'joueur_plus_proche' prend la valeur True
            """
            if sqrt((ia_x - self.mission_proche_position[0])**2 + (ia_y - self.mission_proche_position[1])**2) > 2*sqrt((self.liste_position_joueurs[i]['position'][0] - self.mission_proche_position[0])**2 + (self.liste_position_joueurs[i]['position'][1] - self.mission_proche_position[1])**2):
                joueur_plus_proche = True     
        return joueur_plus_proche

    
    
    
    def retour_JC(self):
    
        #######################################################################################################################
        #Cette méthode va faire l'IA retourner au JC et y reste si elle y est déjà                                            #
        #######################################################################################################################
        
        
        
        
        if self.JC_x != self.ia_positionx:
            if self.JC_x > self.ia_positionx:
                print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEJC', ' ---- Notre IA retourne au JC', '---- Position actuelle :', (self.ia_positionx,  self.ia_positiony))
                return 'E'
            else:
                print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWJC', ' ---- Notre IA retourne au JC', '---- Position actuelle :', (self.ia_positionx,  self.ia_positiony))
                return 'W'
        if self.JC_y != self.ia_positiony:
            if self.JC_y < self.ia_positiony:
                print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNJC', ' ---- Notre IA retourne au JC', '---- Position actuelle :', (self.ia_positionx,  self.ia_positiony))
                return 'N'
            else:
                print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSJC', ' ---- Notre IA retourne au JC', '---- Position actuelle :', (self.ia_positionx,  self.ia_positiony))
                return 'S' 
        if self.JC_x == self.ia_positionx and self.JC_y == self.ia_positiony:
            print('PPPPPPPPPPAAAAAASSSSSSSSSSSSSSEEEEEEJC', ' ---- Notre IA se recharge au JC', '---- Position actuelle:', (self.ia_positionx, self.ia_positiony))
            return 'PASSE'
        
        
        

    def action(self, game_dict : dict) -> str:
    
        #####################################################################################################################
        #Appelé à chaque décision du joueur IA                                                                              #
        #                                                                                                                   #
        #Args:                                                                                                              #
        #    tour (str): descriptif de l'état de la partie                                                                  #
        #                                                                                                                   #
        #Returns:                                                                                                           #
        #    str : une action 'N', 'S', 'E', 'W', 'L', 'EM', 'P'                                                            #
        #####################################################################################################################


        
        
        """
        appel de la méthode pour savoir sur quelle mission la plus proche l'IA va se rendre
        """
        self.mission_plus_proche()
        
        
        """
        appel de la méthode pour savoir quelle mission es la plus prospère
        """
        self.mission_gros_gain()
        
        
        """
        dans le dico 'game_dict' à la clé "coders" va prendre la 3ème (donc indice 2) valeur (qui est un tuple de coordonnées),
        puis va prendre la 1ère valeur du tuple pour 'self.ia_positionx',
        puis va prendre la 2ème valeur du tuple pour 'self.ia_positiony'
        """
        self.ia_positionx = game_dict['coders'][self.numero_joueurIA]['position'][0]   
        self.ia_positiony = game_dict['coders'][self.numero_joueurIA]['position'][1]
        
        
        """
        va récupérer l'énergie du coder dans le dico
        """
        self.ia_energie = game_dict['coders'][self.numero_joueurIA]['energy']
        
        
        """
        définition d'une liste 'liste_missions_a_jour',
        va dans le dictionnaire 'game_dict' à la clé "missions" (dont la valeur est une liste)
        PS : cette liste se met a jour contrairement à la liste 'self.liste_missions'
        """
        self.liste_mission_a_jour = game_dict['missions']                



        """
        appel de la méthode pour retourner au JC
        """
        if self.ia_energie == 0:
            return self.retour_JC()
            
            
        """
        si la methode 'self.distance_joueur()' retourne True,
        alors notre IA va aller vers la mission le plus proche 'self.mission_proche_position'
        """
        if not self.distance_joueur(self.ia_positionx, self.ia_positiony, game_dict):       
            """
            définition des coordonnées x et y de la mission 'self.mission_proche_position' que la méthode appelé ('self.mission_plus_proche') a sortie,
            'self.mission_cible_coordx' va être la 1ère valeur du tuple et 'self.mission_cible_coordy' va être la 2éme valeur du tuple
            """
            self.mission_cible_coordx = self.mission_proche_position[0] 
            self.mission_cible_coordy = self.mission_proche_position[1]


            """
            va se rendre sur la mission la plus proche 'self.mission_proche_position' si elle n'a pas été faite et que l'IA à l'énergie nécessaire
            """
            if self.mission_proche_Sworkload != 0 and self.ia_energie != 0:
                if self.mission_cible_coordx !=  self.ia_positionx:
                    if self.mission_cible_coordx >  self.ia_positionx:
                        print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', ' ---- Position actuelle :', (self.ia_positionx,  self.ia_positiony), '---- Notre IA cible la mission :', (self.mission_cible_coordx, self.mission_cible_coordy))
                        return 'E'
                    else:
                        print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW', ' ---- Position actuelle :', (self.ia_positionx,  self.ia_positiony), '---- Notre IA cible la mission :', (self.mission_cible_coordx, self.mission_cible_coordy))
                        return 'W'
                if self.mission_cible_coordy !=  self.ia_positiony:
                    if  self.mission_cible_coordy < self.ia_positiony:
                        print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN', ' ---- Position actuelle :', (self.ia_positionx,  self.ia_positiony), '---- Notre IA cible la mission :', (self.mission_cible_coordx, self.mission_cible_coordy))
                        return 'N'
                    else:
                        print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', ' ---- Position actuelle :', (self.ia_positionx,  self.ia_positiony), '---- Notre IA cible la mission :', (self.mission_cible_coordx, self.mission_cible_coordy))
                        return 'S'
       
        
        if self.distance_joueur(self.ia_positionx, self.ia_positiony, game_dict):
            self.mission_cible_coordx = self.mission_fortune_position[0] 
            self.mission_cible_coordy = self.mission_fortune_position[1]
                
            if self.mission_proche_Sworkload != 0 and self.ia_energie != 0:
                        if self.mission_cible_coordx !=  self.ia_positionx:
                            if self.mission_cible_coordx >  self.ia_positionx:
                                print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', ' ---- Position actuelle :', (self.ia_positionx,  self.ia_positiony), '---- Notre IA cible la mission :', (self.mission_cible_coordx, self.mission_cible_coordy))
                                return 'E'
                            else:
                                print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW', ' ---- Position actuelle :', (self.ia_positionx,  self.ia_positiony), '---- Notre IA cible la mission :', (self.mission_cible_coordx, self.mission_cible_coordy))
                                return 'W'
                        if self.mission_cible_coordy !=  self.ia_positiony:
                            if  self.mission_cible_coordy < self.ia_positiony:
                                print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN', ' ---- Position actuelle :', (self.ia_positionx,  self.ia_positiony), '---- Notre IA cible la mission :', (self.mission_cible_coordx, self.mission_cible_coordy))
                                return 'N'
                            else:
                                print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', ' ---- Position actuelle :', (self.ia_positionx,  self.ia_positiony), '---- Notre IA cible la mission :', (self.mission_cible_coordx, self.mission_cible_coordy))
                                return 'S'
                

        """
        si aucun des 2 if n'es validé, 
        alors notre IA passe son tour
        """
        return 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
        
        
        



                    
    def game_over(self, game_dict: dict) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            descr (str): descriptif du dernier tour de jeu
        """
        pass
    
    
    

