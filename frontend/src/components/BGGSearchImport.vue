<template>
  <div class="max-w-4xl mx-auto p-6 bg-gray-50 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6 text-indigo-800 flex items-center">
      <span class="mr-2">🔍</span> Pridėti žaidimą iš BoardGameGeek
    </h2>

    <!-- Paieškos laukas -->
    <div class="bg-white p-5 rounded-lg shadow-sm mb-6">
      <div class="flex gap-2">
        <input
          v-model="query"
          @keyup.enter="search"
          type="text"
          placeholder="Įveskite žaidimo pavadinimą..."
          class="border border-gray-300 rounded-md px-4 py-3 w-full focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
        />
        <button
          @click="search"
          class="bg-gradient-to-r from-blue-500 to-blue-700 text-white px-6 py-3 rounded-md hover:from-blue-600 hover:to-blue-800 transition flex items-center gap-2"
        >
          <span>🔍</span>
          Ieškoti
        </button>
      </div>
    </div>

    <!-- Žinutės -->
    <div v-if="message" class="mb-6">
      <p
        class="py-3 px-4 rounded-md text-sm"
        :class="message.includes('✅') ? 'bg-green-100 text-green-800' : message.includes('⚠️') ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'"
      >
        {{ message }}
      </p>
    </div>

    <!-- Rezultatai -->
    <div v-if="results.length" class="space-y-4">
      <h3 class="text-xl font-semibold text-gray-700 mb-4">Paieškos rezultatai</h3>

      <div
        v-for="game in results"
        :key="game.bgg_id"
        class="bg-white border border-gray-200 p-4 rounded-lg shadow-sm hover:shadow-md transition flex justify-between items-center gap-4"
      >
        <div class="flex items-center gap-4">
          <div class="w-20 h-20 flex-shrink-0">
            <img
              v-if="game.thumbnail_url"
              :src="game.thumbnail_url"
              alt="Game thumbnail"
              class="w-full h-full object-cover rounded-md shadow"
            />
            <div v-else class="w-full h-full bg-gray-200 rounded-md flex items-center justify-center text-gray-500">
              🎲
            </div>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-indigo-800">{{ game.title }}</h3>
            <p class="text-sm text-gray-600" v-if="game.year">Išleista: {{ game.year }} m.</p>
            <p class="text-xs text-gray-500 mt-1">BGG ID: {{ game.bgg_id }}</p>
          </div>
        </div>
        <button
          @click="importGame(game.bgg_id)"
          class="bg-white border border-emerald-500 text-emerald-600 px-4 py-2 rounded-md hover:bg-emerald-50 transition-all duration-200 flex items-center gap-2 shadow-sm group"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform duration-300 group-hover:rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>Pridėti į kolekciją</span>
        </button>
      </div>

      <div v-if="results.length > 5" class="text-center mt-6">
        <button
          @click="search"
          class="bg-indigo-100 text-indigo-700 px-4 py-2 rounded-md hover:bg-indigo-200 transition"
        >
          Atnaujinti paiešką
        </button>
      </div>
    </div>

    <!-- Tuščios paieškos būsena -->
    <div v-if="results.length === 0 && message && message.includes('Nieko')" class="text-center py-8">
      <p class="text-lg text-gray-600">Pabandykite kitą paiešką...</p>
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
