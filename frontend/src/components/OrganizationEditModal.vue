<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-lg relative">
      <h2 class="text-xl font-bold mb-4">Redaguoti organizaciją</h2>

      <!-- Forma -->
      <div class="space-y-4">
        <div>
          <label class="block mb-1 font-medium">Pavadinimas:</label>
          <input v-model="form.name" class="w-full border rounded px-3 py-2" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Aprašymas:</label>
          <textarea v-model="form.description" class="w-full border rounded px-3 py-2" rows="3" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Miestas:</label>
          <select v-model="form.city" required class="w-full border rounded px-3 py-2">
            <option disabled value="">-- Pasirinkite miestą --</option>
            <option value="vilnius">Vilnius</option>
            <option value="kaunas">Kaunas</option>
            <option value="klaipeda">Klaipėda</option>
            <option value="siauliai">Šiauliai</option>
            <option value="panevezys">Panevėžys</option>
          </select>
        </div>

        <div>
          <label class="block mb-1 font-medium">Grupė (kategorija):</label>
          <select v-model="form.category" required class="w-full border rounded px-3 py-2">
            <option disabled value="">-- Pasirinkite kategoriją --</option>
            <option v-for="option in categories" :key="option" :value="option">{{ option }}</option>
          </select>
        </div>

        <div>
          <label class="block mb-1 font-medium">Viešumo tipas:</label>
          <select v-model="form.privacy" required class="w-full border rounded px-3 py-2">
            <option value="public">🔓 Vieša – matoma visiems</option>
            <option value="protected">🔐 Apsaugota – reikia leidimo jungtis</option>
            <option value="private">🚫 Privati – tik pakviestiesiems</option>
          </select>
        </div>
      </div>

      <!-- Mygtukai -->
      <div class="flex justify-end space-x-2 mt-6">
        <button @click="$emit('close')" class="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500">
          Atšaukti
        </button>
        <button @click="submitEdit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Išsaugoti pakeitimus
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from '@/api/axios'

const props = defineProps<{
  visible: boolean
  organization: any
}>()

const emit = defineEmits(['close', 'updated'])

const categories = [
  'Board games',
  'D&D',
  'Card games',
  'Miniatures',
  'Social deduction'
]

const form = ref({
  name: '',
  description: '',
  city: '',
  category: '',
  privacy: ''
})

watch(() => props.organization, (org) => {
  if (org) {
    form.value = {
      name: org.name || '',
      description: org.description || '',
      city: org.city || '',
      category: org.categories?.[0]?.name || '',
      privacy: org.privacy || ''
    }
  }
}, { immediate: true })

const submitEdit = async () => {
  try {
    await axios.patch(`/organizations/${props.organization.id}/`, {
      ...form.value,
      category_name: form.value.category // API naudoja šitą lauką
    })
    emit('updated')
    emit('close')
  } catch (err) {
    console.error('❌ Nepavyko atnaujinti organizacijos:', err)
    alert('Nepavyko atnaujinti organizacijos.')
  }
}
</script>
