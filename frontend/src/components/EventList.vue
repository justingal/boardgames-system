<template>
  <div class="space-y-4">
    <div
      v-for="event in events"
      :key="event.id"
      class="border rounded-lg overflow-hidden bg-white shadow-sm hover:shadow-md transition duration-300"
      :class="{
        'ring-2 ring-blue-400': highlight === 'today',
        'opacity-60': past
      }"
    >
      <!-- Spalvota viršutinė juosta -->
      <div class="h-2" :class="highlight === 'today' ? 'bg-blue-500' : (past ? 'bg-gray-400' : 'bg-indigo-500')"></div>

      <div class="p-5">
        <div class="flex justify-between items-start mb-3">
          <h2 class="text-xl font-bold text-gray-800">{{ event.title }}</h2>

          <div v-if="event.first_player_is_organizer && event.players_count === 0"
               class="mt-1 py-1 px-3 bg-green-100 text-green-800 rounded-full inline-block text-sm font-medium">
            🟢 Laisvas - narių 0 - tapk organizatoriumi!
          </div>
        </div>

        <p class="text-gray-600 mb-4">{{ event.description }}</p>

        <div class="grid grid-cols-2 gap-6">
          <div class="space-y-2">
            <p class="text-sm text-gray-800">
              <span class="font-semibold inline-flex items-center">
                <span class="mr-1.5 text-indigo-500">📍</span>Adresas:
              </span>
              {{ event.address }}
            </p>

            <p class="text-sm text-gray-800">
              <span class="font-semibold inline-flex items-center">
                <span class="mr-1.5 text-indigo-500">🪑</span>Stalo dydis:
              </span>
              {{ tableSizeLabels[event.table_size] }}
            </p>

            <div v-if="event.first_player_is_organizer && event.players_count === 0"
                 class="mt-2 mb-2 py-1 px-3 bg-green-100 text-green-800 rounded-full inline-block text-sm font-medium">
              🟢 Laisvas - narių 0 - tapk organizatoriumi!
            </div>
            <p v-else class="text-sm text-gray-800">
              <span class="font-semibold inline-flex items-center">
                <span class="mr-1.5 text-indigo-500">👥</span>Dalyviai:
              </span>
              {{ event.players_count }}
              <span v-if="event.organizers && event.organizers.length" class="text-green-600 ml-1">
                (Organizatorius: {{ getOrganizerNames(event) }})
              </span>
            </p>

            <p class="text-sm text-gray-800">
              <span class="font-semibold inline-flex items-center">
                <span class="mr-1.5 text-indigo-500">🔒</span>Viešumas:
              </span>
              {{ privacyLabels[event.visibility] }}
            </p>
          </div>

          <div class="space-y-2">
            <p class="text-sm text-gray-800">
              <span class="font-semibold inline-flex items-center">
                <span class="mr-1.5 text-indigo-500">🕒</span>Pradžia:
              </span>
              {{ formatDateTime(event.start_time) }}
            </p>

            <p class="text-sm text-gray-800">
              <span class="font-semibold inline-flex items-center">
                <span class="mr-1.5 text-indigo-500">✅</span>Pabaiga:
              </span>
              {{ formatDateTime(event.end_time) }}
            </p>

            <p v-if="event.perks" class="text-sm text-gray-800">
              <span class="font-semibold inline-flex items-center">
                <span class="mr-1.5 text-indigo-500">✨</span>Papildomos galimybės:
              </span>
              {{ event.perks }}
            </p>

            <div class="flex items-center justify-between mt-4">
              <button
                v-if="event.created_by === user?.username"
                @click="deleteEvent(event.id)"
                class="px-3 py-1.5 bg-red-100 text-red-600 border border-red-200 rounded-lg hover:bg-red-600 hover:text-white transition-colors flex items-center"
              >
                <span>🗑️ Ištrinti</span>
              </button>

              <div class="ml-auto">
                <button
                  v-if="event.is_participant"
                  @click="$emit('go-to', event.id)"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-sm"
                >
                  Eiti į renginį
                </button>
                <button
                  v-else
                  @click="$emit('join', event.id)"
                  class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 shadow-sm"
                >
                  {{ event.first_player_is_organizer && event.players_count === 0 ? 'Tapti organizatoriumi' : 'Prisijungti' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import axios from '../api/axios'
const props = defineProps({
  events: Array,
  highlight: String,
  past: Boolean
})

const emit = defineEmits(['go-to', 'join', 'deleted'])
const token = localStorage.getItem('access')
const user = ref(null)

// Fetch user once (creator check)
const fetchUser = async () => {
  try {
    const res = await axios.get('/users/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = res.data
  } catch (err) {
    console.error('Nepavyko gauti vartotojo informacijos:', err)
  }
}
fetchUser()

const deleteEvent = async (eventId) => {
  if (!confirm('Ar tikrai nori ištrinti šį renginį?')) return
  try {
    await axios.delete(`/events/${eventId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('Renginys sėkmingai ištrintas!')
    emit('deleted', eventId)
  } catch (error) {
    console.error('Klaida trinant renginį:', error)
    alert('Nepavyko ištrinti renginio.')
  }
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

function getOrganizerNames(event) {
  if (!event.organizers || !event.organizers.length) return ''
  return event.organizers.map(org => org.username).join(', ')
}

function formatDateTime(datetimeStr) {
  if (!datetimeStr) return ''
  const date = new Date(datetimeStr)
  return date.toLocaleString('lt-LT', {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'UTC'
  })
}
</script>
