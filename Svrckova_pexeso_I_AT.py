import tkinter
from random import *
canvas=tkinter.Canvas(width=1020,height=500,bg="white")
canvas.pack()

def nacitaj_obrazky(nazov_suboru,typ_suboru,pocet_kariet,par_pole_obrazkov):
    for i in range(pocet_kariet):
        obr = tkinter.PhotoImage(file = nazov_suboru + str(i) + typ_suboru)
        par_pole_obrazkov.append(obr)

def kresli_rub(sur_x,sur_y,par_pole_oznacenia_kariet):
    c = 0
    for y in range(4):
        for x in range(8):
            canvas.create_image(sur_x+x*125, sur_y+y*85, image=zadna_strana_karty, tag=par_pole_oznacenia_kariet[c])#vykreslí kartu a dá jej štítok(tag)
            c = c + 1

def informacie():
    oznam1 = "Na ťahu je "+hrac
    oznam2 = "Skóre:     " +meno1 + " :  " +str(body1) + "     " +meno2 + " :  " +str(body2)
    canvas.delete("ťah")
    canvas.delete("výsledok")
    canvas.create_text(500, 400, text = oznam1, font = "Arial 24", fill = "darkgreen", tag = "ťah")
    canvas.create_text(500, 450, text = oznam2, font = "Arial 24", fill = "darkblue", tag = "výsledok")

def kliknutie_mysou(sur):
    global pocet_otocenych_kariet, pole_otocene_karty, body1, body2, hrac
    ID_zakliknuteho_objektu = canvas.find_withtag("current") #každý vykreslený objekt má svoje číslo (identifikátor) 
                                                             #príkaz "find.withtag" vracia poradové číslo, v ktorom bol objekt vykreslený na plochu (premenná má typ "pole")
    if len(ID_zakliknuteho_objektu) > 0: #ak bolo klinuté na kartu
        print(ID_zakliknuteho_objektu)
        ID_zakliknuteho_objektu = ID_zakliknuteho_objektu[0]#cislo objektu na ktory som klikla
        print("Klikol si na ",ID_zakliknuteho_objektu)
        tagy = canvas.gettags(ID_zakliknuteho_objektu)       #príkaz "gettags" vracia všetky tagy, ktoré sú priradené k zakliknutému objektu (premenná má typ "pole")
        print("Karta má tag: ", tagy)  #prvý tag je "rub_x" a druhý tag je "current"
        stara_znacka = tagy[0]  
        print("Je to karta so starou značkou: ",stara_znacka)
        info = stara_znacka.split("_")#premenná info má typ poľa
        print(info)
        
        #klikli sme na rub alebo líce?
        if info[0] == "rub":
            pocet_otocenych_kariet += 1
            nova_znacka="lice_" + info[1]#vytvorí sa nová značka
            pole_otocene_karty.append(nova_znacka) #do poľa(zoznamu) otočených kariet pridá novú značku
            print("Táto karta bude mať novú značku: ",nova_znacka)
            cislo_obrazku=int(info[1]) #zistíme číslo obrázku
            print("Pridám nový tag k zakliknutej karte: ")
            canvas.addtag_withtag(nova_znacka,ID_zakliknuteho_objektu) #príkaz "addtag.withtag" pridá nový tag k zakliknutému objektu
            print(canvas.gettags(ID_zakliknuteho_objektu)) #funkcia vracia všetky tagy, ktoré sú priradené k zakliknutému objektu (premenná má typ "pole")
            print("Vymažem starý tag na zakliknutej karte: ")
            canvas.dtag(ID_zakliknuteho_objektu,stara_znacka)#vymaže starý tag zo zakliknutého objektu
            print(canvas.gettags(ID_zakliknuteho_objektu)) #funkcia vracia všetky tagy, ktoré sú priradené k zakliknutému objektu (premenná má typ "pole")
            canvas.itemconfig(ID_zakliknuteho_objektu, image=pole_obrazkov[cislo_obrazku])#v zakliknutom objekte zmení parameter "image" (namiesto zadnej strany dá obrázok)
        else:
            print("Klikol si na líce")
            
        if pocet_otocenych_kariet == 2:
            print("Sú otočené kartičky: ", pole_otocene_karty)
            canvas.update() #zobrazí nové zmeny v grafickej ploche
            canvas.after(1000) #pozdrží beh programu o zadaný počet milisekúnd
            if pole_otocene_karty[0] == pole_otocene_karty[1]: #otočené karty sú rovnaké
                canvas.delete(pole_otocene_karty[0]) # zruší objekt, teda vymaže otočené kartičky
                if hrac == meno1:
                    body1 += 1
                else:
                    body2 += 1
                informacie()
                if body1 + body2 == 16: #to znamená, že už boli otočené všetky karty
                    if body1 > body2:
                        canvas.create_text(560,200,text="Vyhral hráč: "+meno1,font="Arial 50", fill="red")
                    elif body1 < body2:
                        canvas.create_text(560,200,text="Vyhral hráč: "+meno2,font='Arial 50', fill="red")
                    else:
                        canvas.create_text(560,200,text="Remíza!",font="Arial 50", fill="red")
                    
            else:    #karty nie sú rovnaké, otoč ich naspäť
                for k in pole_otocene_karty:
                    print(k)
                    info = k.split("_")
                    print(info)
                    nova_znacka = "rub_" + info[1]
                    ID = canvas.find_withtag(k) #príkaz zistí čísla objektov, ktoré boli otočené
                    print(ID)
                    canvas.addtag_withtag(nova_znacka,ID) #príkaz "addtag.withtag" pridá nový tag k zakliknutému objektu
                    canvas.dtag(ID,k)  #vymaže tag "lice_x" z oboch zakliknutých (otočených) objektov
                    canvas.itemconfig(ID, image=zadna_strana_karty) #v oboch zakliknutých objektoch zmení parameter "image" (namiesto "obrázku" dá "zadnú stranu")    
            pocet_otocenych_kariet = 0
            pole_otocene_karty = []
            if hrac == meno1:
                hrac = meno2
            else:
                hrac = meno1
            informacie()    
    else:
        print("Klikol si mimo karty")
              
#hlavny program
meno1 = input(str("Zadaj meno 1.hráča: "))
meno2 = input(str("Zadaj meno 2.hráča: "))
hrac = meno1 #meno hráča
body1 = 0 # počet bodov 1. hráča
body2 = 0 # počet bodov 2. hráča
pocet_otocenych_kariet = 0  #koľko kartičiek je otočených
pole_otocene_karty = []  #zoznam otočených kartičiek (toto pole má max 2 prvky)
pole_obrazkov = [] #do tohoto poľa načítam obrázky
pole_oznacenia_kariet = [] #toto pole používam ako "tagy" (na identifikáciu kartičky)
nacitaj_obrazky("obrazky/vlajka_", ".png", 16, pole_obrazkov)
zadna_strana_karty=tkinter.PhotoImage(file = "obrazky/pexeso_vlajky.png")
for i in range(16):  #naplním si pole označenia kariet
    pole_oznacenia_kariet.append("rub_" + str(i))
print(pole_oznacenia_kariet)
pole_oznacenia_kariet = pole_oznacenia_kariet + pole_oznacenia_kariet
print(pole_oznacenia_kariet)
shuffle(pole_oznacenia_kariet) #náhodne premiešam prvky poľa 
print(pole_oznacenia_kariet)
kresli_rub(70, 50, pole_oznacenia_kariet)#vykreslenie 32 kariet(rubov)
informacie()   #výpis informácií o hráčoch
canvas.bind('<Button-1>', kliknutie_mysou)

