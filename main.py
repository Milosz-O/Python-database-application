import sqlalchemy as db
import pandas as pd
import numpy as np
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from tkinter import *

#Polaczenie z baza
engine = db.create_engine("mysql://root:Bi9z!ydu3p@127.0.0.1:3306/dane_schema")
connection = engine.connect()
metadata = db.MetaData()
Base = declarative_base()

class Uzytkownik(Base):
    __tablename__ = 'uzytkownik'
    ID_uzytkownik = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(25))
    haslo = db.Column(db.String(25))
class Gatunek(Base):
    __tablename__ = 'gatunek'
    ID_gatunek = db.Column(db.Integer, primary_key=True)
    nazwa_gatunek = db.Column(db.String(25))
class Kontynent(Base):
    __tablename__ = 'kontynent'
    ID_kontynent = db.Column(db.Integer, primary_key=True)
    nazwa_kontynent = db.Column(db.String(25))
class Zywienie(Base):
    __tablename__ = 'zywienie'
    ID_zywienie = db.Column(db.Integer, primary_key=True)
    nazwa_zywienie = db.Column(db.String(25))
class Zagrozenie(Base):
    __tablename__ = 'zagrozenie'
    ID_zagrozenie = db.Column(db.Integer, primary_key=True)
    nazwa_zagrozenie = db.Column(db.String(25))
class Zwierze(Base):
    __tablename__ = 'zwierze'
    ID_zwierze = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nazwa_zwierze= db.Column(db.String(60))
    nazwa_lacinska_zwierze = db.Column(db.String(60))
    gatunek_numer = db.Column(db.Integer, db.ForeignKey(Gatunek.ID_gatunek))
    kontynent_numer = db.Column(db.Integer, db.ForeignKey(Kontynent.ID_kontynent))
    zywienie_numer = db.Column(db.Integer, db.ForeignKey(Zywienie.ID_zywienie))
    zagrozenie_numer = db.Column(db.Integer, db.ForeignKey(Zagrozenie.ID_zagrozenie))

Session = sessionmaker(bind=engine)
session = Session()

global gatunek
gatunek = ["Ssak", "Ptak", "Gad", "Plaz", "Ryba", "Bezkregowiec"]
global kontynent
kontynent = ["Ameryka Polnocna", "Ameryka Poludniowa", "Europa", "Afryka", "Antarktyda", "Azja", "Australia"]
global zywienie
zywienie = ["Miesozerca", "Roslinozerca", "Wszystkozerca"]
global zagrozenie
zagrozenie = ["Zagrozony", "Niezagrozony"]

def join_wyswietl():
    obszar.delete(0, END)

    rezultat = session.query(Zwierze, Gatunek, Kontynent, Zywienie, Zagrozenie) \
        .join(Gatunek, Zwierze.gatunek_numer == Gatunek.ID_gatunek) \
        .join(Kontynent, Zwierze.kontynent_numer == Kontynent.ID_kontynent) \
        .join(Zywienie, Zwierze.zywienie_numer == Zywienie.ID_zywienie) \
        .join(Zagrozenie, Zwierze.zagrozenie_numer == Zagrozenie.ID_zagrozenie).order_by(Zwierze.ID_zwierze).all()

    for Zwierze1, Gatunek1, Kontynent1, Zywienie1, Zagrozenie1 in rezultat:
        obszar.insert(END, "ID: " + str(Zwierze1.ID_zwierze) + " / Nazwa polska: " + Zwierze1.nazwa_zwierze + " / Nazwa lacinska: " + Zwierze1.nazwa_lacinska_zwierze + " / Gatunek: " + Gatunek1.nazwa_gatunek + " / Kontynent: " + Kontynent1.nazwa_kontynent + " / Zywienie: " + Zywienie1.nazwa_zywienie + " / Zagrozenie: " + Zagrozenie1.nazwa_zagrozenie)
def info_label(okno, wiadomosc, tytul):
    okno.title(tytul)
    okno.geometry("256x69")
    label = Label(okno,
                  text=wiadomosc,
                  font=("Arial", 10))
    label.pack()
def dodawanie():
    if (len(entry_nazwa.get()) > 60 or len(entry_nazwa_lacinska.get()) > 60 or len(entry_nazwa.get()) == 0 or len(entry_nazwa_lacinska.get()) == 0):
        wiadomosc_dodawanie = "Nazwa i nazwa lacinska nie moga\nbyc dluzsze niz 60 znakow oraz nie moga\nbyc puste"
        tytul_wiadomosc_dodawania = "Error"
        okno_wiadomosc_dodawanie = Toplevel(okno_dodaj)
        info_label(okno_wiadomosc_dodawanie, wiadomosc_dodawanie, tytul_wiadomosc_dodawania)
        okno_wiadomosc_dodawanie.mainloop()

        gatunek_wartosc.set(value=0)
        kontynent_wartosc.set(value=0)
        zywienie_wartosc.set(value=0)
        zagrozenie_wartosc.set(value=0)
    else:
        nowy_nazwa = entry_nazwa.get()
        nowy_nazwa_lacinska = entry_nazwa_lacinska.get()

        nowy_gatunek = gatunek_wartosc.get()+1
        nowy_kontynent = kontynent_wartosc.get()+1
        nowy_zywienie = zywienie_wartosc.get()+1
        nowy_zagrozenie =zagrozenie_wartosc.get()+1

        session.add(Zwierze(nazwa_zwierze=nowy_nazwa, nazwa_lacinska_zwierze=nowy_nazwa_lacinska, gatunek_numer=nowy_gatunek, kontynent_numer=nowy_kontynent, zywienie_numer=nowy_zywienie, zagrozenie_numer=nowy_zagrozenie))
        session.commit()

        gatunek_wartosc.set(value=0)
        kontynent_wartosc.set(value=0)
        zywienie_wartosc.set(value=0)
        zagrozenie_wartosc.set(value=0)

        join_wyswietl()

        okno_dodaj.destroy()
def dodaj():
    global okno_dodaj
    okno_dodaj = Toplevel(nowe_okno)

    okno_dodaj.title("Dodawanie")

    frame_dodaj = Frame(okno_dodaj)
    frame_dodaj.pack()

    label_nazwa = Label(frame_dodaj,text="Nazwa: ",font=("Arial", 25))
    label_nazwa.grid(row=0, column=0)

    global entry_nazwa
    entry_nazwa = Entry(frame_dodaj,font=("Arial", 25))
    entry_nazwa.grid(row=0, column=1, columnspan=2)

    label_nazwa_lacinska = Label(frame_dodaj,text="Nazwa lacinska: ",font=("Arial", 25))
    label_nazwa_lacinska.grid(row=1, column=0)

    global entry_nazwa_lacinska
    entry_nazwa_lacinska = Entry(frame_dodaj, font=("Arial", 25))
    entry_nazwa_lacinska.grid(row=1, column=1, columnspan=2)

    label_gatunek = Label(frame_dodaj, text="Gatunek: ", font=("Arial", 25))
    label_gatunek.grid(row=2, column=0)

    label_kontynent = Label(frame_dodaj, text="Kontynent: ", font=("Arial", 25))
    label_kontynent.grid(row=3, column=0)

    label_zywienie = Label(frame_dodaj, text="Zywienie: ", font=("Arial", 25))
    label_zywienie.grid(row=4, column=0)

    label_zagrozenie = Label(frame_dodaj, text="Zagrozenie: ", font=("Arial", 25))
    label_zagrozenie.grid(row=5, column=0)

    for index in range(len(gatunek)):
        radiobutton_gatunek = Radiobutton(frame_dodaj, text=gatunek[index],variable=gatunek_wartosc, value=index, width = 20, indicatoron=0)
        radiobutton_gatunek.grid(row=2, column=index+1)

    for index in range(len(kontynent)):
        radiobutton_kontynent = Radiobutton(frame_dodaj, text=kontynent[index], variable=kontynent_wartosc, value=index, width = 20, indicatoron=0)
        radiobutton_kontynent.grid(row=3, column=index + 1)

    for index in range(len(zywienie)):
        radiobutton_zywienie = Radiobutton(frame_dodaj, text=zywienie[index], variable=zywienie_wartosc, value=index, width = 20, indicatoron=0)
        radiobutton_zywienie.grid(row=4, column=index + 1)

    for index in range(len(zagrozenie)):
        radiobutton_zagrozenie = Radiobutton(frame_dodaj, text=zagrozenie[index], variable=zagrozenie_wartosc, value=index, width = 20, indicatoron=0)
        radiobutton_zagrozenie.grid(row=5, column=index + 1)

    przycisk_dodawania = Button(frame_dodaj, text="Dodaj", font=("Arial", 25, "bold"), command=dodawanie)
    przycisk_dodawania.grid(row=5, column=7)

    okno_dodaj.mainloop()
def usun():
    try:
        usun_ID = wpisywanie_ID.get()
        session.delete(session.query(Zwierze).get(usun_ID))
        session.commit()
        join_wyswietl()
    except:
        wiadomosc_usuwanie = "Wpisane ID jest niepoprawne."
        tytul_wiadomosc_usuwanie = "Error"
        okno_wiadomosc_usuwanie = Toplevel(nowe_okno)
        info_label(okno_wiadomosc_usuwanie, wiadomosc_usuwanie, tytul_wiadomosc_usuwanie)
        okno_wiadomosc_usuwanie.mainloop()
def updatowanie():
    if (len(entry_nazwa_update.get()) > 60 or len(entry_nazwa_lacinska_update.get()) > 60 or len(entry_nazwa_update.get()) == 0 or len(entry_nazwa_lacinska_update.get()) == 0):
        wiadomosc_update = "Nazwa i nazwa lacinska nie moga\nbyc dluzsze niz 60 znakow oraz nie moga\nbyc puste"
        tytul_wiadomosc_update = "Error"
        okno_wiadomosc_update = Toplevel(okno_update)
        info_label(okno_wiadomosc_update, wiadomosc_update, tytul_wiadomosc_update)
        okno_wiadomosc_update.mainloop()

        gatunek_wartosc.set(value=0)
        kontynent_wartosc.set(value=0)
        zywienie_wartosc.set(value=0)
        zagrozenie_wartosc.set(value=0)
    else:
        try:
            nowy_nazwa_update = entry_nazwa_update.get()
            nowy_nazwa_lacinska_update = entry_nazwa_lacinska_update.get()

            nowy_gatunek = gatunek_wartosc.get() + 1
            nowy_kontynent = kontynent_wartosc.get() + 1
            nowy_zywienie = zywienie_wartosc.get() + 1
            nowy_zagrozenie = zagrozenie_wartosc.get() + 1

            zwierze_nowy = session.query(Zwierze).filter(Zwierze.ID_zwierze == entry_ID_update.get()).one()
            zwierze_nowy.ID_zwierze = entry_ID_update.get()
            zwierze_nowy.nazwa_zwierze = nowy_nazwa_update
            zwierze_nowy.nazwa_lacinska_zwierze = nowy_nazwa_lacinska_update
            zwierze_nowy.gatunek_numer = nowy_gatunek
            zwierze_nowy.kontynent_numer = nowy_kontynent
            zwierze_nowy.zywienie_numer = nowy_zywienie
            zwierze_nowy.zagrozenie_numer = nowy_zagrozenie
            session.commit()

            gatunek_wartosc.set(value=0)
            kontynent_wartosc.set(value=0)
            zywienie_wartosc.set(value=0)
            zagrozenie_wartosc.set(value=0)

            join_wyswietl()

            okno_update.destroy()
        except:
            wiadomosc_update2 = "Wpisane ID jest niepoprawne."
            tytul_wiadomosc_update2 = "Error"
            okno_wiadomosc_update2 = Toplevel(okno_update)
            info_label(okno_wiadomosc_update2, wiadomosc_update2, tytul_wiadomosc_update2)
            okno_wiadomosc_update2.mainloop()

            gatunek_wartosc.set(value=0)
            kontynent_wartosc.set(value=0)
            zywienie_wartosc.set(value=0)
            zagrozenie_wartosc.set(value=0)
def update():
    global okno_update
    okno_update = Toplevel(nowe_okno)

    okno_update.title("Update")

    frame_update = Frame(okno_update)
    frame_update.pack()

    label_ID_update = Label(frame_update, text="ID: ", font=("Arial", 25))
    label_ID_update.grid(row=0, column=0)

    global entry_ID_update
    entry_ID_update = Entry(frame_update, font=("Arial", 25))
    entry_ID_update.grid(row=0, column=1, columnspan=2)

    label_nazwa_update = Label(frame_update,text="Nazwa: ",font=("Arial", 25))
    label_nazwa_update.grid(row=1, column=0)

    global entry_nazwa_update
    entry_nazwa_update = Entry(frame_update,font=("Arial", 25))
    entry_nazwa_update.grid(row=1, column=1, columnspan=2)

    label_nazwa_lacinska_update = Label(frame_update,text="Nazwa lacinska: ",font=("Arial", 25))
    label_nazwa_lacinska_update.grid(row=2, column=0)

    global entry_nazwa_lacinska_update
    entry_nazwa_lacinska_update = Entry(frame_update, font=("Arial", 25))
    entry_nazwa_lacinska_update.grid(row=2, column=1, columnspan=2)

    label_gatunek_update = Label(frame_update, text="Gatunek: ", font=("Arial", 25))
    label_gatunek_update.grid(row=3, column=0)

    label_kontynent_update = Label(frame_update, text="Kontynent: ", font=("Arial", 25))
    label_kontynent_update.grid(row=4, column=0)

    label_zywienie_update = Label(frame_update, text="Zywienie: ", font=("Arial", 25))
    label_zywienie_update.grid(row=5, column=0)

    label_zagrozenie_update = Label(frame_update, text="Zagrozenie: ", font=("Arial", 25))
    label_zagrozenie_update.grid(row=6, column=0)

    for index in range(len(gatunek)):
        radiobutton_gatunek_update = Radiobutton(frame_update, text=gatunek[index],variable=gatunek_wartosc, value=index, width = 20, indicatoron=0)
        radiobutton_gatunek_update.grid(row=3, column=index+1)

    for index in range(len(kontynent)):
        radiobutton_kontynent_update = Radiobutton(frame_update, text=kontynent[index], variable=kontynent_wartosc, value=index, width = 20, indicatoron=0)
        radiobutton_kontynent_update.grid(row=4, column=index + 1)

    for index in range(len(zywienie)):
        radiobutton_zywienie_update = Radiobutton(frame_update, text=zywienie[index], variable=zywienie_wartosc, value=index, width = 20, indicatoron=0)
        radiobutton_zywienie_update.grid(row=5, column=index + 1)

    for index in range(len(zagrozenie)):
        radiobutton_zagrozenie_update = Radiobutton(frame_update, text=zagrozenie[index], variable=zagrozenie_wartosc, value=index, width = 20, indicatoron=0)
        radiobutton_zagrozenie_update.grid(row=6, column=index + 1)

    przycisk_update = Button(frame_update, text="Update", font=("Arial", 25, "bold"), command=updatowanie)
    przycisk_update.grid(row=6, column=7)

    okno_update.mainloop()
def on_closing():
    okno.destroy()
def aplikacja():
    # CALA STREFA APLIKACJI
    global nowe_okno
    nowe_okno = Toplevel()

    okno.withdraw()
    nowe_okno.title("Atlas zwierzat")
    nowe_okno.geometry("1600x900")

    frame = Frame(nowe_okno)
    frame.place(x=10, y=10)

    #PRZYCISKI
    przycisk_dodaj = Button(frame,text="Dodaj",font=("Arial", 15, "bold"),command=dodaj)
    przycisk_dodaj.grid(row=0, column=0)

    przycisk_usun = Button(frame,text="Usun",font=("Arial", 15, "bold"),command=usun)
    przycisk_usun.grid(row=0, column=1)

    przycisk_update = Button(frame,text="Update",font=("Arial", 15, "bold"),command=update)
    przycisk_update.grid(row=0, column=2)

    #TWORZENIE MIEJSCA DO WYSWIETLANIA RZECZY
    frame2 = Frame(nowe_okno)
    scrollbar = Scrollbar(frame2, orient=VERTICAL)

    global obszar
    obszar = Listbox(frame2, width = 200, height= 15, yscrollcommand=scrollbar.set)

    scrollbar.config(command=obszar.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    frame2.place(x=10, y=55)

    obszar.pack()

    przycisk_wyswietl_wszystko = Button(frame,text="Wyswietl wszystko",font=("Arial", 15, "bold"),command=join_wyswietl)
    przycisk_wyswietl_wszystko.grid(row=0, column=3, columnspan=2)

    label_wpisywanie_ID = Label(frame,text="Wpisz ID:",font=("Arial", 15, "bold"))
    label_wpisywanie_ID.grid(row=0, column=5)

    global wpisywanie_ID
    wpisywanie_ID = Entry(frame,font=("Arial", 15),width=4)
    wpisywanie_ID.grid(row=0, column=6)

    nowe_okno.protocol("WM_DELETE_WINDOW", on_closing)
    nowe_okno.mainloop()
def rejestracja():
    username = login.get()
    password = haslo.get()

    #BLEDY REJESTRACJI
    wiadomosc_rejestracja = ""
    tytul_wiadomosc_rejestracja = ""
    istnieje = 0
    if(len(username) > 25 or len(password) > 25):
        wiadomosc_rejestracja = "Login lub haslo sa za dlugie. \n(max. 25 znakow)"
        tytul_wiadomosc_rejestracja = "Error"
        if(len(username) == 0 or len(password) == 0):
            wiadomosc_rejestracja += "\n Login i haslo nie moga byc puste."
    elif(len(username) == 0 or len(password) == 0):
        wiadomosc_rejestracja = "Login i haslo nie moga byc puste."
        tytul_wiadomosc_rejestracja = "Error"
    else:
        #UDANA REJESTRACJA
        wiadomosc_rejestracja = "Udalo sie pomyslnie zarejestrowac."
        tytul_wiadomosc_rejestracja = "Sukces"
        #SPRAWDZANIE CZY LOGIN JEST ZAJETY
        for uzytkownik in session.query(Uzytkownik):
            if(uzytkownik.login == username):
                istnieje = 1
                wiadomosc_rejestracja = "Login jest zajety."
                tytul_wiadomosc_rejestracja = "Error"
        #LOGIN NIE JEST ZAJETY
        if (istnieje == 0):
            session.add(Uzytkownik(login = username, haslo = password))
            session.commit()

    #WYSWIETLENIE WIADOMOSCI
    okno_wiadomosc_rejestracja = Toplevel()
    info_label(okno_wiadomosc_rejestracja, wiadomosc_rejestracja, tytul_wiadomosc_rejestracja)
    okno_wiadomosc_rejestracja.mainloop()
def zaloguj():
    username = login.get()
    password = haslo.get()

    #BLEDY LOGOWANIA
    wiadomosc_logowanie = ""
    tytul_wiadomosc_logowanie = ""
    udane_logowanie = 0
    if (len(username) > 25 or len(password) > 25):
        wiadomosc_logowanie = "Login lub haslo sa za dlugie. \n(max. 25 znakow)"
        tytul_wiadomosc_logowanie = "Error"
        if (len(username) == 0 or len(password) == 0):
            wiadomosc_logowanie += "\n Login i haslo nie moga byc puste."
    elif (len(username) == 0 or len(password) == 0):
        wiadomosc_logowanie = "Login i haslo nie moga byc puste."
        tytul_wiadomosc_logowanie = "Error"
    else:
        for uzytkownik in session.query(Uzytkownik):
            if(uzytkownik.login == username and uzytkownik.haslo == password):
                udane_logowanie = 1
            else:
                wiadomosc_logowanie = "Uzytkownik nie istnieje"
                tytul_wiadomosc_logowanie = "Error"

    #UDANE LOGOWANIE
    if(udane_logowanie == 1):
        aplikacja()
    else:
        #WYSWIETLENIE WIADOMOSCI
        okno_wiadomosc_logowanie = Toplevel()
        info_label(okno_wiadomosc_logowanie, wiadomosc_logowanie, tytul_wiadomosc_logowanie)
        okno_wiadomosc_logowanie.mainloop()


#PIERWSZE OKNO
okno = Tk()

global gatunek_wartosc
gatunek_wartosc = IntVar()
global kontynent_wartosc
kontynent_wartosc = IntVar()
global zywienie_wartosc
zywienie_wartosc = IntVar()
global zagrozenie_wartosc
zagrozenie_wartosc = IntVar()

okno.title("Logowanie")
okno.geometry("1024x576")

frame = Frame(okno)
frame.place(x = 340, y = 165)

#NAPIS LOGIN
label_login = Label(frame,text="Login:",font=("Arial", 25, "bold"))
label_login.grid(row = 0, column = 0)

#ENTRYBOX DLA LOGINU
login = Entry(frame,font=("Arial", 25))
login.grid(row = 1, column = 0)

#NAPIS HASLO
label_login = Label(frame,text="Haslo:",font=("Arial", 25, "bold"))
label_login.grid(row = 2, column = 0)

#ENTRYBOX DLA HASLA
haslo = Entry(frame,font=("Arial", 25),show="*")
haslo.grid(row = 3, column = 0)

#PRZYCISK LOGOWANIA
zaloguj_przycisk = Button(frame,text="Zaloguj",command=zaloguj)
zaloguj_przycisk.grid(row = 4, column = 0)

#PRZYCISK REJESTRACJI
rejestracja_przycisk = Button(frame,text="Zaloz konto",command=rejestracja)
rejestracja_przycisk.grid(row = 5, column = 0)

okno.mainloop()





