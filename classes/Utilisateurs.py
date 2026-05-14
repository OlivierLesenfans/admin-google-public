from .Authentification import Service
import pickle


LG_MAX_MAIL = 70

class Utilisateur:
    def __init__(self,mail: str,service: Service, nom="générique",prenom="adresse"):
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.id = str()
        self.dateCreation = str()
        self.etat = str()
        self.derniere_co = str()
        self.espace = str() 

        self.service = service


    def __str__(self):
        ch = "Id {}\t\t\tetat {}\t\t\tmail {}\n".format(self.id,self.etat,self.mail)
        return ch
    

class listeUtilisateurs:
    def __init__(self,service: Service,deleted=False) -> None:
        self.l = []
        self.d : dict[str, Utilisateur] = dict()
        self.service = service
        self.deleted = deleted


    def maj(self):
        lst_users = []
        page_token = None
        c = 0
        file = "pickle/utilisateurs.pkl"
        while True:
            print("page: ",c)
            response = self.service.object.users().list(
                customer='my_customer',
                maxResults=500,
                pageToken=page_token,
                showDeleted = self.deleted
            ).execute() 
            page_token = response.get('nextPageToken')
            lst_users.extend(response.get('users', []))
            if not page_token:
                break
            c += 1

        for user in lst_users:
            u2 = Utilisateur(user['primaryEmail'],self.service,user['name']['familyName'],user['name']['givenName'])
            u2.id = user['id'];u2.dateCreation = user['creationTime'];u2.derniere_co = user['lastLoginTime']
            if self.deleted:
                file = "pickle/utilisateurs_supprimes.pkl"
            else:
                if user['suspended'] == True:
                    u2.etat = 'suspended'
                else:
                    u2.etat = 'active'
            self.l.append(u2)
            self.d[u2.mail] = u2
        
        with open(file,"wb") as f:
            pickle.dump(self,f)

    def nbUser(self):
        page_token = None
        page = 0
        while True:
            print("page: ",page)
            response = self.service.object.users().list(
                customer='my_customer',
                maxResults=500,
                pageToken=page_token,
            ).execute() 
            page_token = response.get('nextPageToken')
            if not page_token:
                break
            page += 1
        return 
    
    def load(self):
        file: str = "pickle/utilisateurs.pkl"
        if self.deleted:
            file = "pickle/utilisateurs_supprimes.pkl"
        with open(file,"rb") as f:
            temp = pickle.load(f)
        self.l = temp.l                 #Petit tour de passe passe pour modifier l'instance

    def __str__(self):
        ch="-"*23+"| Liste d'utilisateurs: |"+"-"*22+"\n"
        for user in self.l:
            ch+=str(user)
        return ch
    
    def supprimerUserListe(self,mail:str):
        usr: Utilisateur
        l2 = list()
        for usr in self.l:
            if usr.mail != mail:
                l2.append(usr)
        return l2 


    def ajouter(self,mdp:str,u:Utilisateur):
        user_body = {
            "primaryEmail": u.mail,
            "name": {
                "givenName": u.prenom,
                "familyName": u.nom
            },
            "password": mdp,
            "changePasswordAtNextLogin": True
        }

        self.service.object.users().insert(body=user_body).execute()
        self.l.append(u)
        print("Utilisateur {} ajouté".format(u.mail))

    def update(self,mdp:str,u:Utilisateur):
        user_body = {
            "primaryEmail": u.mail,
            "name": {
                "givenName": u.prenom,
                "familyName": u.nom
            },
            "password": mdp,
            "changePasswordAtNextLogin": True
        }

        self.service.object.users().update(body=user_body,userKey=u.mail).execute()
        print("Utilisateur {} mis à jour".format(u.mail))

    def supprimer(self,mail: str):
        self.service.object.users().delete(userKey=mail).execute()
        self.l = self.supprimerUserListe(mail)
        print("Utilisateur {} supprimé.".format(mail))

    def write(self):
        with open("sorties_textes/users.txt","w",encoding='utf8') as f:
            f.write(str(self))

    def restore_user(self,mail):
        us: Utilisateur
        user_id = ''
        for us in self.l:
            if us.mail == mail:
                user_id = us.id
                print("---------------------------------------------")
                print(us)
        print("debug")
        print(user_id)
        print(len(user_id))
        
        self.service.object.users().undelete(
            userKey=user_id,
            body={"suspended": False}
        ).execute()
        

        print("restauré :", mail)


    def get(self,mail:str) -> Utilisateur | None:
        return self.d.get(mail)
    
    def get2(self,mail:str) -> Utilisateur | None:
        u: Utilisateur
        for u in self.l:
            if u.mail == mail:
                return u
        return None