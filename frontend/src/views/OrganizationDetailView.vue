<template>
  <div class="max-w-5xl mx-auto px-4 py-6">
    <div v-if="!organization" class="text-center text-gray-500">Kraunama...</div>

    <div v-else>
      <!-- Organizacijos informacija -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold mb-2">{{ organization.name }}</h1>
        <p class="text-gray-600 mb-2">{{ organization.description }}</p>
        <div class="text-sm text-gray-500 space-y-1">
          <p><strong>Miestas:</strong> {{ organization.city }}</p>
          <p><strong>Sukūrė:</strong> {{ organization.created_by }}</p>
          <p><strong>Narių skaičius:</strong> {{ organization.members.length }}</p>
          <p><strong>Viešumo tipas:</strong> {{ privacyLabels[organization.privacy] }}</p>
          <p><strong>Grupė: </strong>
            <span v-if="organization.categories.length > 0">
              {{ organization.categories.map(cat => cat.name).join(', ') }}
            </span>
            <span v-else class="italic text-gray-400">Nenurodyta</span>
          </p>
        </div>
      </div>

      <!-- Organizacijos renginiai -->
      <h2 class="text-2xl font-semibold mb-4">Renginiai</h2>

      <div v-if="organization.events.length === 0" class="text-gray-500">
        Šiuo metu nėra renginių.
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="event in organization.events"
          :key="event.id"
          class="border rounded-lg p-4 bg-white shadow-sm"
        >
          <h2 class="text-xl font-bold mb-2">{{ event.title }}</h2>
          <p class="text-gray-600 mb-2">{{ event.description }}</p>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-800"><span class="font-semibold">Adresas:</span> {{ event.address }}</p>
              <p class="text-sm text-gray-800"><span class="font-semibold">Stalo dydis:</span> {{ tableSizeLabels[event.table_size] }}</p>
              <p class="text-sm text-gray-800"><span class="font-semibold">Organizatorius:</span> {{ event.created_by }}</p>
              <p class="text-sm text-gray-800"><span class="font-semibold">Viešumas:</span> {{ privacyLabels[event.visibility] }}</p>
            </div>

            <div>
              <p class="text-sm text-gray-800"><span class="font-semibold">Pradžia:</span> {{ formatDateTime(event.start_time) }}</p>
              <p class="text-sm text-gray-800"><span class="font-semibold">Pabaiga:</span> {{ formatDateTime(event.end_time) }}</p>
              <p class="text-sm text-gray-800" v-if="event.perks">
                <span class="font-semibold">Papildomos galimybės:</span> {{ event.perks }}
              </p>

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
                  Prisijungti
                </button>
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
import { useRoute, useRouter } from 'vue-router'
import axios from '../api/axios'
import { jwtDecode } from 'jwt-decode'

const route = useRoute()
const router = useRouter()
const organization = ref<any>(null)

const token = localStorage.getItem('access')
let userRole = null

if (token) {
  const decoded = jwtDecode(token)
  userRole = decoded.role
}

const tableSizeLabels: Record<string, string> = {
  S: 'Mažas (2 žmonės) ~ 80x80cm',
  M: 'Vidutinis (4 žmonės) ~ 120x80cm',
  L: 'Didelis (6–8 žmonės) ~ 180x90cm',
  XL: 'Labai didelis (8–10 žmonių) ~ 200x100cm'
}

const privacyLabels: Record<string, string> = {
  public: '🔓 Vieša – matoma visiems',
  protected: '🔐 Apsaugota – matoma, bet reikia leidimo jungtis',
  private: '🚫 Privati – nematoma, tik pakviestiesiems'
}

const formatDateTime = (datetimeStr: string) => {
  const options = { dateStyle: 'medium', timeStyle: 'short' }
  return new Date(datetimeStr).toLocaleString('lt-LT', options)
}

const fetchOrganization = async () => {
  try {
    const orgId = route.params.id
    const response = await axios.get(`/organizations/${orgId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    organization.value = response.data
  } catch (error) {
    console.error('Nepavyko gauti organizacijos:', error)
  }
}

const joinEvent = async (eventId: number) => {
  try {
    await axios.post(`/events/${eventId}/join/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('Prisijungei prie renginio!')
    fetchOrganization()
  } catch (error) {
    console.error('Nepavyko prisijungti prie renginio:', error)
  }
}

const goToEvent = (eventId: number) => {
  router.push(`/events/${eventId}`)
}

onMounted(fetchOrganization)
</script>
