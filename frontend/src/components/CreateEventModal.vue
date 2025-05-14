<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
    <div class="bg-white rounded-xl shadow-2xl p-6 w-full max-w-2xl overflow-y-auto max-h-[90vh] animate-fadeIn">
      <div class="absolute top-3 right-3">
        <button @click="close" class="text-gray-400 hover:text-gray-600 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="text-center mb-6">
        <div class="w-14 h-14 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-3">
          <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">Sukurti renginį</h2>
        <p class="text-gray-500 mt-1">Užpildykite formą, kad sukurti naują stalo žaidimų renginį</p>
      </div>

      <form @submit.prevent="submit" class="space-y-5">
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
              required
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        <!-- Organizacija -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Organizacija</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <select
              v-model="form.organization"
              required
              class="w-full border rounded-lg pl-10 pr-3 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option disabled value="">-- Pasirinkite organizaciją --</option>
              <option v-for="org in userOrganizations" :key="org.id" :value="org.id">
                {{ org.name }}
              </option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Pradžios ir pabaigos data + laikas -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="border rounded-lg p-4 bg-gray-50">
            <div class="flex items-center mb-2">
              <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <label class="font-medium text-gray-700">Pradžia</label>
            </div>
            <input
              v-model="form.start_date"
              type="date"
              required
              class="w-full border rounded-lg px-3 py-2 mb-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
            <div class="flex items-center mt-1 mb-2">
              <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <label class="font-medium text-gray-700">Laikas</label>
            </div>
            <input
              v-model="form.start_time"
              type="time"
              required
              class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div class="border rounded-lg p-4 bg-gray-50">
            <div class="flex items-center mb-2">
              <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <label class="font-medium text-gray-700">Pabaiga</label>
            </div>
            <input
              v-model="form.end_date"
              type="date"
              required
              class="w-full border rounded-lg px-3 py-2 mb-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
            <div class="flex items-center mt-1 mb-2">
              <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <label class="font-medium text-gray-700">Laikas</label>
            </div>
            <input
              v-model="form.end_time"
              type="time"
              required
              class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

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
              required
              class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="S">Mažas (2 žmonės) ~ 80x80cm</option>
              <option value="M">Vidutinis (4 žmonės) ~ 120x80cm</option>
              <option value="L">Didelis (6-8 žmonės) ~ 180x90cm</option>
              <option value="XL">Labai didelis (8-10 žmonių) ~ 200x100cm</option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
          <label class="flex items-center space-x-3 mt-3 py-2 px-3 rounded-lg bg-indigo-50 border border-indigo-100">
            <input type="checkbox" v-model="form.first_player_is_organizer" class="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
            <div>
              <span class="font-medium text-gray-700">Pirmas prisijungęs tampa organizatoriumi</span>
              <p class="text-xs text-gray-500 mt-0.5">Pirmasis prisijungęs žaidėjas automatiškai gaus organizatoriaus teises</p>
            </div>
          </label>
        </div>

        <!-- Papildomos galimybės (Perks) -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Papildomos galimybės (Perks)</label>
          <details class="bg-gray-50 border rounded-lg p-4">
            <summary class="cursor-pointer font-medium text-gray-700 flex items-center">
              <svg class="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Pasirinkti galimybes
            </summary>
            <div class="mt-3 flex flex-wrap gap-3">
              <label v-for="perk in allPerks" :key="perk" class="flex items-center gap-2 bg-white border rounded-lg px-3 py-2 hover:bg-gray-50 transition">
                <input type="checkbox" :value="perk" v-model="form.perksList" class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
                <span>{{ perk }}</span>
              </label>
            </div>
            <div v-if="form.perksList.length" class="mt-3 p-3 bg-indigo-50 rounded-lg text-sm text-gray-700">
              <div class="font-medium mb-1">Pasirinkta:</div>
              <div class="flex flex-wrap gap-2">
                <span v-for="perk in form.perksList" :key="perk" class="bg-white px-2 py-1 rounded-md border border-indigo-200">
                  {{ perk }}
                </span>
              </div>
            </div>
          </details>
        </div>

        <!-- Kartojasi datos -->
        <div class="border rounded-lg p-4 bg-gray-50">
          <label class="inline-flex items-center space-x-3">
            <input type="checkbox" v-model="form.is_repeating" class="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
            <div>
              <span class="font-medium text-gray-700">Renginys kartojasi pasirinktomis datomis</span>
              <p class="text-xs text-gray-500 mt-0.5">Pasirinkite, ar šis renginys vyks daugiau nei vieną kartą</p>
            </div>
          </label>

          <div v-if="form.is_repeating" class="mt-4">
            <p class="mb-2 text-sm text-gray-600">Pasirinkite konkrečias kalendoriaus datas, kuriomis norite kartoti renginį:</p>
            <!-- Using your RepeatDatePicker component -->
            <RepeatDatePicker v-model="form.repeat_days" />
            <div class="mt-2 text-xs text-gray-500 flex items-start p-2 bg-indigo-50 rounded-md border border-indigo-100">
              <svg class="w-4 h-4 text-indigo-500 mr-1 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Pastaba: Pasirinkite tikslias datas. Renginys bus kartojamas tik pasirinktomis datomis.</span>
            </div>
          </div>
        </div>

        <!-- Veiksmai -->
        <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
          <button
            type="button"
            @click="close"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition shadow-sm flex items-center gap-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Atšaukti
          </button>
          <button
            type="submit"
            class="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition shadow-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Sukurti
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/axios'
import RepeatDatePicker from '../components/RepeatDatePicker.vue'

const props = defineProps({
  show: Boolean
})
const emit = defineEmits(['close', 'created'])

const userOrganizations = ref([])

const form = ref({
  title: '',
  description: '',
  address: '',
  organization: '',
  start_date: '',
  end_date: '',
  start_time: '',
  end_time: '',
  table_size: 'M',
  perksList: [],
  is_repeating: false,
  repeat_days: [],
  first_player_is_organizer: true
})

const allPerks = [
  'Atskira salė',
  'Leidžiama triukšmauti',
  'Prieiga prie virtuvėlės',
  'Projektorius',
  'Oro kondicionierius',
  'Galima naudoti garsiakalbius',
  'Lentynos žaidimams',
  'Stalo apšvietimas',
  'Privatus įėjimas',
  'Šalia WC',
  'Galimybė užrakinti stalą',
  'Stalas pritaikytas neįgaliesiems',
  'Parkavimas šalia',
  'Vieta puodeliui'
]

const fetchOrganizations = async () => {
  try {
    const token = localStorage.getItem('access')
    const response = await axios.get('/organizations/user/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    userOrganizations.value = response.data
  } catch (err) {
    console.error('Nepavyko gauti organizacijų:', err)
  }
}

onMounted(() => {
  fetchOrganizations()
  // Set default dates to today
  const today = new Date()
  const yyyy = today.getFullYear()
  const mm = String(today.getMonth() + 1).padStart(2, '0')
  const dd = String(today.getDate()).padStart(2, '0')
  const formattedDate = `${yyyy}-${mm}-${dd}`

  form.value.start_date = formattedDate
  form.value.end_date = formattedDate
  form.value.start_time = '09:00'
  form.value.end_time = '10:00'
})

// Konvertuoja pasirinktas datas į formą, kuri tinkama API
function formatRepeatDaysForAPI(dates) {
  if (!dates || !dates.length) return '';

  // Grąžiname datas kaip išrinktų datų ISO YYYY-MM-DD formatu sarašą
  return dates.join(',');
}

const submit = async () => {
  try {
    const token = localStorage.getItem('access')

    // Įsitikinime, kad first_player_is_organizer yra teisingai perduodamas
    const isFirstPlayerOrganizer = form.value.first_player_is_organizer === true;

    // Sukuriame vietinius DateTime objektus pradžios ir pabaigos laikams
    let startDate = new Date(`${form.value.start_date}T${form.value.start_time}`);
    let endDate = new Date(`${form.value.end_date}T${form.value.end_time}`);

    // Gaukime vietinį laiko poslinkį minutėmis
    const localOffset = new Date().getTimezoneOffset();

    // Konvertuokime į ISO string, bet išsaugodami vietinį laiką
    const startISOString = new Date(
      startDate.getTime() - (localOffset * 60000)
    ).toISOString();

    const endISOString = new Date(
      endDate.getTime() - (localOffset * 60000)
    ).toISOString();

    // Paruošiame pasikartojančias datas - svarbu išlaikyti formatą
    // Išsaugome pilnus datų stringus YYYY-MM-DD formatu
    const repeatedDays = form.value.is_repeating && form.value.repeat_days.length
      ? form.value.repeat_days.join(',')
      : '';

    const payload = {
      title: form.value.title,
      description: form.value.description,
      address: form.value.address,
      start_time: startISOString,
      end_time: endISOString,
      table_size: form.value.table_size,
      perks: form.value.perksList.join(', '),
      is_repeating: form.value.is_repeating,
      repeat_days: repeatedDays,
      organization: form.value.organization,
      first_player_is_organizer: isFirstPlayerOrganizer
    }

    console.log('Siunčiami duomenys:', payload);

    await axios.post('/events/', payload, {
      headers: { Authorization: `Bearer ${token}` }
    })

    emit('created')
    close()
  } catch (err) {
    console.error('Nepavyko sukurti renginio:', err)
    alert('Klaida kuriant renginį: ' + (err.response?.data?.message || err.message))
  }
}

const close = () => {
  form.value = {
    title: '',
    description: '',
    address: '',
    organization: '',
    start_date: '',
    end_date: '',
    start_time: '',
    end_time: '',
    table_size: 'M',
    perksList: [],
    is_repeating: false,
    repeat_days: [],
    first_player_is_organizer: true
  }
  emit('close')
}
</script>

<style>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Stilius papildomiems elementams */
input[type="checkbox"] {
  cursor: pointer;
}

summary {
  list-style: none;
}

summary::-webkit-details-marker {
  display: none;
}

summary::after {
  content: '+';
  display: inline-block;
  margin-left: 10px;
  font-weight: bold;
  transition: transform 0.2s;
}

details[open] summary::after {
  transform: rotate(45deg);
}
</style>
