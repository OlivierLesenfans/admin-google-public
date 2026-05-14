from .Authentification import Service
from .Utilisateurs import *
import pickle



class Group:
    def __init__(self,mail: str, nom: str, service: Service,description = ""):
        self.mail = mail
        self.nom = nom
        self.description = description
        self.id = '\0'
        self.membresKey = list()
        self.membres : listeUtilisateurs
        
        self.service = service

    def format(self):
        c2 = str()
        for ch in self.mail:
            c = ch.lower()
            if c == 'ç':
                c2 += 'c'
            elif c == 'à':
                c2+= 'a'
            elif c== 'é' or c== 'è' or c == 'ê':
                c2+= 'e'
            elif c== " ":
                pass
            else:
                c2+= c
        self.mail = c2


    def upload(self):

        # Création du groupe
        group_body = {
            'email': self.mail,
            'name': self.nom,
        }
        
        group = self.service.object.groups().insert(body=group_body).execute()
        self.id = group['id']
        print("Groupe créé avec l'ID :", group['id'])


    def rename(self,mail: str,nom: str):

        # Création du groupe

        
        group_body = {
            'email':mail
        }
        
        self.service.object.groups().update(body=group_body,groupKey=self.mail).execute()
        self.mail = mail
        print("Groupe renommé :", self.mail)



    def ajouter_membre(self,user_mail: str, role: str):
        """Permet d'ajouter un membre à un groupe"""
        member_body = {
            "role": role,   # ou "OWNER" pour admin max
            "email": user_mail
        }

        self.service.object.members().insert(
            groupKey=self.mail,
            body=member_body
        ).execute()
        self.membresKey.append(user_mail)
        print("{} Ajouté au groupe :{}".format(user_mail, self.mail))

    def modifier_membres(self,user_mail: str, role: str):
        """Permet d'ajouter un membre à un groupe
        MEMBER ou "OWNER" pour admin max"""
        member_body = {
            "role": role,   
            "email": user_mail
        }

        reponse = self.service.object.members().update(
            groupKey=self.mail,
            memberKey=member_body["email"],
            body=member_body
        ).execute()
        self.membresKey.append(user_mail)
        print("Utilisateur modifié :", user_mail)

    def lister_membres(self):
        print("chargement groupe en coours du groupe:",self.mail)
        lst_usr = []
        page_token = None
        c = 0
        while True:
            response = self.service.object.members().list(
                groupKey = self.mail,
                maxResults=500,
                pageToken=page_token,
            ).execute() 
            page_token = response.get('nextPageToken')

            lst_usr.extend(response.get('members', []))
            # print(response)
            if not page_token:
                break
            c += 1
        print("chargement groupe terminé")

        tousUtilisateurs = listeUtilisateurs(Service('u'))
        tousUtilisateurs.load()

        for usr in lst_usr:
            usrTemp = usr.get("email")
            if usrTemp != None:
                u = tousUtilisateurs.get(usrTemp)
                if (u):
                    self.membresKey.append(u.mail)

    
    def __str__(self):
        return "Id {}\t\t\tName {}\t\t\tmail: {}\n".format(self.id,self.nom,self.mail)
    
    def get_id(self):
        request = self.service.object.groups().get(groupKey=self.mail).execute()
        self.id = request['id']
    
    def supprimer_Membre(self,mail):
        self.service.object.members().delete(
            groupKey=self.mail,
            memberKey=mail
        ).execute()

        print("Membre {} supprimé.".format(mail))
    
    def charger_membres(self,lu: listeUtilisateurs):
        u : Utilisateur | None

        self.membres = listeUtilisateurs(self.service)
        for mail in self.membresKey:
            u = lu.get(mail)
            self.membres.l.append(u)
            pass


class ListGroups:
    def __init__(self,service: Service) -> None:
        self.l = list()
        self.service = service



    def maj(self):
        lst_grp = []
        page_token = None
        c = 0
        while True:
            print("page: ",c)
            response = self.service.object.groups().list(
                customer='my_customer',
                maxResults=500,
                pageToken=page_token,
            ).execute() 
            page_token = response.get('nextPageToken')
            lst_grp.extend(response.get('groups', []))
            if not page_token:
                break
            c += 1
        for grp in lst_grp:
            u2 = Group(grp['email'],grp['name'],self.service)
            u2.id = grp['id']
            u2.lister_membres()
            self.l.append(u2)
        
        with open("pickle/groupes.pkl","wb") as f:
            pickle.dump(self,f)

    def load(self):
        with open("pickle/groupes.pkl","rb") as f:
            temp = pickle.load(f)
        self.l = temp.l  

    def __str__(self):
        ch="-"*23+"| Liste de groupes |"+"-"*22+"\n"
        for drive in self.l:
            ch+=str(drive)
        return ch
    
    def get(self,mail:str) -> Group:
        g: Group
        for g in self.l:
            if g.mail == mail:
                return g
        return g

    def write(self,bin=0):
        if bin == 0:
            with open("sorties_textes/groupes.txt","w",encoding='utf8') as f:
                f.write(str(self))
        else:
            with open("pickle/groupes.pkl","wb") as f:
                pickle.dump(self,f)


    
