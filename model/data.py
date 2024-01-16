import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import json
import tkinter as tk
from tkinter import Entry, Button, StringVar, ttk, Listbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#
#Class qui sert à manipuler et afficher les données
class Data:

    #
    #Initialisation des objets
    def __init__(self, chemin_fic):
        self.activites_df = None
        self.categories_df = None
        self.transitions_df = None
        self.types_utilisateur_df = None
        self.user_files_df = None
        self.messageParEleve = None
        self.chemin_file = chemin_fic
        self.cluster_df = None

        self.charger_json_pandas()

    #########################################################
    #
    #Récupération des données, et transformation en dataframe
    def charger_json_pandas(self):
        with open(self.chemin_file, 'r', encoding='utf-8') as fichier:
            data = json.load(fichier)

        self.activites_df = pd.json_normalize(data[2]['data']).map(str)
        self.categories_df = pd.json_normalize(data[3]['data']).map(str)
        self.transitions_df = pd.json_normalize(data[4]['data']).map(str)
        self.types_utilisateur_df = pd.json_normalize(data[8]['data']).map(str)
        self.user_files_df = pd.json_normalize(data[10]['data']).map(str)

        return self.activites_df, self.categories_df, self.transitions_df, self.types_utilisateur_df, self.user_files_df



    ############################################################################################
    #
    # Permet de récupérer les messages des élèves pour chaque date, et les met dans un dataframe
    def getNbMessagesParElevesPourUneDate(self):
        print("### Get NbMessages Start ###")

        cond1 = self.activites_df['IDAct'] == "9"
        reponse = self.activites_df[cond1]  # reponse à un message

        cond2 = self.activites_df['IDAct'] == "10"
        nouveau = self.activites_df[cond2]  # poster un nouveau message

        # Les deux conditions pour le DataFrame transitions_df
        cond3 = self.transitions_df['Titre'].isin(reponse['Titre'])
        cond4 = self.transitions_df['Titre'].isin(nouveau['Titre'])

        resultat = self.transitions_df[cond3 | cond4]

        self.transitions_df['Date'] = pd.to_datetime(resultat['Date'], errors='coerce')

        df_messages_par_utilisateur = pd.pivot_table(
            self.transitions_df,
            values='IDTran', 
            index='Utilisateur',
            columns='Date',
            aggfunc='count',
            fill_value=0  # Remplacez les valeurs NaN par 0
        )

        self.messageParEleve = df_messages_par_utilisateur
        print("### Get NbMessages End ###")

        return df_messages_par_utilisateur
    

    ##########################################
    #
    # Afficher les message dans un graphique
    def afficher_message(self, debut=None, fin=None):

        print(self.transitions_df)

        if self.messageParEleve == None:
            self.getNbMessagesParElevesPourUneDate()

        df_messages_par_utilisateur_transpose = self.messageParEleve.T

        _, ax = plt.subplots(figsize=(10, 8))

        for i, eleve in enumerate(df_messages_par_utilisateur_transpose.columns):
            couleur = plt.cm.rainbow(i / len(df_messages_par_utilisateur_transpose.columns))
            ax.plot(df_messages_par_utilisateur_transpose.index, df_messages_par_utilisateur_transpose[eleve], label=eleve, color=couleur)

        if debut != None and fin != None:
            date_debut = pd.to_datetime(debut)
            date_fin = pd.to_datetime(fin)

            ax.set_xlim(date_debut, date_fin)

        ax.set_xlabel('Dates')
        ax.set_ylabel('Nombre de messages')
        ax.set_title('Nombre de messages par élève par date')
        ax.legend()

        plt.show()


    ######################################################################
    #
    #permet de préparer les données pour pouvoir faire de la classification
    def preparerData(self):

        df = self.transitions_df

        # Extraire les IDForum de la colonne Attribut
        df['IDForum'] = df['Attribut'].str.extract(r'IDForum=(\d+)')

        pivot_df = pd.pivot_table(df, values='IDTran', index='Utilisateur', columns='IDForum', aggfunc='count', fill_value=0)

        # Normaliser en divisant par la somme des valeurs pour chaque utilisateur
        normalized_df = pivot_df.div(pivot_df.sum(axis=1), axis=0)
        scaler = StandardScaler()
        normalized_data_scaled = scaler.fit_transform(normalized_df)

        num_clusters = 4
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        normalized_df['Cluster'] = kmeans.fit_predict(normalized_data_scaled)

        self.cluster_df = normalized_df

    #####################################
    #
    # Permet d'afficher un diagramme camembert sur le taux de participation des utilisteur dans les forum sur l'inteface générée
    def creer_diagramme_camembert(self, utilisateur, root):
        plt.clf()

        plt.figure(figsize=(6, 6))
        
        taux_participation = self.cluster_df.loc[utilisateur, :]
        taux_participation = taux_participation.drop('Cluster', errors='ignore')
        taux_participation_non_zero = taux_participation[taux_participation > 0]


        plt.pie(taux_participation_non_zero, labels=taux_participation_non_zero.index, autopct='%1.1f%%', startangle=90)
        plt.title(f"Taux de participation de {utilisateur} aux forums")


        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()


        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        root.update()


    #####################################
    #
    # Permet d'afficher les message utilisateur dans un graphique sur l'inteface générée
    def afficher_messages_utilisateur(self, utilisateur, root):
        if self.messageParEleve is None:
            self.getNbMessagesParElevesPourUneDate()

        df_messages_par_utilisateur_transpose = self.messageParEleve.T

        if utilisateur not in df_messages_par_utilisateur_transpose.columns:
            print(f"L'utilisateur {utilisateur} n'est pas présent dans les données.")
            return

        plt.clf()


        _, ax = plt.subplots(figsize=(10, 8))
        ax.plot(df_messages_par_utilisateur_transpose.index, df_messages_par_utilisateur_transpose[utilisateur], label=utilisateur, color='blue')


        ax.set_xlabel('Dates')
        ax.set_ylabel('Nombre de messages')
        ax.set_title(f'Nombre de messages pour {utilisateur} par date')
        ax.legend()


        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()


        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()


        root.update()


    ######################################
    #
    # Génère et affiche l'interface graphique
    def creer_interface_utilisateur(self):
        root = tk.Tk()
        root.title("Choisir un utilisateur")


        utilisateurs = self.cluster_df.index.tolist()

        labels = self.cluster_df['Cluster'].unique().tolist()


        choix_utilisateur = StringVar()
        choix_utilisateur.set(utilisateurs[0])

        liste_deroulante_utilisateur = ttk.Combobox(root, textvariable=choix_utilisateur, values=utilisateurs)
        liste_deroulante_utilisateur.pack(pady=10)

        bouton_afficher_messages = Button(root, text="Afficher quantité de messages par date", command=lambda: self.afficher_messages_utilisateur(choix_utilisateur.get(), root))
        bouton_afficher_messages.pack(pady=10)

        bouton_camembert_messages = Button(root, text="Participation aux Forums", command=lambda: self.creer_diagramme_camembert(choix_utilisateur.get(), root))
        bouton_camembert_messages.pack(pady=10)


        frame_groupes = tk.Frame(root)
        frame_groupes.pack(pady=10)

        for label in labels:

            label_groupe = tk.Label(frame_groupes, text=f"Groupe {label} :")
            label_groupe.grid(row=0, column=labels.index(label), padx=10)


            utilisateurs_groupe = self.cluster_df[self.cluster_df['Cluster'] == label].index.tolist()


            listbox_utilisateurs = Listbox(frame_groupes, selectmode=tk.SINGLE, height=len(utilisateurs_groupe))
            listbox_utilisateurs.grid(row=1, column=labels.index(label), padx=10)


            for utilisateur in utilisateurs_groupe:
                listbox_utilisateurs.insert(tk.END, utilisateur)


        root.mainloop()
        

chemin_json = "../eiah.json"
data = Data(chemin_fic=chemin_json)

data.preparerData()
data.creer_interface_utilisateur()








