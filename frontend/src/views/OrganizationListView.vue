<template>
  <div class="bg-gray-50 min-h-screen py-8">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800">Organizacijos</h1>
          <p class="text-gray-500 mt-1">Raskite ir prisijunkite prie įdomių žaidimų organizacijų</p>
        </div>
        <button
          v-if="userRole === 'organizer'"
          @click="showModal = true"
          class="px-5 py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white rounded-lg hover:from-green-700 hover:to-green-600 shadow-md transition flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Nauja organizacija
        </button>
      </div>

      <CreateOrganizationModal :show="showModal" @close="showModal = false" @created="fetchOrganizations" />

      <!-- Filtrai -->
      <div class="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 class="text-lg font-semibold text-gray-700 mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          Filtrai
        </h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
          <div class="col-span-1 sm:col-span-2 lg:col-span-3">
            <label class="block mb-1 text-sm font-medium text-gray-700">Paieška</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                v-model="filters.search"
                @input="fetchOrganizations"
                placeholder="Ieškoti pagal pavadinimą..."
                class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <label class="block mb-1 text-sm font-medium text-gray-700">Viešumas</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <select
                v-model="filters.privacy"
                @change="fetchOrganizations"
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Visi tipai</option>
                <option value="public">🔓 Vieša</option>
                <option value="protected">🔐 Apsaugota</option>
                <option value="private">🚫 Privati</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <div>
            <label class="block mb-1 text-sm font-medium text-gray-700">Miestas</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <select
                v-model="filters.city"
                @change="fetchOrganizations"
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Visi miestai</option>
                <option value="vilnius">Vilnius</option>
                <option value="kaunas">Kaunas</option>
                <option value="klaipeda">Klaipėda</option>
                <option value="siauliai">Šiauliai</option>
                <option value="panevezys">Panevėžys</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <div>
            <label class="block mb-1 text-sm font-medium text-gray-700">Kategorija</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
              </div>
              <select
                v-model="filters.category"
                @change="fetchOrganizations"
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Visos grupės</option>
                <option v-for="cat in categoryOptions" :key="cat.value" :value="cat.value">{{ cat.name }}</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <div v-if="userRole !== 'organizer'" class="flex items-center">
            <label class="flex items-center cursor-pointer">
              <div class="relative">
                <input
                  type="checkbox"
                  v-model="filters.onlyMine"
                  @change="fetchOrganizations"
                  class="sr-only"
                />
                <div class="block bg-gray-200 w-14 h-7 rounded-full"></div>
                <div class="dot absolute left-1 top-1 bg-white w-5 h-5 rounded-full transition transform"
                     :class="{'translate-x-7 bg-indigo-600': filters.onlyMine}"></div>
              </div>
              <span class="ml-3 text-sm text-gray-700">Tik mano organizacijos</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Informacinė žinutė organizatoriams -->
      <div v-if="userRole === 'organizer'" class="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-100">
        <div class="flex">
          <div class="mr-3 flex-shrink-0">
            <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="text-sm text-blue-800">
            <p class="font-medium">Organizatorių režimas</p>
            <p class="mt-1">Jūs matote tik savo sukurtas organizacijas. Kaip organizatorius, galite kurti naujas organizacijas ir valdyti esamas.</p>
          </div>
        </div>
      </div>

      <!-- Organizacijų sąrašas -->
      <div class="space-y-5">
        <div
          v-for="org in filteredOrganizations"
          :key="org.id"
          class="border rounded-lg overflow-hidden bg-white shadow-sm hover:shadow-md transition"
        >
          <div class="h-2 bg-gradient-to-r"
               :class="org.is_member ? 'from-indigo-500 to-blue-600' : 'from-gray-300 to-gray-400'"></div>

          <div class="p-5">
            <div class="flex flex-col md:flex-row justify-between gap-4">
              <div class="flex-1">
                <h2 class="text-xl font-bold text-gray-800 mb-2">{{ org.name }}</h2>
                <p class="text-gray-600 text-sm mb-4">{{ org.description }}</p>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2 text-sm">
                  <div class="flex items-center">
                    <span class="inline-block w-5 text-indigo-500 mr-1">🔒</span>
                    <span class="text-gray-500">Viešumas:</span>
                    <span class="ml-1 text-gray-800">{{ privacyLabels[org.privacy] }}</span>
                  </div>

                  <div class="flex items-center">
                    <span class="inline-block w-5 text-indigo-500 mr-1">👤</span>
                    <span class="text-gray-500">Sukūrė:</span>
                    <span class="ml-1 text-gray-800">{{ org.created_by }}</span>
                  </div>

                  <div class="flex items-center">
                    <span class="inline-block w-5 text-indigo-500 mr-1">📍</span>
                    <span class="text-gray-500">Miestas:</span>
                    <span class="ml-1 text-gray-800 capitalize">{{ org.city }}</span>
                  </div>

                  <div class="flex items-center">
                    <span class="inline-block w-5 text-indigo-500 mr-1">🏷️</span>
                    <span class="text-gray-500">Kategorija:</span>
                    <span class="ml-1 text-gray-800">
                      <span v-if="org.category_display">{{ org.category_display }}</span>
                      <span v-else class="italic text-gray-400">–</span>
                    </span>
                  </div>
                </div>
              </div>

              <div class="flex flex-col gap-2 justify-end">
                <div v-if="org.is_member" class="inline-flex items-center text-sm bg-green-100 text-green-800 px-3 py-1 rounded-full">
                  <svg class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Esate narys
                </div>

                <button
                  v-if="org.is_member"
                  @click="goToOrganization(org.id)"
                  class="px-4 py-2 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg hover:from-indigo-700 hover:to-blue-700 shadow-sm transition flex items-center justify-center gap-2"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Eiti į grupę
                </button>
                <button
                  v-else-if="org.privacy !== 'private'"
                  @click="joinOrganization(org.id)"
                  class="px-4 py-2 bg-gradient-to-r from-green-600 to-green-500 text-white rounded-lg hover:from-green-700 hover:to-green-600 shadow-sm transition flex items-center justify-center gap-2"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Prisijungti
                </button>
                <button
                  v-if="user?.username === org.created_by"
                  @click="deleteOrganization(org.id)"
                  class="px-3 py-1.5 bg-red-100 text-red-600 border border-red-200 rounded-lg hover:bg-red-600 hover:text-white hover:border-red-600 transition flex items-center justify-center gap-1 mt-2 text-sm"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Ištrinti organizaciją
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Kai nėra organizacijų -->
        <div v-if="filteredOrganizations.length === 0" class="bg-white rounded-xl shadow-md p-10 text-center">
          <div class="flex flex-col items-center justify-center py-6">
            <div class="text-6xl mb-4">🏢</div>
            <h3 class="text-xl font-semibold text-gray-700 mb-2">Nerasta organizacijų</h3>
            <p class="text-gray-500 max-w-md mx-auto">
              Nerasta organizacijų, atitinkančių pasirinktus filtrus. Pabandykite pakeisti filtrus arba sukurkite naują organizaciją.
            </p>

            <button
              v-if="userRole === 'organizer'"
              @click="showModal = true"
              class="mt-6 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg hover:from-indigo-700 hover:to-blue-700 shadow-md transition flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Sukurti naują organizaciją
            </button>
          </div>
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
    const res = await axios.post(`/organizations/${orgId}/join/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const detail = res.data?.detail || ''
    if (detail.includes('Prašymas')) {
      alert('🕓 Prašymas išsiųstas. Laukiama organizatoriaus patvirtinimo.')
    } else {
      alert('✅ Prisijungta prie organizacijos!')
    }

    fetchOrganizations()
  } catch (error) {
    console.error('Nepavyko prisijungti:', error)
    alert(error.response?.data?.detail || 'Nepavyko prisijungti.')
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
