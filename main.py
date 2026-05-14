#main.py


from classes import *




def main():

    su = Service("u")

    listeDrives = listeUtilisateurs(su)

    listeDrives.load() #Attention, nécessite que vous ayez applé la fonction maj au moins une fois
    

    print(listeDrives)
    
    return 0

main()