# -*- coding: utf-8 -*-
'''
LE JEU DE LA VIE
Mini projet numéro 2 de NSI

Modélisation Objet :

Q1) On peut dégager, au premier abord : une classe cellule (avec un attribut état et un autre voisins) et une classe grille (avec un attribut ordonnée et un autre abscisse). En effet, ce sont les deux éléments du jeu.

Q2) On pourrait donner une méthode pour changer l’état de la cellule, une autre pour obtenir son état. Une autre pour définir les voisins et encore une pour les obtenir. Avec ces méthodes, on pourra modifier l’état des cellules  et calculer celui-ci en fonction de ses voisins.
Pour ce qui est de la classe grille, on pourrait coder une méthode pour obtenir les coordonnées, un autre pour les modifier. Ainsi, on pourra placer les cellules dans la grille là où il n’y en a pas forcément.

Q3) Il sera plus simple de représenter la notion de voisinage dans la cellule avec la classe grille. En effet, c’est elle qui contient les coordonnées.
Quand au calcul de celle-ci, elle sera plus simple dans la classe cellule car c’est cette classe qui contient l’état. 

Q4) Une cellule qui n’est pas au bord a 8 voisins. En effet, le voisinage de Moore compte les diagonales.
Une cellule sur le côté mais pas dans un coin a 5 voisins.
Dans un coin, elle en a 3.

Q5) Pour la case en haut à droite, on pourrait considérer comme voisin de droite la case tout en haut à gauche. Pour le voisin du haut, on peut considérer la case de même abscisse mais d’ordonnée 0 (celle tout en bas). En fait, on prendrait la case d’abscisse ou d’ordonnée « opposée » comme suivante. Cela afin de ne pas avoir que 3 cases prises en compte lors du calcul de l’état en fonction des voisins.

Q8) Cela peut être utile pour vérifier facilement l’état d’une cellule. Ainsi, on peut l’interpréter dans une autre fonction ou même créer facilement une liste qui serait utilisée comme « historique » de la cellule.
'''

from random import randint
from time import sleep
from tkinter import filedialog
from tkinter import *

class Cellule:
    def __init__(self):
        '''constructeur qui initialise les variables'''
        self.__actuel= False
        self.__futur= False
        self.__voisins= None
    
    def est_vivant(self):
        '''accesseur qui retourne l'état actuel de la cellule'''
        return self.__actuel
    
    def set_voisins(self,L):
        '''mutateur qui permet de modifier les voisins de la cellule. Prends en argument une liste'''
        if type(L)== list: #vérifie si l'élément donné est bien une liste
            self.__voisins= L
    
    def get_voisins(self):
        '''accesseur qui renvoie les voisins de la cellule'''
        return self.__voisins
    
    def naitre(self):
        '''mutateur qui passe l'état futur de la cellule à True'''
        self.__futur=True

    def mourir(self):
        '''mutateur qui passe l'état futur de la cellule à False'''
        self.__futur=False
    
    def basculer(self):
        '''mutateur qui change l'état actuel de la cellule pour l'état futur'''
        self.__actuel=self.__futur
    
    def __str__(self):
        '''méthode protégée qui renvoie 🌱 si la cellule est actuellement vivante. Sinon, elle renvoie  💀'''
        if self.__actuel== True:
            return "🌱"
        else:
            return "💀"

    def calcule_etat_futur(self):
        '''fonction qui calcule l'état futur des cellules via les règles du jeu'''
        acc=0 #compteur qui va permettre de savoir le nombre de voisins vivants
        for i in range (len(self.__voisins)):#parcours tout les voisins
            if self.__voisins[i]==True: #si le voisin est vivant
                acc=acc+1
        
        #vérifie toutes les possibilités offertes par les règles du voisinage de Moore
        if acc==3 and self.__actuel==False:
            self.naitre()
        if acc!=3 and self.__actuel==False:
            self.mourir()

        elif (acc==2 or acc==3) and self.__actuel==True:
            self.naitre()
        elif (acc!=2 or acc!=3) and self.__actuel==True:
            self.mourir()

class Grille:
    def __init__(self):
        '''constructeur qui initialise les variables'''
        self.largeur=20
        self.hauteur=30
        self.matrice=[]
    
    def clear_matrice(self):
        '''mutateur qui remet la matrice à 0'''
        self.matrice=[]

    def set_largeur(self,x):
        '''mutateur qui change la largeur de la grille. Prends un nombre entier en paramètre'''
        if type(x)==int:
            self.largeur=x

    def set_hauteur(self,x):
        '''mutateur qui change la hauteur de la grille. Prends un nombre entier en paramètre'''
        if type(x)==int:
            self.hauteur=x

    def dansgrille(self,i,j):
        '''Fonction qui prends en paramètres 2 points (nombres entiers) et dit si ils se trouvent dans la grille''' 
        if self.hauteur-1>=i>=0 and self.largeur-1>=j>=0: #si les coordonées de l'utilisateur sont comprises entre 0 et la largeur/hauteur en fonction du point
            return True
        
        else:
            return False

    def setXY(self,i,j,valeur):
        '''mutateur qui prend en compte des coordonées (nombres entiers) et une valeur. Si les coordonées sont dans la liste, ajoute la valeur à cet endroit'''
        if self.dansgrille(i,j)==True:
            self.matrice[i][j]= valeur
        else:
            return 'out of range, not added'
    
    def getXY(self,i,j):
        '''accesseur qui renvoie la valeur de la celllule dans la coordonée rentée par l'utilisateur si celle ci est dans la grille'''
        if self.dansgrille(i,j)==True:
            return self.matrice[i][j]
   
    def get_largeur(self):
        '''accesseur qui retourne la largeur de la grille'''
        return self.largeur
    
    def get_hauteur(self):
        '''accesseur qui permet de récupérer la valeur de la hauteur de la grille'''
        return self.hauteur
    
    @staticmethod
    def est_voisins(i,j,x,y,instance):
        '''fonction qui prend en paramètres les coordonées de deux points et retourne True si ils remplissent la notion de voisinage selon Moore'''
        abx=None
        ordo=None
        if i==x and j==y: #si c'est le même point
            return False

        for b in range (-1,2):
            #regarde si i est en bordure, adapte le point voisin à chercher en fonction
            if b+i<0: 
                abx= instance.largeur+b
            if b+i>instance.get_largeur()-1:
                abx=0
            else:
                abx=b+i
            for c in range(-1,2):
                #regarde si j est en bordure, adapte le point voisin à chercher en fonction
                if j+c<0:
                    ordo= instance.get_hauteur()+c
                if j+c>instance.get_hauteur()-1:
                    ordo=0
                else:
                    ordo=c+j
                #compare le point à chercher avec x et y. Si ils correspondent, ça veut dire que les points sont voisins
                if x==abx and y==ordo:
                    return True
            
        return False #si aucun des points n'est voisins. En effet, sinon la fonction s'arrête avec le "return True" à la ligne 162
    
    def get8voisins(self,i,j):
        '''fonction qui donne la liste des voisins d'une cellule si celle ci est dans la grille'''
        if self.dansgrille(i,j)==True:
            L_voisins=[]
            for b in range (-1,2):
            #regarde si i est en bordure, adapte le point voisin à chercher en fonction
                if b+i<0: 
                    abx= self.get_hauteur()+b
                elif b+i>self.get_hauteur()-1:
                    abx=0
                else:
                    abx=b+i
                for c in range(-1,2):
                    #regarde si j est en bordure, adapte le point voisin à chercher en fonction
                    if j+c<0:
                        ordo= self.get_largeur()+c
                    elif j+c>self.get_largeur()-1:
                        ordo=0
                    else:
                        ordo=c+j
                    
                    #ajoute le point voisin
                    if abx!=i or ordo!=j:
                        data=self.getXY(abx,ordo)
                        L_voisins.append(data.est_vivant())
            return L_voisins
        
        else:
            return None

    def __str__(self):
        '''fonction qui affiche le jeu de la vie dans le terminal'''
        #parcours tout les éléments du jeu
        for i in range(len(self.matrice)):
            display=[]
            for j in range(len(self.matrice[i])):
                display.append(self.matrice[i][j].__str__())#ajoute le résultat
            print(display)
        
        print('\n')

    def getallstate(self):
        '''fonction qui renvoie tout les etats'''
        #parcours tout les éléments du jeu
        allin=""
        for i in range(len(self.matrice)):
            display=""
            for j in range(len(self.matrice[i])):
                display=display+str(self.matrice[i][j].__str__())#ajoute le résultat
            allin=allin+display+'\n'
        return allin
        

    def remplir_alea(self,pourcent):
        '''fonction qui prends en paramètres un nombre entier faisant office de pourcentage et qui rempli la matrice de cellule. Un poucentage (celui rentré) de ces cellules sont aléatoirement vivantes'''
        if 0<int(pourcent)<=100:
            cases=self.largeur*self.hauteur
            nombre=int(cases*(pourcent/100))# calcule le nombre de cellules devant être vivantes
            L_vivant=[]
            
            while len(L_vivant)!=nombre: #boucle qui crée des ordonées ou abscisses aléatoire jusqu'a ce que le nombre demandé soit atteint
                y= randint(0,self.largeur-1)
                x= randint(0, self.hauteur-1)
                if (x,y) not in L_vivant: #ajoute l'abscisse si elle n'est pas deja dans la liste
                    L_vivant.append((x,y))
            
            for i in range(0,self.hauteur):
                self.matrice.append([])#crée une nouvelle liste pour stocker une ligne supplémentaire
                for b in range(0,self.largeur):
                    self.matrice[i].append(Cellule())#ajoute une cellule dans la liste
                    if (i,b) in L_vivant: #si la cellule est dans la liste de celles devant être vivantes
                        cellule=self.getXY(i,b) #obtient la cellule
                        cellule.naitre()#passer l'état futur de la celllule à vivant
                        cellule.basculer()#fait naître la cellule
                        self.setXY(i,b,cellule) #remplace la cellule "morte"
        else:
            return False

    def Jeu(self):
        '''fonction qui calcule l'état futur de chaque cellule'''
        for i in range(0,self.hauteur): #parcours chaque point en hauteur
            for b in range(0,self.largeur):#parcours chaque point en largeur
                cellule=self.getXY(i,b) #obtiens les informations
                cellule.set_voisins(self.get8voisins(i,b))#change la valeur des voisins du point
                cellule.calcule_etat_futur()
                self.setXY(i,b,cellule)#change les données de la cellule dans la matrice
    
    def actualise(self):
        '''fonction qui actualise l'état de toutes le cellules'''
        for i in range(0,self.hauteur):#parcours chaque point en hauteur
            for b in range(0,self.largeur):#parcours chaque point en largeur
                cellule=self.getXY(i,b) #obtiens la cellule
                cellule.basculer() #bascule l'état
                self.setXY(i,b,cellule) #change l'état de la cellule dans la matrice

def bakbak(*args):
    '''fonction qui affiche le jeu en interface graphique'''
    prépartie.pack_forget() #cache l'écran de paramètrage
    plateau.clear_matrice() #nettoye le plateau
    plateau.set_largeur(int(numberofcol.get()))#change la largeur du plateau selon celle renseignée
    plateau.set_hauteur(int(numberoflign.get()))#change la hauteur du plateau selon celle renseignée
    tours=int(numberofturn.get()) #change le nombre de tours
    partie=Frame(fenetre,bg='#85c17e')
    plateau.remplir_alea(int(pourcent.get()))#crée le plateau de base
    touracc=StringVar()
    printer=Label(partie, textvariable=touracc,bg="#85c17e",font=('Time News Roman', 19), fg="white")#crée une zone de texte dynamique pour le nombre de tour
    printer.pack(padx=10,pady=10)
    actuel=StringVar()
    actuel.set('')
    printer1=Label(partie, textvariable=actuel,bg="#85c17e",font=('Time News Roman', 20))#crée une zone de texte dynamique pour le plateau
    printer1.pack()
    

    def update(n=1,chain=''):
        '''fonction récursive qui prends pour paramètres un chaine de caractères et un nombre entier'''
        ch=''
        if n<tours+1:#si le nombre de tours demandés n'a pas été effectué
            touracc.set("Tour: "+str(n)) #affiche le numéro du tour
            plateau.Jeu()#actualise le jeu
            actuel.set(plateau.getallstate())#affiche le plateau pour ce tour
            plateau.actualise()#actualise le tour
            ch="Tour: "+str(n)+"\n"+plateau.getallstate()+'\n' #stocke les infos du tour
            chain=chain+ch#les ajoute à l'historique des tours
            partie.after(2000, update, n+1,chain)#attends 2 secondes puis recommence
        else:#si le nombre de tours demandés a été effectué
            def save():
                '''fonction qui sauvegarde chaque étape de la partie au forma .txt'''
                f = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("txt files"),("all files","*.*")))
                if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                    return
                with open(f,'w',encoding='utf-8') as result: #enregsitre le fichier sous le format UTF-8
                    result.write(chain)
                    result.close()
            Button(partie,text="Recommencer",command=restart,bg="#85c17e",font=('Noto Serif', 11)).pack(side=LEFT,padx=5) #affiche un bouton pour resélectionner des paramètres
            Button(partie,text='Sauvegarder la partie',command=save,bg="#85c17e",font=('Noto Serif', 11)).pack(side=LEFT,padx=5) #affiche un bouton pour sauvegarder l'historique de la partie
        
    def restart():
        partie.destroy()
        prépartie.pack()

    update()
    Button(partie,text="Quitter le jeu (fermera complètement la fenêtre)",command=quit,bg="#85c17e",font=('Noto Serif', 11)).pack(side=LEFT,padx=10) #affiche un bouton pour quitter la fenêtre
    partie.pack()
    
fenetre=Tk()
fenetre.title("Le jeu de la vie")
fenetre['bg']='#85c17e' #crée une couleur de fond verte
fenetre.geometry("1000x500") #choisis les dimensions de la fenêtre
plateau=Grille()

#titre de présentation
title= Label(fenetre, text="Le jeu de la vie", bg="#85c17e", font=('Courier New', 30), fg="white")
title.pack(padx=10)


'''Prépartie'''

prépartie=Frame(fenetre,borderwidth=2,relief='ridge',bg="#85c17e") #crée un cadre pour contenir tout les cadres de preparties
choix=Frame(prépartie,bg="#85c17e")#frame pour contenir le choix du pourcent
titlepourcent=Label(choix, text="Entrez le pourcentage de cellules vivantes souhaitées au démarrage ",bg="#85c17e",font=('Noto Serif', 11))
titlepourcent.pack(side=LEFT,padx=10)

'''pourcent'''
value = DoubleVar()
pourcent=Scale(choix, variable=value,cursor='dot',orient=HORIZONTAL,bg="#85c17e",troughcolor='white')#reglètte pour choisir le pourcentage
pourcent.pack(side=LEFT,padx=5,pady=10)


'''nombre de tours'''
nombretour=Frame(prépartie,bg="#85c17e")#contient le choix du nombre de tour
Label(nombretour, text="Entrez le nombre de tour souhaités",bg="#85c17e",font=('Noto Serif', 11)).pack(side=LEFT,padx=10)
numberofturn = Spinbox(nombretour, from_=1, to=100,bg="#85c17e",buttonbackground='white',cursor='dot') #spinbox pour choisir le nombre de tours
numberofturn.pack()

'''hauteur et largeur'''
nombrecolonnes=Frame(prépartie,bg="#85c17e",pady=10)#contient le choix du nombre de colonnes
Label(nombrecolonnes, text="Entrez le nombre de colonnes souhaitées",bg="#85c17e",font=('Noto Serif', 11)).pack(side=LEFT,padx=10)
numberofcol = Spinbox(nombrecolonnes, from_=1, to=100,bg="#85c17e",buttonbackground='white',cursor='dot')#spinbox pour choisir le nombre de colonnes
numberofcol.pack()

nombrelignes=Frame(prépartie,bg="#85c17e",pady=10)#contient le choix du nombre de colonnes
Label(nombrelignes, text="Entrez le nombre de lignes souhaitées",bg="#85c17e",font=('Noto Serif', 11)).pack(side=LEFT,padx=10)
numberoflign = Spinbox(nombrelignes, from_=1, to=100,bg="#85c17e",buttonbackground='white',cursor='dot')#spinbox pour choisir le nombre de lignes
numberoflign.pack()

'''validation'''
validate= Frame(prépartie,bg="#B76E79")
Button(validate,text="Valider et lancer le jeu",command=bakbak,bg="#85c17e", activebackground='white',cursor='star',font=('Noto Serif', 11)).pack(side=LEFT,padx=10,pady=15) #bouton qui permet de valider les paramètres séléctionnés


prépartie.pack()
choix.pack()
nombretour.pack()
nombrecolonnes.pack()
nombrelignes.pack()
validate.pack()

fenetre.mainloop()



    
