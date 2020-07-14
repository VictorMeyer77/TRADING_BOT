# TRADING BOT
### 4IABD Alexandre Matthieu, Fauvert Baptiste, Meyer Victor

Pour lancer le Bot, référez vous à la documentation.
Les instructions suivantes décrivent les manipultaion pour lancer
l'oracle en local

    1) installer docker et docker-compose
    2) ouvrir un compte chez https://newsapi.org/
    3) dans NewsPredicter/conf/configuration.json:
       remplacer "newsKeyApi" par votre clef d'api
    4) Rechercher et remplacer tous les "debian" par votre machine:
        - NewsPredicter/conf/configuration.json
        - Api/conf/configuration.json
        - Api/conf/server.conf
    5) sudo docker-compose up