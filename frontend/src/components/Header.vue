<template>
  <header class="bg-gray-800 text-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">

      <!-- LOGO su router-link -->
      <RouterLink to="/" class="text-xl font-semibold hover:text-yellow-400 transition">
        🎲 BoardGamers
      </RouterLink>

      <!-- Navigacija -->
      <nav class="hidden md:flex space-x-6">
        <RouterLink to="/organizations" class="hover:text-yellow-400 transition">Organizacijos</RouterLink>
        <RouterLink to="/collection" class="hover:text-yellow-400 transition">Kolekcija</RouterLink>
      </nav>

      <!-- Profilio ikona -->
      <div class="relative group">
        <button class="w-10 h-10 rounded-full bg-yellow-500 text-black font-bold hover:scale-105 transition">
          🧑
        </button>
        <div class="absolute right-0 mt-2 w-40 bg-white text-black rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10">
          <RouterLink to="/profile" class="block px-4 py-2 hover:bg-gray-200">Profilis</RouterLink>
          <RouterLink to="/settings" class="block px-4 py-2 hover:bg-gray-200">Nustatymai</RouterLink>
          <button @click="logout" class="block w-full text-left px-4 py-2 hover:bg-gray-200 text-red-600 font-medium">Atsijungti</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  router.push('/')
  location.reload()
}
</script>

