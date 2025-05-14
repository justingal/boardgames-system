<template>
  <div class="min-h-screen bg-gray-50 py-10">
    <div v-if="event" class="max-w-5xl mx-auto px-4 sm:px-6">
      <!-- Renginio antraštė ir pagrindinė informacija -->
      <div class="bg-white rounded-xl overflow-hidden shadow-lg mb-8 relative">
        <!-- Renginio viršutinė juosta su statusu -->
        <div class="h-3 bg-gradient-to-r from-indigo-500 to-blue-600"></div>

        <div class="p-6 sm:p-8">
          <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-4">
            <!-- Kairė pusė: pavadinimas ir detalės -->
            <div class="flex-1">
              <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ event.title }}</h1>

              <div class="flex items-center flex-wrap gap-3 mb-6">
                <!-- "First player is organizer" badge -->
                <div v-if="event.first_player_is_organizer"
                     class="inline-flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                  <svg class="h-3.5 w-3.5 mr-1.5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                  Pirmas prisijungęs žaidėjas tampa organizatoriumi
                </div>
                <div class="inline-flex items-center gap-1 text-sm text-gray-600 px-3 py-1 rounded-full bg-gray-100">
                  <span>{{ privacyLabels[event.visibility] }}</span>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 text-sm">
                <div class="flex items-start">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Adresas</p>
                    <p class="font-medium text-gray-900">{{ event.address }}</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Stalo dydis</p>
                    <p class="font-medium text-gray-900">{{ tableSizeLabels[event.table_size] }}</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Pradžia</p>
                    <p class="font-medium text-gray-900">{{ formatDateTime(event.start_time) }}</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Pabaiga</p>
                    <p class="font-medium text-gray-900">{{ formatDateTime(event.end_time) }}</p>
                  </div>
                </div>

                <div class="flex items-start md:col-span-2">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Organizatoriai</p>
                    <p class="font-medium text-gray-900">
                      <span v-if="event.organizers && event.organizers.length > 0">
                        {{ event.organizers.map(org => org.username).join(', ') }}
                      </span>
                      <span v-else>{{ event.created_by }}</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Dešinė pusė: veiksmai ir aprašymas -->
            <div class="flex flex-col gap-3 md:w-1/4">
              <button
                v-if="userIsOrganizer"
                @click="showEditModal = true"
                class="flex items-center justify-center gap-2 px-4 py-2.5 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition shadow-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                Redaguoti renginį
              </button>

              <button
                v-if="userIsOrgCreator"
                @click="deleteEvent"
                class="flex items-center justify-center gap-2 px-4 py-2.5 bg-white border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition shadow-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Ištrinti renginį
              </button>
            </div>
          </div>

          <!-- Aprašymas -->
          <div class="mt-8 p-4 bg-gray-50 rounded-lg text-sm leading-relaxed border border-gray-200">
            <h3 class="font-medium text-gray-900 mb-2">Aprašymas:</h3>
            <p class="text-gray-700 whitespace-pre-line">{{ event.description }}</p>
          </div>

          <!-- Pranešimai -->
          <div v-if="message" class="mt-6 p-4 rounded-lg border" :class="messageClass">
            {{ message }}
          </div>
        </div>
      </div>

      <!-- Dalyviai ir žaidimai -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Dalyvių sąrašas -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="bg-gradient-to-r from-indigo-500 to-blue-600 px-6 py-4">
              <h2 class="text-lg font-semibold text-white flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                Dalyviai ({{ event.players?.length || 0 }})
              </h2>
            </div>

            <div v-if="event.players && event.players.length > 0" class="divide-y divide-gray-200">
              <div v-for="player in event.players" :key="player.id" class="p-4 hover:bg-gray-50 transition">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold mr-3">
                      {{ player.username.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <p class="font-medium">{{ player.username }}</p>
                      <p v-if="isOrganizer(player.id)" class="text-xs text-green-600 font-semibold">
                        Organizatorius
                      </p>
                    </div>
                  </div>

                  <!-- Veiksmai -->
                  <div v-if="userIsOrganizer" class="flex flex-col gap-2">
                    <button
                      v-if="!isOrganizer(player.id)"
                      @click="makeOrganizer(player.id)"
                      class="text-xs px-2 py-1 bg-indigo-50 text-indigo-600 rounded hover:bg-indigo-100 transition"
                    >
                      Suteikti teises
                    </button>
                    <button
                      v-else-if="canRemoveOrganizerStatus(player.id)"
                      @click="removeOrganizer(player.id)"
                      class="text-xs px-2 py-1 bg-orange-50 text-orange-600 rounded hover:bg-orange-100 transition"
                    >
                      Atimti teises
                    </button>
                    <button
                      v-if="canKickPlayer(player.id)"
                      @click="kickPlayer(player.id)"
                      class="text-xs px-2 py-1 bg-red-50 text-red-600 rounded hover:bg-red-100 transition"
                    >
                      Išmesti
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="p-6 text-center text-gray-500">
              Nėra prisijungusių dalyvių.
            </div>
          </div>
        </div>

        <!-- Žaidimų sąrašas -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="bg-gradient-to-r from-indigo-500 to-blue-600 px-6 py-4 flex justify-between items-center">
              <h2 class="text-lg font-semibold text-white flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Žaidimai ({{ visibleGames.length }}/{{ allGames.length }})
              </h2>

              <div class="flex items-center gap-2">
                <button
                  @click="showImportModal = true"
                  class="px-3 py-1.5 bg-green-500 text-white text-sm rounded-md hover:bg-green-600 transition shadow-sm flex items-center gap-1"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                  Importuoti
                </button>

                <button
                  @click="showVoteModal = true"
                  class="px-3 py-1.5 bg-blue-500 text-white text-sm rounded-md hover:bg-blue-800 transition shadow-sm flex items-center gap-1"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Balsuoti
                </button>
              </div>
            </div>

            <div v-if="visibleGames.length > 0" class="p-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-for="(item, index) in visibleGames" :key="item.game.id"
                     class="flex gap-3 border rounded-lg p-3 bg-gray-50 hover:bg-gray-100 transition">
                  <div class="w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-xs flex items-center justify-center flex-shrink-0">
                    {{ index + 1 }}
                  </div>
                  <img :src="item.game.thumbnail_url" class="w-14 h-14 object-cover rounded-md" />
                  <div class="overflow-hidden">
                    <p class="font-medium text-sm truncate">{{ item.game.title }}</p>
                    <p class="text-xs text-gray-600">
                      {{ item.game.min_players }}–{{ item.game.max_players }} žaidėjai • {{ item.game.playtime_minutes }} min
                    </p>
                  </div>
                </div>
              </div>

              <div v-if="visibleGames.length < allGames.length" class="mt-4 text-center">
                <button @click="showMoreGames" class="px-4 py-2 bg-gray-100 text-gray-600 rounded-md hover:bg-gray-200 transition">
                  Rodyti daugiau žaidimų
                </button>
              </div>
            </div>

            <div v-else class="p-6 text-center text-gray-500">
              Nėra pasirinktų žaidimų. Importuokite žaidimus arba balsuokite už juos.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loaderis kol event dar neatėjo -->
    <div v-else class="flex justify-center items-center h-screen">
      <div class="text-center">
        <svg class="animate-spin h-12 w-12 mx-auto text-indigo-600 mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-lg font-medium text-gray-700">Kraunama renginio informacija...</p>
      </div>
    </div>

    <!-- Modalai -->
    <ImportGamesModal
      :visible="showImportModal"
      @close="showImportModal = false"
      @imported="fetchEvent"
    />
    <EventVoteModal
      :visible="showVoteModal"
      @close="showVoteModal = false"
      @voted="fetchEvent"
    />
    <EditEventModal
      :visible="showEditModal"
      :eventData="event"
      @close="showEditModal = false"
      @updated="handleEventUpdated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router' // <- BŪTINA!
import axios from '@/api/axios'
import EditEventModal from '@/components/EditEventModal.vue'
import ImportGamesModal from '@/components/ImportGamesModal.vue'
import EventVoteModal from "@/components/EventVoteModal.vue";

const showVoteModal = ref(false)
const showImportModal = ref(false)
const router = useRouter() // <- PRIDĖTA!
const token = localStorage.getItem('access') // <- PRIDĖTA!

const route = useRoute()
const event = ref<any>(null)
const message = ref('')
const messageClass = ref('bg-green-100 text-green-800')

const tableSizeLabels = {
  S: 'Mažas',
  M: 'Vidutinis',
  L: 'Didelis',
  XL: 'Labai didelis',
}

const privacyLabels = {
  public: '🔓 Viešas',
  protected: '🔐 Apsaugotas',
  private: '🚫 Privatus',
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
const fetchEvent = async () => {
  try {
    const res = await axios.get(`/events/${route.params.id}/`)
    event.value = res.data
  } catch (err) {
    console.error('Nepavyko gauti renginio:', err)
    message.value = '❌ Klaida gaunant renginio informaciją.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}
const userIsOrgCreator = computed(() => {
  return event.value?.organization_creator === user.value?.username
})



const user = ref<any>(null)

const fetchUser = async () => {
  try {
    const res = await axios.get('/users/me/')
    user.value = res.data
  } catch (err) {
    console.error('Nepavyko gauti vartotojo informacijos:', err)
  }
}

// Check if current user is an organizer
const userIsOrganizer = computed(() => {
  if (!event.value || !user.value) return false

  // Check if user is in organizers list
  if (event.value.organizers && event.value.organizers.length > 0) {
    return event.value.organizers.some((org: any) => org.id === user.value.id)
  }

  // Or if user is the one who created the event
  return event.value.created_by === user.value.username
})

// Check if a specific player is an organizer
const isOrganizer = (playerId: number) => {
  if (!event.value || !event.value.organizers) return false
  return event.value.organizers.some((org: any) => org.id === playerId)
}

// Check if current user can remove organizer status from a player
const canRemoveOrganizerStatus = (playerId: number) => {
  if (!event.value || !user.value) return false

  // You can't remove yourself if you're the creator
  if (playerId === user.value.id && event.value.created_by === user.value.username) {
    return false
  }

  return true
}

// Check if current user can kick a player
const canKickPlayer = (playerId: number) => {
  if (!event.value || !user.value) return false

  // Can't kick organizers
  if (isOrganizer(playerId)) {
    return false
  }

  return true
}

const makeOrganizer = async (userId: number) => {
  try {
    const res = await axios.post(`/events/${route.params.id}/make-organizer/`, { user_id: userId })
    message.value = res.data.message || '✅ Organizatoriaus teisės suteiktos.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent() // Refresh event data
  } catch (err) {
    console.error('Klaida suteikiant organizatoriaus teises:', err)
    message.value = '❌ Klaida suteikiant organizatoriaus teises.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}



const deleteEvent = async () => {
  if (!confirm('Ar tikrai nori ištrinti šį renginį?')) return
  try {
    await axios.delete(`/events/${event.value.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('✅ Renginys ištrintas.')
    router.push('/events') // arba `/organizations/${event.value.organization}`
  } catch (error) {
    console.error('Nepavyko ištrinti renginio:', error)
    alert('❌ Klaida trinant renginį.')
  }
}

const removeOrganizer = async (userId: number) => {
  try {
    const res = await axios.post(`/events/${route.params.id}/remove-organizer/`, { user_id: userId })
    message.value = res.data.message || '✅ Organizatoriaus teisės pašalintos.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent() // Refresh event data
  } catch (err) {
    console.error('Klaida šalinant organizatoriaus teises:', err)
    message.value = '❌ Klaida šalinant organizatoriaus teises.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}

const kickPlayer = async (userId: number) => {
  try {
    const res = await axios.post(`/events/${route.params.id}/kick-player/`, { user_id: userId })
    message.value = res.data.message || '✅ Žaidėjas išmestas.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent() // Refresh event data
  } catch (err) {
    console.error('Klaida metant žaidėją lauk:', err)
    message.value = '❌ Klaida metant žaidėją lauk.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}

const showEditModal = ref(false)
const openEditModal = () => {
  showEditModal.value = true
}
const handleEventUpdated = async () => {
  await fetchEvent()               // Tavo jau esama funkcija, kuri atnaujina event duomenis
  message.value = '✅ Renginys atnaujintas!'
  messageClass.value = 'bg-green-100 text-green-800'
}
const allGames = ref<any[]>([])
const visibleGames = ref<any[]>([])
const gamesToShow = ref(10)

const fetchGames = async () => {
  try {
    const res = await axios.get(`/events/${route.params.id}/available-games/`)
    allGames.value = res.data
    visibleGames.value = allGames.value.slice(0, gamesToShow.value)
  } catch (err) {
    console.error('Nepavyko gauti žaidimų:', err)
  }
}

const showMoreGames = () => {
  gamesToShow.value += 10
  visibleGames.value = allGames.value.slice(0, gamesToShow.value)
}

onMounted(() => {
  fetchUser()
  fetchEvent()
  fetchGames()
})
</script>
