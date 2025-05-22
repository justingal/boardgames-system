<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Mano profilis</h1>
        <p class="text-gray-500 mt-1">Valdykite savo paskyros informaciją ir kvietimus</p>
      </div>

      <!-- Loading State -->
      <div v-if="!profile" class="flex justify-center items-center py-16">
        <div class="text-center">
          <svg class="animate-spin h-12 w-12 mx-auto text-indigo-600 mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="text-lg font-medium text-gray-700">Kraunama profilio informacija...</p>
        </div>
      </div>

      <div v-else class="space-y-6">
        <!-- Profile Information Card -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="h-2 bg-gradient-to-r from-indigo-500 to-blue-600"></div>
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6 flex items-center">
              <svg class="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Asmeninė informacija
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-500 mb-1">Vartotojo vardas</label>
                <p class="text-gray-900 font-medium">{{ profile.user.username }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-500 mb-1">El. paštas</label>
                <p class="text-gray-900 font-medium">{{ profile.user.email }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-500 mb-1">Vardas</label>
                <p class="text-gray-900 font-medium">{{ profile.user.first_name || 'Nenurodyta' }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-500 mb-1">Pavardė</label>
                <p class="text-gray-900 font-medium">{{ profile.user.last_name || 'Nenurodyta' }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-500 mb-1">Rolė</label>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                      :class="profile.role === 'organizer' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path v-if="profile.role === 'organizer'" fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                    <path v-else fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                  </svg>
                  {{ roleLabels[profile.role] || profile.role }}
                </span>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-500 mb-1">Organizacija</label>
                <p class="text-gray-900 font-medium">
                  {{ profile.organization?.name || 'Nepriskirta' }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Event Invitations -->
        <div v-if="eventInvites.length > 0" class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="h-2 bg-gradient-to-r from-green-500 to-green-600"></div>
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6 flex items-center">
              <svg class="w-6 h-6 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Kvietimai į renginius
              <span class="ml-2 bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm font-medium">
                {{ eventInvites.length }}
              </span>
            </h2>

            <div class="space-y-3">
              <div v-for="invite in eventInvites" :key="invite.id"
                   class="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200 hover:bg-green-100 transition">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-green-100 text-green-600 rounded-full flex items-center justify-center mr-4">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ invite.event_title }}</p>
                    <p class="text-sm text-gray-500">Renginys</p>
                  </div>
                </div>
                <div class="flex gap-2">
                  <button
                    @click="acceptEventInvite(invite.id)"
                    class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium flex items-center gap-1"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    Priimti
                  </button>
                  <button
                    @click="rejectEventInvite(invite.id)"
                    class="px-4 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-600 hover:text-white transition font-medium flex items-center gap-1"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    Atmesti
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Organization Invitations -->
        <div v-if="invites.length > 0" class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="h-2 bg-gradient-to-r from-purple-500 to-indigo-600"></div>
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6 flex items-center">
              <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              Kvietimai į organizacijas
              <span class="ml-2 bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-sm font-medium">
                {{ invites.length }}
              </span>
            </h2>

            <div class="space-y-3">
              <div
                v-for="invite in filteredInvites"
                :key="invite.id"
                class="flex items-center justify-between p-4 bg-purple-50 rounded-lg border border-purple-200 hover:bg-purple-100 transition"
              >
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mr-4">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ invite.organization_name }}</p>
                    <p class="text-sm text-gray-500">Organizacija</p>
                  </div>
                </div>
                <div class="flex gap-2">
                  <button
                    @click="acceptInvite(invite.id)"
                    class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-medium flex items-center gap-1"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    Priimti
                  </button>
                  <button
                    @click="rejectInvite(invite.id)"
                    class="px-4 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-600 hover:text-white transition font-medium flex items-center gap-1"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    Atmesti
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State for Invitations -->
        <div v-if="invites.length === 0 && eventInvites.length === 0" class="bg-white rounded-xl shadow-md p-8 text-center">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Nėra naujų kvietimų</h3>
          <p class="text-gray-500">Kai gausite kvietimų į organizacijas ar renginius, jie bus rodomi čia.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue'
import axios from '../api/axios'

const profile = ref(null)
const invites = ref([])
const eventInvites = ref([])

const token = localStorage.getItem('access')

const roleLabels = {
  organizer: 'Organizatorius',
  player: 'Žaidėjas'
}

// Užklausos
const fetchProfile = async () => {
  try {
    const res = await axios.get('/users/me/full/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    profile.value = res.data
  } catch (error) {
    console.error('❌ Nepavyko gauti profilio:', error)
  }
}

const fetchOrganizationInvites = async () => {
  try {
    const res = await axios.get('/organizations/invites/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    invites.value = res.data
  } catch (error) {
    console.error('❌ Nepavyko gauti organizacijų kvietimų:', error)
  }
}
const filteredInvites = computed(() => {
  return invites.value.filter(inv => inv.organization_name && inv.organization_name.trim() !== '');
});
const fetchEventInvites = async () => {
  try {
    const res = await axios.get('/events/invites/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    eventInvites.value = res.data
  } catch (error) {
    console.error('❌ Nepavyko gauti kvietimų į renginius:', error)
  }
}

// Kvietimų priėmimas/atmetimas
const acceptInvite = async (inviteId) => {
  try {
    await axios.post('/organizations/accept_invite/', { invite_id: inviteId }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('✅ Sėkmingai prisijungėte prie organizacijos!')
    await fetchProfile()
    await fetchOrganizationInvites()
  } catch (err) {
    alert('❌ Nepavyko priimti organizacijos kvietimo.')
    console.error(err)
  }
}

const rejectInvite = async (inviteId) => {
  try {
    await axios.post('/organizations/reject_invite/', { invite_id: inviteId }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('✅ Kvietimas atmestas.')
    await fetchOrganizationInvites()
  } catch (err) {
    alert('❌ Nepavyko atmesti kvietimo.')
    console.error(err)
  }
}

const acceptEventInvite = async (inviteId) => {
  try {
    await axios.post('/events/accept_invite/', {invite_id: inviteId}, {
      headers: {Authorization: `Bearer ${token}`}
    })
    alert('✅ Prisijungėte prie renginio!')
    await fetchEventInvites()
  } catch (err) {
    alert('❌ Nepavyko priimti kvietimo į renginį.')
    console.error(err)
  }
}

const rejectEventInvite = async (inviteId) => {
  try {
    await axios.post('/events/reject_invite/', {invite_id: inviteId}, {
      headers: {Authorization: `Bearer ${token}`}
    })
    alert('✅ Kvietimas į renginį atmestas.')
    await fetchEventInvites()
  } catch (err) {
    alert('❌ Nepavyko atmesti kvietimo.')
    console.error(err)
  }
}

// Inicijavimas
onMounted(() => {
  fetchProfile()
  fetchOrganizationInvites()
  fetchEventInvites()
})
</script>
