#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#Wir laden zuerst alle Bausteine im HTML-Format von folgender Seite herunter und entpacken die Datei:
#https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/Kompendium/html_kompendium2020.zip?__blob=publicationFile&v=2
#für die weitere Arbeit benötigen wir folgende Module

from bs4 import BeautifulSoup
import glob
import pandas

#dann definieren wir die Listen, aus denen nachher die Spalten generiert werden sollen

baustein=[]
baustein_nr=[]
siegelstufe=[]
anforderungen=[]

#dann gehen wir den heruntergeladenen Ordner durch und parsen jede vorhandene HTML-Datei

for filename in glob.glob("/home/eisler/Dokumente/html_kompendium2020/bausteine_und_umsetzungshinweise/*"):   #in dem Ordner befinden sich die HTML-Dateien
    file=open(filename,errors='ignore',encoding='utf-8')                #ohne das encoding werden Umlaute fehlerhaft angezeigt
    soup = BeautifulSoup(file, 'html.parser')                           #pro File bauen wir uns ein soup-objekt
#Beautifulsoup arbeitet mit Tags, die in einer Liste gespeichert werden. Wir gehen jedes Tag durch und hangeln uns in der Hierarchie der HTML-Datei zu dem Punkt, den wir haben wollen. Den Inhalt fügen wir dann an die eingangs erstellten Listen an


    li=soup.find_all('li')
    for child in li:
        if child.h4:
            inhalt=child.h4.text.split()
            baustein_nr.append(child.h4.text[:-3])
            anforderungen.append(child.p.text)
            siegelstufe.append(inhalt[-1][1:-1])
            baustein.append(soup.title.string.strip())
#Nun bauen wir uns das Dataframe und weisen die Listen den einzelnen Spalten zu
GSC=pandas.DataFrame(columns=["Baustein","Nummer","Siegelstufe","Anforderungen"])
GSC["Baustein"]=baustein
GSC["Nummer"]=baustein_nr
GSC["Siegelstufe"]=siegelstufe
GSC["Anforderungen"]=anforderungen


#Wir schauen, ob überhaupt Inhalte im Dataframe gelandet sind

print (len(GSC))

#1735

#und am Schluss speichern wir die Tabelle noch im Excel-Format ab. Den Index benötigen wir dabei nicht

GSC.to_csv("/home/eisler/Dokumente/GSC_Kompendium_gesamt.csv",index=False)
