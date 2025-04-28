<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-lg relative">
      <h2 class="text-xl font-bold mb-4">Redaguoti renginį</h2>

      <!-- Form -->
      <div>
        <label class="block mb-2">Pavadinimas:</label>
        <input v-model="form.title" class="w-full border rounded px-3 py-2 mb-3" />

        <label class="block mb-2">Aprašymas:</label>
        <textarea v-model="form.description" class="w-full border rounded px-3 py-2 mb-3"></textarea>

        <label class="block mb-2">Adresas:</label>
        <input v-model="form.address" class="w-full border rounded px-3 py-2 mb-3" />

        <label class="block mb-2">Stalo dydis:</label>
        <select v-model="form.table_size" class="w-full border rounded px-3 py-2 mb-3">
          <option value="S">Mažas</option>
          <option value="M">Vidutinis</option>
          <option value="L">Didelis</option>
        </select>

        <label class="block mb-2">Viešumas:</label>
        <select v-model="form.visibility" class="w-full border rounded px-3 py-2 mb-3">
          <option value="public">Viešas</option>
          <option value="protected">Apsaugotas</option>
          <option value="private">Privatus</option>
        </select>

        <label class="block mb-2">Pradžios laikas:</label>
        <input type="datetime-local" v-model="form.start_time" class="w-full border rounded px-3 py-2 mb-3" />

        <label class="block mb-2">Pabaigos laikas:</label>
        <input type="datetime-local" v-model="form.end_time" class="w-full border rounded px-3 py-2 mb-3" />
      </div>

      <!-- Buttons -->
      <div class="flex justify-end space-x-2 mt-4">
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

// Props
const props = defineProps<{
  visible: boolean
  eventData: any
}>()

const emit = defineEmits(['close', 'updated'])

// Local form state
const form = ref({
  title: '',
  description: '',
  address: '',
  table_size: '',
  visibility: '',
  start_time: '',
  end_time: ''
})

// Sync form fields when modal opens
watch(() => props.eventData, (newData) => {
  if (newData) {
    form.value = {
      title: newData.title,
      description: newData.description,
      address: newData.address,
      table_size: newData.table_size,
      visibility: newData.visibility,
      start_time: newData.start_time?.slice(0, 16),
      end_time: newData.end_time?.slice(0, 16)
    }
  }
}, { immediate: true })

// Submit handler
const submitEdit = async () => {
  try {
    await axios.patch(`/events/${props.eventData.id}/`, form.value)
    emit('updated')      // Inform parent that update was successful
    emit('close')        // Close modal
  } catch (error) {
    console.error('Klaida atnaujinant renginį:', error)
    alert('❌ Klaida atnaujinant renginį.')
  }
}
</script>
