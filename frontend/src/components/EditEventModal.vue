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
        <input v-model="form.address" class="w-full border rounded px-3 py-2 mb-3" :disabled="isLimitedOrganizer"
               :class="{ 'bg-gray-100 cursor-not-allowed': isLimitedOrganizer }" />

        <label class="block mb-2">Stalo dydis:</label>
        <select v-model="form.table_size" class="w-full border rounded px-3 py-2 mb-3" :disabled="isLimitedOrganizer"
                :class="{ 'bg-gray-100 cursor-not-allowed': isLimitedOrganizer }">
          <option value="S">Mažas</option>
          <option value="M">Vidutinis</option>
          <option value="L">Didelis</option>
          <option value="XL">Labai didelis</option>
        </select>

        <label class="block mb-2">Viešumas:</label>
        <select v-model="form.visibility" class="w-full border rounded px-3 py-2 mb-3">
          <option value="public">Viešas</option>
          <option value="protected">Apsaugotas</option>
          <option value="private">Privatus</option>
        </select>

        <label class="block mb-2">Pradžios laikas:</label>
        <input type="datetime-local" v-model="form.start_time" class="w-full border rounded px-3 py-2 mb-3"
               :disabled="isLimitedOrganizer" :class="{ 'bg-gray-100 cursor-not-allowed': isLimitedOrganizer }" />

        <label class="block mb-2">Pabaigos laikas:</label>
        <input type="datetime-local" v-model="form.end_time" class="w-full border rounded px-3 py-2 mb-3"
               :disabled="isLimitedOrganizer" :class="{ 'bg-gray-100 cursor-not-allowed': isLimitedOrganizer }" />
      </div>

      <!-- Informacija apie ribotą redagavimą -->
      <div v-if="isLimitedOrganizer" class="mt-2 p-3 bg-yellow-50 border border-yellow-200 rounded-md text-sm text-yellow-700">
        <p><strong>Pastaba:</strong> Kadangi tapote organizatoriumi per "pirmas prisijungęs tampa organizatoriumi" funkciją,
          galite redaguoti tik renginio pavadinimą, aprašymą ir viešumą.</p>
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
import { ref, watch, computed, onMounted } from 'vue'
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

// Nustatome dabartinio vartotojo duomenis
const user = ref<any>(null)
const fetchUser = async () => {
  try {
    const res = await axios.get('/users/me/')
    user.value = res.data
  } catch (err) {
    console.error('Nepavyko gauti vartotojo informacijos:', err)
  }
}

// Ar dabartinis vartotojas yra originalus renginio kūrėjas
const isOriginalCreator = computed(() => {
  if (!props.eventData || !user.value) return false;
  return props.eventData.created_by === user.value.username;
});

// Ar dabartinis vartotojas yra organizatorius, kuris tapo juo per "pirmas prisijungęs" funkciją
const isLimitedOrganizer = computed(() => {
  if (!props.eventData || !user.value || isOriginalCreator.value) return false;

  // Jei vartotojas yra organizatorius, bet ne kūrėjas, ir renginys turi nustatymą "pirmas prisijungęs tampa organizatoriumi"
  const isOrganizer = props.eventData.organizers &&
    props.eventData.organizers.some(org => org.id === user.value.id);

  return isOrganizer && props.eventData.first_player_is_organizer;
});

watch(() => props.eventData, (newData) => {
  if (newData) {
    // Konvertuokime laikus į vietinę laiko juostą
    const startTime = new Date(newData.start_time);
    const endTime = new Date(newData.end_time);

    // Formatuojame į YYYY-MM-DDThh:mm formatą, bet vietinės laiko juostos
    const formatLocalDateTime = (date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');

      return `${year}-${month}-${day}T${hours}:${minutes}`;
    };

    form.value = {
      title: newData.title,
      description: newData.description,
      address: newData.address,
      table_size: newData.table_size,
      visibility: newData.visibility,
      start_time: formatLocalDateTime(startTime),
      end_time: formatLocalDateTime(endTime)
    }
  }
}, { immediate: true })

// Submit handler
const submitEdit = async () => {
  try {
    // Gaukime vietinį laiko poslinkį minutėmis
    const localOffset = new Date().getTimezoneOffset();

    // Paruoškime duomenis siuntimui, įvertindami laiko juostos skirtumą
    let formData = {...form.value};

    // Jei vartotojas yra ribotas organizatorius, išvalome negalimus redaguoti laukus
    if (isLimitedOrganizer.value) {
      // Išsaugome visus laukus, bet backend'e bus apdoroti tik leistini
      // Išvalyti laukai, kurie nebus siunčiami į serverį
      delete formData.address;
      delete formData.table_size;
      delete formData.start_time;
      delete formData.end_time;
    } else {
      // Jei start_time ir end_time yra įvesti
      if (formData.start_time) {
        const startDate = new Date(formData.start_time);
        formData.start_time = new Date(
          startDate.getTime() - (localOffset * 60000)
        ).toISOString();
      }

      if (formData.end_time) {
        const endDate = new Date(formData.end_time);
        formData.end_time = new Date(
          endDate.getTime() - (localOffset * 60000)
        ).toISOString();
      }
    }

    await axios.patch(`/events/${props.eventData.id}/`, formData)
    emit('updated')      // Inform parent that update was successful
    emit('close')        // Close modal
  } catch (error) {
    console.error('Klaida atnaujinant renginį:', error)
    alert('❌ Klaida atnaujinant renginį.')
  }
}

// Gaukime vartotojo informaciją, kai komponentas bus sukurtas
onMounted(() => {
  fetchUser()
})
</script>
