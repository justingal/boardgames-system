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

    <div class="bg-white shadow p-4 rounded-lg mb-6 flex flex-wrap gap-4 items-center">
      <!-- Paieška -->
      <input
        v-model="filters.search"
        @input="fetchEvents"
        placeholder="Ieškoti pagal pavadinimą..."
        class="border border-gray-300 rounded px-3 py-2"
      />

      <!-- Stalo dydis -->
      <select v-model="filters.table_size" @change="fetchEvents" class="border border-gray-300 rounded px-3 py-2">
        <option value="">Visi stalai</option>
        <option value="S">S</option>
        <option value="M">M</option>
        <option value="L">L</option>
        <option value="XL">XL</option>
      </select>

      <!-- Pradžios data -->
      <input
        type="date"
        v-model="filters.start_date"
        @change="fetchEvents"
        class="border border-gray-300 rounded px-3 py-2"
      />

      <!-- Viešumas -->
      <select v-model="filters.visibility" @change="fetchEvents" class="border border-gray-300 rounded px-3 py-2">
        <option value="">Visi viešumai</option>
        <option value="public">Vieša</option>
        <option value="protected">Apsaugota</option>
        <option value="private">Privati</option>
      </select>

      <!-- PERK'ai -->
      <div class="flex flex-wrap gap-2">
        <label v-for="perk in allPerks" :key="perk" class="flex items-center space-x-1 text-sm">
          <input type="checkbox" :value="perk" v-model="filters.perks" @change="fetchEvents" />
          <span>{{ perk }}</span>
        </label>
      </div>
    </div>


    <CreateEventModal :show="showModal" @close="showModal = false" @created="fetchEvents" />

    <div class="space-y-4">
      <div
        v-for="event in events"
        :key="event.id"
        class="border rounded-lg p-4 bg-white shadow-sm"
      >
        <h2 class="text-xl font-bold mb-2">{{ event.title }}</h2>
        <p class="text-gray-600 mb-2">{{ event.description }}</p>


        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-800"><span class="font-semibold">Adresas:</span> {{ event.address }}</p>
            <p class="text-sm text-gray-800"><span class="font-semibold">Stalo dydis:</span> {{ tableSizeLabels[event.table_size] }}</p>

            <!-- Organizatoriaus informacija su žalia žyme, jei laisvas ir pirmas prisijungęs tampa organizatoriumi -->
            <div v-if="event.first_player_is_organizer && event.players_count === 0"
                 class="mt-2 mb-2 py-1 px-3 bg-green-100 text-green-800 rounded-full inline-block text-sm font-medium">
              🟢 Laisvas - narių 0 - tapk organizatoriumi!
            </div>
            <p v-else class="text-sm text-gray-800">
              <span class="font-semibold">Dalyviai:</span> {{ event.players_count }}
              <span v-if="event.organizers && event.organizers.length">
                (Organizatorius: {{ getOrganizerNames(event) }})
              </span>
            </p>

            <p class="text-sm text-gray-800"><span class="font-semibold">Viešumas:</span> {{ privacyLabels[event.visibility] }}</p>
          </div>

          <div>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Pradžia:</span>
              {{ formatDateTime(event.start_time) }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Pabaiga:</span>
              {{ formatDateTime(event.end_time) }}
            </p>
            <p class="text-sm text-gray-800" v-if="event.perks">
              <span class="font-semibold">Papildomos galimybės:</span> {{ event.perks }}
            </p>

            <!-- Prisijungimo ar perėjimo mygtukas -->
            <div class="mt-4">
              <button
                v-if="event.is_participant"
                @click="goToEvent(event.id)"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Eiti į renginį
              </button>
              <button
                v-else
                @click="joinEvent(event.id)"
                class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                {{ event.first_player_is_organizer && event.players_count === 0 ? 'Tapti organizatoriumi' : 'Prisijungti' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/axios'
import { jwtDecode } from 'jwt-decode'
import CreateEventModal from '../components/CreateEventModal.vue'
import router from "@/router/index.js";

const showModal = ref(false)
const events = ref([])

const token = localStorage.getItem('access')
let userRole = null

if (token) {
  const decoded = jwtDecode(token)
  userRole = decoded.role
}

const filters = ref({
  search: '',
  table_size: '',
  start_date: '',
  visibility: '',
  perks: []
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

// Naujas metodas organizatorių vardams gauti
const getOrganizerNames = (event) => {
  if (!event.organizers || !event.organizers.length) return '';
  return event.organizers.map(org => org.username).join(', ');
}

const formatDateTime = (datetimeStr) => {
  if (!datetimeStr) return '';

  // Sukuriame datą iš ISO string
  const date = new Date(datetimeStr);

  // Formatuojame pagal vietinę laiko juostą
  const options = {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'UTC'  // Tai leis rodyti laiką taip, kaip jis buvo įvestas
  };

  return date.toLocaleString('lt-LT', options);
}
const goToEvent = (eventId) => {
  router.push(`/events/${eventId}`)
}
const fetchEvents = async () => {
  try {
    const params = {}

    if (filters.value.search) params.search = filters.value.search
    if (filters.value.table_size) params.table_size = filters.value.table_size
    if (filters.value.start_date) params.start_date = filters.value.start_date
    if (filters.value.visibility) params.visibility = filters.value.visibility
    if (filters.value.perks.length) params.perks = filters.value.perks.join(',')

    const response = await axios.get('/events/', {
      headers: {Authorization: `Bearer ${token}`},
      params
    })

    // Surūšiuoti pagal start_time
    events.value = response.data.sort((a, b) => new Date(a.start_time) - new Date(b.start_time))
  } catch (error) {
    console.error('Nepavyko gauti renginių:', error)
  }
}
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


onMounted(fetchEvents)
</script>
