<template>
  <div class="max-w-md mx-auto mt-12 p-6 bg-white shadow rounded">
    <h1 class="text-2xl font-bold mb-6">Registracija organizatoriui</h1>
    <form @submit.prevent="register">
      <div class="mb-4">
        <label class="block mb-1 font-medium">Vartotojo vardas</label>
        <input v-model="username" required class="w-full border p-2 rounded" />
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-medium">El. paštas</label>
        <input v-model="email" type="email" required class="w-full border p-2 rounded" />
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-medium">Slaptažodis</label>
        <input v-model="password" type="password" required class="w-full border p-2 rounded" />
      </div>
      <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        Registruotis kaip organizatorius
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../api/axios'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const router = useRouter()

const register = async () => {
  try {
    await axios.post('/register/organizer/', {
      username: username.value,
      email: email.value,
      password: password.value,
    })
    alert('Registracija sėkminga!')
    router.push('/login')
  } catch (error) {
    alert('Klaida registruojantis.')
    console.error(error)
  }
}
</script>
