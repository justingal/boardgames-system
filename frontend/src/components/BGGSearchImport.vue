<template>
  <div class="max-w-3xl mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">Pridėti žaidimą iš BGG</h2>

    <!-- Paieškos laukas -->
    <div class="flex gap-2 mb-4">
      <input
        v-model="query"
        @keyup.enter="search"
        type="text"
        placeholder="Įveskite žaidimo pavadinimą..."
        class="border rounded px-4 py-2 w-full"
      />
      <button
        @click="search"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Ieškoti
      </button>
    </div>

    <!-- Žinutės -->
    <p v-if="message" class="mb-4 text-sm text-gray-700">{{ message }}</p>

    <!-- Rezultatai -->
    <div v-if="results.length" class="space-y-3">
      <div
        v-for="game in results"
        :key="game.bgg_id"
        class="border p-3 rounded bg-white shadow flex justify-between items-center gap-4"
      >
        <div class="flex items-center gap-4">
          <img
            v-if="game.thumbnail_url"
            :src="game.thumbnail_url"
            alt="Game thumbnail"
            class="w-16 h-16 object-cover rounded"
          />
          <div>
            <h3 class="text-lg font-semibold">{{ game.title }}</h3>
            <p class="text-sm text-gray-600" v-if="game.year">Metai: {{ game.year }}</p>
          </div>
        </div>
        <button
          @click="importGame(game.bgg_id)"
          class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
        >
          Pridėti
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from '@/api/axios'

const query = ref('')
const results = ref<any[]>([])
const message = ref('')

const search = async () => {
  if (!query.value.trim()) return
  message.value = '🔍 Ieškoma...'
  try {
    const res = await axios.get('/bgg/search/', { params: { query: query.value } })
    results.value = res.data
    message.value = results.value.length ? '' : '⚠️ Nieko nerasta.'
  } catch (err) {
    console.error('BGG paieškos klaida:', err)
    message.value = '❌ Nepavyko gauti rezultatų.'
  }
}

const importGame = async (bgg_id: number) => {
  try {
    const res = await axios.post('/bgg/import/', { bgg_id })
    message.value = res.data.message || '✅ Pridėta!'
  } catch (err) {
    console.error('Importo klaida:', err)
    message.value = err.response?.data?.error || '❌ Klaida pridedant.'
  }
}
</script>
