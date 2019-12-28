    ____               _      __     ____                           _             _______ 
   / __ \_________    (_)__  / /_   / __ \___ _   _____  __________(_)           /  _/   |
  / /_/ / ___/ __ \  / / _ \/ __/  / /_/ / _ \ | / / _ \/ ___/ ___/ /  ______    / // /| |
 / ____/ /  / /_/ / / /  __/ /_   / _, _/  __/ |/ /  __/ /  (__  ) /  /_____/  _/ // ___ |
/_/   /_/   \____/_/ /\___/\__/  /_/ |_|\___/|___/\___/_/  /____/_/           /___/_/  |_|
                /___/     


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
*                                                                                           *
* Université de Bordeaux                                                                    *
* Projet d'Intelligence Artificielle - Master Informtatique semestre 1                      *
*                                                                                           *
* Python Version 3.6.9                                                                      *
*                                                                                           *
* @author:      Wilfried Augeard <wilfried.augeard@etu.u-bordeaux.fr>                       *
* @version:     1.0.0                                                                       *
* @require      pygame                                                                      *
*                                                                                           *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


CONSIGNES: 
    - Vous devez rendre un joueur de Reversi (version spéciale de Othello) qui puisse s'intégrer au tournoi entre les joueurs.
    - Le tournoi sera organisé (chacun rencontre les autres dans deux matchs (en tant que Noirs puis en tant que Blancs)). 
    - Chaque joueur n'aura le droit qu'à 5 minutes de temps réel de réflexion sur toute la partie. 
    - Il est interdit de consommer du temps CPU en dehors des appels explicites au fonction de l'interface.

PRINCIPE GLOBAL DE L'IA IMPLÉMENTÉE:
    - L'IA implémentée se base sur la stratégie suivante: Prendre les coups amenant aux meilleurs positionnements possibles.
      Sur les 5 derniers coups, on simule les fins de parties et on joue les coup où l'on a le plus de chances de gagner.

HEURISTIQUES:
    - La principale heuristique de cette IA se base sur le positionnement des jetons. 
    - Chaque case valant un poids définit.
    - Les cases stratégiques à avoir sont celles qui ne changeront pas dans le temps: les coins. Les bords sont aussi importants (surtout
      si on a déjà les coins). 
    - En revanche la "couche" avant les bords est à éviter (elle donne accès aux bords/coins à l'ennemi).
    - On prend en compte la distance entre la case à jouer et le coins afin de donner du poids.
    - Les coups prioritaires sont: coins, coup menant à une victoire directe.
    - Les coups "interdits": voisins du coin si coins pas prit par nous.

    - Lors du "rush final" c'est-à-dire sur les derniers coups, on ne se base plus sur le positionnement mais sur la probailité de gagner. 
    - On parcourt alors chaque possibilité de fin de jeu selon les moves effectués. On retourne la somme des parties gagnées divisées par le nombre de fins possibles.
      On joue donc là où on a le plus de chances de gagner.
    

ARCHITECTURES FICHIERS:
    |_ Wilfried_Augeard
        |_ __init__.py
        |_ myPlayer.py
        |_ random.py
        |_ localGame.py
        |_ playerInterface.py
        |_ Reversi.py
        |_ ui.py
        |_ annexes
            |_ alpha_beta.py
            |_ heuritic.py
            |_ tools.py
        |_ ressources
            |_ board.bmp
            |_ ...
        |_ README.txt
        |_ tmp
            #Après lancement d'une partie où l'écriture est activée, dossier vide sinon
            |_ log.txt
            |_ heuritic.txt


POINTS FORTS:
    - Réflexion rapide (en moyenne moins d'une seconde pour retourner un coup)
    - Se base sur le meilleur positionnement, dans un sens ne prend pas en compte ce que fait l'adversaire. Il peut jouer stratégique ou random, cela ne change rien.
    - Fonctionne qu'elle ait les jetons noirs ou blancs.
    - La combinaison des 2 techniques décrites précédemment: en principe, nous nous sommes positionné de la manière la plus stratégique possible, on optimise donc nos chances d'avoir des fins de parties gagnantes.

    Quelques chiffres:
    - Sur Intel® Core™ i7-8700 CPU @ 3.20GHz × 12 :
        - IA contre elle-même: Time: [54.69798970222473, 38.17041087150574], White gagnant.
        - IA contre random: Time: [0.04088568687438965, 48.54544281959534], IA gagnante white.
        - Sur 500 parties contre l'IA Random: gagne 494 fois (réussite à 98,8%).


POINTS À AMÉLIORER:
    - Pour l'heuristique ainsi que les fonctions annexes, on peut définir les coins, voisins des coins etc en fonction de la taille du board au lieu
      de mettre des valeurs brutes. Par exemple, au lieu de mettre (9,9) on peut mettre (boardsize-1, boardsize-1).
    - Mieux évaluer les statistiques lors des derniers coups (faire remonter la probabilité de gagner mais aussi le nombre de jetons gagnés au final).


NOTE:
    - Dans le constructeur de l'IA de base donné pour le projet, il y a 2 champs (board et color). 
      Ici j'y ai ajouté totalTime et tours correspondant au temps total que met l'IA à jouer depuis le début de la partie (utile pour limiter le temps) et
      le nombre de tours que l'IA a joué (utilse pour savoir combien de tours il reste). 
    - Possibilité d'enregistrer quelques données dans le dossier tmp en activant les _DIR_LOG dans les fichiers localGame ou alpha_beta.
    - Possibilité de jouer plusieurs parties à la suite en alternant les couleurs: activer le MULTY_MODE.