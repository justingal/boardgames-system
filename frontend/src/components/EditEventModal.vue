<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
    <div class="bg-white rounded-xl shadow-2xl p-6 w-full max-w-2xl overflow-y-auto max-h-[90vh] animate-fadeIn">
      <div class="absolute top-3 right-3">
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="text-center mb-6">
        <div class="w-14 h-14 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-3">
          <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">Redaguoti renginį</h2>
        <p class="text-gray-500 mt-1">Atnaujinkite renginio informaciją</p>
      </div>

      <form class="space-y-5">
        <!-- Pavadinimas -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Pavadinimas</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <input
              v-model="form.title"
              required
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Renginio pavadinimas"
            />
          </div>
        </div>

        <!-- Aprašymas -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Aprašymas</label>
          <div class="relative">
            <div class="absolute top-3 left-3 flex items-start pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
              </svg>
            </div>
            <textarea
              v-model="form.description"
              class="w-full border rounded-lg pl-10 pr-3 py-2 min-h-[100px] focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Trumpas renginio aprašymas..."
            ></textarea>
          </div>
        </div>

        <!-- Adresas -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Adresas</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <input
              v-model="form.address"
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              :class="{ 'bg-gray-100 cursor-not-allowed': isLimitedOrganizer }"
              placeholder="Renginio vieta"
              :disabled="isLimitedOrganizer"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- Stalo dydis -->
          <div>
            <label class="block mb-1 font-medium text-gray-700">Stalo dydis</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
              </div>
              <select
                v-model="form.table_size"
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                :class="{ 'bg-gray-100 cursor-not-allowed': isLimitedOrganizer }"
                :disabled="isLimitedOrganizer"
              >
                <option value="S">Mažas</option>
                <option value="M">Vidutinis</option>
                <option value="L">Didelis</option>
                <option value="XL">Labai didelis</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Viešumas -->
          <div>
            <label class="block mb-1 font-medium text-gray-700">Viešumas</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <select
                v-model="form.visibility"
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="public">🔓 Viešas</option>
                <option value="protected">🔐 Apsaugotas</option>
                <option value="private">🚫 Privatus</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- Pradžios laikas -->
          <div>
            <label class="block mb-1 font-medium text-gray-700">Pradžios laikas</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <input
                type="datetime-local"
                v-model="form.start_time"
                class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                :class="{ 'bg-gray-100 cursor-not-allowed': isLimitedOrganizer }"
                :disabled="isLimitedOrganizer"
              />
            </div>
          </div>

          <!-- Pabaigos laikas -->
          <div>
            <label class="block mb-1 font-medium text-gray-700">Pabaigos laikas</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <input
                type="datetime-local"
                v-model="form.end_time"
                class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                :class="{ 'bg-gray-100 cursor-not-allowed': isLimitedOrganizer }"
                :disabled="isLimitedOrganizer"
              />
            </div>
          </div>
        </div>

        <!-- Informacija apie ribotą redagavimą -->
        <div v-if="isLimitedOrganizer" class="p-4 bg-amber-50 rounded-lg border border-amber-100">
          <div class="flex">
            <div class="mr-3 flex-shrink-0">
              <svg class="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-sm text-amber-800">
              <p class="font-medium">Ribotos redagavimo teisės</p>
              <p class="mt-1">Kadangi tapote organizatoriumi per "pirmas prisijungęs tampa organizatoriumi" funkciją, galite redaguoti tik renginio pavadinimą, aprašymą ir viešumą.</p>
            </div>
          </div>
        </div>

        <!-- Veiksmai -->
        <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition shadow-sm flex items-center gap-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Atšaukti
          </button>
          <button
            type="button"
            @click="submitEdit"
            class="px-5 py-2 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg hover:from-indigo-700 hover:to-blue-700 transition shadow-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Išsaugoti pakeitimus
          </button>
        </div>
      </form>
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
