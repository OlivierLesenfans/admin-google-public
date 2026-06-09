
from googleapiclient.discovery import build
from google.oauth2 import service_account

from cle.compte import *


def parcourtTuple(t,l):
    """
    Méthode qui ne sert qu'à la construction de la liste des droits
    en fonction du tuple en paramètre
    """
    acces = list()
    for idx in range (len(t)):
        if t[idx] != 0:
            acces.append(l[idx])
    return acces
    

class Auth:
    def __init__(self,file,compte,nameService,version):
        self.SERVICE_ACCOUNT_FILE = file
        self.DELEGATED_ADMIN = compte

        self.nameService = nameService
        self.version = version

    SCOPES = [ #Définie de façon inépendante de l'instance
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.group',
        'https://www.googleapis.com/auth/admin.directory.group.member',
        'https://www.googleapis.com/auth/admin.reports.usage.readonly'
    ]

    def init_Drive(self,drive,user,group,groupMember,reports = 0):
        """
        Permet d'inistialiser la bibliothèque de l'Api google de façon à prendre 
        les accès nécessaires au contrôle des drives\n
        On déclare donc 1 pour ceux que l'on veut, et 0 pour le reste\n
        1--> Drives\n
        2--> Utilisateurs\n
        3--> Groupes\n
        4--> Membres des groupes\n
        """
        droits = drive,user,group,groupMember,reports
        access = parcourtTuple(droits,self.SCOPES)
        # print(access)
        
        creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=access)
        self.delegated_creds = creds.with_subject(self.DELEGATED_ADMIN)

    def Build(self):
        return build(self.nameService, self.version,credentials=self.delegated_creds)

class Authentification:
    def __init__(self,nomDuService, version,compte) -> None:
        self.auth = Auth("cle/key.json",compte,\
        nomDuService,version)


    
class Service:
    """
    Nécessite les scopes 2 et 3

    Constructieur qui donne les scopes nécessaires à la manipulation de ce qui est demandé
    """
    def __init__(self,c:str,compte=COMPTE_PERSO):
        autho : Authentification
        if (c=='g'):
            autho = Authentification('admin','directory_v1',compte) #Authentifications relatives aux groupes
            autho.auth.init_Drive(0,0,1,1) #On définit le type d'action que l'on veut réaliser
        elif (c== 'd'):
            autho = Authentification('drive','v3',compte) #Authentifications relatives aux drives partagés
            (autho.auth).init_Drive(1,0,1,1)
        elif(c=='r'):
            autho = Authentification('admin', 'reports_v1',compte)
            autho.auth.init_Drive(0,0,0,0,1)
        else:
            autho = Authentification("admin","directory_v1",compte)
            autho.auth.init_Drive(0,1,0,0)
        self.object = autho.auth.Build()
        


"""
fileOrganizer, writer, commenter, reader
"""



    
