from .Authentification import Service


class Dossier:
    def __init__(self,name:str,service):
        self.name = name
        self.id = '\0'
        self.service = service
        self.parent_id = '\0'
    
    def upload(self,service : Service, idD2 : str):
        file_metadata = {
            'name': self.name,
            'mimeType': 'application/vnd.google-apps.folder',
            'driveId': self.id,
            'parents': [idD2]  # mettre le dossier parent si tu veux un sous-dossier
        }
        folder = service.object.files().create(
            body=file_metadata,
            supportsAllDrives=True,
            fields='id'
        ).execute()
        self.id = folder['id']
        print('Dossier créé, ID:', folder.get('id'))



    def move_drive_to_drive(self, folder_id,service: Service):



        # pylint: disable=maybe-no-member
        # Retrieve the existing parents to remove
        file = service.object.files().get(fileId=self.id,fields="parents",supportsAllDrives=True).execute()
        previous_parents = ",".join(file.get("parents"))
        # Move the file to the new folder
        file = (
            service.object.files()
            .update(
                fileId=self.id,
                addParents=folder_id,
                removeParents=previous_parents,
                supportsAllDrives=True,
                fields="id, parents",
            )
            .execute()
        )
        print("Déplacement effectué")

    def transfer_folder_ownership(self,NEW_OWNER: str):
        # 1️⃣ Ajouter le nouveau propriétaire
        permission = self.service.object.permissions().create(
            fileId=self.id,
            body={
                "type": "user",
                "role": "reader",
                "emailAddress": NEW_OWNER
            },
            # transferOwnership=True
        ).execute()



        print("Transfert effectué avec succès.")
        print(permission)

    def restore_folder(self):
        self.service.object.files().update(
            fileId=self.id,
            body={"trashed": False},
            supportsAllDrives=True
        ).execute()

        print("Dossier restauré avec succès.")

    def __str__(self):

        ch = "Id {}\t\t\tName {}\n".format(self.id,self.name)

        return ch

class listeDossiers:
    def __init__(self,service: Service) -> None:
        self.l = []
        self.service = service
        pass
    
    def remplir(self):
        """Permet de remplir la liste des dossier d'après le 'monDrove' du user authntifié dans Service"""
        page_token = None

        while True:
            response = self.service.object.files().list(
                corpora="user",
                fields="nextPageToken, files(id, name,parents)",
                q="trashed = false and 'me' in owners",
                pageToken=page_token
            ).execute()

            for file in response.get("files", []):
                d = Dossier(file['name'],self.service)
                d.id = file['id']
                d.parent_id = file['parents']
                self.l.append(d)

            page_token = response.get("nextPageToken", None)
            if not page_token:
                break

    def list_user_files(self):
        page_token = None

        while True:
            response = self.service.object.files().list(
                corpora="user",
                fields="nextPageToken, files(id, name, mimeType, parents)",
                q="trashed = false and 'me' in owners",
                pageToken=page_token
            ).execute()

            for file in response.get("files", []):
                print(f"{file['name']} | {file['mimeType']} | {file['id']} | {file['parents']}")

            page_token = response.get("nextPageToken", None)
            if not page_token:
                break

    def __str__(self):
        ch="-"*23+"| Liste de dossiers |"+"-"*22+"\n"
        dossier: Dossier
        for dossier in self.l:
            ch+=str(dossier)
        return ch