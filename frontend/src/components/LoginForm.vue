<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br  px-4">
    <div class="w-full max-w-md bg-white rounded-xl shadow-lg p-8 animate-fadeIn">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-indigo-100 text-indigo-600 rounded-full mx-auto mb-4 flex items-center justify-center">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">Prisijungti prie paskyros</h2>
        <p class="text-gray-500 mt-1">Įveskite duomenis, kad prisijungtumėte</p>
      </div>

      <form @submit.prevent="login" class="space-y-5">
        <div>
          <label for="username" class="block mb-1 font-medium text-gray-700">Vartotojo vardas</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <input v-model="username" type="text" id="username" required
                   class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          </div>
        </div>

        <div>
          <label for="password" class="block mb-1 font-medium text-gray-700">Slaptažodis</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <input v-model="password" type="password" id="password" required
                   class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          </div>
        </div>

        <button type="submit"
                class="w-full bg-gradient-to-r from-indigo-600 to-blue-600 text-white font-semibold py-3 px-4 rounded-lg hover:from-indigo-700 hover:to-blue-700 shadow-md transition flex items-center justify-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
          </svg>
          Prisijungti
        </button>
      </form>

      <div class="mt-8 pt-6 border-t border-gray-200">
        <p class="text-sm text-center text-gray-600 mb-3">
          Neturi paskyros?
          <router-link to="/register" class="text-indigo-600 hover:text-indigo-800 font-medium">Registruokis čia</router-link>
        </p>
        <p class="text-sm text-center text-gray-600">
          Nori būti organizatorius?
          <router-link to="/register-organizer" class="text-indigo-600 hover:text-indigo-800 font-medium">Organizatoriaus registracija</router-link>
        </p>
      </div>
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
