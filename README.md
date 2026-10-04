# Frontier Models Watch

[![Weekly collection](https://github.com/valorisa/AI-Frontier-Watcher/actions/workflows/weekly-collection.yml/badge.svg)](https://github.com/valorisa/AI-Frontier-Watcher/actions/workflows/weekly-collection.yml)
[![Markdownlint](https://github.com/valorisa/AI-Frontier-Watcher/actions/workflows/markdownlint.yml/badge.svg)](https://github.com/valorisa/AI-Frontier-Watcher/actions/workflows/markdownlint.yml)
[![pylint](https://github.com/valorisa/AI-Frontier-Watcher/actions/workflows/pylint.yml/badge.svg)](https://github.com/valorisa/AI-Frontier-Watcher/actions/workflows/pylint.yml)
[![License](https://img.shields.io/github/license/valorisa/AI-Frontier-Watcher)](LICENSE)

> Veille documentaire reproductible sur les modèles d'IA de pointe, avec un suivi renforcé de GPT-6 Astra, de sa disponibilité, de ses évolutions, de ses modes d'accès et de ses concurrents directs.

## Objectif

**AI-Frontier-Watcher** est un projet de veille documentaire consacré à l'évolution des modèles d'IA de pointe.

Le projet cherche notamment à suivre :

- les nouveaux modèles et nouvelles versions ;
- les conditions d'accès selon le produit, le forfait, l'API et le fournisseur ;
- les capacités, fenêtres de contexte, modes de raisonnement et outils ;
- les changements de prix et de limites lorsqu'ils sont documentés ;
- les retraits, remplacements, alias et changements de cycle de vie ;
- les benchmarks et évaluations indépendantes ;
- les évolutions des plateformes qui exposent plusieurs modèles.

GPT-6 Astra constitue un axe de suivi prioritaire, mais le projet n'est pas limité à OpenAI.

## État actuel

**État de référence : 2026-10-04.**

À cette date, la documentation officielle OpenAI indique que GPT-6 Astra est disponible dans ChatGPT pour les offres Pro, Business et Enterprise, tandis que les offres Plus incluent Astra dans ChatGPT Work et Codex. La documentation API indique par ailleurs que le niveau Free n'est pas pris en charge pour `gpt-6-astra`.

Le projet distingue donc explicitement :

- **ChatGPT Free** ;
- **ChatGPT Plus, Pro, Business et Enterprise** ;
- **ChatGPT Work** ;
- **Codex** ;
- **OpenAI API** ;
- **Microsoft Azure** ;
- **AWS Bedrock** ;
- **plateformes tierces**, notamment OpenRouter.

> **Règle de prudence :** l'absence d'une offre dans une page officielle n'est pas transformée en affirmation absolue d'indisponibilité. Le dépôt emploie de préférence des formulations telles que « officiellement documenté », « non documenté dans la source consultée » ou « disponibilité non vérifiée ».

## Modèles suivis

Le périmètre initial comprend notamment :

| Famille | Suivi |
| --- | --- |
| OpenAI | GPT-6 Astra, GPT-6 Sol, GPT-6 Luna et évolutions associées |
| Anthropic | Claude Fable, Claude Opus et autres modèles frontier pertinents |
| Google | Gemini et modèles associés pertinents |
| xAI | Grok et évolutions associées |
| OpenRouter | Catalogue, disponibilité, routage et données d'usage pertinentes |
| Microsoft | Exposition des modèles via Azure / Microsoft Foundry |
| AWS | Exposition des modèles via Bedrock |
| Autres laboratoires | Ajoutés lorsqu'ils atteignent une importance comparable dans la frontière des modèles |

La liste est volontairement évolutive : un modèle n'est pas conservé dans le périmètre uniquement parce qu'il porte un nom prestigieux.

## Sources et hiérarchie de confiance

La veille applique quatre niveaux.

### Niveau 1 — Sources primaires

Sources publiées directement par les fournisseurs ou laboratoires concernés :

- OpenAI ;
- Anthropic ;
- Google ;
- xAI ;
- OpenRouter ;
- Microsoft ;
- AWS ;
- autres fournisseurs concernés.

Ces sources constituent la référence principale pour les annonces, disponibilités, prix et conditions d'accès propres à leur produit.

### Niveau 2 — Documentation technique primaire

Sont privilégiés :

- documentation API ;
- catalogues de modèles ;
- changelogs ;
- notes de version ;
- documentation de déploiement ;
- pages de cycle de vie ;
- pages de tarification officielles.

### Niveau 3 — Sources secondaires

Utilisées pour compléter ou contextualiser :

- presse spécialisée ;
- benchmarks indépendants ;
- analyses techniques ;
- études comparatives.

Une source secondaire ne remplace pas une source primaire lorsqu'une information officielle existe.

### Niveau 4 — Réseaux sociaux et forums

Ils servent uniquement de **signal** pour détecter une information à vérifier.

Un post, commentaire ou message de forum ne constitue pas à lui seul une preuve de disponibilité, de prix ou de changement de politique.

## Suivi chronologique

### 2026-10-04

Initialisation du projet.

Le premier état documenté porte une attention particulière à GPT-6 Astra. Les sources officielles OpenAI consultées indiquent une disponibilité dans les offres Pro, Business et Enterprise de ChatGPT, ainsi que dans ChatGPT Work et Codex pour Plus. L'API `gpt-6-astra` est documentée avec un niveau Free non pris en charge.

La documentation Microsoft Foundry documente également `gpt-6-astra` et sa date de modèle du 3 septembre 2026. OpenRouter documente Astra comme modèle disponible sur sa plateforme, avec OpenAI et Azure parmi les fournisseurs servis.

Le bulletin OpenRouter fourni comme source documentaire initiale au projet signale notamment :

- GPT-6 Astra lancé le 4 septembre ;
- GPT-6 Sol et GPT-6 Luna lancés le 22 septembre ;
- Grok 4.7 lancé le 21 septembre ;
- Claude Fable 5.1 lancé le 1er septembre ;
- Claude Opus 5.5 lancé le 22 septembre ;
- GPT-6 Astra, Claude Fable 5.1 et GPT-6 Sol placés parmi les trois premiers de l'Intelligence Index d'OpenRouter au moment couvert par ce bulletin.

Ces éléments provenant du bulletin OpenRouter restent identifiés comme **source secondaire/plateforme** lorsqu'ils concernent des affirmations sur les modèles eux-mêmes.

## Disponibilité des modèles

La disponibilité est suivie par **produit et mode d'accès**, et non comme une propriété binaire du modèle.

| Modèle | ChatGPT Free | Plus | Pro | Business | Enterprise | API | OpenRouter | Azure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-6 Astra | Non documenté officiellement | Work/Codex | ChatGPT | ChatGPT | ChatGPT, selon droits | Oui | Oui | Oui |
| GPT-6 Sol | À vérifier | À vérifier | À vérifier | À vérifier | À vérifier | Oui | Oui | Oui |
| GPT-6 Luna | À vérifier | À vérifier | À vérifier | À vérifier | À vérifier | Oui | Oui | Oui |
| Claude Fable 5.1 | N/A | N/A | N/A | N/A | N/A | Selon Anthropic | Oui | Selon fournisseur |
| Grok 4.7 | N/A | N/A | N/A | N/A | N/A | Oui | Oui | N/A |
| Gemini frontier | N/A | N/A | N/A | N/A | N/A | Oui | Selon catalogue | Selon catalogue |

**Important :** `Oui`, `Non documenté`, `À vérifier` et `N/A` ne sont pas interchangeables.

- **Oui** : une source pertinente confirme l'accès.
- **Non documenté** : aucune confirmation officielle suffisante n'a été retenue.
- **À vérifier** : la cellule nécessite une vérification ultérieure.
- **N/A** : la colonne ne correspond pas au produit concerné.

Les cellules sont destinées à évoluer avec la veille.

## Méthodologie

Chaque information importante doit idéalement être accompagnée des éléments suivants :

1. date de publication ou de dernière mise à jour ;
2. source ;
3. niveau de confiance de la source ;
4. produit concerné ;
5. modèle concerné ;
6. mode d'accès ;
7. statut de vérification ;
8. formulation qui distingue fait établi et interprétation.

### Distinction modèle / produit / accès

Le dépôt ne déduit jamais automatiquement :

```text
modèle disponible sur une plateforme
        ≠
modèle disponible dans tous les produits du fournisseur
        ≠
modèle disponible pour tous les forfaits
```

Exemple :

```text
GPT-6 Astra disponible sur OpenRouter
        ≠
GPT-6 Astra disponible dans ChatGPT Free
```

### Prix

Les prix doivent toujours être associés à leur contexte :

- fournisseur ;
- produit ;
- API ou interface ;
- type de requête ;
- date de référence.

Un prix OpenRouter n'est pas automatiquement un prix OpenAI direct.

## Automatisation hebdomadaire

Le projet utilise GitHub Actions selon le schéma :

```text
GitHub Actions
      |
      v
collecte automatique des sources
      |
      v
comparaison avec l'état précédent
      |
      v
rapport hebdomadaire
      |
      v
validation humaine
      |
      +---- rejet ----> aucun changement publié
      |
      +---- validation ----> mise à jour du README
```

La première version automatise surtout la **collecte et la détection de changements**. Elle ne modifie pas automatiquement le README publié.

Le workflow hebdomadaire peut également être lancé manuellement.

## Secrets et API

Le dépôt est conçu pour pouvoir utiliser ultérieurement un secret GitHub Actions nommé :

```text
OPENAI_API_KEY
```

Le secret n'est jamais stocké dans le dépôt.

La première version de la collecte fonctionne sans ce secret. Une étape ultérieure pourra utiliser l'API OpenAI pour produire une synthèse structurée du rapport, après collecte des sources.

Le principe retenu est celui du moindre privilège : les workflows disposent uniquement des permissions nécessaires et les secrets ne sont exposés qu'aux étapes qui en ont réellement besoin.

## Historique des mises à jour

| Date | Type | Résumé |
| --- | --- | --- |
| 2026-10-04 | Initialisation | Création du dépôt et définition de la méthodologie |
| À venir | Veille | Premier rapport hebdomadaire automatisé |

## Limites et précautions

Cette veille ne prétend pas fournir une disponibilité universelle et instantanée.

Les principales limites sont :

- les offres peuvent varier selon le pays, le compte, le contrat ou l'espace de travail ;
- les déploiements peuvent être progressifs ;
- les pages officielles peuvent changer sans conserver toutes les versions précédentes ;
- les plateformes tierces peuvent exposer un modèle avant ou après son intégration dans un produit donné ;
- les benchmarks ne mesurent pas toutes les capacités ;
- les noms commerciaux et identifiants API peuvent changer ;
- les résultats automatisés doivent être vérifiés avant publication dans le README.

Une information non vérifiée reste une information à vérifier.

## Sources principales

Les sources de référence initiales sont :

- OpenAI — annonces et documentation des modèles ;
- OpenAI Help Center — disponibilité dans ChatGPT, Work et Codex ;
- OpenAI API documentation ;
- Anthropic — Newsroom et documentation Claude ;
- Google AI for Developers — catalogue Gemini ;
- xAI — documentation des modèles Grok ;
- Microsoft Foundry — catalogue des modèles Azure ;
- OpenRouter — catalogue et données de plateforme ;
- Artificial Analysis — évaluations indépendantes, performances, prix et disponibilité.

Le bulletin OpenRouter fourni comme document de départ est conservé comme source documentaire de contexte ; il ne remplace pas les sources primaires.

## Licence

Ce projet est distribué sous licence MIT. Voir [LICENSE](LICENSE).

---

**Dernière révision documentaire : 2026-10-04.**
