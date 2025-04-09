<template>
  <div class="min-h-screen bg-gray-100">
    <div class="max-w-5xl mx-auto px-4 py-12 text-center">
      <h1 class="text-4xl font-bold text-gray-800 mb-6">
        {{ greetingTitle }}
      </h1>
      <p class="text-lg text-gray-600 mb-8">{{ greetingSubtitle }}</p>

      <div v-if="isAuthenticated">
        <router-link to="/organizations" class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition">
          Eiti į organizacijas
        </router-link>
      </div>

      <div v-else class="flex justify-center space-x-4">
        <router-link to="/login" class="bg-indigo-600 text-white px-6 py-3 rounded hover:bg-indigo-700 transition">
          Prisijungti
        </router-link>
        <router-link to="/register" class="bg-gray-700 text-white px-6 py-3 rounded hover:bg-gray-800 transition">
          Registruotis
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

// Ištraukiam username iš JWT (arba localStorage, jei laikai atskirai)
const username = ref('')

onMounted(() => {
  const access = localStorage.getItem('access')
  if (access) {
    try {
      const payload = JSON.parse(atob(access.split('.')[1]))
      username.value = payload.username || 'ninja'
    } catch {
      username.value = 'ninja'
    }
  }
})

const isAuthenticated = !!localStorage.getItem('access')

const greetingTitle = computed(() =>
  isAuthenticated ? `Sveikas sugrįžęs, ${username.value}!` : 'Prisijunk prie stalo žaidimų bendruomenės!'
)

const greetingSubtitle = computed(() =>
  isAuthenticated
    ? 'Pamatyk artimiausius renginius ir organizacijas.'
    : 'Prisijunk prie bendruomenės ir pradėk žaisti šiandien.'
)
</script>


