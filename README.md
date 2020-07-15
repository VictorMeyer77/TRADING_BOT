# TRADING BOT
### 4IABD Alexandre Matthieu, Fauvert Baptiste, Meyer Victor

Pour lancer le Bot, référez vous à la documentation.

#### important
NewsPredicter et Api ne sont pas maintenues sur la branche master, certains problèmes
peuvent survenir.
Si vous disposez d'un Raspberry, utilisez la branche rpi.

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
    
#### liens

ihm:  http://ihm.tradingbot.business/
api:  tradingbot4iabd.hopto.org/