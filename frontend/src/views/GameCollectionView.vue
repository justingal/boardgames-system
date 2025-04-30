<template>
  <div class="max-w-5xl mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Mano žaidimų kolekcija</h1>

    <!-- Failo importas -->
    <div class="mb-6">
      <label class="block mb-2 font-medium">Įkelti CSV arba JSON failą:</label>

      <input
        type="file"
        ref="fileInput"
        accept=".csv,.json"
        @change="onFileChange"
        class="hidden"
      />

      <button
        @click="triggerFileSelect"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Importuoti
      </button>

      <p v-if="message" class="mt-2 text-sm text-gray-700">{{ message }}</p>
    </div>

    <!-- BGG paieška -->
    <div class="mb-6">
      <label class="block mb-2 font-medium">Ieškoti žaidimų per BGG:</label>
      <div class="flex gap-2">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Įveskite žaidimo pavadinimą..."
          class="w-full border border-gray-300 rounded px-3 py-2"
        />
        <button
          @click="searchBGG"
          class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
        >
          Ieškoti
        </button>
      </div>
      <ul v-if="searchResults.length" class="mt-4 space-y-2">
        <li
          v-for="result in searchResults"
          :key="result.bgg_id"
          class="border rounded p-3 bg-gray-50 flex items-center gap-4"
        >
          <img
            v-if="result.thumbnail_url"
            :src="result.thumbnail_url"
            :alt="result.title"
            class="w-16 h-16 object-cover rounded"
          />
          <div class="flex-1">
            <h3 class="text-lg font-semibold">{{ result.title }}</h3>
            <p class="text-sm text-gray-600" v-if="result.year">Metai: {{ result.year }}</p>
          </div>
          <button
            @click="importFromBGG(result.bgg_id)"
            class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
          >
            ➕ Pridėti
          </button>
        </li>
      </ul>

    </div>

    <!-- Kolekcijos atvaizdavimas -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="item in collection"
        :key="item.id"
        class="bg-white shadow rounded p-4 flex gap-4 items-center"
      >
        <img
          v-if="item.game.thumbnail_url"
          :src="item.game.thumbnail_url"
          :alt="item.game.title"
          class="w-16 h-16 object-cover rounded"
        />
        <div>
          <h2 class="text-lg font-semibold">{{ item.game.title }}</h2>
          <p class="text-sm text-gray-600">
            Žaidėjų: {{ item.game.min_players }}–{{ item.game.max_players }}<br />
            Trukmė: {{ item.game.playtime_minutes }} min
          </p>
        </div>
        <button
          @click="deleteGame(item.game.id)"
          class="ml-2 bg-red-600 text-white px-1 py-0.25 rounded hover:bg-red-700"
        >
          🗑️
        </button>
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
