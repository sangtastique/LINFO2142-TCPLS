# Entretient 1:

Explorer les différentes foncitonnalittés
- Stream multiple
- plusieurs connection
- migrer d'un connection à une autre
- utiliser plusieurs co en meme temps

Implem open source

Prendre l'implem et la tester sur différent scénarios sur Mininet (qui permet de faire différentes topologie de réseau).
Exécuter des programmes entre des clients et de serveurs sur cette topologie.

Possible qu'on doive étendre le client/server avec l'API fournit.


Le plus simple est d'avoir une topologie mininet qui focntionne et dans laquelle on peut lancer un test iperf3.

1) Faire une topo simple (mais suffisante pour faire des tests). Vérfier les délais avec ping. Vérifier la bande passante avec iperf3 (juste pour vérifer qu'ils arrivent à communiquer ensemble). 

On utilise aps iperf3 pour faire les tests avec TCPLS car ca marchera pas (pas supporté).

A faire:
- Une idée de ce qu'on veut évaluer
- Avoir les outils qui marchent:
	- Mininet avec la topo qui marche

Comme ca 

(basic): mpiraux/rapido (code de rapido.c) (public)
(wrk/client): (en cours/ privé)

wrk permet de lancer plein de requete HTTP et de mesurer la latence.
http H2O server: pour gérer ca. 

Pour l'instant on reste sans WRK et H2O (pas assez maturé).

Baseline : 

MPTCP: saturation de plusieurs chemin. (dispo sur les plateformes).


Mesurer la réaction des pannes, des fichiers volumineux (sur plusieurs connections), ...


# Entretient 2:

Entretient 2: 

Il faut que le server ai une deuxième deuxieme adresse (celle d'une autre interface par exemple). Avec un autre argument en ligne de commande

Print de l'estimation de la bande passante (ligne 330).

Python HTTPS server. curl pour télécharger un fichier (100 mb) (avec un flag pour imprimer un le débit).

Diff de plus de 10%: il  y a quelque chose à creuser, sinon non. 

Plus faire varier les bandes passantes : 30/70, 40/60, 50/50, 60/40, 70/30,... avec le meme total.  (netox), tcpdump, ...

1) Varier la bande passante (2 liens)
2) Failure avec 2 liens
3) TEst avec plus de liens
4) Comparaison avec MPTCP