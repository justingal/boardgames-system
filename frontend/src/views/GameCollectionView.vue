<template>
  <div class="max-w-5xl mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Mano žaidimų kolekcija</h1>

    <!-- Failo importas -->
    <div class="mb-6">
      <label class="block mb-2 font-medium">Įkelti CSV arba JSON failą:</label>

      <!-- Paslėptas failo įvestis -->
      <input
        type="file"
        ref="fileInput"
        accept=".csv,.json"
        @change="onFileChange"
        class="hidden"
      />

      <!-- Mygtukas, kuris atidaro failų pasirinkimo langą -->
      <button
        @click="triggerFileSelect"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Importuoti
      </button>

      <p v-if="message" class="mt-2 text-sm text-gray-700">{{ message }}</p>
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

const collection = ref<GameCollectionItem[]>([])
const file = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const message = ref('')

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
</script>
