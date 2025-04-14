<template>
  <div class="max-w-5xl mx-auto px-4 py-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Organizacijos</h1>
      <button @click="showModal = true" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
        + Nauja organizacija
      </button>
    </div>

    <CreateOrganizationModal :show="showModal" @close="showModal = false" @created="fetchOrganizations" />

    <!-- Filtrai -->
    <div class="bg-white shadow p-4 rounded-lg mb-6 flex flex-wrap gap-4 items-center">
      <label class="flex items-center space-x-2 text-sm text-gray-700">
        <input type="checkbox" v-model="filters.onlyMine" @change="fetchOrganizations" />
        <span>Rodyti tik savo organizacijas</span>
      </label>

      <input
        v-model="filters.search"
        @input="fetchOrganizations"
        placeholder="Ieškoti pagal pavadinimą..."
        class="flex-1 border border-gray-300 rounded px-3 py-2"
      />

      <select v-model="filters.privacy" @change="fetchOrganizations" class="border border-gray-300 rounded px-3 py-2">
        <option value="">Visi tipai</option>
        <option value="public">🔓 Vieša</option>
        <option value="protected">🔐 Apsaugota</option>
        <option value="private">🚫 Privati</option>
      </select>

      <select v-model="filters.city" @change="fetchOrganizations" class="border border-gray-300 rounded px-3 py-2">
        <option value="">Visi miestai</option>
        <option value="vilnius">Vilnius</option>
        <option value="kaunas">Kaunas</option>
        <option value="klaipeda">Klaipėda</option>
        <option value="siauliai">Šiauliai</option>
        <option value="panevezys">Panevėžys</option>
      </select>

      <select v-model="filters.category" @change="fetchOrganizations" class="border border-gray-300 rounded px-3 py-2">
        <option value="">Visos grupės</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
    </div>

    <!-- Organizacijų sąrašas -->
    <div class="space-y-4">
      <div
        v-for="org in organizations"
        :key="org.id"
        class="border rounded-lg p-4 bg-white shadow-sm flex justify-between items-center"
      >
        <div class="flex-1">
          <h2 class="text-xl font-bold">{{ org.name }}</h2>
          <p class="text-gray-600 text-sm mb-2">{{ org.description }}</p>
          <p class="text-sm text-gray-500">Viešumas: {{ org.privacy }}</p>
          <p class="text-sm text-gray-500">Sukūrė: {{ org.created_by }}</p>
          <p class="text-sm text-gray-500">Miestas: {{ org.city }}</p>
        </div>

        <div class="ml-4">
          <button
            v-if="org.is_member"
            @click="goToOrganization(org.id)"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Eiti į grupę
          </button>
          <button
            v-else-if="org.privacy !== 'private'"
            @click="joinOrganization(org.id)"
            class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Prisijungti
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/axios'
import CreateOrganizationModal from '../components/CreateOrganizationModal.vue'

const showModal = ref(false)
const organizations = ref([])
const filters = ref({
  search: '',
  privacy: '',
  category: '',
  city: '',
  onlyMine: false
})

const categories = [
  'Board games',
  'D&D',
  'Card games',
  'Miniatures',
  'Social deduction'
]

const fetchOrganizations = async () => {
  try {
    const params = {}

    if (filters.value.search) params.search = filters.value.search
    if (filters.value.privacy) params.privacy = filters.value.privacy
    if (filters.value.category) params.category_name = filters.value.category
    if (filters.value.city) params.city = filters.value.city

    const token = localStorage.getItem('access')

    const response = await axios.get('/organizations/', {
      headers: { Authorization: `Bearer ${token}` },
      params
    })

    let all = response.data

    if (filters.value.onlyMine) {
      all = all.filter(o => o.is_member)
    }

    all.sort((a, b) => (b.is_member === true) - (a.is_member === true))

    organizations.value = all
  } catch (error) {
    console.error('Nepavyko gauti organizacijų:', error)
  }
}

const joinOrganization = async (orgId) => {
  try {
    const token = localStorage.getItem('access')

    await axios.post(`/organizations/${orgId}/join/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })

    alert('Prisijungei prie organizacijos!')
    fetchOrganizations()
  } catch (error) {
    console.error('Nepavyko prisijungti:', error)
    alert('Nepavyko prisijungti. Galbūt jau esi narys?')
  }
}

const goToOrganization = (orgId) => {
  alert(`Nueiti į organizaciją ${orgId} – čia bus puslapis vėliau`)
}

onMounted(fetchOrganizations)
</script>
