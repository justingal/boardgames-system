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
            <p class="text-sm text-gray-800"><span class="font-semibold">Organizacija:</span> {{ event.organization_name }}</p>
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

const showModal = ref(false)
const events = ref([])

const token = localStorage.getItem('access')
let userRole = null

if (token) {
  const decoded = jwtDecode(token)
  userRole = decoded.role
}

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

const formatDateTime = (datetimeStr) => {
  const options = { dateStyle: 'medium', timeStyle: 'short' }
  return new Date(datetimeStr).toLocaleString('lt-LT', options)
}

const fetchEvents = async () => {
  try {
    const response = await axios.get('/events/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    events.value = response.data
  } catch (error) {
    console.error('Nepavyko gauti renginių:', error)
  }
}

onMounted(fetchEvents)
</script>
