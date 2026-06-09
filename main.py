#main.py


from classes import *




def main():

    su = Service("u")


    listeDrives = listeUtilisateurs(su)
    listeDrives.maj()
    listeDrives.load() #Attention, nécessite que vous ayez appelé la fonction maj au moins une fois
    

    print(listeDrives)
    
    return 0

main()