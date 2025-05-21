<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-blue-100 px-4 py-8">
    <div class="w-full max-w-md bg-white rounded-xl shadow-lg p-8 animate-fadeIn">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-indigo-100 text-indigo-600 rounded-full mx-auto mb-4 flex items-center justify-center">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">Sukurti paskyrą</h2>
        <p class="text-gray-500 mt-1">Užpildykite formą, kad sukurtumėte naują paskyrą</p>
      </div>

      <form @submit.prevent="register" class="space-y-4">
        <div>
          <label for="first_name" class="block mb-1 font-medium text-gray-700">Vardas</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <input
              v-model="first_name"
              type="text"
              id="first_name"
              required
              placeholder="Įveskite savo vardą"
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        <div>
          <label for="last_name" class="block mb-1 font-medium text-gray-700">Pavardė</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <input
              v-model="last_name"
              type="text"
              id="last_name"
              required
              placeholder="Įveskite savo pavardę"
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        <div>
          <label for="username" class="block mb-1 font-medium text-gray-700">Vartotojo vardas</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <input
              v-model="username"
              type="text"
              id="username"
              required
              placeholder="Pasirinkite vartotojo vardą"
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        <div>
          <label for="email" class="block mb-1 font-medium text-gray-700">El. paštas</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <input
              v-model="email"
              type="email"
              id="email"
              required
              placeholder="jusu.pastas@pavyzdys.lt"
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
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
            <input
              v-model="password"
              type="password"
              id="password"
              required
              placeholder="Sukurkite saugų slaptažodį"
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        <!-- Informacinė žinutė apie slaptažodį -->
        <div class="p-4 bg-blue-50 rounded-lg border border-blue-100">
          <div class="flex">
            <div class="mr-3 flex-shrink-0">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-sm text-blue-800">
              <p class="font-medium">Reikalavimai slaptažodžiui</p>
              <p class="mt-1">Slaptažodis turi būti bent 8 simbolių ilgio ir turėti bent vieną didžiąją raidę, vieną mažąją raidę ir vieną skaičių.</p>
            </div>
          </div>
        </div>

        <button
          type="submit"
          class="w-full bg-gradient-to-r from-indigo-600 to-blue-600 text-white font-semibold py-3 px-4 rounded-lg hover:from-indigo-700 hover:to-blue-700 shadow-md transition mt-6 flex items-center justify-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Registruotis
        </button>
      </form>

      <div class="mt-8 pt-6 border-t border-gray-200">
        <p class="text-sm text-center text-gray-600 mb-3">
          Jau turite paskyrą?
          <router-link to="/login" class="text-indigo-600 hover:text-indigo-800 font-medium">Prisijungti čia</router-link>
        </p>
        <p class="text-sm text-center text-gray-600">
          Norite būti organizatorius?
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
