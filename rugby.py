import csv
import re
import unicodedata

def nettoyer_chaine(chaine):
    try:
        chaine_correcte = chaine.encode('latin-1').decode('utf-8')
        chaine_propre = re.sub(r'[^\x00-\x7F]+', '', chaine_correcte)
        chaine_normalisée = unicodedata.normalize('NFKD', chaine_propre).encode('ASCII', 'ignore').decode('utf-8')
        return chaine_normalisée
    except UnicodeEncodeError:
        return chaine

with open('rugby dataset.csv', 'r', encoding='latin-1') as fichier_entree:
    lecteur_csv = csv.reader(fichier_entree)
    entetes = next(lecteur_csv)
    lignes_propres = []

    for ligne in lecteur_csv:
        ligne_propre = [nettoyer_chaine(champ) for champ in ligne]
        lignes_propres.append(ligne_propre)

with open('rugbydataset_propres.csv', 'w', encoding='utf-8', newline='') as fichier_sortie:
    ecrivain_csv = csv.writer(fichier_sortie)
    ecrivain_csv.writerow(entetes)
    ecrivain_csv.writerows(lignes_propres)

print("Nettoyage terminé. Les données propres ont été enregistrées dans 'donnees_propres.csv'.")
