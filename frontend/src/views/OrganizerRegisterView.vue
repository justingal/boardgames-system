<template>
  <div class="max-w-xl mx-auto mt-10 p-6 bg-white shadow rounded-lg">
    <h1 class="text-2xl font-bold mb-4 text-center">Registracija – Organizatoriui</h1>

    <form @submit.prevent="submit">
      <!-- Vartotojo info -->
      <input v-model="form.username" placeholder="Vartotojo vardas" required
             class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />
      <input v-model="form.email" placeholder="El. paštas" required
             class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />
      <input v-model="form.password" type="password" placeholder="Slaptažodis" required
             class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />
      <input v-model="form.first_name" placeholder="Vardas" required
             class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />
      <input v-model="form.last_name" placeholder="Pavardė" required
             class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />


      <h2 class="text-lg font-semibold mb-2 mt-6 text-center text-gray-700">🎯 Kuriama organizacija</h2>

      <!-- Organizacijos info -->
      <input v-model="form.organization.name" placeholder="Organizacijos pavadinimas" required
             class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />
      <textarea v-model="form.organization.description" placeholder="Aprašymas"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />

      <select v-model="form.organization.privacy" required
              class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3">
        <option value="public">Vieša</option>
        <option value="protected">Apsaugota</option>
        <option value="private">Privati</option>
      </select>

      <select v-model="form.organization.category" required
              class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3">
        <option disabled value="">-- Pasirinkite kategoriją --</option>
        <option v-for="cat in categories" :key="cat.value" :value="cat.value">{{ cat.name }}</option>
      </select>

      <select v-model="form.organization.city" required
              class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3">
        <option value="vilnius">Vilnius</option>
        <option value="kaunas">Kaunas</option>
        <option value="klaipeda">Klaipėda</option>
        <option value="siauliai">Šiauliai</option>
        <option value="panevezys">Panevėžys</option>
      </select>

      <button type="submit"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg mt-4 hover:bg-blue-700 w-full">
        Registruotis
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../api/axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// Hardcoded categories matching backend CATEGORY_CHOICES
const categories = [
  { value: 'classic_strategic', name: 'Klasikiniai & Strateginiai' },
  { value: 'rpg', name: 'RPG (Role-playing games)' },
  { value: 'miniature_games', name: 'Miniatiūrų žaidimai' },
  { value: 'party_social', name: 'Vakarėlių ir socialiniai žaidimai' },
  { value: 'children_games', name: 'Vaikų žaidimai' },
  { value: 'educational', name: 'Edukaciniai žaidimai' }
]

const form = ref({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  organization: {
    name: '',
    description: '',
    privacy: 'protected',
    category: 'classic_strategic',
    city: 'vilnius',
  }
})

const submit = async () => {
  try {
    await axios.post('/register/organizer/', form.value)
    alert('Registracija sėkminga! Dabar prisijunkite.')
    router.push('/login')
  } catch (error) {
    if (error.response && error.response.data.password) {
      alert('Slaptažodžio klaida: ' + error.response.data.password.join(', '))
    }
    else if (error.response && error.response.data.username) {
      alert('Vartotojo vardo klaida: ' + error.response.data.username.join(', '))
    } else if (error.response && error.response.data.email) {
      alert('El. pašto klaida: ' + error.response.data.email.join(', '))
    } else if (error.response && error.response.data.organization) {
      alert('Organizacijos klaida: ' + error.response.data.organization.join(', '))
    } else {
      console.error('Nežinoma klaida:', error)
      alert('Įvyko klaida registruojantis.')
    }
  }
}
</script>
