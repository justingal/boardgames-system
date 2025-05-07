<template>
  <div class="max-w-5xl mx-auto px-4 py-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Organizacijos</h1>
      <button
        v-if="userRole === 'organizer'"
        @click="showModal = true"
        class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        + Nauja organizacija
      </button>
    </div>

    <CreateOrganizationModal :show="showModal" @close="showModal = false" @created="fetchOrganizations" />

    <!-- Filtrai -->
    <div class="bg-white shadow p-4 rounded-lg mb-6 flex flex-wrap gap-4 items-center">
      <label v-if="userRole !== 'organizer'" class="flex items-center space-x-2 text-sm text-gray-700">
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
        <option v-for="cat in categoryOptions" :key="cat.value" :value="cat.value">{{ cat.name }}</option>
      </select>
    </div>

    <!-- Informacinė žinutė organizatoriams -->
    <div v-if="userRole === 'organizer'" class="mb-4 p-3 bg-blue-50 border-l-4 border-blue-500 text-blue-700">
      Jūs matote tik savo sukurtas organizacijas
    </div>

    <!-- Organizacijų sąrašas -->
    <div class="space-y-4">
      <div
        v-for="org in filteredOrganizations"
        :key="org.id"
        class="border rounded-lg p-4 bg-white shadow-sm flex justify-between items-center"
      >
        <div class="flex-1">
          <h2 class="text-xl font-bold">{{ org.name }}</h2>
          <p class="text-gray-600 text-sm mb-2">{{ org.description }}</p>
          <p class="text-sm text-gray-500">Viešumas: {{ privacyLabels[org.privacy] }}</p>
          <p class="text-sm text-gray-500">Sukūrė: {{ org.created_by }}</p>
          <p class="text-sm text-gray-500">Miestas: {{ org.city }}</p>
          <p class="text-sm text-gray-500">
            Kategorija:
            <span v-if="org.category">{{ getCategoryName(org.category) }}</span>
            <span v-else-if="org.categories && org.categories.length > 0">
              {{ org.categories.map(cat => cat.name).join(', ') }}
            </span>
            <span v-else>–</span>
          </p>
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
          <button
            v-if="user?.username === org.created_by"
            @click="deleteOrganization(org.id)"
            class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
          >
            🗑️ Ištrinti organizaciją
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '../api/axios'
import { jwtDecode } from 'jwt-decode'
import CreateOrganizationModal from '../components/CreateOrganizationModal.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const showModal = ref(false)
const organizations = ref([])
const user = ref(null)
const filters = ref({
  search: '',
  privacy: '',
  category: '',
  city: '',
  onlyMine: false
})

const privacyLabels = {
  public: '🔓 Vieša – matoma visiems',
  protected: '🔐 Apsaugota – matoma, bet reikia leidimo jungtis',
  private: '🚫 Privati – nematoma, tik pakviestiesiems'
}

// Hardcoded categories to match backend CATEGORY_CHOICES
const categoryOptions = [
  { value: 'classic_strategic', name: 'Klasikiniai & Strateginiai' },
  { value: 'rpg', name: 'RPG (Role-playing games)' },
  { value: 'miniature_games', name: 'Miniatiūrų žaidimai' },
  { value: 'party_social', name: 'Vakarėlių ir socialiniai žaidimai' },
  { value: 'children_games', name: 'Vaikų žaidimai' },
  { value: 'educational', name: 'Edukaciniai žaidimai' }
]

const getCategoryName = (categoryValue) => {
  const category = categoryOptions.find(cat => cat.value === categoryValue)
  return category ? category.name : categoryValue
}

const userRole = ref(null)
const token = localStorage.getItem('access')
if (token) {
  try {
    const decoded = jwtDecode(token)
    userRole.value = decoded.role ||
      (decoded.groups && decoded.groups.includes('organizer') ? 'organizer' : 'user') ||
      (decoded.profile?.role) ||
      'user'
  } catch (error) {
    console.error('Klaida dekoduojant token:', error)
    userRole.value = 'user'
  }
}

const fetchUser = async () => {
  try {
    const res = await axios.get('/users/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = res.data
  } catch (error) {
    console.error('Nepavyko gauti vartotojo informacijos:', error)
  }
}

const filteredOrganizations = computed(() => {
  let result = [...organizations.value]

  if (userRole.value !== 'organizer' && filters.value.onlyMine) {
    result = result.filter(o => o.is_member)
  }

  result.sort((a, b) => (b.is_member === true) - (a.is_member === true))

  return result
})

const fetchOrganizations = async () => {
  try {
    const params = {}

    if (filters.value.search) params.search = filters.value.search
    if (filters.value.privacy) params.privacy = filters.value.privacy
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.city) params.city = filters.value.city

    const response = await axios.get('/organizations/', {
      params,
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    organizations.value = response.data
  } catch (error) {
    console.error('Nepavyko gauti organizacijų:', error)
  }
}

const joinOrganization = async (orgId) => {
  try {
    await axios.post(`/organizations/${orgId}/join/`)
    alert('Prisijungei prie organizacijos!')
    fetchOrganizations()
  } catch (error) {
    console.error('Nepavyko prisijungti:', error)
    alert('Nepavyko prisijungti. Galbūt jau esi narys?')
  }
}

const deleteOrganization = async (orgId) => {
  if (!confirm('Ar tikrai nori ištrinti šią organizaciją?')) return
  try {
    await axios.delete(`/organizations/${orgId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('✅ Organizacija ištrinta.')
    fetchOrganizations()
  } catch (error) {
    console.error('Klaida trinant organizaciją:', error)
    alert('❌ Nepavyko ištrinti organizacijos.')
  }
}

const goToOrganization = (orgId) => {
  router.push(`/organizations/${orgId}`)
}

onMounted(() => {
  fetchOrganizations()
  fetchUser()
})
</script>
