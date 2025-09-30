<script setup>
const result = defineProps({
  title: {
    type: String,
    default: "Title",
  },
  content: {
    type: String,
    default:
      "This is a brief excerpt from the document to give context about its content...",
  },
  similarity: {
    type: Number,
    default: 0.85,
  },
});
</script>

<template>
  <div class="p-5  hover:border-purple-400 transition-colors border-1 bg-white border-gray-200 rounded-xl">
    <div class="flex items-start justify-between mb-2">
      <h3
        class="text-lg font-semibold text-slate-800 group-hover:text-blue-600 transition-colors"
      >
        {{ result.title }}
      </h3>
      <div
        class="flex items-center gap-1.5 bg-gradient-to-r from-blue-50 to-purple-50 px-3 py-1 rounded-full"
      >
        <div
          class="w-2 h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
        ></div>
        <span class="text-xs font-semibold text-slate-700">
          {{ (result.similarity * 100).toFixed(0) }}%
        </span>
      </div>
    </div>
    <p class="text-sm text-slate-600 leading-relaxed line-clamp-2">
      {{ result.content }}
    </p>
    <div class="mt-3 flex items-center gap-2">
      <span class="text-xs text-slate-500 bg-slate-100 px-2 py-1 rounded">
        Cosine similarity: {{ result.similarity.toFixed(3) }}
      </span>
    </div>
  </div>
</template>

<style scoped>

</style>
