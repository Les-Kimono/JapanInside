# JapanInside

## Table des matières
- Badges
- ...

## Badges

[![CI](https://github.com/Les-Kimono/JapanInside/actions/workflows/ci-frontend.yml/badge.svg)](
https://github.com/ORG/Les-Kimono/JapanInside/workflows/ci-frontend.yml
)
[![CI](https://github.com/Les-Kimono/JapanInside/actions/workflows/ci-backend.yml/badge.svg)](
https://github.com/ORG/Les-Kimono/JapanInside/workflows/ci-backend.yml
)


![Status](https://img.shields.io/badge/status-en%20développement-orange?style=for-the-badge)
![Licence](https://img.shields.io/github/license/Les-Kimono/JapanInside?style=for-the-badge)
![Dernier commit](https://img.shields.io/github/last-commit/Les-Kimono/JapanInside?style=for-the-badge)
![Contributeurs](https://img.shields.io/github/contributors/Les-Kimono/JapanInside?style=for-the-badge)
![Equipe](https://img.shields.io/badge/team-Les--Kimono-blue?style=for-the-badge)

## Equipe

- [@justine](https://github.com/WitheredFlower10)
- [@lucas](https://github.com/luucas7)
- [@adrien](https://github.com/baffionia)
- [@jordan](https://github.com/ZedRoff)
- [@auguste](https://github.com/ZedRoff)
- [@aman](https://github.com/ZedRoff)

## Descriptif

Ce projet a été réalisé dans le cadre de l'unité DevOps encadré par M. Badr TAJINI en 2ème année d'ingénieur à l'école ESIEE Paris (E4FI).

L'objectif est d'utilisé les pratiques de DevOps sur un projet déjà existant, pour y intégrer les pipelines CI/CD, de la dockerisation, kubernetes (minikube) et la gestion du travail collaboratif sur GitHub.

## Idée

Ce projet est une application full-stack, permettant d'organiser un voyage au Japon. Une partie front-office vous permet de visualiser votre voyage, les attractions, les spécialités culinaires et les étapes de votre voyage. Une partie back-office vous permet d'éditer votre voyage pour ajouter des étapes, attractions etc. en fonction de vos recherches Internet.

## Stack Technique

- Front-End : ReactJS
- Back-end : FastAPI
- DB : Posgresql
- Conteneurisation : Docker
- Déploiement : Minikube

## Tree

```
.
├── backend
│   ├── __pycache__
│   ├── crud
│   ├── data
│   ├── models
│   ├── routes
│   ├── schemas
│   ├── tests
│   └── utils
├── frontend
│   ├── node_modules
│   ├── public
│   └── src
└── k8s
    ├── backend
    ├── config
    ├── db
    └── frontend
```


Ce projet est muni de tests unitaires pour le front-end et le back-end, de makefiles, de pre-commit pour s'assurer du bon fonctionnement et d'un code "production-ready".

## Setup

### Installation

HTTPS : 
git clone https://github.com/Les-Kimono/JapanInside.git japan-inside <br />
SSH : 
git clone git@github.com:Les-Kimono/JapanInside.git japan-inside
cd japan-inside

### Lancement du projet

make first-install
make start
make stop
make start

(les deux dernières étapes sont pour l'instant obligatoires pour que la base de données se créé bien)

### Développement local

git checkout staging
make restart

## Pipeline CI

Nous dissocions deux pipelines, une pour le front-end et une pour le back-end

### Front-end

- Setup
- Linting
- Security Check
- Build
- Unit Testing

### Back-end

- Setup
- Code Sniffing
- Linting
- Safety Check
- Unit Testing

## Les Makefiles

Des Makefiles sont proposés dans ce projet afin de faciliter l'usage des commandes. On en distingue trois : 
- Le Makefile principal (dans la racine du projet), qui permet de lancer kubernetes, lancer les tests unitaires du front et du back. Aussi, pour lancer docker et build les images.
- Le Makefile du backend, qui permet de lancer les tests unitaires, réalisé du linting, faire du code-sniffing, lancer le container du back
- Le Makefile du frontend, qui permet de réaliser les mêmes actions sur le backend

## Pipeline CD

Lorsqu'un push est réalisé sur la branche main, la pipeline CD se lance.

- Build des images docker en utilisant les Dockerfile.prod du front et du back
- Déploiement des images sur Docker Hub
- Récupération des images depuis le Docker Hub vers Minikube
- Lancement de l'application en local sur Minikube (simulation d'un environnement Kubernetes similaire à la production)

