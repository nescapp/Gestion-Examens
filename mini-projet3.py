import os
import time

"""
utilisation des libairies:
    - os : gestion des fichiers et dossiers
    - time : gestion du temps (timer, compte à rebours)
    - threading : gestion des threads (timer, compte à rebours)
"""


class App:
    """Classe principale de l'application"""

    def __init__(self):
        """Constructeur de la classe"""
        self.username = ""
        self.password = ""
        self.nom_dossier = ""  # Nom du dossier du QCM

    def quit(self):
        """Fontion pour quitter l'application"""
        print("\033c")  # Effacer le terminal
        print("\033[93mAu revoir!\033[0m")
        exit()

    def compte_a_rebours(self, duration):
        """Fonction pour lancer un compte à rebours"""
        print(f"Vous avez {duration} secondes pour répondre aux questions")

        for i in range(3, 0, -1):
            print(i) # Afficher le compte à rebours
            time.sleep(1) 

    def action_form(self, actions):
        """Fonction pour afficher un formulaire d'actions et executer la fonction correspondante"""
        while True: # Boucle pour afficher le formulaire
            for key in actions:
                print(f"'{key}' - {actions[key][0]}") # Afficher les actions
            choice = input(
                f"Entrez votre choix \033[2m({', '.join(actions.keys())})\033[0m : " # Demander le choix
            ).lower()
            if choice in actions:
                actions[choice][1]()
                return choice # Retourner le choix
            else:
                print("\033[91mVeuillez entrer un choix valide!\033[0m") # Afficher un message d'erreur si le choix n'est pas valide

    def menu_principal(self):
        """Fonction pour afficher le menu principal"""
        print("\033[4m  GESTION DE QCM  \033[0m")

        self.action_form(
            {
                "e": ("Mode Eleve", lambda: self.verifier_compte("ELEVE")),
                "p": ("Mode Professeur", lambda: self.verifier_compte("PROF")),
                "q": ("quitter", lambda: self.quit()),
            }
        )

    def verifier_compte(self, user):
        """Fonction pour vérifier si l'utilisateur a un compte ou non"""
        answer = input("Avez-vous un compte? \033[2m(o/n)\033[0m : ")
        while True: # Boucle pour vérifier la réponse
            if answer == "o":
                if user == "PROF" and self.connecter_compte() == "PROF":
                    self.mode_prof() # Lancer le mode professeur
                elif user == "ELEVE" and self.connecter_compte() == "ELEVE":
                    self.mode_eleve() # Lancer le mode élève
                else:
                    print("\033[91mVous n'aviez pas de compte\033[0m")
                    time.sleep(1)
                    print("\033c", end="")
                    self.menu_principal()
                break
            elif answer == "n":
                self.cree_compte(user, user)
                break
            else:
                answer = input("Please enter a valid answer \033[2m(o/n)\033[0m : ") # Demander une réponse valide

    def cree_compte(self, qui_enregistre, qui_creer):
        """Fonction pour créer un compte"""
        while True: # Boucle pour demander le nom d'utilisateur et le mot de passe
            username = input("Nom d'utilisateur: ").lower()
            password = input("Mot de passe: ").lower()
            confirmPassword = input("Confirmer le mot de passe: ").lower()
            if len(username) < 2 or len(password) < 2 or password != confirmPassword: # Vérifier si le nom d'utilisateur et le mot de passe sont valides
                print(
                    "Le nom d'utilisateur et le mot de passe doivent contenir au moins 2 caractères et les mots de passe doivent correspondre"
                )
            else:
                self.username = username # Initialiser le nom d'utilisateur et le mot de passe
                self.password = password
                break
        try:
            with open(file="Accounts\\eleves.txt", mode="r", encoding="utf-8") as file: # Ouvrir le fichier des comptes
                accounts = file.readlines()
                for account in accounts: # Boucle pour vérifier si le nom d'utilisateur existe déjà
                    account = account.strip().split("|") # Séparer le nom d'utilisateur et le mot de passe
                    existingUsername = account[1].split(":")[0] # Récupérer le nom d'utilisateur
                    if existingUsername == self.username: # Vérifier si le nom d'utilisateur existe déjà
                        print("\033[91m• Nom d'utilisateur déjà utilisé\033[0m")
                        self.menu_principal()

            with open(file="Accounts\\eleves.txt", mode="a", encoding="utf-8") as file: # Ajouter le compte au fichier des comptes
                file.write(f"{qui_enregistre}|{username}:{password}\n")

            print("\033[92m• Compte créé avec succès\033[0m")
            time.sleep(1.5)
            print("\033c", end="") # Effacer l'écran

            if qui_creer == "PROF": # Vérifier qui a créé le compte
                self.mode_prof()
            else:
                self.menu_principal()
        except FileNotFoundError: # Afficher un message d'erreur si le fichier des comptes n'existe pas
            print("\033[91mPas de fichier de comptes trouvé\033[0m")

    def connecter_compte(self):
        """Fonction pour se connecter à un compte"""
        username = input("Nom d'utilisateur: ").lower()
        password = input("Mot de passe: ").lower()
        self.username = username
        self.password = password

        try: # Ouvrir le fichier des comptes
            with open(file="Accounts\\eleves.txt", mode="r", encoding="utf-8") as file:
                accounts = file.readlines()
        except FileNotFoundError:
            print("\033[91mPas de fichier de comptes trouvé\033[0m")

        for account in accounts: # Boucle pour vérifier si le nom d'utilisateur et le mot de passe sont valides
            account = account.strip().split("|")
            role = account[0]
            account = account[1].split(":")
            if self.username == account[0] and self.password == account[1]:
                return role

    def mode_prof(self):
        """Fonction pour afficher le menu du mode professeur"""
        print("\033c", end="")
        print("\033[4m  MENU PROFESSEUR  \033[0m") # Afficher le menu du mode professeur

        self.action_form(
            {
                "1": ("Créer un QCM", lambda: self.cree_qcm()),
                "2": (
                    "Créer un compte pour un élève",
                    lambda: self.creer_compte_eleve(),
                ),
                "3": (
                    "Consulter les résultats d'un élève",
                    lambda: self.montrer_resultats_eleves(),
                ),
                "4": ("Main Menu", lambda: (print("\033c", end=""), self.menu_principal())),
                "q": ("quitter", lambda: self.quit()),
            }
        )

    def cree_qcm(self):
        """Fontion pour créer un QCM"""
        # Nettoyer l'écran
        print("\033c", end="")
        # Demander le nom du QCM, le nombre de questions, le nombre de réponses par question et la durée du QCM
        qcm_questions = []
        qcm_name = input("Veuillez entrer le nom du QCM : ")
        qcm_question_number = input("Veuillez entrer le nombre de questions du QCM : ")
        qcm_nombre_rep = input(
            "Veuillez entrer le nombre de réponses par question : "
        )
        duree_qcm = input("Veuillez entrer la durée du QCM (en seconds) : ")

        for i in range(int(qcm_question_number)): # Boucle pour demander la question et les réponses
            question = input(f"Veuillez entrer la question {i+1} : ")
            qcm_questions.append(f"q: {question}")
            for j in range(int(qcm_question_number)):
                answer = input(f"Veuillez entrer la réponse {j+1} : ")
                qcm_questions.append(f"{j + 1}) {answer}")
                # si c'est la dernière réponse, demander la bonne réponse
                if j == int(qcm_nombre_rep) - 1:
                    quizCorrectAnswer = input(
                        "Veuillez entrer le numéro de la bonne réponse : "
                    )
                    qcm_questions.append(f"Correct: {quizCorrectAnswer}\n")
        qcm_questions.append(f"Quiz duration: {duree_qcm}") # Ajouter la durée du QCM à la liste des questions

        try:
            # créer un fichier pour le QCM s'il n'existe pas
            if not os.path.exists(f"QCM\\{qcm_name}.txt"):
                open(f"QCM\\{qcm_name}.txt", "w").close()
            # ouvrir le fichier du QCM et écrire les questions
            with open(file=f"QCM\\{qcm_name}.txt", mode="a", encoding="utf-8") as file:
                for i in range(len(qcm_questions)):
                    file.write(f"{qcm_questions[i]}\n")
    
            print("QCM créé avec succes!")
            time.sleep(1)
            print("\033c", end="")
            self.mode_prof()
        except FileNotFoundError: # Afficher un message d'erreur si le fichier des QCM n'existe pas
            print("\033[91mPas de fichier de QCM trouvé\033[0m")

    def creer_compte_eleve(self):
        """Fonction pour créer un compte pour un élève"""
        print("\033c", end="")
        self.cree_compte("ELEVE", "PROF") # Appeler la fonction cree_compte() pour créer un compte pour un élève

    def montrer_resultats_eleves(self):
        """Fonction pour consulter les résultats d'un élève"""
        print("\033c", end="")

        dossier_etudiant = {}
        count = 1

        if len([folder for folder in os.listdir() if folder.endswith("_QCM")]) == 0:
            print("\033[91mPas de QCM trouvé\033[0m")
            time.sleep(1.5)
            print("\033c", end="")
            self.mode_prof()
        for folder in os.listdir():
            if folder.endswith("_QCM"):
                print(f"{count}) {folder}")
                dossier_etudiant[str(len(dossier_etudiant) + 1)] = folder
                count += 1

        while True:
            try:
                nom_dossier_etudiant = int(
                    input(
                        f"Veuillez entrer un numéro valide ({', '.join(dossier_etudiant.keys())}) : "
                    )
                )
                nom_dossier_etudiant = str(nom_dossier_etudiant)
                if nom_dossier_etudiant in dossier_etudiant.keys():
                    print("Vous avez sélectioné ", dossier_etudiant[nom_dossier_etudiant])
                    selectedStudentFolder = dossier_etudiant[nom_dossier_etudiant]
                    break
                else:
                    print("Choix invalide")
            except ValueError:
                print("Choix invalide")

        studentFiles = {}
        count2 = 1
        for file in os.listdir(selectedStudentFolder):
            print(f"{count2}) {file}")
            studentFiles[str(count2)] = file
            count2 += 1

        while True:
            try:
                studentFileNumber = int(
                    input(
                        f"Veuillez entrer un numéro valide ({', '.join(studentFiles.keys())}) : "
                    )
                )
                studentFileNumber = str(studentFileNumber)
                if studentFileNumber in studentFiles.keys():
                    print("Vous avez sélectioné ", studentFiles[studentFileNumber])
                    selectedStudentFile = studentFiles[studentFileNumber]
                    break
                else:
                    print("Choix invalide")
            except ValueError:
                print("Choix invalide")

        print("\033c", end="")

        with open(
            f"{selectedStudentFolder}\\{selectedStudentFile}", "r", encoding="utf-8"
        ) as file:
            print(file.read())
        # Demander à l'utilisateur s'il veut continuer ou retourner au menu principal
        self.action_form(
            {
                "1": ("Continuer?", lambda: self.montrer_resultats_eleves()),
                "2": ("Menu principal", lambda: (print("\033c", end=""), self.menu_principal())),
            }
        )

    def mode_eleve(self):
        """Fonction pour le mode élève"""
        print("\033c", end="")
        print("\033[4m  MENU ELEVE  \033[0m")
        self.action_form(
            {
                "1": ("Passer un QCM", lambda: self.faire_qcm()),
                "2": ("Menu Principal", lambda: (print("\033c", end=""), self.menu_principal())),
                "q": ("Quitter", lambda: self.quit()),
            }
        )

    def faire_qcm(self):
        """Fonction pour passer un QCM"""
        print("\033c", end="")
        # définir les variables
        questions = []
        reponses = []
        reponses_correctes = []
        fichiers_qcm = {}
        duree_qcm = 0
        note = 0

        self.nom_dossier = f"{self.username}_QCM"
        if not os.path.exists(self.nom_dossier):
            os.mkdir(self.nom_dossier)

        print("Liste des QCM disponibles : ")

        count = 1
        for i, file in enumerate(os.listdir("QCM")):
            if f"{self.username}_{file}" not in os.listdir(self.nom_dossier):
                print(f"{count}) {file}")
                fichiers_qcm[str(count)] = file.split(".")[0]
                count += 1

        while True: # Demander à l'utilisateur de choisir un QCM
            try:
                num_qcm = int(
                    input(
                        f"Veuillez entrer un numéro valide ({', '.join(fichiers_qcm.keys())}) : "
                    )
                )
                num_qcm = str(num_qcm)
                if num_qcm in fichiers_qcm.keys():
                    print("You selected", fichiers_qcm[num_qcm])
                    selectedQCM = fichiers_qcm[num_qcm]
                    break
                else:
                    print("Invalid choice")
            except ValueError: # Si l'utilisateur entre une valeur qui n'est pas un nombre
                print("Invalid choice")

        time.sleep(1)
        print("\033c", end="")

        with open(f"QCM\{selectedQCM}.txt", "r", encoding="utf-8") as file: # Ouvrir le fichier QCM
            lines = file.readlines()

        i = 0
        while i < len(lines): # Parcourir le fichier ligne par ligne
            if lines[i].startswith("q:"):
                question = lines[i].replace("q:", "").strip()
                questions.append(question)
                i += 1
                answer_choices = []

                while not lines[i].startswith("Correct:"):
                    answer = lines[i].strip()
                    answer_choices.append(answer)
                    i += 1
                reponses.append(answer_choices)
                correct_answer = lines[i].replace("Correct:", "").strip()
                reponses_correctes.append(int(correct_answer))

            if lines[i].startswith("Quiz duration:"):
                duree_qcm = int(lines[i].replace("Quiz duration:", "").strip())
            i += 1

        self.compte_a_rebours(duree_qcm)

        # start timer
        start = time.time()


        for question in range(len(questions)):
            print(f"Question : {questions[question]}")
            print("\n".join(reponses[question]))
            while True:
                try:
                    userInput = int(input("Entrez votre réponse : "))
                    break
                except ValueError:
                    print("Choix Invalide")

            if userInput == reponses_correctes[question]:
                print("Correcte!\n")
                note += 1
            else:
                print("Incorrecte!\n")

            if not os.path.exists(
                f"{self.nom_dossier}\\{self.username}_{selectedQCM}.txt"
            ):
                open(
                    f"{self.nom_dossier}\\{self.username}_{selectedQCM}.txt", "w"
                ).close()

            with open(
                f"{self.nom_dossier}\\{self.username}_{selectedQCM}.txt",
                "a",
                encoding="utf-8",
            ) as file: # Enregistrer les réponses de l'élève dans un fichier
                file.write(f"Question: {questions[question]}\n")
                file.write("Réponses:\n")
                file.write("\n".join(reponses[question]) + "\n")
                file.write(f"Réponse correcte : {reponses_correctes[question]}\n")
                file.write(f"Réponse de l'élève : {userInput}\n")
                file.write("\n")
            
        # stop timer
        end = time.time()
        
        # Enregistrer la note de l'élève dans un fichier
        with open(
            f"{self.nom_dossier}\\{self.username}_{selectedQCM}.txt",
            "a",
            encoding="utf-8",
        ) as file:
            file.write(f"Temps pris pour completer le qcm: {round(end - start)} secondes\n")
            file.write(f"Note: {note}/{len(questions)}\n")
            file.write("--------------------------------------------------\n")

        time.sleep(1)
        print("\033c", end="")

        print("QCM Terminé!\033[0m") # Afficher la note de l'élève
        print(f"Vous avez pris {round(end - start)} secondes pour completer le QCM")
        if note == len(questions):
            print(f"Très Bien! ({note}/{len(questions)})")
        elif note >= len(questions) / 2:
            print(f"Bien! {note}/{len(questions)}")
        else:
            print(f"Insuffisant : {note}/{len(questions)}\033[0m")
        time.sleep(2)
        self.mode_eleve()


def main():
    """Function principale"""
    # Créer les dossiers nécessaires
    if not os.path.exists("Accounts"):
        os.mkdir("Accounts")
    if not os.path.exists("QCM"):
        os.mkdir("QCM")
    if not os.path.exists("Accounts\eleves.txt"):
        open("Accounts\eleves.txt", "w").close()

    print("\033c", end="")  # Nettoie la console
    user = App()  # Crée une instance de la classe App
    user.menu_principal()  # Lance le menu principal


if __name__ == "__main__":
    # Execute seulement si lancé depuis le fichier principal
    main()
