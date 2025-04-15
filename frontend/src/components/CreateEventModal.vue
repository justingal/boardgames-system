<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-2xl p-6 w-full max-w-2xl overflow-y-auto max-h-[90vh]">
      <h2 class="text-xl font-bold mb-4">Sukurti renginį</h2>

      <form @submit.prevent="submit">
        <!-- Pavadinimas -->
        <div class="mb-4">
          <label class="block mb-1 font-medium">Pavadinimas</label>
          <input v-model="form.title" required class="w-full border rounded-lg px-3 py-2" />
        </div>

        <!-- Aprašymas -->
        <div class="mb-4">
          <label class="block mb-1 font-medium">Aprašymas</label>
          <textarea v-model="form.description" class="w-full border rounded-lg px-3 py-2" />
        </div>

        <!-- Adresas -->
        <div class="mb-4">
          <label class="block mb-1 font-medium">Adresas</label>
          <input v-model="form.address" required class="w-full border rounded-lg px-3 py-2" />
        </div>

        <!-- Stalo dydis -->
        <div class="mb-4">
          <label class="block mb-1 font-medium">Stalo dydis</label>
          <select v-model="form.table_size" required class="w-full border rounded-lg px-3 py-2">
            <option value="S">Mažas (2 žmonės) ~ 80x80cm</option>
            <option value="M">Vidutinis (4 žmonės) ~ 120x80cm</option>
            <option value="L">Didelis (6-8 žmonės) ~ 180x90cm</option>
            <option value="XL">Labai didelis (8-10 žmonių) ~ 200x100cm</option>
          </select>
        </div>

        <!-- Perk'ai -->
        <div class="mb-4">
          <label class="block mb-1 font-medium">Papildomos galimybės (Perks)</label>
          <div class="flex flex-wrap gap-3">
            <label v-for="perk in allPerks" :key="perk" class="flex items-center gap-2">
              <input type="checkbox" :value="perk" v-model="form.perksList" />
              <span>{{ perk }}</span>
            </label>
          </div>
          <div v-if="form.perksList.length" class="mt-2 text-sm text-gray-600">
            Pažymėta: {{ form.perksList.join(', ') }}
          </div>
        </div>

        <!-- Veiksmai -->
        <div class="flex justify-end gap-2">
          <button type="button" @click="close" class="bg-gray-300 px-4 py-2 rounded-lg hover:bg-gray-400">
            Atšaukti
          </button>
          <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            Sukurti
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from '../api/axios'

const props = defineProps({
  show: Boolean
})
const emit = defineEmits(['close', 'created'])

const form = ref({
  title: '',
  description: '',
  address: '',
  table_size: 'M',
  perksList: []
})

const allPerks = [
  'Atskira salė',
  'Leidžiama triukšmauti',
  'Prieiga prie virtuvėlės',
  'Projektorius',
  'Oro kondicionierius'
]

const submit = async () => {
  try {
    const token = localStorage.getItem('access')
    const payload = {
      ...form.value,
      perks: form.value.perksList.join(', ')
    }

    await axios.post('/events/', payload, {
      headers: { Authorization: `Bearer ${token}` }
    })

    emit('created')
    close()
  } catch (err) {
    console.error('Nepavyko sukurti renginio:', err)
    alert('Klaida kuriant renginį')
  }
}

const close = () => {
  form.value = {
    title: '',
    description: '',
    address: '',
    table_size: 'M',
    perksList: []
  }
  emit('close')
}
</script>
