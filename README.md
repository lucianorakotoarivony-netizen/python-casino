# 🎰 Python Casino - Projet d'Apprentissage POO

> **⚠️ Statut : PROJET ARCHIVÉ - JALON D'APPRENTISSAGE** > *Ce projet représente ma progression après 3 semaines de Python. Il est laissé en l'état pour témoigner de mon niveau à cet instant précis.*

## 📝 À propos du projet
Ce projet est une simulation de casino en ligne de commande. Il a été conçu pour explorer et mettre en pratique les concepts de la **Programmation Orientée Objet (POO)** en Python.

L'architecture permet de gérer dynamiquement l'ajout de nouveaux jeux via l'introspection, et gère les mises et les jetons via des décorateurs.

## 🤖 Note sur la réalisation (Transparence IA)
Ce code est le fruit d'une collaboration entre logique humaine et assistance artificielle :
* **Conception & Architecture** : Structure des classes, logique métier (Casino, Croupier, Héritage) et algorithmique globale pensées par l'auteur.
* **Assistance IA** : Sollicitée pour la syntaxe Python idiomatique et l'implémentation technique de concepts avancés (notamment le module `inspect` pour le chargement dynamique des classes et la syntaxe des décorateurs).

## 🎯 Contexte du développeur
* **Expérience Python** : 3 semaines (Autodidacte).
* **Background** : Profil littéraire (Bac L) avec un fort intérêt pour les mathématiques et l'algorithmique.
* **Objectif initial** : Comprendre et appliquer l'héritage, le polymorphisme et l'encapsulation.

## 🛠️ Concepts Techniques Explorés
* **POO** : Classes, Héritage (`Game` -> `Roulette`), Composition (`Player` possède `Token`).
* **Introspection** : Utilisation de `inspect` pour détecter et charger automatiquement les jeux disponibles sans modifier le code principal.
* **Décorateurs** : Gestion des pré-requis (`@mandatory_token_purchase`) et validation des mises (`@control_bet`).
* **Typing** : Utilisation des type hints pour la clarté du code.

## 🛑 Le "Mur" (Pourquoi ce projet s'arrête ici)
Malgré le fonctionnement du code, j'ai atteint ma limite de compétence actuelle sur :
1.  La séparation propre entre l'interface utilisateur (I/O) et la logique pure.
2.  La gestion d'états complexes et immuables.
3.  L'architecture logicielle avancée (Design Patterns).

Plutôt que de "bricoler" sans comprendre, je choisis d'archiver ce projet comme une **première victoire** 🏆 et de consolider mes bases avant d'aller plus loin.

## 🚀 Installation et Lancement
1.  Cloner le repo.
2.  S'assurer d'avoir le fichier `cartes.py` dans le même répertoire.
3.  Lancer le jeu :
    ```bash
    python main.py
    ```

---
*"J'ai poussé jusqu'où je pouvais, pas jusqu'où je voulais."*
