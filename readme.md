# Module de pilotage d’engin

## Rôle

Ce projet est destiné à accueillir l’application métier de pilotage d’un engin
Wild Thumper 6WD. Il est conçu pour utiliser le runtime fourni par MasterLib.

Le dépôt source s’appelle actuellement `Wildthumper_6wd`. Lors de son
intégration dans MasterLib, le module sera rangé sous :

`src/mastermodule/module/module_pilotage_engin/`

## État actuel

Le projet est un prototype d’intégration ; le pilotage de l’engin n’est pas
encore développé.

À ce stade :

- `main.py` démarre le runtime avec `WildthumperCore` ;
- `WildthumperCore` écrit un message lorsque le runtime est prêt ;
- `WildthumperCore` demande l’arrêt du noyau lorsque l’événement `Ctrl+Q` est
  reçu ;
- aucun contrôle moteur, capteur ou communication avec l’engin n’est encore
  implémenté.

## Démarrage

Le point d’entrée Python est `main.py`. Il nécessite que MasterLib soit
disponible dans l’environnement Python :

```bash
python main.py