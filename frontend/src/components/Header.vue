<template>
  <header class="bg-gradient-to-r from-gray-900 to-indigo-900 text-white shadow-lg sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- LOGO su router-link -->
        <RouterLink to="/" class="flex items-center space-x-2 text-xl font-bold hover:text-yellow-300 transition-colors duration-200">
          <span class="text-2xl">🎲</span>
          <span class="bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 to-yellow-200">BoardGamers</span>
        </RouterLink>

        <!-- Navigacija -->
        <nav class="hidden md:flex items-center">
          <div class="flex space-x-1">
            <RouterLink to="/organizations" class="px-4 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200"
                        active-class="bg-indigo-700 text-white">
              Organizacijos
            </RouterLink>
            <RouterLink to="/events" class="px-4 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200"
                        active-class="bg-indigo-700 text-white">
              Renginiai
            </RouterLink>
            <RouterLink to="/collection" class="px-4 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200"
                        active-class="bg-indigo-700 text-white">
              Kolekcija
            </RouterLink>

            <!-- Profilio meniu -->
            <div class="relative ml-4 group">
              <button class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200">
                <span>🧑</span>
                <span>Profilis</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div class="absolute right-0 mt-2 w-48 bg-white text-black rounded-md shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform origin-top-right">
                <div class="py-1">
                  <RouterLink to="/profile">
                    <button class="block w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors duration-150">
                      Mano profilis
                    </button>
                  </RouterLink>
                  <RouterLink to="/settings">
                    <button class="block w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors duration-150">
                      Nustatymai
                    </button>
                  </RouterLink>
                </div>
              </div>
            </div>

            <!-- Atsijungimo mygtukas iškeltas į headerį -->
            <button
              @click="logout"
              class="ml-2 px-3.5 py-1.5 rounded-md border border-gray-600 text-gray-300 hover:bg-indigo-800 hover:text-white transition-colors duration-200 flex items-center gap-1.5 text-sm"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </nav>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <!-- Mobilaus atsijungimo mygtukas -->
          <button
            @click="logout"
            class="mr-2 p-2 text-gray-300 hover:text-white hover:bg-indigo-800 rounded-md transition-colors duration-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>

          <!-- Hamburgerio mygtukas -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="p-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white focus:outline-none"
          >
            <span v-if="!mobileMenuOpen">≡</span>
            <span v-else>✕</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="mobileMenuOpen" class="md:hidden">
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-indigo-950">
        <RouterLink
          to="/organizations"
          class="block px-3 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200"
          @click="mobileMenuOpen = false"
          active-class="bg-indigo-700 text-white"
        >
          Organizacijos
        </RouterLink>
        <RouterLink
          to="/events"
          class="block px-3 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200"
          @click="mobileMenuOpen = false"
          active-class="bg-indigo-700 text-white"
        >
          Renginiai
        </RouterLink>
        <RouterLink
          to="/collection"
          class="block px-3 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200"
          @click="mobileMenuOpen = false"
          active-class="bg-indigo-700 text-white"
        >
          Kolekcija
        </RouterLink>
        <div class="pt-4 pb-2 border-t border-indigo-800">
          <div class="flex items-center">
            <div class="ml-3">
              <RouterLink
                to="/profile"
                @click="mobileMenuOpen = false"
                class="block px-3 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200"
              >
                Mano profilis
              </RouterLink>
              <RouterLink
                to="/settings"
                @click="mobileMenuOpen = false"
                class="block px-3 py-2 rounded-md text-gray-200 hover:bg-indigo-800 hover:text-white transition-colors duration-200"
              >
                Nustatymai
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()
const mobileMenuOpen = ref(false)

const logout = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  router.push('/login')
}
</script>
