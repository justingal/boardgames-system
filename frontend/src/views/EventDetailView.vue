<template>
  <div class="min-h-screen bg-gray-100 flex items-start justify-center pt-12">
    <div v-if="event" class="bg-white rounded-lg shadow-md p-6 w-full max-w-4xl">
      <h1 class="text-2xl font-bold mb-4">{{ event.title }}</h1>
      <button
        v-if="userIsOrganizer"
        @click="showEditModal = true"
        class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 mt-4"
      >
        ✏️ Redaguoti renginį
      </button>

      <div class="mb-6">

        <p><span class="font-semibold">Aprašymas:</span> {{ event.description }}</p>
        <p><span class="font-semibold">Adresas:</span> {{ event.address }}</p>
        <p><span class="font-semibold">Stalo dydis:</span> {{ tableSizeLabels[event.table_size] }}</p>

        <!-- Organizatoriai -->
        <p>
          <span class="font-semibold">Organizatoriai:</span>
          <span v-if="event.organizers && event.organizers.length > 0">
            {{ event.organizers.map(org => org.username).join(', ') }}
          </span>
          <span v-else>{{ event.created_by }}</span>
        </p>

        <p><span class="font-semibold">Viešumas:</span> {{ privacyLabels[event.visibility] }}</p>
        <p><span class="font-semibold">Pradžia:</span> {{ formatDateTime(event.start_time) }}</p>
        <p><span class="font-semibold">Pabaiga:</span> {{ formatDateTime(event.end_time) }}</p>

        <!-- "First player is organizer" badge -->
        <div v-if="event.first_player_is_organizer" class="mt-3 inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
          Pirmas prisijungęs žaidėjas tampa organizatoriumi
        </div>
      </div>


      <div v-if="message" class="mb-4 p-3 rounded" :class="messageClass">
        {{ message }}
      </div>

      <h2 class="text-lg font-semibold mt-8 mb-4">Dalyviai:</h2>
      <div v-if="event.players && event.players.length > 0">
        <table class="w-full border border-gray-300 text-sm">
          <thead>
          <tr class="bg-gray-100">
            <th class="border border-gray-300 px-4 py-2 text-left">Vartotojas</th>
            <th class="border border-gray-300 px-4 py-2 text-left">Veiksmai</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="player in event.players" :key="player.id" class="hover:bg-gray-50">
            <td class="border border-gray-300 px-4 py-2">
              {{ player.username }}
              <span v-if="isOrganizer(player.id)" class="text-green-600 font-semibold ml-2">
                (Organizatorius)
              </span>
            </td>
            <td class="border border-gray-300 px-4 py-2 space-x-2">
              <!-- Rodyti mygtukus tik jeigu prisijungęs vartotojas yra organizatorius -->
              <template v-if="userIsOrganizer">
                <!-- Nerodyti suteikimo mygtuko, jei tas žmogus jau yra organizatorius -->
                <button
                  v-if="!isOrganizer(player.id)"
                  @click="makeOrganizer(player.id)"
                  class="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                >
                  Suteikti organizatoriaus teises
                </button>
                <button
                  v-else-if="canRemoveOrganizerStatus(player.id)"
                  @click="removeOrganizer(player.id)"
                  class="px-3 py-1 bg-orange-600 text-white rounded hover:bg-orange-700"
                >
                  Pašalinti organizatoriaus teises
                </button>
                <button
                  v-if="canKickPlayer(player.id)"
                  @click="kickPlayer(player.id)"
                  class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  Išmesti
                </button>
              </template>
            </td>
          </tr>
          </tbody>
        </table>
        <h2 class="text-lg font-semibold mt-8 mb-4">🎲 Žaidimai:</h2>
        <div v-if="visibleGames.length > 0" class="space-y-2">
          <div v-for="(item, index) in visibleGames" :key="item.game.id" class="flex items-center gap-3 border rounded px-3 py-2 bg-gray-50">
            <div class="w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-xs flex items-center justify-center">
              {{ index + 1 }}
            </div>
            <img :src="item.game.thumbnail_url" class="w-12 h-12 object-cover rounded" />
            <div class="text-sm">
              <p class="font-semibold">{{ item.game.title }}</p>
              <p class="text-gray-600">{{ item.game.min_players }}–{{ item.game.max_players }} žaidėjai • {{ item.game.playtime_minutes }} min</p>
            </div>
          </div>
          <div v-if="visibleGames.length < allGames.length" class="text-center mt-4">
            <button @click="showMoreGames" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
              Rodyti daugiau
            </button>
          </div>
        </div>
        <button
          @click="showImportModal = true"
          class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 mt-4 ml-2"
        >
          📥 Importuoti žaidimus į renginį
        </button>
        <button
          @click="showVoteModal = true"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 mt-4"
        >
          🗳️ Balsuoti už žaidimus
        </button>
      </div>
      <p v-else>Nėra prisijungusių dalyvių.</p>
    </div>





    <!-- Loaderis kol event dar neatejo -->
    <div v-else>
      <p>🔄 Kraunama renginio informacija...</p>
    </div>
    <!-- ImportGamesModal (PRIDĖTA ČIA!) -->
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
  </div>
  <EditEventModal
    :visible="showEditModal"
    :eventData="event"
    @close="showEditModal = false"
    @updated="handleEventUpdated"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/api/axios'
import EditEventModal from '@/components/EditEventModal.vue'
import ImportGamesModal from '@/components/ImportGamesModal.vue'
import EventVoteModal from "@/components/EventVoteModal.vue";

const showVoteModal = ref(false)
const showImportModal = ref(false)


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

const formatDateTime = (datetimeStr: string) => {
  const options = { dateStyle: 'medium', timeStyle: 'short' }
  return new Date(datetimeStr).toLocaleString('lt-LT', options)
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
