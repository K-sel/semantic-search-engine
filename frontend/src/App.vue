<script setup>
import { ref } from "vue";
import TextCard from "./component/Text-Card.vue";
import Visualisation from "./component/Text.vue";
import SearchBar from "./component/SearchBar.vue";
import Header from "./component/Header.vue";
const searchQuery = ref("");
const isSearching = ref(false);

const mockResults = ref([
  {
    id: 1,
    title: "Introduction to Machine Learning",
    content:
      "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed...",
    similarity: 0.94,
  },
  {
    id: 2,
    title: "Neural Networks Explained",
    content:
      "Neural networks are computing systems inspired by biological neural networks that constitute animal brains. They learn to perform tasks by considering examples...",
    similarity: 0.89,
  },
  {
    id: 3,
    title: "Deep Learning Fundamentals",
    content:
      "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning...",
    similarity: 0.87,
  },
  {
    id: 4,
    title: "Natural Language Processing",
    content:
      "NLP is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language...",
    similarity: 0.82,
  },
  {
    id: 5,
    title: "Computer Vision Applications",
    content:
      "Computer vision is an interdisciplinary scientific field that deals with how computers can gain high-level understanding from digital images or videos...",
    similarity: 0.78,
  },
]);

const handleSearch = (e) => {
  e.preventDefault();
  isSearching.value = true;
  setTimeout(() => {
    isSearching.value = false;
  }, 800);
};
</script>

<template>
  <main
    class="w-full h-screen flex bg-gradient-to-br from-slate-50 to-slate-100"
  >
    <!-- Left Panel - Search Interface -->
    <div class="flex flex-col w-full md:w-1/2 overflow-hidden">
      <Header />

      <!-- Search Bar -->
      <SearchBar />

      <!-- Results -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div class="flex items-center justify-between mb-4">
          <h2
            class="text-sm font-semibold text-slate-700 uppercase tracking-wide"
          >
            Meilleurs résultats
          </h2>
          <span
            class="text-xs text-slate-500 bg-slate-200 px-3 py-1 rounded-full"
          >
            5 résultats
          </span>
        </div>

        <div v-for="result in 5">
          <TextCard />
        </div>
      </div>
    </div>
    <div
      class="border-l hidden md:flex border-gray-200 bg-white w-[50%] h-full flex-col"
    >
      <Visualisation />
    </div>
  </main>
</template>

<style scoped></style>
