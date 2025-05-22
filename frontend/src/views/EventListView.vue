<template>
  <div class="bg-gray-50 min-h-screen py-10">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <h1 class="text-3xl font-bold text-gray-800">Renginiai</h1>
        <button
          v-if="userRole === 'organizer'"
          @click="showModal = true"
          class="px-5 py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white rounded-lg hover:from-green-700 hover:to-green-600 shadow-md transition flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Naujas renginys
        </button>
      </div>

      <!-- Patobulinti filtrai -->
      <div class="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 class="text-lg font-semibold text-gray-700 mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          Filtrai
        </h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
          <div>
            <label class="block mb-1 text-sm font-medium text-gray-700">Paieška</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                v-model="filters.search"
                @input="fetchEvents"
                placeholder="Ieškoti pagal pavadinimą..."
                class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <label class="block mb-1 text-sm font-medium text-gray-700">Stalo dydis</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
              </div>
              <select
                v-model="filters.table_size"
                @change="fetchEvents"
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Visi stalai</option>
                <option value="S">Mažas (S)</option>
                <option value="M">Vidutinis (M)</option>
                <option value="L">Didelis (L)</option>
                <option value="XL">Labai didelis (XL)</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <div>
            <label class="block mb-1 text-sm font-medium text-gray-700">Viešumas</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <select
                v-model="filters.visibility"
                @change="fetchEvents"
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Visi viešumai</option>
                <option value="public">🔓 Vieša</option>
                <option value="protected">🔐 Apsaugota</option>
                <option value="private">🚫 Privati</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <div>
            <label class="block mb-1 text-sm font-medium text-gray-700">Renginio diena</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <input
                type="date"
                v-model="filters.start_date"
                @change="fetchEvents"
                class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <label class="block mb-1 text-sm font-medium text-gray-700">Mėnesis</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <select
                v-model="filters.month"
                @change="fetchEvents"
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                :disabled="!!filters.start_date"
                :class="{ 'bg-gray-100 cursor-not-allowed': !!filters.start_date }"
              >
                <option value="">Visi mėnesiai</option>
                <option v-for="month in months" :key="month.value" :value="month.value">{{ month.label }}</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <div class="flex items-center">
            <label class="flex items-center cursor-pointer">
              <div class="relative">
                <input
                  type="checkbox"
                  v-model="filters.participating"
                  @change="fetchEvents"
                  class="sr-only"
                />
                <div class="block bg-gray-200 w-14 h-7 rounded-full"></div>
                <div class="dot absolute left-1 top-1 bg-white w-5 h-5 rounded-full transition transform"
                     :class="{'translate-x-7 bg-indigo-600': filters.participating}"></div>
              </div>
              <span class="ml-3 text-sm text-gray-700">Tik mano renginiai</span>
            </label>
          </div>
        </div>

        <!-- Papildomos galimybės -->
        <details class="mt-4 bg-indigo-50 rounded-lg p-4 border border-indigo-100">
          <summary class="cursor-pointer font-medium text-indigo-700 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
            </svg>
            Papildomos galimybės
          </summary>
          <div class="mt-3 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2">
            <label v-for="perk in allPerks" :key="perk" class="flex items-center space-x-2 text-sm">
              <input
                type="checkbox"
                :value="perk"
                v-model="filters.perks"
                @change="fetchEvents"
                class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <span>{{ perk }}</span>
            </label>
          </div>
        </details>
      </div>

      <!-- Modalas -->
      <CreateEventModal :show="showModal" @close="showModal = false" @created="fetchEvents" />

      <!-- Renginių skyriai -->
      <div class="space-y-10">
        <!-- Šiandienos renginiai -->
        <div v-if="todayEvents.length" class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="h-2 bg-gradient-to-r from-blue-500 to-blue-600"></div>
          <div class="p-6">
            <div class="flex items-center mb-6">
              <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h2 class="text-2xl font-bold text-blue-700">Šiandienos renginiai</h2>
              <span class="ml-3 bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                {{ todayEvents.length }} renginiai
              </span>
            </div>

            <!-- Čia naudojame EventList komponentą kaip ir anksčiau! -->
            <EventList
              :events="todayEvents"
              highlight="today"
              @go-to="goToEvent"
              @join="joinEvent"
              @deleted="fetchEvents"
            />
          </div>
        </div>

        <!-- Artėjantys renginiai -->
        <div v-if="upcomingEvents.length" class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="h-2 bg-gradient-to-r from-green-500 to-green-600"></div>
          <div class="p-6">
            <div class="flex items-center mb-6">
              <div class="w-10 h-10 rounded-full bg-green-100 text-green-600 flex items-center justify-center mr-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.933 12.8a1 1 0 000-1.6L6.6 7.2A1 1 0 005 8v8a1 1 0 001.6.8l5.333-4z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.933 12.8a1 1 0 000-1.6l-5.333-4A1 1 0 0013 8v8a1 1 0 001.6.8l5.333-4z" />
                </svg>
              </div>
              <h2 class="text-2xl font-bold text-green-700">Artėjantys renginiai</h2>
              <span class="ml-3 bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                {{ upcomingEvents.length }} renginiai
              </span>
            </div>

            <!-- Čia naudojame EventList komponentą kaip ir anksčiau! -->
            <EventList
              :events="upcomingEvents"
              @go-to="goToEvent"
              @join="joinEvent"
              @deleted="fetchEvents"
            />
          </div>
        </div>

        <!-- Praėję renginiai -->
        <div v-if="pastEvents.length" class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="h-2 bg-gradient-to-r from-gray-400 to-gray-500"></div>
          <div class="p-6">
            <div class="flex items-center cursor-pointer mb-6" @click="showPastEvents = !showPastEvents">
              <div class="w-10 h-10 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center mr-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 class="text-2xl font-bold text-gray-600">Praėję renginiai</h2>
              <span class="ml-3 bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-medium">
                {{ pastEvents.length }} renginiai
              </span>
              <button class="ml-auto bg-gray-200 text-gray-700 w-8 h-8 rounded-full flex items-center justify-center hover:bg-gray-300 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" :class="{'rotate-180': showPastEvents}">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>

            <!-- Atvaizduojame praėjusius renginius, jeigu jie yra rodomi -->
            <EventList
              v-if="showPastEvents"
              :events="pastEvents"
              past
              @go-to="goToEvent"
              @join="joinEvent"
              @deleted="fetchEvents"
            />
          </div>
        </div>

        <!-- Kai nėra renginių -->
        <div v-if="!todayEvents.length && !upcomingEvents.length && !pastEvents.length" class="bg-white rounded-xl shadow-md p-10 text-center">
          <div class="flex flex-col items-center justify-center py-6">
            <div class="text-6xl mb-4">📅</div>
            <h3 class="text-xl font-semibold text-gray-700 mb-2">Nerasta renginių</h3>
            <p class="text-gray-500 max-w-md mx-auto">
              Nerasta renginių, atitinkančių pasirinktus filtrus. Pabandykite pakeisti filtrus arba sukurkite naują renginį.
            </p>

            <button
              v-if="userRole === 'organizer'"
              @click="showModal = true"
              class="mt-6 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg hover:from-indigo-700 hover:to-blue-700 shadow-md transition flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Sukurti naują renginį
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Toggle button styling */
.dot {
  transition: all 0.3s ease-in-out;
}
</style>

<style scoped>
/* Toggle button styling */
.dot {
  transition: all 0.3s ease-in-out;
}
</style>


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
    const res = await axios.post(`/events/${eventId}/join/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (res.status === 201) {
      alert('🛡️ Prašymas prisijungti išsiųstas organizatoriui.');
    } else {
      alert('✅ Prisijungei prie renginio!');
    }

    fetchEvents();
  } catch (error) {
    console.error('Nepavyko prisijungti prie renginio:', error);
    alert('❌ Klaida jungiantis prie renginio.');
  }
};


onMounted(() => {
  fetchEvents()
})
</script>
