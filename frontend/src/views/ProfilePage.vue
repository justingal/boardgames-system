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

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
label {
  display: block;
  margin-bottom: 0.25rem;
}
</style>
