<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-2xl overflow-y-auto max-h-[90vh]">
      <h2 class="text-xl font-bold mb-4">Sukurti organizaciją</h2>

      <form @submit.prevent="submitOrganization">
        <!-- Pavadinimas -->
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Pavadinimas</label>
          <input v-model="name" required class="w-full border rounded p-2" />
        </div>

        <!-- Aprašymas -->
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Aprašymas</label>
          <textarea v-model="description" class="w-full border rounded p-2" />
        </div>

        <!-- Viešumo tipas -->
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Viešumo tipas</label>
          <select v-model="privacy" required class="w-full border rounded p-2">
            <option value="public">🔓 Vieša – matoma visiems, jungtis gali bet kas</option>
            <option value="protected">🔐 Apsaugota – matoma, bet reikia leidimo jungtis</option>
            <option value="private">🚫 Privati – nematoma, tik pakviestieji</option>
          </select>
        </div>

        <!-- Kategorijos -->
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium">Grupė (kategorija)</label>
          <select v-model="category" required class="w-full border rounded p-2">
            <option disabled value="">-- Pasirinkite kategoriją --</option>
            <option v-for="option in categories" :key="option" :value="option">{{ option }}</option>
          </select>
        </div>

        <!-- Veiksmai -->
        <div class="flex justify-end space-x-2 mt-4">
          <button type="button" @click="close" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Atšaukti</button>
          <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Sukurti</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../api/axios'

const props = defineProps({
  show: Boolean
})
const emit = defineEmits(['close', 'created'])

const name = ref('')
const description = ref('')
const privacy = ref('public')
const category = ref('')

const categories = [
  'Board games',
  'D&D',
  'Card games',
  'Miniatures',
  'Social deduction'
]

const submitOrganization = async () => {
  try {
    const token = localStorage.getItem('access')
    const payload = {
      name: name.value,
      description: description.value,
      privacy: privacy.value,
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
    alert('Nepavyko sukurti organizacijos')
    console.error(error)
  }
}

const close = () => {
  name.value = ''
  description.value = ''
  privacy.value = 'public'
  category.value = ''
  emit('close')
}
</script>
