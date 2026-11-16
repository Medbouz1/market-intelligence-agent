# Market Intelligence Agent — Guide français

**Un point de départ partageable pour créer son propre agent de veille financière.**

Ce dépôt décrit une architecture **reproductible** inspirée du fonctionnement observable des rapports Market Intelligence : collecte, provenance, validation, analyse, scénarios, portefeuille facultatif, rendu PDF et export JSON.

**Ce n'est pas une copie du fonctionnement interne de ChatGPT** : pas de raisonnement caché, pas de prompts système confidentiels, pas de moteur de recherche propriétaire, pas de clés API personnelles.

## Ce qui est déjà utilisable

- Un programme Python qui reçoit une photographie structurée du marché, en vérifie les dates, les sources et les types d'affirmation ;
- Un contrôle des poids de portefeuille et du rapprochement valeur liquidative / titres / liquidités **lorsque des données réelles autorisées sont fournies** ;
- Un PDF A4 structuré en sept rubriques et un JSON consommable par d'autres projets ;
- Un exemple entièrement fictif, clairement marqué, et des tests automatiques GitHub Actions.

## Installation

Sur Windows ou Linux (Python 3.11 minimum) :

    git clone https://github.com/Medbouz1/market-intelligence-agent.git
    cd market-intelligence-agent
    python -m venv .venv
    # Activer l'environnement virtuel :
    # Windows : .venv\Scripts\activate
    # Linux/macOS : source .venv/bin/activate
    python -m pip install -e .
    market-intelligence --input examples/demo_snapshot.json --out reports --allow-synthetic

Le programme crée deux fichiers dans le répertoire reports : un PDF et un JSON. **Les prix du fichier de démonstration sont inventés uniquement pour tester le logiciel.** Ils ne doivent jamais être interprétés comme des cotations.

## Comment construire son propre agent, étape par étape

1. **Copier le prompt public** du dossier prompts dans son assistant préféré. Ce prompt donne la structure d'un rapport institutionnel français.
2. **Choisir les sources de données** : banques centrales, bureaux statistiques, administrateurs d'indices, données des émetteurs, fournisseurs ayant les droits de diffusion. Voir docs/SOURCES.md.
3. **Écrire un adaptateur** qui collecte les données et fournit le JSON attendu (l'exemple contient la structure des champs). Toutes les valeurs réelles exigent source URL et horodatage.
4. **Vérifier le résultat** avec le moteur Python, qui refuse les cours sans preuve, les heures futures et les compositions IBKR non disponibles.
5. **Créer le PDF et le JSON**. La génération elle-même ne nécessite pas un abonnement LLM.
6. **Automatiser** à 08 h Europe/Paris les jours ouvrés, sur GitHub Actions, un serveur, un orchestrateur, ou via une tâche planifiée de son assistant si son environnement autorise la génération de fichiers. La planification n'est pas activée automatiquement par le dépôt.
7. **Brancher un courtier uniquement si nécessaire et avec autorisation en lecture seule.** Ne jamais publier ses positions ni ses identifiants dans GitHub.

## Ce qui reste à développer

Le projet v0.1 n'interroge pas encore automatiquement les marchés, ne lit pas le compte IBKR et n'écrit pas tout seul une analyse d'actualité à partir d'un LLM. Une installation seule **ne** produit donc **pas** de véritable édition du jour.

Ces modules figurent dans ROADMAP.md. Un système complet exige aussi un budget API éventuel, des licences de données, du contrôle qualité et un journal de corrections.

## Usage avec Alpha Lab / Quorum AI

Le JSON du rapport est conçu comme **contexte de recherche** : observations macro, risques, dates, sources, fenêtres temporelles. Il pourra alimenter des études d'allocation, de volatilité, de réactions aux événements ou de sensibilité aux taux et à l'énergie.

Il **ne constitue pas** un signal d'achat/vente. L'intégration aux dépôts privés n'a pas encore été réalisée. Le document docs/ALPHA_LAB_INTEGRATION.md décrit une interface qui exige contrôles temporels, validation de données et absence de connexion directe à la passation d'ordres.

## Partager

Lien du dépôt : https://github.com/Medbouz1/market-intelligence-agent

Créer sa propre copie : https://github.com/Medbouz1/market-intelligence-agent/generate

Licence MIT ; toute contribution doit conserver les garde-fous sur la provenance des sources, la confidentialité et les ordres.
