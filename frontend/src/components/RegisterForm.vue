<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <div class="w-full max-w-md bg-white rounded-xl shadow-md p-8">
      <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">Create Your Account</h2>

      <form @submit.prevent="register">
        <div class="mb-4">
          <label for="first_name" class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
          <input v-model="first_name" type="text" id="first_name" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-4">
          <label for="last_name" class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
          <input v-model="last_name" type="text" id="last_name" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input v-model="username" type="text" id="username" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="email" type="email" id="email" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input v-model="password" type="password" id="password" required
                 class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <button type="submit"
                class="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 transition">
          Register
        </button>
      </form>

      <p class="text-sm text-center mt-4 text-gray-600">
        Already have an account?
        <router-link to="/login" class="text-blue-600 hover:underline font-medium">Login here</router-link>
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
    alert('Registration failed')
    console.error(error)
  }
}
</script>
