<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
    <div class="bg-white p-6 sm:p-8 rounded-xl shadow-2xl max-w-6xl w-full relative animate-fadeIn max-h-[90vh] overflow-y-auto">
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
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">🗳️ Sudėliok žaidimų eilę</h2>
        <p class="text-gray-500 mt-1">Surikiuok žaidimus pagal tai, kuriuos labiausiai norėtum žaisti</p>
      </div>

      <!-- Filtrai -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <h3 class="font-medium text-gray-900 mb-3">Filtrai:</h3>
        <div class="flex flex-wrap gap-3 items-center">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="filterQuery"
              placeholder="Pavadinimas..."
              class="border rounded-lg pl-10 pr-3 py-2 text-sm w-60 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div class="flex items-center gap-1 text-sm bg-white px-3 py-2 rounded-lg border border-gray-200">
            <div class="group relative">
              <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                Žaidimo trukmė minutėmis
                <div class="tooltip-arrow"></div>
              </div>
            </div>
            <input v-model.number="filterPlaytimeMin" type="number" class="w-16 border rounded px-2 py-1" placeholder="min" />
            –
            <input v-model.number="filterPlaytimeMax" type="number" class="w-16 border rounded px-2 py-1" placeholder="max" />
          </div>

          <div class="flex items-center gap-1 text-sm bg-white px-3 py-2 rounded-lg border border-gray-200">
            <div class="group relative">
              <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12h2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm12-3h2a2 2 0 012 2v8a2 2 0 01-2 2h-2a2 2 0 01-2-2v-8a2 2 0 012-2z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12h2a2 2 0 012 2v5a2 2 0 01-2 2H9a2 2 0 01-2-2v-5a2 2 0 012-2zm8-7h2a2 2 0 012 2v11a2 2 0 01-2 2h-2a2 2 0 01-2-2V7a2 2 0 012-2z" />
              </svg>
              <div class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                Kompleksiškumas: sudėtingumo lygis nuo 1 iki 5
                <div class="tooltip-arrow"></div>
              </div>
            </div>
            <input v-model.number="filterComplexityMin" type="number" class="w-16 border rounded px-2 py-1" placeholder="min" />
            –
            <input v-model.number="filterComplexityMax" type="number" class="w-16 border rounded px-2 py-1" placeholder="max" />
          </div>

          <div class="flex items-center gap-1 text-sm bg-white px-3 py-2 rounded-lg border border-gray-200">
            <div class="group relative">
              <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
              <div class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                BoardGameGeek reitingas, vertinimas nuo 1 iki 10
                <div class="tooltip-arrow"></div>
              </div>
            </div>
            <input v-model.number="filterRatingMin" type="number" class="w-16 border rounded px-2 py-1" placeholder="min" />
            –
            <input v-model.number="filterRatingMax" type="number" class="w-16 border rounded px-2 py-1" placeholder="max" />
          </div>

          <div class="flex items-center gap-1 text-sm bg-white px-3 py-2 rounded-lg border border-gray-200">
            <div class="group relative">
              <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <div class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                Optimaliausias žaidėjų skaičius
              </div>
            </div>
            <input v-model.number="filterBestPlayers" type="number" class="w-16 border rounded px-2 py-1" placeholder="#" />
          </div>

          <select v-model="filterMechanic" class="border rounded-lg px-3 py-2 text-sm bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
            <option value="">🎮 Visi mechanikos</option>
            <option v-for="m in allMechanics" :key="m" :value="m">{{ m }}</option>
          </select>

          <select v-model="filterCategory" class="border rounded-lg px-3 py-2 text-sm bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
            <option value="">🎭 Visos temos</option>
            <option v-for="c in allCategories" :key="c" :value="c">{{ c }}</option>
          </select>

          <select v-model="filterLanguage" class="border rounded-lg px-3 py-2 text-sm bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
            <option value="">🗣️ Visi kalbos lygiai</option>
            <option v-for="(label, key) in languageOptions" :key="key" :value="key">
              {{ label }}
            </option>
          </select>
        </div>
      </div>

      <div v-if="sortedFilteredGames.length === 0" class="py-12 text-center">
        <div class="w-20 h-20 mx-auto mb-4 flex items-center justify-center rounded-full bg-gray-100">
          <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-700 mb-1">❌ Pagal pasirinktus filtrus žaidimų nerasta!</h3>
        <p class="text-gray-500">Pabandykite pakeisti filtrus, kad rastumėte žaidimų.</p>
      </div>

      <!-- DRAGGABLE DALIS -->
      <div v-else class="mb-6">
        <p class="mb-2 text-sm text-gray-600 font-medium flex items-center">
          <svg class="w-5 h-5 mr-1 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
          </svg>
          Vilkite žaidimus, kad sudarytumėte norimą eilę:
        </p>

        <draggable
          v-model="displayGames"
          item-key="id"
          handle=".drag-handle"
          class="space-y-3"
          @end="updateRanks"
        >
          <template #item="{ element, index }">
            <div class="flex items-start gap-3 border rounded-lg px-4 py-3 bg-white shadow-sm hover:shadow-md transition duration-200">
              <div class="flex items-center justify-center h-full">
                <div class="flex flex-col items-center">
                  <div class="cursor-move drag-handle">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
                    </svg>
                  </div>
                  <div class="relative mt-1">
                    <input
                      type="number"
                      v-model.number="element.rank"
                      min="1"
                      :max="displayGames.length"
                      class="w-12 h-8 rounded-full bg-indigo-100 text-indigo-700 text-xs text-center focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      @blur="handleRankChange(element.game.id, element.rank)"
                      @keydown.enter="handleRankChange(element.game.id, element.rank)"
                    />
                  </div>
                </div>
              </div>

              <div class="w-16 h-16 flex-shrink-0 rounded-md overflow-hidden border border-gray-200">
                <img :src="element.game.thumbnail_url" alt="thumbnail" class="w-full h-full object-cover" />
              </div>

              <div class="flex-1">
                <p class="font-semibold text-gray-900">{{ element.game.title }}</p>
                <div class="mt-1 text-sm text-gray-600 grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-1">
                  <p class="flex items-center">
                    <div class="group relative inline-flex items-center">
                      <svg class="w-4 h-4 mr-1 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                      <div class="absolute bottom-full left-0 mb-1 hidden group-hover:block bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap z-10">
                        Žaidėjų skaičius: nuo {{ element.game.min_players }} iki {{ element.game.max_players }}
                      </div>
                      {{ element.game.min_players }}–{{ element.game.max_players }} žaidėjai
                      <span v-if="element.game.best_player_count" class="inline-flex items-center ml-1 text-green-600 font-medium">
                        (🎯 {{ element.game.best_player_count }})
                      </span>
                    </div>
                  </p>
                  <p class="flex items-center">
                    <div class="group relative inline-flex items-center">
                      <svg class="w-4 h-4 mr-1 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div class="absolute bottom-full left-0 mb-1 hidden group-hover:block bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap z-10">
                        Partijos trukmė minutėmis
                      </div>
                      {{ element.game.playtime_minutes }} min
                    </div>
                  </p>
                  <p class="flex items-center">
                    <div class="group relative inline-flex items-center">
                      <svg class="w-4 h-4 mr-1 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                      </svg>
                      <div class="absolute bottom-full left-0 mb-1 hidden group-hover:block bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap z-10">
                        BoardGameGeek reitingas: {{ element.game.average_rating?.toFixed(2) ?? '–' }}/10
                      </div>
                      {{ element.game.average_rating?.toFixed(2) ?? '–' }}
                    </div>
                  </p>
                  <p class="flex items-center">
                    <div class="group relative inline-flex items-center">
                      <svg class="w-4 h-4 mr-1 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12h2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm12-3h2a2 2 0 012 2v8a2 2 0 01-2 2h-2a2 2 0 01-2-2v-8a2 2 0 012-2z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12h2a2 2 0 012 2v5a2 2 0 01-2 2H9a2 2 0 01-2-2v-5a2 2 0 012-2zm8-7h2a2 2 0 012 2v11a2 2 0 01-2 2h-2a2 2 0 01-2-2V7a2 2 0 012-2z" />
                      </svg>
                      <div class="absolute bottom-full left-0 mb-1 hidden group-hover:block bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap z-10">
                        Kompleksiškumas: {{ element.game.complexity?.toFixed(2) ?? '–' }}/5
                      </div>
                      {{ element.game.complexity?.toFixed(2) ?? '–' }}
                    </div>
                  </p>
                </div>
                <div class="mt-1">
                  <p class="text-xs text-gray-500">
                    <span class="inline-flex items-center bg-gray-100 px-2 py-0.5 rounded text-gray-700 mr-1">
                      🗣️ {{ localizeLanguageDependence(element.game.language_dependence) }}
                    </span>
                  </p>
                  <p class="text-xs text-gray-500 mt-1 line-clamp-1">
                    <span class="text-gray-600">🎭:</span> {{ element.game.categories?.join(', ') || '–' }}
                  </p>
                  <p class="text-xs text-gray-500 mt-0.5 line-clamp-1">
                    <span class="text-gray-600">🧩:</span> {{ element.game.mechanics?.join(', ') || '–' }}
                  </p>
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>

      <div class="flex justify-end mt-6 gap-3 border-t border-gray-200 pt-4">
        <button
          @click="$emit('close')"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition shadow-sm flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          Atšaukti
        </button>
        <button
          @click="submitVotes"
          :disabled="displayGames.length === 0"
          :class="displayGames.length === 0 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-indigo-700'"
          class="px-5 py-2 bg-indigo-600 text-white rounded-lg transition shadow-sm flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          🗳️ Balsuoti
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
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
const filterLanguage = ref("") // Aprašome čia prieš naudojimą
const filterPlaytimeMin = ref<number | null>(null)
const filterPlaytimeMax = ref<number | null>(null)
const filterComplexityMin = ref<number | null>(null)
const filterComplexityMax = ref<number | null>(null)
const filterRatingMin = ref<number | null>(null)
const filterRatingMax = ref<number | null>(null)
const filterBestPlayers = ref<number | null>(null)

const allMechanics = ref<string[]>([])
const allCategories = ref<string[]>([])

// Kalbos teksto vertimai
const languageOptions: Record<string, string> = {
  "No necessary in-game text": "Kalbos nereikia",
  "Some necessary text - easily memorized or small crib sheet": "Mažai teksto – lengva įsiminti",
  "Moderate in-game text": "Vidutinis kalbos poreikis",
  "Extensive use of text - massive conversion needed to be playable": "Daug teksto – sunku be vertimo",
  "Unplayable in another language": "Neįmanoma žaisti be kalbos žinių",
}

const languageDependenceMap: Record<string, string> = {
  "No necessary in-game text": "Kalbos nereikia",
  "Some necessary text - easily memorized or small crib sheet": "Mažai teksto – lengva įsiminti",
  "Moderate in-game text": "Vidutinis kalbos poreikis",
  "Extensive use of text - massive conversion needed to be playable": "Daug teksto – žaisti sudėtinga be vertimo",
  "Unplayable in another language": "Neįmanoma žaisti be kalbos žinių",
}

const localizeLanguageDependence = (value: string | null) => {
  if (!value) return "–"
  return languageDependenceMap[value] || value
}

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
    const languageMatch = !filterLanguage.value || g.language_dependence === filterLanguage.value

    const bestPlayersValue = filterBestPlayers.value
    const bestPlayersMatch = !bestPlayersValue || (
      g.best_player_count === String(bestPlayersValue) ||
      (g.min_players <= bestPlayersValue && g.max_players >= bestPlayersValue)
    )

    return titleMatch && mechanicMatch && categoryMatch && playtimeMatch &&
      complexityMatch && ratingMatch && bestPlayersMatch && languageMatch
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
  // galėtų teisingai identifikuoti elementus ir išlaikytų rangą
  displayGames.value = sortedFilteredGames.value.map((game, index) => {
    // Tikriname, ar žaidimas jau buvo displayGames sąraše ir turi rangą
    const existingGame = displayGames.value.find(g => g.game.id === game.game.id)
    return {
      ...game,
      id: game.game.id, // naudojame game.id kaip unikalų identifikatorių
      rank: existingGame?.rank || index + 1 // Išsaugome esamą rangą arba priskiriame naują
    }
  }).sort((a, b) => a.rank - b.rank) // Rikiuojame pagal rangą
}

const handleRankChange = (gameId, newRank) => {
  // Konvertuojame į skaičių ir validuojame
  let rankNumber = parseInt(newRank)
  if (isNaN(rankNumber)) rankNumber = 1
  if (rankNumber < 1) rankNumber = 1
  if (rankNumber > displayGames.value.length) rankNumber = displayGames.value.length

  // Randame žaidimą, kurį norime perkelti
  const gameIndex = displayGames.value.findIndex(g => g.game.id === gameId)
  if (gameIndex === -1) return

  // Jei naujas rangas toks pat kaip dabartinis indeksas + 1, nieko nekeičiame
  if (rankNumber === gameIndex + 1) return

  // Sukuriame naują masyvą, kuriame perkelsime elementą
  const newDisplayGames = [...displayGames.value]

  // Išimame žaidimą iš dabartinės pozicijos
  const [gameToMove] = newDisplayGames.splice(gameIndex, 1)

  // Įdedame jį į naują poziciją (rankNumber-1 nes masyvai prasideda nuo 0)
  newDisplayGames.splice(rankNumber - 1, 0, gameToMove)

  // Atnaujiname displayGames ir priskiriame naujus rangus
  displayGames.value = newDisplayGames.map((game, idx) => ({
    ...game,
    rank: idx + 1
  }))

  // Programiškai perpiešiame UI po šio pakeitimo
  nextTick(() => {
    updateRanks()
  })
}

// Atnaujina visų žaidimų rank savybes
const updateRanks = () => {
  displayGames.value.forEach((game, index) => {
    game.rank = index + 1
  })
}

// Stebime filtrus ir atnaujiname rodomų žaidimų sąrašą
watch([
  filterQuery, filterMechanic, filterCategory, filterLanguage,
  filterPlaytimeMin, filterPlaytimeMax,
  filterComplexityMin, filterComplexityMax,
  filterRatingMin, filterRatingMax,
  filterBestPlayers
], updateDisplayGames)

// Papildoma funkcija pozicijos keitimui per drag-and-drop
const onDragEnd = () => {
  updateRanks() // Atnaujina rangus po vilkimo
}

const submitVotes = async () => {
  // Prieš išsiunčiant balsus, atnauliname rangus pagal esamą eiliškumą
  updateRanks()

  const votes = displayGames.value.map((item) => ({
    game_id: item.game.id,
    rank: item.rank, // Naudojame item.rank vietoje index + 1
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

<style>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tooltip-arrow {
  position: absolute;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 5px 5px 0 5px;
  border-color: #1f2937 transparent transparent transparent;
  bottom: -5px;
  left: 10px;
}
</style>
