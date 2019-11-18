import pygame
import random


fini = False

pygame.init()

###variable terrain et musique###

GRIS = (80,80,80)
VERT = (34,139,34)
BLANC = (255,255,255)
GRIS_CLAIR=(212,211,211)


FENETRE_LARGEUR = 600
FENETRE_HAUTEUR = 800

LARGEUR_COULOIR_ROUTIER = FENETRE_LARGEUR/5.6

LARGEUR_VERT=(69+(4*LARGEUR_COULOIR_ROUTIER)+12)

BERNE_LARGEUR = 20

COTE_LARGEUR = 150
COTE_HAUTEUR = FENETRE_HAUTEUR

BANDE_LARGEUR = 12
BANDE_HAUTEUR = FENETRE_HAUTEUR

PETITE_BANDE_LARGEUR=12
PETITE_BANDE_HAUTEUR = 50

BANDE_MILIEU_LARGEUR = 12
BANDE_MILIEU_HAUTEUR = 100

COULOIRS_ROUTIERS = 4

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)

position_ligne = 20
NBR_BANDE = 3
nbr_bande_affichee = 0
position_bande = FENETRE_LARGEUR/3.5

pygame.mixer.init()

musique = pygame.mixer.Sound('sons/musiquejeu.ogg')

###fin variables terrain et musique###

###différent type de voiture###

############################################################################
# creer un nouveau type de voiture:                                        #
#     type = ['type', 'image', longueur_horizontale, longueur_verticale]   #
############################################################################

type_voiture_joueur = ('voiture_joueur', ('image/voiture.png', 'image/voiture_gauche.png', 'image/voiture_droite.png'),FENETRE_LARGEUR//13,FENETRE_HAUTEUR//8)
type_voiture_blanche = ('voiture_blanche', ('image/voiture_blanche.png', None, None),FENETRE_LARGEUR//13,FENETRE_HAUTEUR//8)

###fin des types de voitures###

def dessiner_voiture(voiture):
    fenetre.blit(voiture['image'], (voiture['position'][0], voiture['position'][1]))

###début de la gestion de la scène de jeu###

def nouvelle_scene():
    return{
        'acteurs': []
    }

def ajoute_voiture(scene, voiture):
    scene['acteurs'].append(voiture)

def enleve_voiture(scene, voiture):
    acteurs = scene['acteurs']
    if voiture in acteurs:
        acteurs.remove(voiture)

def acteurs(scene):
    return list(scene['acteurs'])

def affiche(scene):
    voitures = acteurs(scene)
    for objet in voitures:
        dessiner_voiture(objet)

###début création et gestion du terrain###

def dessine_bande():
    global position_ligne
    nbr_bande_affichee = 0
    bande_en_cours = position_bande
    if position_ligne/230 >= 0:
        position_ligne = -230
    position_ligne_en_cours = position_ligne
    while(nbr_bande_affichee < NBR_BANDE):
        while(position_ligne_en_cours<=FENETRE_HAUTEUR + 230):
            pygame.draw.rect(fenetre,BLANC,((bande_en_cours,position_ligne_en_cours),(PETITE_BANDE_LARGEUR,PETITE_BANDE_HAUTEUR)))
            position_ligne_en_cours += 230
        nbr_bande_affichee += 1
        bande_en_cours += LARGEUR_COULOIR_ROUTIER
        position_ligne_en_cours = position_ligne

def dessine_terrain():
    fenetre.fill(GRIS)
    pygame.draw.rect(fenetre,GRIS_CLAIR,((20,0),(BERNE_LARGEUR,COTE_HAUTEUR)))
    pygame.draw.rect(fenetre,VERT,((LARGEUR_VERT,0),(COTE_LARGEUR,COTE_HAUTEUR)))
    pygame.draw.rect(fenetre,BLANC,((60,0),(BANDE_LARGEUR,BANDE_HAUTEUR)))
    pygame.draw.rect(fenetre,BLANC,((LARGEUR_VERT-19,0),(BANDE_LARGEUR,BANDE_HAUTEUR)))
    pygame.draw.rect(fenetre,BLANC,((0,0),(3,BANDE_HAUTEUR)))
    avance_bande()
    dessine_bande()

def avance_bande():
    global position_ligne
    position_ligne -= test_vitesse(voiture_joueur)

###fin gestion du terrain###

###manipulation des voitures###

def creer_voiture(type_vehicule, position_x, position_y):
    creation = voiture()
    attribue_type(creation, type_vehicule[0])
    if creation['type'] == 'voiture_joueur':
        joueur(creation)
    cree_image(creation, type_vehicule[1][0], type_vehicule[2], type_vehicule[3], 0)
    if type_vehicule[1][1]:
        cree_image(creation, type_vehicule[1][1], type_vehicule[2]+20, type_vehicule[3]+5, 1)
    if type_vehicule[1][2]:
        cree_image(creation, type_vehicule[1][2], type_vehicule[2]+20, type_vehicule[3]+5, 2)
    position(creation, position_x, position_y)
    creation['image'] = creation['images'][0]
    return creation

def voiture():
    return{
        'images': [None, None, None],
        'image' : None,
        'type': None,
        'joueur': False,
        'position': [0, 0],
        'vitesse' : 0,
        'vitesse_a_l_ecran' : 0,
        'taille' : [0,0]
        }

def attribue_type(voiture, type):
    voiture['type'] = type

def cree_image(voiture, image, x, y, nb):
    voiture['images'][nb] = image
    voiture['taille'][0] = x
    voiture['taille'][1] = y
    voiture['images'][nb] = pygame.image.load(voiture['images'][nb]).convert_alpha(fenetre)
    voiture['images'][nb] = pygame.transform.scale(voiture['images'][nb], (voiture['taille']))

def pnj(voiture):
    voiture['joueur'] = False

def joueur(voiture):
    voiture['joueur'] = True

def est_le_joueur(voiture):
    return voiture['joueur']

def position(voiture, x, y):
    voiture['position'][0] = x
    voiture['position'][1] = y

def test_position(voiture):
    return voiture['position']

def vitesse(voiture, vitesse_voiture):
    voiture['vitesse'] = vitesse_voiture

def test_vitesse(voiture):
    return voiture['vitesse']

def vitesse_a_l_ecran(voiture, vitesse_voiture):
    voiture['vitesse_a_l_ecran'] = vitesse_voiture

def accelere(voiture):
    voiture['vitesse'] -= 1

def ralenti(voiture):
    voiture['vitesse'] += 1

def avance(voiture):
    voiture['position'][1] += voiture['vitesse_a_l_ecran']

def tourne(voiture, direction):
    if direction == 'gauche':
        tourne_gauche(voiture)
    elif direction == 'droite':
        tourne_droite(voiture)

def tourne_gauche(voiture):
    voiture['position'][0] -= 5
    voiture['image'] = voiture['images'][1]

def tourne_droite(voiture):
    voiture['position'][0] += 5
    voiture['image'] = voiture['images'][2]

def avance_voiture(voiture):
    vitesse_voiture = test_vitesse(voiture) - test_vitesse(voiture_joueur)
    vitesse_a_l_ecran(voiture, vitesse_voiture)
    avance(voiture)

def rectangle(voiture):
    return voiture['image'].get_rect().move(voiture['position'][0], voiture['position'][1])

###fin manipulation des voitures###

###gestion de la route et des autres voiture###

def nouvelle_route():
    random.seed()
    taille_bande = LARGEUR_COULOIR_ROUTIER
    return{
        'bande': [0] + [60 + BANDE_MILIEU_LARGEUR//2 + n*taille_bande for n in range(COULOIRS_ROUTIERS + 1)],
        'vitesse': [0] * (COULOIRS_ROUTIERS + 1),
        'nombre_bandes': COULOIRS_ROUTIERS,
        'taille_bandes': LARGEUR_COULOIR_ROUTIER
    }

def range_bande(route):
    return range(1, route['nombre_bandes'])

def vitesse_bande(route, bande):
    return route['vitesse'][bande]

def change_vitesse_bande(route, bande, vitesse):
    route['vitesse'][bande] = vitesse

def debut_bande(route, bande):
    return route['bande'][bande]

def nouvelle_voiture(route, bande, voiture_type):
    creation = creer_voiture(voiture_type, 0, 0)
    rect = rectangle(creation)
    debut = debut_bande(route, bande)
    fin = debut_bande(route, bande + 1)
    position_centre_bande = debut + (fin - debut)/2
    rect.left = position_centre_bande - rect.height/2
    x = rect.left
    y = - voiture_type[3]
    creation = creer_voiture(voiture_type, x, y)
    vitesse(creation, vitesse_bande(route, bande))
    return creation

###fin gestion de la route et des autres voitures###

###gestion du clavier###

def nouvel_etat_touche():
    return{
        'actif': False,
        'delai': 0,
        'periode': 0,
        'suivant': 0
    }

def nouvelle_gestion_clavier():
    return{}

def repete_touche(gc, touche, delai, periode):
    pygame.key.set_repeat()
    if touche in gc:
        entree = gc[touche]
    else:
        entree = nouvel_etat_touche()
    entree['delai'] = delai
    entree['periode'] = periode
    gc[touche] = entree

def scan(gc):
    maintenant = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    for touche in gc:
        if keys[touche] == 1:
            if gc[touche]['actif']:
                if maintenant >= gc[touche]['suivant']:
                    gc[touche]['suivant'] = gc[touche]['periode'] + maintenant
                    pygame.event.post(pygame.event.Event(pygame.KEYPRESSED, {'key': touche}))
            else:
                gc[touche]['actif'] = True
                gc[touche]['suivant'] = gc[touche]['delai'] + maintenant
        else:
            gc[touche]['actif'] = False
            gc[touche]['suivant'] = 0

def traite_entree():
    global fini
    scan(gc)
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYPRESSED:
            if evenement.key == TOUCHE_HAUT:
                accelere(voiture_joueur)
            elif evenement.key == TOUCHE_BAS:
                ralenti(voiture_joueur)
            elif evenement.key == TOUCHE_GAUCHE:
                tourne(voiture_joueur, 'gauche')
            elif evenement.key == TOUCHE_DROITE:
                tourne(voiture_joueur, 'droite')
        elif evenement.type == pygame.KEYUP:
            if evenement.key == TOUCHE_DROITE or evenement.key == TOUCHE_GAUCHE:
                voiture_joueur['image'] = voiture_joueur['images'][0]
                
def musique():
    musique.play()

temps = pygame.time.Clock()

pygame.KEYPRESSED = pygame.USEREVENT
gc = nouvelle_gestion_clavier()

TOUCHE_HAUT = pygame.K_UP
TOUCHE_BAS = pygame.K_DOWN
TOUCHE_DROITE = pygame.K_RIGHT
TOUCHE_GAUCHE = pygame.K_LEFT

repete_touche(gc, TOUCHE_HAUT, 50, 200)
repete_touche(gc, TOUCHE_BAS, 50, 100)
repete_touche(gc, TOUCHE_DROITE, 0, 0)
repete_touche(gc, TOUCHE_GAUCHE, 0, 0)

###fin de la gestion du clavier###

###test de la route###

route = nouvelle_route()
for coul in range_bande(route):
    change_vitesse_bande(route, coul, -2)

scene = nouvelle_scene()
###création de la voiture du joueur###

voiture_joueur = creer_voiture(type_voiture_joueur, 300, 700 - type_voiture_joueur[2])
ajoute_voiture(scene, voiture_joueur)
voiture1 = nouvelle_voiture(route, 1, type_voiture_blanche)
ajoute_voiture(scene, voiture1)
voiture2 = nouvelle_voiture(route, 2, type_voiture_blanche)
ajoute_voiture(scene, voiture2)
voiture3 = nouvelle_voiture(route, 3, type_voiture_blanche)
ajoute_voiture(scene, voiture3)
voiture4 = nouvelle_voiture(route, 4, type_voiture_blanche)
ajoute_voiture(scene, voiture4)

###fin création de la voiture du joueur###

musique.play()

while not fini:
    traite_entree()
    fenetre.fill(NOIR)
    dessine_terrain()
    avance_voiture(voiture2)
    affiche(scene)
    pygame.display.flip()
    temps.tick(50)
