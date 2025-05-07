<!-- OrganizacijosRenginiai.vue -->
<template>
  <div class="max-w-5xl mx-auto px-4 py-6">
    <div v-if="!organization" class="text-center text-gray-500">Kraunama...</div>

    <div v-else>
      <!-- Organizacijos informacija -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl font-bold">{{ organization.name }}</h1>
          <button
            v-if="userIsCreator"
            @click="showEditModal = true"
            class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
          >
            ✏️ Redaguoti
          </button>
        </div>
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

              <div v-if="event.first_player_is_organizer && event.players_count === 0"
                   class="mt-2 mb-2 py-1 px-3 bg-green-100 text-green-800 rounded-full inline-block text-sm font-medium">
                🟢 Laisvas - narių 0 - tapk organizatoriumi!
              </div>
              <p v-else class="text-sm text-gray-800">
                <span class="font-semibold">Dalyviai:</span> {{ event.players_count || 0 }}
                <span v-if="event.organizers && event.organizers.length">
                  (Organizatorius: {{ getOrganizerNames(event) }})
                </span>
                <span v-else>
                  (Organizatorius: {{ event.created_by }})
                </span>
              </p>

              <p class="text-sm text-gray-800"><span class="font-semibold">Viešumas:</span> {{ privacyLabels[event.visibility] }}</p>
            </div>

            <div>
              <p class="text-sm text-gray-800"><span class="font-semibold">Pradžia:</span> {{ formatDateTime(event.start_time) }}</p>
              <p class="text-sm text-gray-800"><span class="font-semibold">Pabaiga:</span> {{ formatDateTime(event.end_time) }}</p>
              <p class="text-sm text-gray-800" v-if="event.perks">
                <span class="font-semibold">Papildomos galimybės:</span> {{ event.perks }}
              </p>

              <div class="mt-4 flex gap-2">
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

                <!-- Trinimo mygtukas matomas TIK jei esi organizacijos kūrėjas -->
                <button
                  v-if="userIsCreator"
                  @click="deleteEvent(event.id)"
                  class="px-3 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  🗑️ Ištrinti
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Organizacijos nariai -->
      <h2 class="text-2xl font-semibold mt-10 mb-4">Nariai</h2>

      <div v-if="members.length === 0" class="text-gray-500">
        Šiuo metu nėra narių.
      </div>

      <ul v-else class="grid gap-2">
        <li
          v-for="member in members"
          :key="member.id"
          class="p-3 bg-white rounded shadow flex justify-between items-center"
        >
          <div class="flex items-center gap-3">
            <div>
              <p class="font-medium text-gray-800">{{ member.username }}</p>

              <div v-if="userIsCreator">
                <p class="text-sm text-gray-500">{{ member.first_name }} {{ member.last_name }}</p>
                <p class="text-sm text-gray-400">{{ member.email }}</p>
              </div>
            </div>
          </div>

          <div v-if="canKick(member.id)">
            <button
              @click="kickMember(member.id)"
              class="px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
            >
              Išmesti
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>

  <OrganizationEditModal
    v-if="organization"
    :visible="showEditModal"
    :organization="organization"
    @close="showEditModal = false"
    @updated="handleUpdated"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import OrganizationEditModal from '@/components/OrganizationEditModal.vue'
import axios from '../api/axios'

const route = useRoute()
const router = useRouter()
const token = localStorage.getItem('access')

const organization = ref<any>(null)
const members = ref<any[]>([])
const user = ref<any>(null)

const fetchOrganization = async () => {
  const orgId = route.params.id
  const response = await axios.get(`/organizations/${orgId}/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  organization.value = response.data
}

const fetchMembers = async () => {
  const orgId = route.params.id
  const response = await axios.get(`/organizations/${orgId}/members/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  members.value = response.data
}

const fetchUser = async () => {
  const res = await axios.get('/users/me/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  user.value = res.data
}

const userIsCreator = computed(() => {
  return organization.value && user.value && organization.value.created_by === user.value.username
})

const joinEvent = async (eventId: number) => {
  await axios.post(`/events/${eventId}/join/`, {}, {
    headers: { Authorization: `Bearer ${token}` }
  })
  fetchOrganization()
}

const deleteEvent = async (eventId: number) => {
  if (!confirm('Ar tikrai nori ištrinti šį renginį?')) return
  await axios.delete(`/events/${eventId}/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  fetchOrganization()
}

const goToEvent = (eventId: number) => {
  router.push(`/events/${eventId}`)
}

const getOrganizerNames = (event: any) => {
  return event.organizers?.map((org: any) => org.username).join(', ') || ''
}

const formatDateTime = (datetimeStr: string) => {
  return new Date(datetimeStr).toLocaleString('lt-LT', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

const canKick = (memberId: number) => {
  return userIsCreator.value && user.value?.id !== memberId
}

const kickMember = async (memberId: number) => {
  const orgId = route.params.id
  await axios.delete(`/organizations/${orgId}/remove-member/${memberId}/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  fetchMembers()
}

const showEditModal = ref(false)
const handleUpdated = async () => {
  await fetchOrganization()
  showEditModal.value = false
}

onMounted(() => {
  fetchOrganization()
  fetchMembers()
  fetchUser()
})

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
</script>
