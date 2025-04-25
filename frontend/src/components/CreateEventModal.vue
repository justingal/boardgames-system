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

        <!-- Organizacija -->
        <div class="mb-4">
          <label class="block mb-1 font-medium">Organizacija</label>
          <select v-model="form.organization" required class="w-full border rounded-lg px-3 py-2">
            <option disabled value="">-- Pasirinkite organizaciją --</option>
            <option v-for="org in userOrganizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>

        <!-- Pradžios ir pabaigos data + laikas -->
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block mb-1 font-medium">Pradžios data</label>
            <input v-model="form.start_date" type="date" required class="w-full border rounded-lg px-3 py-2" />
            <label class="block mb-1 font-medium mt-2">Laikas</label>
            <input v-model="form.start_time" type="time" required class="w-full border rounded-lg px-3 py-2" />
          </div>
          <div>
            <label class="block mb-1 font-medium">Pabaigos data</label>
            <input v-model="form.end_date" type="date" required class="w-full border rounded-lg px-3 py-2" />
            <label class="block mb-1 font-medium mt-2">Laikas</label>
            <input v-model="form.end_time" type="time" required class="w-full border rounded-lg px-3 py-2" />
          </div>
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
          <label class="flex items-center space-x-2 mt-4">
            <input type="checkbox" v-model="form.first_player_is_organizer" />
            <span>Pirmas prisijungęs tampa organizatoriumi</span>
          </label>
        </div>


        <!-- Perk'ai -->
        <div class="mb-6">
          <label class="block mb-1 font-medium">Papildomos galimybės (Perks)</label>
          <details class="bg-gray-50 border rounded-lg p-3">
            <summary class="cursor-pointer font-medium text-gray-700">Pasirinkti galimybes</summary>
            <div class="mt-3 flex flex-wrap gap-3">
              <label v-for="perk in allPerks" :key="perk" class="flex items-center gap-2">
                <input type="checkbox" :value="perk" v-model="form.perksList" />
                <span>{{ perk }}</span>
              </label>
            </div>
            <div v-if="form.perksList.length" class="mt-2 text-sm text-gray-600">
              Pasirinkta: {{ form.perksList.join(', ') }}
            </div>
          </details>
        </div>

        <!-- Kartojasi datos -->
        <div class="mb-6">
          <label class="inline-flex items-center space-x-2">
            <input type="checkbox" v-model="form.is_repeating" />
            <span>Renginys kartojasi pasirinktomis datomis</span>
          </label>

          <div v-if="form.is_repeating" class="mt-4">
            <p class="mb-2 text-sm text-gray-600">Pasirinkite konkrečias kalendoriaus datas, kuriomis norite kartoti renginį tuo pačiu metu:</p>
            <RepeatDatePicker v-model="form.repeat_days" />
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
  repeat_days: []
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

const submit = async () => {
  try {
    const token = localStorage.getItem('access')
    const payload = {
      title: form.value.title,
      description: form.value.description,
      address: form.value.address,
      start_time: `${form.value.start_date}T${form.value.start_time}`,
      end_time: `${form.value.end_date}T${form.value.end_time}`,
      table_size: form.value.table_size,
      perks: form.value.perksList.join(', '),
      is_repeating: form.value.is_repeating,
      repeat_days: form.value.repeat_days.length ? form.value.repeat_days.join(',') : '',
      organization: form.value.organization,
      first_player_is_organizer: form.value.first_player_is_organizer ?? true, // 🟢 ŠITAS SVARBIAUSIAS!
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
    repeat_days: []
  }
  emit('close')
}
</script>
