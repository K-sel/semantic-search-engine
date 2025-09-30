<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  selectedResult: {
    type: Object,
    default: null,
  },
});

const projectInfo = ref({
  id: 0,
  title: "À propos de ce moteur de recherche sémantique",
  content: `Bienvenue dans ce moteur de recherche sémantique basé sur l'intelligence artificielle !

Ce projet est une démonstration avancée de recherche sémantique utilisant des techniques modernes de traitement du langage naturel (NLP) et d'apprentissage automatique.

Comment ça fonctionne ?

Ce système utilise une architecture sophistiquée basée sur plusieurs composants clés :

1. Modèle d'Embeddings
Le moteur utilise un modèle de langage pré-entraîné pour convertir les documents textuels en vecteurs numériques (embeddings). Ces vecteurs capturent la signification sémantique du texte, permettant de comparer des documents non pas sur la base de mots-clés exacts, mais sur leur sens réel.

2. Base de données vectorielle FAISS
FAISS (Facebook AI Similarity Search) est une bibliothèque développée par Meta AI qui permet de rechercher efficacement des vecteurs similaires dans de grandes collections. Elle utilise des structures d'index optimisées pour effectuer des recherches de similarité à grande échelle en quelques millisecondes.

3. Similarité Cosinus
Pour déterminer la pertinence d'un document par rapport à une requête, le système calcule la similarité cosinus entre le vecteur de la requête et les vecteurs des documents indexés. Un score de 1.0 indique une correspondance parfaite, tandis qu'un score proche de 0 indique peu de similarité.

Avantages de la recherche sémantique :

- Compréhension contextuelle : Le système comprend le sens des mots dans leur contexte, pas seulement leur présence littérale.

- Recherche multilingue : Les embeddings peuvent capturer des concepts similaires dans différentes langues.

- Tolérance aux variations : Les synonymes, paraphrases et formulations différentes donnent des résultats pertinents.

- Recherche conceptuelle : Vous pouvez rechercher des concepts abstraits sans connaître les mots-clés exacts.

Architecture technique :

Backend (Python)
- Framework : Flask
- Modèle d'embeddings : Sentence-Transformers (BERT, RoBERTa, etc.)
- Dimension des vecteurs : 384 dimensions
- Base vectorielle : FAISS avec index IVF (Inverted File Index)

Frontend (Vue.js)
- Framework : Vue.js 
- Styling : Tailwind CSS
- Composants : Architecture modulaire et réactive

Utilisation :

1. Saisissez votre requête dans la barre de recherche
2. Le système convertit votre requête en vecteur
3. FAISS recherche les documents les plus similaires
4. Les résultats sont classés par score de similarité
5. Cliquez sur un résultat pour voir le contenu complet

Ce projet démontre la puissance de l'IA moderne pour améliorer l'expérience de recherche et de découverte d'information. La recherche sémantique représente une évolution majeure par rapport aux systèmes traditionnels basés sur des mots-clés.`,
  score: 1.0,
});

const displayResult = computed(() => {
  return props.selectedResult || projectInfo.value;
});

</script>

<template>
  <!-- Contenu du document -->
  <div class="flex-1 flex flex-col overflow-hidden">
    <!-- Header -->
    <div
      class="p-6 border-b h-[150px] border-slate-200 bg-gradient-to-r from-slate-50 to-white"
    >
      <div class="flex items-start justify-between mb-4">
        <div class="flex-1">
          <div class="flex items-center gap-2 mb-2">
            <div
              class="flex items-center gap-1.5 bg-gradient-to-r from-blue-50 to-purple-50 px-3 py-1 rounded-full"
            >
              <div
                class="w-2 h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
              ></div>
              <span class="text-xs font-semibold text-slate-700">
                {{ Math.round(displayResult.score * 100) }}% similarité
              </span>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-slate-900">
            {{ displayResult.title }}
          </h2>
        </div>
        <button
          v-if="selectedResult"
          @click="handleClose"
          class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
          title="Fermer"
        ></button>
      </div>

      <!-- Métadonnées -->
      <div class="flex flex-wrap gap-3 text-xs text-slate-600">
        <div
          class="flex items-center gap-1.5 bg-slate-100 px-2 py-1 rounded-lg"
        >
          <span>{{ displayResult.content?.length || 0 }} caractères</span>
        </div>
        <div
          class="flex items-center gap-1.5 bg-slate-100 px-2 py-1 rounded-lg"
        >
          <span
            >Cosine similarity:
            {{ displayResult.score?.toFixed(4) || "N/A" }}</span
          >
        </div>
      </div>
    </div>

    <!-- Contenu scrollable -->
    <div class="flex-1 overflow-y-auto p-6">
      <div class="prose prose-slate max-w-none">
        <div class="text-slate-700 leading-relaxed whitespace-pre-wrap">
          {{ displayResult.content }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.prose {
  color: inherit;
}
</style>
