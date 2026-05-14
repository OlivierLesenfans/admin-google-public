from .Authentification import Service
import pickle
from .Dossiers import *
import uuid
from .Permissions import *


LG_MAX_DRIVE = 150

class DrivePartage:
    def __init__(self,nom,service):
        self.nom = nom
        self.id = "\0"

        self.permissions: dict[str, Permission]
        self.service = service


    def creerDossier(self, d : Dossier):
        file_metadata = {
            'name': d.name,
            'mimeType': 'application/vnd.google-apps.folder',
            'driveId': self.id,
            'parents': [self.id]  # mettre le dossier parent si tu veux un sous-dossier
        }
        folder = self.service.object.files().create(
            body=file_metadata,
            supportsAllDrives=True,
            fields='id'
        ).execute()

        print('Dossier créé, ID:', folder.get('id'))

    def upload(self):
        drive_metadata = {'name': self.nom}

        drive = self.service.object.drives().create(
            body=drive_metadata,
            requestId=str(uuid.uuid4())  # identifiant unique de la requête
        ).execute()

        self.id = drive['id']

        print(f"Drive créé : {drive['id']} ({drive['name']})")

    def ajouterMembre(self,mailUser : str, role : str):
        """
        Ajouter une personne en tant que 'role' d'un drive partagé 
        Admin: organizer
        Lecteur : reader

        """
        permission = {
            "type": "user",
            "role": role,  # admin du Drive partagé
            "emailAddress": mailUser
        }

        created_permission = self.service.object.permissions().create(
            fileId=self.id,
            body=permission,
            supportsAllDrives=True,
            sendNotificationEmail=False, # facultatif, True pour notifier l'utilisateur
              useDomainAdminAccess=True  
        ).execute()

        print("Permission créée, ID:", created_permission.get("id"))
        return

    def retirer_membre(self,mail:str):
        """
        Permet de retirer une permission en se basant sur son adresse mail
        Pas sûr qu'elle fonctionne pour les groupes.

        """
        p: Permission | None
        p = self.permissions.get(mail)
        if p:
            self.service.object.permissions().delete(
                fileId=self.id,
                permissionId=p.id,
                supportsAllDrives=True,
                useDomainAdminAccess = True
            ).execute()
            print("Permission supprimée, sur le drive ", self.nom)
        else:
            print("permission inexistante")
        
        return  
    

    def lister_fichiers(self) -> listeDossiers:
        """Renvoie un dictionnaire des fichiers du drive partagé"""
        retour = listeDossiers(self.service)
        page_token = None
        c=0
        while True:
            
            response = self.service.object.files().list(
                driveId=self.id,
                corpora="drive",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageSize=500,
                fields="nextPageToken,files(id, name, mimeType, modifiedTime)"   
            ).execute()

            files = response.get("files", [])
            
            
            for f in files:
                d = Dossier(f['name'],self.service)
                d.id = f['id']
                retour.l.append(d)
            print("Tour",c)
            c+=1
            page_token = response.get("nextPageToken")
            if not page_token:
                break

        return retour
    

    def charger_permissions(self):
        
        page_token = None   
        while True:
            response = self.service.object.permissions().list(
                fileId=self.id,
                supportsAllDrives=True,
                pageToken=page_token,
                pageSize=100,
                useDomainAdminAccess = True,
                fields="nextPageToken,permissions(id,emailAddress,type,role)",
            ).execute()
            print("-----------------------------------------------------------------------------------------------  ")

            for permiss in response.get('permissions',[]):
                per = Permission(permiss.get('id'),permiss.get('emailAddress'),permiss.get('role'))

                permiss[per.mail] = per #dictionnaire
            page_token = response.get("nextPageToken")
            if not page_token:
                break

    def afficher_permissions(self):
        ch = "Permissions de "+self.nom+": \n"
        for p in self.permissions :
            ch+= str(p)
        print(ch[:-1])


    # def retirer_permission(self,p: Permission):
    


    def __str__(self):

        ch = "Id {}\t\t\tName {}\n".format(self.id,self.nom)

        return ch

    def list_shared_drive_trash(self):
        page_token = None
        c = 0
        while True:
            response = self.service.object.files().list(
                corpora="drive",
                driveId=self.id,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                q="trashed = true and mimeType = 'application/vnd.google-apps.folder'",
                fields="nextPageToken, files(id, name, mimeType, trashedTime, parents)",
                pageToken=page_token
            ).execute()

            for file in response.get("files", []):
                c+=1
                print(f"{file['name']} | {file['mimeType']} | {file['id']}")

            page_token = response.get("nextPageToken")
            if not page_token:
                break
        print(c)

class ListeDrivePartages:
    def __init__(self,service: Service) -> None:
        self.l : dict[str, DrivePartage]
        self.service = service

    def maj(self):
        drives = []
        page_token = None
        c = 0
        while True:
            print("page: ",c)
            response = self.service.object.drives().list(
                pageSize = 100,
                pageToken=page_token,
                useDomainAdminAccess = 'True',  
            ).execute() 
            page_token = response.get('nextPageToken')
            drives.extend(response.get('drives', []))
            if not page_token:
                break
            
            c += 1
        c = 1
        print("-----------------Ajout des permissions-----------------")
        for d in drives:
            d2 = DrivePartage(d['name'],self.service)
            d2.id = d['id']
            d2.charger_permissions()
            self.l[d2.nom] =  d2
            print(c,"/",len(drives))
            c+=1
        with open("pickle/drives.pkl","wb") as f:
            pickle.dump(self,f)
        
        
    def __str__(self):
        ch="-"*23+"| Liste de drives |"+"-"*22+"\n"
        drive: DrivePartage
        for drive in self.l.values():
            ch+=str(drive)
        return ch
    
    def load(self):
        with open("pickle/drives.pkl","rb") as f:
            temp = pickle.load(f)
        self.l = temp.l

    def write(self):
        with open("sorties_textes/drives.txt","w",encoding='utf8') as f:
            f.write(str(self))

    def get(self,nom:str):
        return self.l.get(nom)
    

                
