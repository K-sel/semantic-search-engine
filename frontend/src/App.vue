<script setup>
import { onMounted, ref } from "vue";
import TextCard from "./component/Text-Card.vue";
import Visualisation from "./component/Text.vue";
import SearchBar from "./component/SearchBar.vue";
import Header from "./component/Header.vue";
const results = ref(null);
const indexes = ref(null);

onMounted(() => {
  fetch("http://localhost:5173/api/")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      indexes.value = data.index_size;
    });
});
const handleSearch = async (query) => {
  if (!query || query.trim() === "") {
    results.value = [];
    return;
  }
  const response = await fetch(`http://localhost:5173/api/search?q=${query}`);
  results.value = await response.json();
};

const doc = ref(null);

const printDoc = (selectedDoc) => {
  doc.value = selectedDoc;
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
      <SearchBar :indexed-count="indexes" @search="handleSearch" />

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

        <div v-for="doc in results" :key="doc.id">
          <TextCard
            @click="printDoc(doc)"
            :content="doc.content"
            :title="doc.title"
            :similarity="doc.score"
          />
        </div>
      </div>
    </div>
    <div
      class="border-l hidden md:flex border-gray-200 bg-white w-[50%] h-full flex-col"
    >
      <Visualisation :selectedResult="doc" />
    </div>
  </main>
</template>

<style scoped></style>
