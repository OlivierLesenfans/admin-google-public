from .Authentification import *
import pickle

class Permission:
    def __init__(self,id,mail,role) -> None:
        self.id = id
        self.mail = mail
        self.role = role

    def __str__(self):
        mail = "mail: {}".format(self.mail)
        while (len(mail) < 70):
            mail += ' '
        return mail+"role: {}\n".format(self.role)