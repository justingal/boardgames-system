<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <div class="w-full max-w-md bg-white rounded-xl shadow-md p-8">
      <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">Sukurti paskyrą</h2>

      <form @submit.prevent="register">
        <div class="mb-4">
          <label for="first_name" class="block text-sm font-medium text-gray-700 mb-1">Vardas</label>
          <input v-model="first_name" type="text" id="first_name" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-4">
          <label for="last_name" class="block text-sm font-medium text-gray-700 mb-1">Pavardė</label>
          <input v-model="last_name" type="text" id="last_name" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Vartotojo vardas</label>
          <input v-model="username" type="text" id="username" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">El.paštas</label>
          <input v-model="email" type="email" id="email" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Slaptažodis</label>
          <input v-model="password" type="password" id="password" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <button type="submit"
                class="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 transition">
          Registruotis
        </button>
      </form>

      <p class="text-sm text-center mt-4 text-gray-600">
        Jau turite paskyrą?
        <router-link to="/login" class="text-blue-600 hover:underline font-medium">Prisijungti čia</router-link>
      </p>
      <p class="text-sm text-center mt-4 text-gray-600">
        Nori būti organizatorius?
        <router-link to="/register-organizer" class="text-blue-600 hover:underline font-medium">Organizatoriaus registracija</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../api/axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const first_name = ref('')
const last_name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')

const register = async () => {
  try {
    await axios.post('/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      first_name: first_name.value,
      last_name: last_name.value
    })

    alert('Account created! You can now log in.')
    router.push('/login')
  } catch (error) {
    if (error.response && error.response.data.password) {
      alert('Slaptažodžio klaida: ' + error.response.data.password.join(', '))
    }
    if (error.response && error.response.data.username) {
      alert('Vartotojo vardo klaida: ' + error.response.data.username.join(', '))
    }
  }
}
</script>
