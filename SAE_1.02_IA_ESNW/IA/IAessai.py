import math
import random

class IA_ESNW:

    def __init__(self, num_joueur: int, game_dic: dict) -> None:
        print("IA num", num_joueur, "chargée : OK")
        self.numero = num_joueur
        self.dictionnaire = game_dic

    def action(self, game_dict: dict) -> str:
        self.dictionnaire = game_dict
        coder = self.dictionnaire["coders"][self.numero]
        x, y = coder["position"]

        mission_intéressante = self.trouver_mission_intéressante()

        if mission_intéressante:
            x_pos, y_pos = mission_intéressante["position"]
            energy_coder = coder["energy"] > 0

            if (x > x_pos and energy_coder) or (x > 10 and not energy_coder):
                return "W"
            elif (x < x_pos and energy_coder) or (x < 10 and not energy_coder):
                return "E"
            elif (y > y_pos and energy_coder) or (y > 10 and not energy_coder):
                return "N"
            elif (y < y_pos and energy_coder) or (y < 10 and not energy_coder):
                return "S"
            else:
                return "P"
        else:
            return "P"

    def trouver_mission_intéressante(self):
        mission_intéressante = None
        récompense_maximum = float('-inf')

        for mission in self.dictionnaire["missions"]:
            if mission["cooldown"] == 0:
                récompense = (mission['starting_workload'] * mission["difficulty"])
                if récompense > récompense_maximum:
                    récompense_maximum = récompense
                    mission_intéressante = mission

        return mission_intéressante
    

    def game_over(self, game_dict: dict) -> None:
        pass






