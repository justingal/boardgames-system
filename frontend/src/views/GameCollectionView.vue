<template>
  <div class="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-6 text-indigo-800 border-b pb-2">Mano žaidimų kolekcija</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- Failo importas -->
      <div class="bg-white p-5 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 flex items-center">
          <span class="mr-2">📁</span> Importuoti iš failo
        </h2>

        <input
          type="file"
          ref="fileInput"
          accept=".csv,.json"
          @change="onFileChange"
          class="hidden"
        />

        <button
          @click="triggerFileSelect"
          class="w-full bg-gradient-to-r from-blue-500 to-blue-700 text-white px-4 py-3 rounded-md hover:from-blue-600 hover:to-blue-800 transition flex items-center justify-center"
        >
          <span class="mr-2">📥</span> Importuoti CSV/JSON
        </button>

        <p v-if="message" class="mt-3 text-sm p-2 rounded"
           :class="message.includes('✅') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
          {{ message }}
        </p>
      </div>

      <!-- BGG paieška -->
      <div class="bg-white p-5 rounded-lg shadow-md col-span-1 lg:col-span-2">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 flex items-center">
          <span class="mr-2">🔍</span> Ieškoti pagal pavadinimą
        </h2>

        <div class="flex gap-2">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Įveskite žaidimo pavadinimą..."
            class="w-full border border-gray-300 rounded-md px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
          <button
            @click="searchBGG"
            class="bg-gradient-to-r from-indigo-500 to-indigo-700 text-white px-6 py-3 rounded-md hover:from-indigo-600 hover:to-indigo-800 transition flex items-center justify-center"
          >
            <span>Ieškoti</span>
          </button>
        </div>
      </div>
    </div>

    <!-- BGG paieškos rezultatai -->
    <div v-if="searchResults.length" class="mb-10 bg-white p-5 rounded-lg shadow-md">
      <h2 class="text-xl font-semibold mb-4 text-gray-700">Paieškos rezultatai</h2>
      <div class="space-y-3">
        <div
          v-for="result in searchResults"
          :key="result.bgg_id"
          class="border rounded-lg p-4 bg-gray-50 flex items-center gap-4 hover:bg-gray-100 transition"
        >
          <img
            v-if="result.thumbnail_url"
            :src="result.thumbnail_url"
            :alt="result.title"
            class="w-30 h-20 object-cover rounded-md shadow"
          />
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-indigo-800">{{ result.title }}</h3>
            <p class="text-sm text-gray-600" v-if="result.year">Metai: {{ result.year }}</p>
          </div>
          <button
            @click="importFromBGG(result.bgg_id)"
            class="bg-gradient-to-br from-blue-500 to-blue-600 text-white px-4 py-2 rounded-md hover:from-blue-600 hover:to-blue-700 transition-all duration-200 flex items-center gap-2 shadow-md hover:shadow-lg"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span>Pridėti</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Kolekcijos atvaizdavimas -->
    <div>
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold text-gray-700 flex items-center">
          <span class="mr-2">🎲</span> Mano kolekcija
        </h2>
        <span class="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
          {{ collection.length }} žaidimų
        </span>
      </div>

      <div v-if="!collection.length" class="bg-white p-8 rounded-lg shadow-md text-center">
        <div class="flex flex-col items-center justify-center py-6">
          <div class="text-6xl mb-4">🎮</div>
          <h3 class="text-xl font-semibold text-gray-700 mb-2">Jūsų kolekcija tuščia</h3>
          <p class="text-gray-500 max-w-md mx-auto">Pradėkite importuodami žaidimus iš failo arba ieškokite jų BoardGameGeek svetainėje.</p>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="item in collection"
          :key="item.id"
          class="bg-white shadow-md rounded-lg overflow-hidden transition duration-300 hover:shadow-lg border border-gray-200 group relative"
        >
          <!-- Žaidimo nuotrauka kompaktiškesnė -->
          <div class="flex justify-center items-center p-4 bg-gray-50">
            <div class="relative w-90 h-40 rounded-lg overflow-hidden shadow-sm">
              <img
                v-if="item.game.thumbnail_url"
                :src="item.game.thumbnail_url"
                :alt="item.game.title"
                class="w-full h-full object-contain transition-transform duration-500 group-hover:scale-110"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center bg-indigo-50 text-4xl text-indigo-300"
              >
                🎲
              </div>
            </div>
          </div>

          <!-- Žaidimo informacija -->
          <div class="p-5">
            <div class="flex justify-between">
              <h2 class="text-lg font-bold text-indigo-800 line-clamp-1">{{ item.game.title }}</h2>

              <!-- Ištrynimo mygtukas -->
              <div class="relative">
                <button
                  @click="deleteGame(item.game.id)"
                  class="text-gray-400 hover:text-red-500 transition-colors duration-200 w-8 h-8 flex items-center justify-center rounded-full hover:bg-red-50"
                  title="Ištrinti žaidimą"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Žaidimo detalės -->
            <div class="mt-4 grid grid-cols-2 gap-3">
              <div class="bg-gray-50 p-2 rounded-lg flex items-center">
                <span class="flex items-center justify-center bg-indigo-100 text-indigo-800 rounded-md w-8 h-8 mr-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                  </svg>
                </span>
                <div class="text-xs">
                  <div class="text-gray-500">Žaidėjų</div>
                  <div class="font-semibold text-gray-900">{{ item.game.min_players }}–{{ item.game.max_players }}</div>
                </div>
              </div>

              <div class="bg-gray-50 p-2 rounded-lg flex items-center">
                <span class="flex items-center justify-center bg-indigo-100 text-indigo-800 rounded-md w-8 h-8 mr-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
                  </svg>
                </span>
                <div class="text-xs">
                  <div class="text-gray-500">Trukmė</div>
                  <div class="font-semibold text-gray-900">{{ item.game.playtime_minutes }} min</div>
                </div>
              </div>
            </div>

            <!-- Papildomos detalės -->
            <div class="mt-4 pt-3 border-t border-gray-100">
              <div class="flex items-center justify-between text-xs text-gray-500">
                <span class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Pridėta {{ new Date(item.added_at).toLocaleDateString() }}
                </span>
                <span class="bg-indigo-50 text-indigo-600 px-2 py-1 rounded-md text-xs font-medium">
                  BGG
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from '@/api/axios'

interface Game {
  title: string
  thumbnail_url: string
  min_players: number
  max_players: number
  playtime_minutes: number
}

interface GameCollectionItem {
  id: number
  added_at: string
  game: Game
}

interface BGGSearchResult {
  bgg_id: number
  title: string
  year: number | null
  thumbnail_url?: string

}

const collection = ref<GameCollectionItem[]>([])
const file = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const message = ref('')
const searchQuery = ref('')
const searchResults = ref<BGGSearchResult[]>([])

const fetchCollection = async () => {
  try {
    const res = await axios.get('/collections/')
    collection.value = res.data
  } catch (err) {
    console.error('Nepavyko gauti kolekcijos:', err)
  }
}

onMounted(fetchCollection)

const triggerFileSelect = () => {
  fileInput.value?.click()
}

const onFileChange = async (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files?.length) {
    file.value = target.files[0]
    await uploadFile()
  }
}

const uploadFile = async () => {
  if (!file.value) {
    message.value = '❗ Pasirinkite failą.'
    return
  }

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const res = await axios.post('/collections/import-csv/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    const added = res.data.added || []
    const skipped = res.data.skipped || []

    message.value = `✅ Pridėta: ${added.length}, ❌ Praleista: ${skipped.length}`

    if (skipped.length > 0) {
      console.warn("Praleisti žaidimai:", skipped)
      console.table(skipped)
    }

    await fetchCollection()
  } catch (err) {
    console.error('Failo importavimo klaida:', err)
    message.value = '❌ Klaida įkeliant failą.'
  }
}

const searchBGG = async () => {
  if (!searchQuery.value.trim()) return

  try {
    const res = await axios.get('/bgg/search/', {
      params: { query: searchQuery.value },
    })
    searchResults.value = res.data
  } catch (err) {
    console.error('Paieškos klaida:', err)
    searchResults.value = []
  }
}
const deleteGame = async (gameId: number) => {
  if (!confirm('Ar tikrai norite ištrinti šį žaidimą iš kolekcijos?')) return

  try {
    await axios.delete(`/collections/${gameId}/delete/`)
    message.value = '✅ Žaidimas pašalintas.'
    await fetchCollection()
  } catch (err) {
    console.error('Klaida trinant žaidimą:', err)
    message.value = '❌ Klaida trinant žaidimą.'
  }
}

const importFromBGG = async (bgg_id: number) => {
  try {
    const res = await axios.post('/collections/add-from-search/', {  bgg_id })
    message.value = res.data.message || 'Žaidimas pridėtas.'
    await fetchCollection()
  } catch (err) {
    console.error('Importavimo klaida:', err)
    message.value = '❌ Klaida importuojant žaidimą.'
  }
}
</script>
