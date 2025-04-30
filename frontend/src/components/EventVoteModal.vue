<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-xl max-w-6xl w-full relative max-h-[90vh] overflow-y-auto">
      <h2 class="text-xl font-bold mb-4">🗳️ Sudėliok savo norimų žaisti žaidimų eilę</h2>

      <!-- Filtrai -->
      <div class="mb-4 flex flex-wrap gap-3 items-center">
        <input v-model="filterQuery" placeholder="🔍 Pavadinimas..." class="border rounded px-3 py-1 text-sm w-60" />

        <div class="flex items-center gap-1 text-sm">
          ⏱️ <input v-model.number="filterPlaytimeMin" type="number" class="w-16 border rounded px-1 py-0.5" placeholder="min" />
          –
          <input v-model.number="filterPlaytimeMax" type="number" class="w-16 border rounded px-1 py-0.5" placeholder="max" />
        </div>

        <div class="flex items-center gap-1 text-sm">
          🧠 <input v-model.number="filterComplexityMin" type="number" class="w-16 border rounded px-1 py-0.5" placeholder="min" />
          –
          <input v-model.number="filterComplexityMax" type="number" class="w-16 border rounded px-1 py-0.5" placeholder="max" />
        </div>

        <div class="flex items-center gap-1 text-sm">
          ⭐ <input v-model.number="filterRatingMin" type="number" class="w-16 border rounded px-1 py-0.5" placeholder="min" />
          –
          <input v-model.number="filterRatingMax" type="number" class="w-16 border rounded px-1 py-0.5" placeholder="max" />
        </div>

        <div class="flex items-center gap-1 text-sm">
          👥 <input v-model.number="filterBestPlayers" type="number" class="w-16 border rounded px-1 py-0.5" placeholder="#" />
        </div>

        <select v-model="filterMechanic" class="border rounded px-2 py-1 text-sm">
          <option value="">🎮 Visi mechanikos</option>
          <option v-for="m in allMechanics" :key="m" :value="m">{{ m }}</option>
        </select>

        <select v-model="filterCategory" class="border rounded px-2 py-1 text-sm">
          <option value="">🎭 Visos temos</option>
          <option v-for="c in allCategories" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>

      <div v-if="sortedFilteredGames.length === 0" class="text-center text-gray-600">
        ❌ Pagal pasirinktus filtrus žaidimų nerasta!
      </div>

      <!-- PATAISYTA DRAGGABLE DALIS -->
      <draggable  v-model="displayGames"
                  item-key="id"
                  handle=".drag-handle"
                  class="space-y-2">
        <template #item="{ element, index }">
          <div class="flex items-start gap-3 border rounded px-3 py-2 bg-gray-50">
            <span class="drag-handle cursor-move mt-2">☰</span>
            <img :src="element.game.thumbnail_url" alt="thumbnail" class="w-16 h-16 object-cover rounded" />
            <div class="flex-1">
              <p class="font-semibold text-base">{{ element.game.title }}</p>
              <p class="text-sm text-gray-600">
                👥 {{ element.game.min_players }}–{{ element.game.max_players }} žaidėjai
                <span v-if="element.game.best_player_count" class="text-green-700 font-medium">
                  (🎯 Geriausia su {{ element.game.best_player_count }})
                </span>
                • ⏱️ {{ element.game.playtime_minutes }} min
              </p>
              <p class="text-sm text-gray-600">
                ⭐ Reitingas: {{ element.game.average_rating?.toFixed(2) ?? '–' }} •
                🧠 Kompleksiškumas: {{ element.game.complexity?.toFixed(2) ?? '–' }} •
                🗣️ Kalbos priklausomybė: {{ element.game.language_dependence ?? '–' }}
              </p>
              <p class="text-sm text-gray-600">
                🎭 Temos: {{ element.game.categories?.join(', ') || '–' }}<br />
                🧩 Mechanikos: {{ element.game.mechanics?.join(', ') || '–' }}
              </p>
            </div>
            <div class="w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-xs flex items-center justify-center mt-2">
              {{ index + 1 }}
            </div>
          </div>
        </template>
      </draggable>

      <div class="flex justify-end mt-6 gap-3">
        <button @click="$emit('close')" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Atšaukti</button>
        <button
            @click="submitVotes"
            :disabled="displayGames.length === 0"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          🗳️ Balsuoti
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import draggable from 'vuedraggable'
import axios from '@/api/axios'
import { useRoute } from 'vue-router'

const props = defineProps<{ visible: boolean }>()
const emit = defineEmits(['close', 'voted'])
const route = useRoute()

const games = ref<any[]>([])
const displayGames = ref<any[]>([])

// Filtrai
const filterQuery = ref('')
const filterMechanic = ref('')
const filterCategory = ref('')
const filterPlaytimeMin = ref<number | null>(null)
const filterPlaytimeMax = ref<number | null>(null)
const filterComplexityMin = ref<number | null>(null)
const filterComplexityMax = ref<number | null>(null)
const filterRatingMin = ref<number | null>(null)
const filterRatingMax = ref<number | null>(null)
const filterBestPlayers = ref<number | null>(null)

const allMechanics = ref<string[]>([])
const allCategories = ref<string[]>([])

const fetchAvailableGames = async () => {
  try {
    const res = await axios.get(`/events/${route.params.id}/available-games/`)
    games.value = res.data

    const mechanicsSet = new Set<string>()
    const categoriesSet = new Set<string>()

    games.value.forEach((item) => {
      item.game.mechanics?.forEach((m: string) => mechanicsSet.add(m))
      item.game.categories?.forEach((c: string) => categoriesSet.add(c))
    })

    allMechanics.value = Array.from(mechanicsSet).sort()
    allCategories.value = Array.from(categoriesSet).sort()

    // Pradinė duomenų užpildymas
    updateDisplayGames()
  } catch (err) {
    console.error('Klaida gaunant žaidimų sąrašą:', err)
  }
}

// Filtruoti
const filteredGames = computed(() =>
    games.value.filter((item) => {
      const g = item.game
      const titleMatch = g.title.toLowerCase().includes(filterQuery.value.toLowerCase())
      const mechanicMatch = !filterMechanic.value || g.mechanics?.includes(filterMechanic.value)
      const categoryMatch = !filterCategory.value || g.categories?.includes(filterCategory.value)
      const playtimeMatch =
          (!filterPlaytimeMin.value || g.playtime_minutes >= filterPlaytimeMin.value) &&
          (!filterPlaytimeMax.value || g.playtime_minutes <= filterPlaytimeMax.value)
      const complexityMatch =
          (!filterComplexityMin.value || g.complexity >= filterComplexityMin.value) &&
          (!filterComplexityMax.value || g.complexity <= filterComplexityMax.value)
      const ratingMatch =
          (!filterRatingMin.value || g.average_rating >= filterRatingMin.value) &&
          (!filterRatingMax.value || g.average_rating <= filterRatingMax.value)

      const bestPlayersValue = filterBestPlayers.value
      const bestPlayersMatch = !bestPlayersValue || (
          g.best_player_count === String(bestPlayersValue) ||
          (g.min_players <= bestPlayersValue && g.max_players >= bestPlayersValue)
      )

      return titleMatch && mechanicMatch && categoryMatch && playtimeMatch && complexityMatch && ratingMatch && bestPlayersMatch
    })
)

const sortedFilteredGames = computed(() => {
  const bestPlayersValue = filterBestPlayers.value
  if (!bestPlayersValue) return filteredGames.value

  const best = filteredGames.value.filter(g => g.game.best_player_count === String(bestPlayersValue))
  const rest = filteredGames.value.filter(g => g.game.best_player_count !== String(bestPlayersValue))
  return [...best, ...rest]
})

// Atnaujinti rodomų žaidimų sąrašą kai pasikeičia filtrai
const updateDisplayGames = () => {
  // Sukuriame duomenų kopiją su unikaliais ID, kad draggable komponentas
  // galėtų teisingai identifikuoti elementus
  displayGames.value = sortedFilteredGames.value.map((game, index) => ({
    ...game,
    id: game.game.id // naudojame game.id kaip unikalų identifikatorių
  }))
}

// Stebime filtrus ir atnaujiname rodomų žaidimų sąrašą
watch([
  filterQuery, filterMechanic, filterCategory,
  filterPlaytimeMin, filterPlaytimeMax,
  filterComplexityMin, filterComplexityMax,
  filterRatingMin, filterRatingMax,
  filterBestPlayers
], updateDisplayGames)

const submitVotes = async () => {
  const votes = displayGames.value.map((item, index) => ({
    game_id: item.game.id,
    rank: index + 1,
  }))

  try {
    await axios.post(`/events/${route.params.id}/vote/`, { votes })
    alert('✅ Balsas išsaugotas!')
    emit('voted')
    emit('close')
  } catch (err) {
    console.error('Balsavimo klaida:', err)
    alert('❌ Nepavyko išsaugoti balsavimo.')
  }
}

const refresh = async () => {
  await fetchAvailableGames()
}
defineExpose({ refresh })
onMounted(fetchAvailableGames)
</script>
