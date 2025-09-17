# free-rdv-sniper
🤖 **Bot de Surveillance de RDV Free** qui vérifie et vous notifie sur Telegram d'un nouveau créneau
![🤖⚡📩 ](https://gifdb.com/images/high/panda-breaking-the-computer-eaqqqzduc702vgi0.gif)
Ce script Python un peu dégeu a pour objectif de surveiller la page de gestion des rendez-vous technicien de l'opérateur Free. Il cherche automatiquement un créneau disponible avant une date limite que vous avez fixée, et vous notifie en temps réel via Telegram dès qu'une opportunité se présente.

**Pourquoi ce script ?** ~~Parce qu'un sous traitant de Free à débranché ma fibre~~ Parce qu'il est difficile d'obtenir un rendez-vous avec un technicien Free avant sortie de la fusion nucléaire en version stable.

-----

### 🎯 **Fonctionnalités Principales**

  * **Connexion Automatique** : Le script se connecte de manière autonome à votre espace abonné Free.
  * **Navigation Intelligente** : Il navigue jusqu'à la section "Mon Assistance" pour accéder à la gestion de votre rendez-vous.
  * **Surveillance Continue** : Le bot rafraîchit la page à intervalle régulier mais safe pour faire apparaître les nouveaux créneaux.
  * **Notification Instantanée** : Si un créneau est trouvé avant votre date butoir, une notification est immédiatement envoyée sur Telegram.
  * **Gestion d'Erreurs Robuste** : Le script gère les déconnexions et les erreurs en tentant de se relancer automatiquement, Il vous notifiera quand même si ça crash ou quand vous serez inévitablement déconnectés au bout de 30minutes.
  * Vous pouvez le mettre en Headless mais j'aime bien voir ce qu'il fait !

-----

⚠️ Avertissement Légal ⚠️

L'automatisation des interactions sur un site web, comme ce script le fait, peut potentiellement enfreindre les conditions générales d'utilisation du service en question. De plus, les sites web évoluent constamment. Si Free met à jour sa page de prise de rendez-vous, le script pourrait cesser de fonctionner et nécessiter des ajustements.


### 🚀 **Guide d'Installation et de Lancement**

1.  **Clonez le dépôt** :

    ```bash
    git clone [URL_DE_VOTRE_DEPOT]
    cd [NOM_DU_DOSSIER]
    ```

2.  **Installez les dépendances** :

    ```bash
    pip install -r requirements.txt
    ```

3.  **Téléchargez ChromeDriver** : Assurez-vous d'avoir Google Chrome installé. Téléchargez la version de ChromeDriver qui correspond à votre version de Chrome et placez-la dans le `PATH` de votre système ou dans le même dossier que le script.

4.  **Créez le fichier de configuration** :
    Un fichier d'exemple `env.example` est fourni. **Copiez-le** pour créer votre propre fichier de configuration `.env` :

    ```bash
    cp env.example .env
    ```

    Ensuite, **modifiez le fichier `.env`** avec vos informations personnelles. Ce fichier ne doit **jamais** être partagé.

    ```ini
    # Vos identifiants pour l'espace abonné Free
    FREE_USER="VOTRE_IDENTIFIANT_FREE"
    FREE_PASS="VOTRE_MOT_DE_PASSE_FREE"

    # Le jour du mois à ne pas dépasser (ex: 24 pour le 24 du mois)
    DATE_LIMITE=24

    # --- Configuration Telegram ---
    # Obtenu via le BotFather sur Telegram
    TOKEN="VOTRE_TOKEN_TELEGRAM"
    # L'ID de la conversation où envoyer la notification
    CHAT_ID="VOTRE_CHAT_ID_TELEGRAM"
    ```

5.  **Exécutez le script** :

    ```bash
    python check_rdv.py
    ```

-----

\<br\>
