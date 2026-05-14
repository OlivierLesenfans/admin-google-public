import sys
sys.path.append("Drives")

import datetime

from classes import *

def conv_jours(date):
    date = str(date).split('-')
    annee,mois,jour = date[0],date[1],date[2]

    return int(annee)*365.25+int(mois)*30.25+int(jour)

class Date_dif:
    def __init__(self,ch:str) -> None:

        date_actuelle = str(datetime.date.today()).split('-')

        date = ch[:10].split('-')
        annee,mois= int(date[0]),int(date[1])
        annee_a,mois_a = int(date_actuelle[0]),int(date_actuelle[1])

        
        dif_annees:int = annee_a-annee
        dif_mois:int = mois_a-mois
        if dif_mois < 0:
            dif_annees-=1
            dif_mois = 12+dif_mois
        
        self.mois = dif_mois
        self.annees = dif_annees

    def __str__(self) -> str:
        return "Depuis {} ans et {} mois".format(self.annees,self.mois)
        



def lst_comptes_anciens():
    l = listeUtilisateurs(Service('u'))
    l.load()

    """
    A retester tout de meme apres modifs
    """
    l2 = []
    user : Utilisateur
    for user in l.l:
        dif = Date_dif(user.dateCreation)
        if (dif.annees > 1 and user.derniere_co == '1970-01-01T00:00:00.000Z'):
            l2.append("inscrit {}\t\tadresse: {}\t\tdate de derniere connexion: never logged in\n".format(str(dif),user.mail))

    
    with open("Mails_Vieux.txt","w",encoding="utf8") as f:
        for ligne in l2:
            f.write(ligne)