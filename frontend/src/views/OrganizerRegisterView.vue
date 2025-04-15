<template>
  <div class="max-w-xl mx-auto mt-10 p-6 bg-white shadow rounded-lg">
    <h1 class="text-2xl font-bold mb-4 text-center">Registracija – Organizatoriui</h1>

    <form @submit.prevent="submit">
      <!-- Vartotojo info -->
      <input v-model="form.username" placeholder="Vardas" required
             class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />
      <input v-model="form.email" placeholder="El. paštas" required
             class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3" />
      <input v-model="form.password" type="password" placeholder="Slaptažodis" required
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
        <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
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

const categories = ['Board games', 'D&D', 'Card games', 'Miniatures', 'Social deduction']

const form = ref({
  username: '',
  email: '',
  password: '',
  organization: {
    name: '',
    description: '',
    privacy: 'protected',
    category: '',
    city: 'vilnius',
  }
})

const submit = async () => {
  try {
    await axios.post('/register/organizer/', form.value)
    alert('Registracija sėkminga! Dabar prisijunkite.')
    router.push('/login')
  } catch (error) {
    console.error('Registracijos klaida:', error)
    alert('Nepavyko užsiregistruoti.')
  }
}
</script>
