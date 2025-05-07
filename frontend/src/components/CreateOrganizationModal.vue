<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/axios'

const props = defineProps({
  show: Boolean
})
const emit = defineEmits(['close', 'created'])

const name = ref('')
const description = ref('')
const privacy = ref('public')
const city = ref('vilnius')
const category = ref('board_games')

// Hardcoded categories - matching the backend CATEGORY_CHOICES
const categories = [
  { value: 'classic_strategic', name: 'Klasikiniai & Strateginiai' },
  { value: 'rpg', name: 'RPG (Role-playing games)' },
  { value: 'miniature_games', name: 'Miniatiūrų žaidimai' },
  { value: 'party_social', name: 'Vakarėlių ir socialiniai žaidimai' },
  { value: 'children_games', name: 'Vaikų žaidimai' },
  { value: 'educational', name: 'Edukaciniai žaidimai' }
]

const submitOrganization = async () => {
  try {
    const token = localStorage.getItem('access')

    const payload = {
      name: name.value,
      description: description.value,
      privacy: privacy.value,
      city: city.value,
      category: category.value
    }

    await axios.post('/organizations/', payload, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    emit('created')
    close()
  } catch (error) {
    if (error.response?.data) {
      alert('❌ Klaida: ' + JSON.stringify(error.response.data))
    } else {
      alert('Nepavyko sukurti organizacijos')
    }
    console.error(error)
  }
}

const close = () => {
  name.value = ''
  description.value = ''
  privacy.value = 'public'
  category.value = 'board_games'
  city.value = 'vilnius'
  emit('close')
}

// Nereikia fetchCategories nes dabar naudojam hardcodintas kategorijas
</script>

<template>
  <div v-if="show"
       class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-2xl overflow-y-auto max-h-[90vh]">
      <h2 class="text-xl font-bold mb-4">Sukurti organizaciją</h2>

      <form @submit.prevent="submitOrganization">
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Pavadinimas</label>
          <input v-model="name" required class="w-full border rounded p-2"/>
        </div>

        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Aprašymas</label>
          <textarea v-model="description" class="w-full border rounded p-2"/>
        </div>

        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Viešumo tipas</label>
          <select v-model="privacy" required class="w-full border rounded p-2">
            <option value="public">🔓 Vieša</option>
            <option value="protected">🔐 Apsaugota</option>
            <option value="private">🚫 Privati</option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Grupė (kategorija)</label>
          <select v-model="category" required class="w-full border rounded p-2">
            <option v-for="cat in categories" :key="cat.value" :value="cat.value">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Miestas</label>
          <select v-model="city" required class="w-full border rounded p-2">
            <option disabled value="">-- Pasirinkite miestą --</option>
            <option value="vilnius">Vilnius</option>
            <option value="kaunas">Kaunas</option>
            <option value="klaipeda">Klaipėda</option>
            <option value="siauliai">Šiauliai</option>
            <option value="panevezys">Panevėžys</option>
          </select>
        </div>

        <div class="flex justify-end space-x-2 mt-4">
          <button type="button" @click="close"
                  class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Atšaukti
          </button>
          <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            Sukurti
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
