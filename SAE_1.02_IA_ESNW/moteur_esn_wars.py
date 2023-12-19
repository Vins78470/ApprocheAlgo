import random
import importlib
import json

#mettre à False pour arrêter l'affichage dans le terminal
RAPPORT = True

#variables globales constantes
DIRECTIONS = {'N':(0,-1), 'S':(0,1), 'E':(-1,0), 'W':(1,0)}
JC = (10,10)
SIZE = 21
MAX_LEVEL = 10
OBJECTIVE = 3000
DURATION = 1000
COST_UPGRADE = 25
COOLDOWN_FACTOR = 10

##############################################################################
# Structures de données
# servant à simplement à stocker les infos en cours de jeu
##############################################################################

class Coder:
    def __init__(self):
        self.position = JC
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

    def __str__(self):
        return str(self.__dict__)

class Game:
    def __init__(self, nb_joueurs, missions):
        self.coders = [Coder() for i in range(nb_joueurs)]
        self.missions = missions
        self.actions = []
    
    def missions_positions(self):
        return {m.position : m for m in self.missions}

    def coders_positions(self):
        return {c.position : c for c in self.coders}

    def to_dict(self):
        return {'coders':[c.__dict__ for c in self.coders], 'missions':[m.__dict__ for m in self.missions], 'actions': self.actions}

##############################################################################
# Fonctions auxilaires
##############################################################################

def save_missions(missions, file_name : str):
    with open("Maps/" + file_name, "w") as file:
        json.dump([m.__dict__ for m in missions], file)

def load_missions(file_name : str):
    with open("Maps/" + file_name, "r") as file:
        return [Mission(**dico) for dico in json.load(file)]
        
def load_IAs(player_names : list, game : Game):
    """Charge les objets IA contenus dans les fichiers (noms des joueurs) donnés
    
    Args:
        player_names ([str]): noms des joueurs
    Returns:
        list : liste des objet IAs par chaque indice de joueur
    """

    list_ia = []

    for i in range(len(player_names)):
        imp = importlib.import_module("IA." + player_names[i])
        list_ia.append(imp.IA_ESNW(i, game.to_dict() ) )

    return list_ia

def get_player_action(num_player : int, IAs : list, game: Game):
    ia = IAs[num_player]
    return ia.action(game.to_dict())

##############################################################################
# Fonctions Logiques des règles du jeu
##############################################################################

def update_cooldowns(missions : list):
    """Met à jour les cooldowns de toutes les missions (appelé en début de tour).

    Args:
        missions (list): liste d'objets Mission
    """
    for m in missions:
        if m.cooldown > 1 :   
            m.cooldown -= 1
        elif m.cooldown == 1: #la mission redevient opérationelle 
            m.cooldown = 0
            m.workload = m.starting_workload


def resolve_action(num_player : int, action : str, game : Game):
    """Résout l'action du joueur. Renvoie True si l'action est réalisable et False sinon.

    Args:
        num_player (int): numéro du joueur
        action (str): caractère décrivant l'action
        game (Game) : état du jeu
    """
    
    coder = game.coders[num_player]

    if action in DIRECTIONS:
        x,y = coder.position
        dx,dy  = DIRECTIONS[action]
        #on teste si le déplacement amène dans une case valide, non occupée, ou au JC
        if (x+dx,y+dy) == JC or (0 <= x + dx < SIZE and 0 <= y + dy < SIZE and (x+dx,y+dy) not in game.coders_positions()):
            coder.position = (x+dx,y+dy)
            if RAPPORT:
                print("Coder", num_player, "se déplace en",x+dx,y+dy)      
            return True

    if action == 'L' and coder.level < MAX_LEVEL and coder.position==JC:
        coût = (coder.level+1)**2 * COST_UPGRADE
        if coder.bitcoins >= coût:
            coder.bitcoins -= coût
            coder.level += 1
            if RAPPORT:
                print("Coder", num_player, "augmente son level à",coder.level)
                input()   
            return True

    if action == 'E' and coder.max_energy < MAX_LEVEL and coder.position==JC:
        coût = (coder.max_energy+1)**2 * COST_UPGRADE
        if coder.bitcoins >= coût:
            coder.bitcoins -= coût
            coder.max_energy += 1
            if RAPPORT:
                print("Coder", num_player, "augmente son énergie max à",coder.max_energy)
                input()  
            return True
        
    return False
    


def end_turn(num_player : int, game : Game):
    """Effectue les actions de fin de tour du joueur
    - lance travail sur missions
    - regain d'énergie au JC

    Args:
        num_player (int): numéro du joueur
        game (Game): données courantes du jeu

    Returns:
        bool: indique si une action a eu lieu
    """

    coder = game.coders[num_player]
    
    if coder.position in game.missions_positions():
        mission = game.missions_positions()[coder.position]
        if mission.cooldown == 0 and coder.energy > 0:
            work_on_mission(coder, mission)
            return True

    if coder.position == JC:
        coder.energy = coder.max_energy
        if RAPPORT:
            print("Coder", num_player, "regagne son énergie")
        return True

    return False


def work_on_mission(coder : Coder, mission : Mission):
    """Applique les effets du travail d'un coder sur une mission

    Args:
        coder (Coder): le codeur
        mission (Mission): la mission
    """

    coder.energy = max(0,coder.energy - mission.difficulty)
    mission.workload = max(0, mission.workload - coder.level)
    if RAPPORT:
        print("Le coder travaille sur une mission, son énergie passe à", coder.energy, "le workload passe à", mission.workload)
        input()
    if mission.workload == 0:
        mission.cooldown = mission.difficulty * COOLDOWN_FACTOR
        coder.bitcoins += (mission.difficulty * mission.starting_workload)**2
        if RAPPORT:
            print("La mission est terminée, elle a un cooldown de", mission.cooldown)
            print("Le codeur a maintenant", coder.bitcoins,"bitcoins")
            input()


def check_endgame(game : Game) -> bool:
    """Check si les conditions de fin de jeu sont vérifiées

    Args:
        game (Game): le jeu

    Returns:
        bool: True si jeu terminé
    """
    if len(game.actions) > DURATION:
        return True
    for c in game.coders:
        if c.bitcoins >= OBJECTIVE:
            return True
    return False
    
##############################################################################
# Fonction principale qui lance le jeu
##############################################################################


def partie(player_names : list, missions_file : str):
    """
    Simule une partie du jeu ESN Wars

    Args:
        joueurs ([str]) : liste contenant les noms des joueurs i.e. les noms des fichiers contenant les IA
            (on peut mettre plusieurs fois le même nom)
        missions_file : nom du fichier contenant la map
    Returns:
        historique (str) : historique complet de la partie
        scores (list) : liste des scores des joueurs en fin de partie
    """

    nb_players = len(player_names)
    missions = load_missions(missions_file)
    game = Game(nb_players, missions)
    IAs = load_IAs(player_names, game)
    game_over = False
    num_current_player = 0

    if RAPPORT:
        print("Début de partie avec", nb_players, "coders")
        print("nom des IAs :", player_names)

    history = [game.to_dict()]

    
    while not game_over:
        if RAPPORT:
            print("\n"+"*"* 20 + "\nDébut tour", len(history), "codeur :", num_current_player)
            print(game.to_dict())
        update_cooldowns(missions)
        action = get_player_action(num_current_player, IAs, game)
        if RAPPORT:
            print("Action choisie", action)
        game.actions.append(action)
        resolve_action(num_current_player, action, game)
        end_turn(num_current_player, game)
        x,y = game.coders[num_current_player].position
        
        num_current_player = (num_current_player + 1) % nb_players
        history.append(game.to_dict())
        game_over = check_endgame(game)
        if RAPPORT:
            print("Fin du tour", len(history)-1)
            #input()

    if RAPPORT:
        print("Scores de fin de partie")
        for i in range(nb_players):
            print("Coder",i,":",game.coders[i].bitcoins)

        
