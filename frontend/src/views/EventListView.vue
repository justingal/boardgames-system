<template>
  <div class="max-w-5xl mx-auto px-4 py-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Renginiai</h1>
      <button
        v-if="userRole === 'organizer'"
        @click="showModal = true"
        class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        + Naujas renginys
      </button>
    </div>

    <!-- Patobulinti filtrai -->
    <div class="bg-white shadow p-4 rounded-lg mb-6 flex flex-wrap gap-4 items-center">
      <input
        v-model="filters.search"
        @input="fetchEvents"
        placeholder="Ieškoti pagal pavadinimą..."
        class="border border-gray-300 rounded px-3 py-2"
      />
      <select v-model="filters.table_size" @change="fetchEvents" class="border border-gray-300 rounded px-3 py-2">
        <option value="">Visi stalai</option>
        <option value="S">S</option>
        <option value="M">M</option>
        <option value="L">L</option>
        <option value="XL">XL</option>
      </select>

      <input
        type="date"
        v-model="filters.start_date"
        @change="fetchEvents"
        class="border border-gray-300 rounded px-3 py-2"
        placeholder="Renginio diena"
      />

      <!-- Naujas mėnesių filtras -->
      <select v-model="filters.month" @change="fetchEvents" class="border border-gray-300 rounded px-3 py-2">
        <option value="">Visi mėnesiai</option>
        <option v-for="month in months" :key="month.value" :value="month.value">{{ month.label }}</option>
      </select>

      <select v-model="filters.visibility" @change="fetchEvents" class="border border-gray-300 rounded px-3 py-2">
        <option value="">Visi viešumai</option>
        <option value="public">Vieša</option>
        <option value="protected">Apsaugota</option>
        <option value="private">Privati</option>
      </select>

      <!-- Renginiai, kuriuose dalyvauju -->
      <label class="flex items-center space-x-2 text-sm">
        <input
          type="checkbox"
          v-model="filters.participating"
          @change="fetchEvents"
          class="rounded text-blue-600"
        />
        <span>Tik renginiai, kuriuose dalyvauju</span>
      </label>

      <details class="w-full md:w-auto">
        <summary class="cursor-pointer flex items-center text-blue-600 font-medium">
          <span class="inline-block w-4 h-4 mr-1">🔍</span> Papildomos galimybės
        </summary>
        <div class="mt-2 flex flex-wrap gap-2">
          <label v-for="perk in allPerks" :key="perk" class="flex items-center space-x-1 text-sm">
            <input type="checkbox" :value="perk" v-model="filters.perks" @change="fetchEvents" />
            <span>{{ perk }}</span>
          </label>
        </div>
      </details>
    </div>

    <!-- Modalas -->
    <CreateEventModal :show="showModal" @close="showModal = false" @created="fetchEvents" />
    <div v-if="pastEvents.length">
      <div class="flex items-center cursor-pointer mb-2" @click="showPastEvents = !showPastEvents">
        <h2 class="text-2xl font-bold text-gray-600">🕓 Praėję renginiai ({{ pastEvents.length }})</h2>
        <button class="ml-2 text-gray-500">
          <span v-if="showPastEvents">▲</span>
          <span v-else>▼</span>
        </button>
      </div>
      <EventList
        v-if="showPastEvents"
        :events="pastEvents"
        past
        @go-to="goToEvent"
        @join="joinEvent"
        @deleted="fetchEvents"
      />
    </div>
    <!-- Renginių skyriai -->
    <div class="space-y-8">
      <div v-if="todayEvents.length">
        <h2 class="text-2xl font-bold text-blue-700">📅 Šiandienos renginiai ({{ todayEvents.length }})</h2>
        <EventList
          :events="todayEvents"
          highlight="today"
          @go-to="goToEvent"
          @join="joinEvent"
          @deleted="fetchEvents"
        />
      </div>

      <div v-if="upcomingEvents.length">
        <h2 class="text-2xl font-bold text-green-700">🔜 Artėjantys renginiai ({{ upcomingEvents.length }})</h2>
        <EventList
          :events="upcomingEvents"
          @go-to="goToEvent"
          @join="joinEvent"
          @deleted="fetchEvents"
        />
      </div>


      <div v-if="!todayEvents.length && !upcomingEvents.length && !pastEvents.length" class="text-center py-8 text-gray-500">
        Nerasta renginių, atitinkančių pasirinktus filtrus.
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '../api/axios'
import { jwtDecode } from 'jwt-decode'
import CreateEventModal from '../components/CreateEventModal.vue'
import router from "@/router/index.js"
import EventList from "@/components/EventList.vue"

const showModal = ref(false)
const showPastEvents = ref(false) // Buvusių renginių rodymo kontrolė
const events = ref([])

const token = localStorage.getItem('access')
let userRole = ref(null)

const todayEvents = ref([])
const upcomingEvents = ref([])
const pastEvents = ref([])

if (token) {
  const decoded = jwtDecode(token)
  userRole.value = decoded.role
}

// Patobulinti filtrai su naujais laukais
const filters = ref({
  search: '',
  table_size: '',
  visibility: '',
  perks: [],
  participating: false, // Naujas filtras - renginiai, kuriuose dalyvauju
  month: getCurrentMonthValue() // Pradinis mėnuo - dabartinis
})

// Gaunama dabartinio mėnesio reikšmė
function getCurrentMonthValue() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
}

// Mėnesių sąrašas (±6 mėnesiai nuo dabartinio)
const months = computed(() => {
  const result = []
  const now = new Date()

  // Lietuviški mėnesių pavadinimai
  const monthNames = [
    'Sausis', 'Vasaris', 'Kovas', 'Balandis', 'Gegužė', 'Birželis',
    'Liepa', 'Rugpjūtis', 'Rugsėjis', 'Spalis', 'Lapkritis', 'Gruodis'
  ]

  // Generuojame mėnesių sąrašą (2 atgal ir 9 į priekį)
  for (let i = -2; i <= 9; i++) {
    const month = new Date(now.getFullYear(), now.getMonth() + i, 1)
    const value = `${month.getFullYear()}-${String(month.getMonth() + 1).padStart(2, '0')}`
    const label = `${monthNames[month.getMonth()]} ${month.getFullYear()}`

    result.push({ value, label })
  }

  return result
})

const allPerks = [
  'Atskira salė',
  'Leidžiama triukšmauti',
  'Prieiga prie virtuvėlės',
  'Projektorius',
  'Oro kondicionierius',
  'Didelis stalų kiekis',
  'Nemokamas parkingas',
  'Galima užsakyti maistą',
  'Uždara erdvė',
  'Žaidimų biblioteka'
]

const tableSizeLabels = {
  S: 'Mažas (2 žmonės) ~ 80x80cm',
  M: 'Vidutinis (4 žmonės) ~ 120x80cm',
  L: 'Didelis (6–8 žmonės) ~ 180x90cm',
  XL: 'Labai didelis (8–10 žmonių) ~ 200x100cm'
}

const privacyLabels = {
  public: '🔓 Vieša – matoma visiems',
  protected: '🔐 Apsaugota – matoma, bet reikia leidimo jungtis',
  private: '🚫 Privati – nematoma, tik pakviestiesiems'
}

const getOrganizerNames = (event) => {
  if (!event.organizers || !event.organizers.length) return ''
  return event.organizers.map(org => org.username).join(', ')
}

const formatDateTime = (datetimeStr) => {
  if (!datetimeStr) return ''
  const date = new Date(datetimeStr)
  return date.toLocaleString('lt-LT', {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'UTC'
  })
}

// Navigacija į renginio puslapį
const goToEvent = (eventId) => {
  router.push(`/events/${eventId}`)
}

// Renginių gavimas
const fetchEvents = async () => {
  try {
    const params = {}

    if (filters.value.search) params.search = filters.value.search
    if (filters.value.table_size) params.table_size = filters.value.table_size
    if (filters.value.visibility) params.visibility = filters.value.visibility
    if (filters.value.perks.length) params.perks = filters.value.perks.join(',')

    if (filters.value.start_date) {
      params.start_date = filters.value.start_date
      // Jei pasirinkta konkreti diena, mėnesio filtrą ignoruojame
      delete params.year
      delete params.month
    }
    else if (filters.value.month) {
      const [year, month] = filters.value.month.split('-')
      params.year = year
      params.month = month
    }

    // Nauji filtrai - svarbu perduoti kaip boolean reikšmę tekstiniame parametre
    params.is_participant = filters.value.participating ? 'true' : 'false'


    // Change the endpoint to use grouped-events
    const response = await axios.get('/events/grouped/', {
      headers: { Authorization: `Bearer ${token}` },
      params
    })

    // Update to work with the new response format
    todayEvents.value = response.data.today || []
    upcomingEvents.value = response.data.upcoming || []
    pastEvents.value = response.data.past || []

  } catch (error) {
    console.error('Nepavyko gauti renginių:', error)
  }
}

// Prisijungimas prie renginio
const joinEvent = async (eventId) => {
  try {
    await axios.post(`/events/${eventId}/join/`, {}, {
      headers: {Authorization: `Bearer ${token}`}
    })
    alert('Prisijungei prie renginio!')
    fetchEvents()
  } catch (error) {
    console.error('Nepavyko prisijungti prie renginio:', error)
  }
}

onMounted(() => {
  fetchEvents()
})
</script>
