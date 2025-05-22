<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Mano profilis</h1>

    <div v-if="!profile" class="text-gray-500">Kraunama...</div>

    <div v-else class="space-y-4">
      <div>
        <label class="font-medium">Vartotojo vardas:</label>
        <div class="text-gray-800">{{ profile.user.username }}</div>
      </div>

      <div>
        <label class="font-medium">El. paštas:</label>
        <div class="text-gray-800">{{ profile.user.email }}</div>
      </div>

      <div>
        <label class="font-medium">Vardas:</label>
        <div class="text-gray-800">{{ profile.user.first_name || '-' }}</div>
      </div>

      <div>
        <label class="font-medium">Pavardė:</label>
        <div class="text-gray-800">{{ profile.user.last_name || '-' }}</div>
      </div>

      <div>
        <label class="font-medium">Rolė:</label>
        <div class="text-gray-800">
          {{ roleLabels[profile.role] || profile.role }}
        </div>
      </div>

      <div>
        <label class="font-medium">Organizacija:</label>
        <div class="text-gray-800">
          {{ profile.organization?.name || 'Nesusieta' }}
        </div>
      </div>
    </div>
    <div v-if="invites.length > 0" class="mt-10">
      <h3 class="text-lg font-semibold mb-2">Kvietimai į organizacijas</h3>
      <ul class="space-y-2">
        <li
          v-for="invite in invites"
          :key="invite.id"
          class="flex justify-between items-center bg-indigo-50 p-4 rounded-lg border border-indigo-200"
        >
          <span class="text-gray-800 font-medium">{{ invite.organization_name }}</span>
          <button
            @click="acceptInvite(invite.id)"
            class="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700"
          >
            Priimti
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/axios'

const profile = ref(null)
const token = localStorage.getItem('access')

const roleLabels = {
  organizer: 'Organizatorius',
  player: 'Žaidėjas'
}

const fetchProfile = async () => {
  try {
    const res = await axios.get('/users/me/full/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    profile.value = res.data
  } catch (error) {
    console.error('Nepavyko gauti profilio:', error)
  }
}
const invites = ref([])

const fetchInvites = async () => {
  try {
    const res = await axios.get(`/organizations/invites/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    invites.value = res.data
  } catch (error) {
    console.error('Nepavyko gauti kvietimų:', error)
  }
}

const acceptInvite = async (inviteId) => {
  try {
    await axios.post(`/organizations/accept_invite/`, { invite_id: inviteId }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('✅ Sėkmingai prisijungei.')
    fetchProfile()
    fetchInvites()
  } catch (err) {
    alert('❌ Nepavyko priimti kvietimo.')
    console.error(err)
  }
}


onMounted(() => {
  fetchProfile()
  fetchInvites()
})
</script>

<style scoped>
label {
  display: block;
  margin-bottom: 0.25rem;
}
</style>
