<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
    <div class="bg-white p-6 sm:p-8 rounded-xl shadow-2xl max-w-3xl w-full relative animate-fadeIn">
      <div class="absolute top-3 right-3">
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="text-center mb-6">
        <div class="w-14 h-14 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-3">
          <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">Pasirink žaidimus renginiu</h2>
        <p class="text-gray-500 mt-1">Pasirink iš savo kolekcijos žaidimus, kuriuos atsineši į renginį</p>
      </div>

      <div class="mb-6">
        <div class="flex items-center border-b border-gray-200 pb-3 mb-1">
          <div class="flex-1 flex items-center">
            <div class="relative">
              <input type="checkbox" id="selectAll" v-model="selectAll" @change="toggleSelectAll"
                     class="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
              <label for="selectAll" class="ml-2 text-sm font-medium text-gray-700">Pažymėti visus žaidimus</label>
            </div>
            <span class="ml-auto text-sm text-indigo-600 font-medium">
              {{ selectedGameIds.length }} iš {{ games.length }} pasirinkta
            </span>
          </div>
        </div>

        <div class="relative">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Ieškoti žaidimų..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg mb-3 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
          <div class="absolute left-3 top-2.5 text-gray-400">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        <div class="max-h-[50vh] overflow-y-auto space-y-2 pr-1" style="scrollbar-width: thin">
          <div v-for="item in filteredGames" :key="item.id"
               class="flex items-center gap-3 border rounded-lg px-4 py-3 hover:bg-gray-50 transition group"
               :class="{'bg-indigo-50 border-indigo-200': selectedGameIds.includes(item.game.id)}">
            <div class="flex items-center h-full">
              <input type="checkbox" v-model="selectedGameIds" :value="item.game.id"
                     class="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
            </div>
            <div class="w-16 h-16 flex-shrink-0 rounded-md overflow-hidden border border-gray-200">
              <img :src="item.game.thumbnail_url" alt="thumbnail" class="w-full h-full object-cover" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-semibold text-gray-900 truncate">{{ item.game.title }}</p>
              <div class="flex gap-3 text-sm text-gray-600 flex-wrap">
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  {{ item.game.min_players }}–{{ item.game.max_players }}
                </span>
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ item.game.playtime_minutes }} min
                </span>
              </div>
            </div>
            <div class="opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                @click="toggleGame(item.game.id)"
                :class="selectedGameIds.includes(item.game.id) ? 'text-indigo-600' : 'text-gray-400'"
                class="p-1 hover:text-indigo-800 transition"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="selectedGameIds.includes(item.game.id)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
              </button>
            </div>
          </div>

          <div v-if="filteredGames.length === 0" class="py-8 text-center text-gray-500">
            <svg class="w-12 h-12 mx-auto text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p>Nerasta žaidimų pagal jūsų paiešką.</p>
          </div>
        </div>
      </div>

      <div class="flex justify-between items-center border-t border-gray-200 pt-4">
        <div class="text-sm text-gray-500">
          <span v-if="selectedGameIds.length > 0">
            Pasirinkta: <span class="font-medium text-indigo-600">{{ selectedGameIds.length }}</span> žaidimų
          </span>
        </div>
        <div class="flex gap-3">
          <button @click="$emit('close')" class="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition">
            Atšaukti
          </button>
          <button
            @click="submitImport"
            :disabled="selectedGameIds.length === 0"
            :class="selectedGameIds.length === 0 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-green-600'"
            class="px-5 py-2 bg-green-500 text-white rounded-lg transition shadow-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Importuoti
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import axios from '@/api/axios'
import { useRoute } from 'vue-router'

const props = defineProps<{ visible: boolean }>()
const emit = defineEmits(['close', 'imported'])

const route = useRoute()
const games = ref<any[]>([])
const selectedGameIds = ref<number[]>([])
const selectAll = ref(false)
const searchQuery = ref('')

const fetchUserCollectionGames = async () => {
  try {
    const res = await axios.get(`/events/${route.params.id}/importable-games/`)
    games.value = res.data
  } catch (err) {
    console.error('Klaida gaunant žaidimų kolekciją:', err)
  }
}

const toggleSelectAll = () => {
  selectedGameIds.value = selectAll.value ? games.value.map(item => item.game.id) : []
}

const toggleGame = (gameId: number) => {
  const index = selectedGameIds.value.indexOf(gameId)
  if (index === -1) {
    selectedGameIds.value.push(gameId)
  } else {
    selectedGameIds.value.splice(index, 1)
  }
}

const filteredGames = computed(() => {
  if (!searchQuery.value.trim()) return games.value

  const query = searchQuery.value.toLowerCase().trim()
  return games.value.filter(item =>
    item.game.title.toLowerCase().includes(query)
  )
})

watch(games, () => {
  if (selectAll.value) {
    selectedGameIds.value = games.value.map(item => item.game.id)
  }
})

// Jei searchQuery pasikeičia ir nieko nerandama, atšaukti "select all"
watch(searchQuery, () => {
  if (filteredGames.value.length === 0) {
    selectAll.value = false
  }
})

// Jei selectedGameIds skaičius = visų žaidimų skaičiui, įjungti "select all"
watch(selectedGameIds, (val) => {
  selectAll.value = val.length === games.value.length
})

const submitImport = async () => {
  try {
    await axios.post(`/events/${route.params.id}/import-games/`, {
      game_ids: selectedGameIds.value,
    })
    alert('✅ Žaidimai sėkmingai importuoti į renginį!')
    emit('imported')
    emit('close')
  } catch (err) {
    console.error('Importavimo klaida:', err)
    alert('❌ Nepavyko importuoti žaidimų.')
  }
}

onMounted(fetchUserCollectionGames)
</script>

<style>
.animate-fadeIn {
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
