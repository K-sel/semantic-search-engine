<script setup>
// Définition des props
const props = defineProps({
  indexedCount: {
    type: Number,
    default: 1000
  }
});

const handleSearch = (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const query = formData.get('query');

  // FETCH TO API 
};
</script>

<template>
  <div class="p-6 bg-white border-b border-slate-200">
    <form @submit="handleSearch" class="relative">
      <div class="relative">
        <input
          name="query"
          type="search"
          placeholder="Rechercher dans la base de connaissances..."
          class="w-full p-4 bg-slate-50 border-2 border-slate-200 rounded-xl focus:outline-none focus:border-blue-500 focus:bg-white transition-all duration-200 text-slate-800 placeholder-slate-400"
        />
      </div>
      <div class="flex items-center gap-2 mt-3 text-xs text-slate-500">
        <span>{{ props.indexedCount }} documents indexés</span>
      </div>
    </form>
  </div>
</template>

<style scoped></style>