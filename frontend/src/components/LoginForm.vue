<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <div class="w-full max-w-md bg-white rounded-xl shadow-md p-8">
      <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">Prisijungti prie paskyros</h2>

      <form @submit.prevent="login">
        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Vartotojo vardas</label>
          <input v-model="username" type="text" id="username" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Slaptažodis</label>
          <input v-model="password" type="password" id="password" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <button type="submit"
                class="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 transition">
          Prisijungti
        </button>
      </form>

      <p class="text-sm text-center mt-4 text-gray-600">
        Neturi paskyros?
        <router-link to="/register" class="text-blue-600 hover:underline font-medium">Registruokis čia</router-link>
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

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const response = await axios.post('/token/', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('access', response.data.access)
    localStorage.setItem('refresh', response.data.refresh)

    router.push('/')
  } catch (error) {
    alert('Login failed')
    console.error(error)
  }
}
</script>
