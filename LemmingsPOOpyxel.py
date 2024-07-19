import pyxel
import time

class Case:
    def __init__(self, caractere):
        self.terrain = caractere
        self.lem = None 
        
    def libre(self):
        return (self.terrain in ['I', ' ', 'O', 'L', 'K']) and self.lem is None

    def arrivee(self, lem):
        if self.terrain == 'O':
            lem.sortDuJeu()
        else:
            self.lem = lem

    def depart(self):
        self.lem = None
        
    def get_caractere(self):
        return self.terrain
    
    def est_cle(self):
        return self.terrain == 'K'
    
    def est_porte_verrouillee(self):
        return self.terrain == 'P'
    
    def est_porte_ouverte(self):
        return self.terrain == 'L'

    def ouvrir_porte(self, liste_lemmings):
        if self.est_porte_verrouillee() and any(lem.cle for lem in liste_lemmings):
            self.terrain = 'L'

        

class Lemming:
    def __init__(self, jeu, ligne, colonne, direction=1):
        self.j = jeu
        self.l = ligne
        self.c = colonne
        self.d = direction
        self.cle = False

    def peutBouger(self):
        return (self.l < len(self.j.grotte) - 1 and self.j.grotte[self.l + 1][self.c].libre()) or \
               (0 <= self.c + self.d < len(self.j.grotte[self.l]) and self.j.grotte[self.l][self.c + self.d].libre())

    def avance(self, dl, dc):
        self.j.grotte[self.l][self.c].depart()
        self.j.grotte[self.l + dl][self.c + dc].arrivee(self)
        self.l += dl
        self.c += dc

    def tourne(self):
        self.d = -self.d
        
    def ramasser_cle(self):
        next_col = self.c + self.d
        if 0 <= next_col < len(self.j.grotte[self.l]):
            next_case = self.j.grotte[self.l][next_col]
            if next_case.est_cle():
                next_case.terrain = ' '
                self.cle = True



    def ouvrir_porte(self):
        if self.j.grotte[self.l][self.c].est_porte_verrouillee() and self.cle:
            self.j.grotte[self.l][self.c].terrain = 'L'

    def action(self):
        if self.peutBouger():
            if self.j.grotte[self.l + 1][self.c].libre():
                self.avance(1, 0)
            else:
                self.avance(0, self.d)
        else:
            self.tourne()

    def sortDuJeu(self):
        self.j.listeLemmings.remove(self)
        
    def update(self):
        self.ramasser_cle()


class Jeu:
    def __init__(self, f: str):
        with open(f, "r", encoding='utf-8') as carte:
            self.grotte = [[Case(caractere) for caractere in ligne if caractere != '\n'] for ligne in carte.readlines()]
        self.listeLemmings = []
        self.pause = False
        self.souris_visible = False
        pyxel.init(len(self.grotte[0]) * 16, len(self.grotte) * 16, title="Jeu des Lemmings", fps=10)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_L):
            self.ajouteLemming()
        elif pyxel.btnp(pyxel.KEY_M):
            self.toggle_souris()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.toggle_pause()
        else:
            self.tour()
            for lem in self.listeLemmings:
                lem.update()
            self.ouvrir_portes(self.listeLemmings)
        if not self.pause:
            pyxel.cls(0)
        pyxel.load(r"game.pyxres") 
    

    def draw(self):
        pyxel.cls(0)
        for y, ligne in enumerate(self.grotte):
            for x, case in enumerate(ligne):
                
                if case.get_caractere() == '#':
                    pyxel.blt(x*16,y*16, 0, 0, 0, 16, 16)
                    
                if case.get_caractere() == ' ':
                    pyxel.blt(x*16,y*16, 0, 32, 16, 16, 16)
                    
                if case.get_caractere() == 'I':
                    pyxel.blt(x*16,y*16, 0, 16, 0, 16, 16)
                    
                if case.get_caractere() == 'O':
                    pyxel.blt(x*16,y*16, 0, 32, 0, 16, 16)
                    
                if case.get_caractere() == 'P':
                    pyxel.blt(x*16,y*16, 0, 0, 16, 16, 16)
                    
                if case.get_caractere() == 'L':
                    pyxel.blt(x*16,y*16, 0, 0, 32, 16, 16)
                    
                if case.get_caractere() == 'K':
                    pyxel.blt(x*16,y*16, 0, 16, 16, 16, 16)
                    
                if case.get_caractere() == 'B':
                    pyxel.blt(x*16,y*16,0,16,32,16,16)
                    
                if case.lem is not None:
                    if case.lem.d == 1:
                        pyxel.blt(x*16, y*16, 0, 48, 16, 16, 16, 5)
                    else:
                        pyxel.blt(x*16, y*16, 0, 48, 0, 16, 16, 5)
                        
        self.print_pause()
                
    def toggle_pause(self):
        self.pause = not self.pause
        
    def print_pause(self):
        if self.pause == True :
            pyxel.rect(275, 25,15,50,7)
            pyxel.rect(305, 25,15,50,7)
            pyxel.text(50, 120,'Le jeu est en pause',7)
                
            

    def ajouteLemming(self):
        if self.grotte[0][1].libre():
            lem = Lemming(self, 0, 1)
            self.listeLemmings.append(lem)
            self.grotte[0][1].arrivee(lem)

    def tour(self):
        if not self.pause :
            for l in self.listeLemmings:
                l.action()
                
    def ouvrir_portes(self, liste_lemmings):
        for ligne in self.grotte:
            for case in ligne:
                case.ouvrir_porte(liste_lemmings)
                
    def toggle_souris(self):
        self.souris_visible = not self.souris_visible
        pyxel.mouse(self.souris_visible)


Jeu('carte.txt')