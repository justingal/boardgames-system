<template>
  <div class="min-h-screen bg-gradient-to-b from-indigo-50 to-blue-100">
    <!-- Header with animated background -->
    <div class="relative overflow-hidden">
      <div class="absolute inset-0 z-0">
        <div class="absolute inset-0 bg-indigo-900 opacity-5"></div>
        <div class="absolute -inset-1/2 top-0 left-1/4 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-full w-96 h-96 filter blur-3xl opacity-20 animate-blob"></div>
        <div class="absolute -inset-1/2 bottom-0 right-1/4 bg-gradient-to-r from-purple-400 to-blue-500 rounded-full w-96 h-96 filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div class="absolute -inset-1/2 top-1/3 right-1/3 bg-gradient-to-r from-indigo-300 to-blue-400 rounded-full w-80 h-80 filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div class="container max-w-5xl mx-auto px-4 py-16 md:py-24 relative z-10">
        <div class="flex flex-col items-center text-center">
          <!-- Logo/Icon -->
          <div class="w-24 h-24 bg-white rounded-full shadow-lg flex items-center justify-center mb-8 animate-fadeDown">
            <svg class="w-12 h-12 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>

          <!-- Greeting -->
          <h1 class="text-4xl md:text-5xl font-bold text-gray-800 mb-4 animate-fadeDown animation-delay-300">
            {{ greetingTitle }}
          </h1>

          <p class="text-lg md:text-xl text-gray-600 mb-10 max-w-2xl animate-fadeDown animation-delay-600">
            {{ greetingSubtitle }}
          </p>

          <!-- Stats -->
          <div v-if="isAuthenticated" class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-3xl mb-12 animate-fadeUp animation-delay-900">
            <div class="bg-white rounded-xl shadow-md p-6 transform hover:scale-105 transition duration-300">
              <div class="text-indigo-600 text-3xl font-bold mb-2">{{ stats.organizationCount }}</div>
              <div class="text-gray-500">Organizacijos</div>
            </div>
            <div class="bg-white rounded-xl shadow-md p-6 transform hover:scale-105 transition duration-300">
              <div class="text-indigo-600 text-3xl font-bold mb-2">{{ stats.eventCount }}</div>
              <div class="text-gray-500">Renginiai</div>
            </div>
            <div class="bg-white rounded-xl shadow-md p-6 transform hover:scale-105 transition duration-300">
              <div class="text-indigo-600 text-3xl font-bold mb-2">{{ stats.memberCount }}</div>
              <div class="text-gray-500">Žaidėjai</div>
            </div>
          </div>

          <!-- Authenticated Buttons -->
          <div v-if="isAuthenticated" class="animate-fadeUp animation-delay-1200">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
              <router-link to="/organizations" class="flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-xl font-semibold hover:from-indigo-700 hover:to-blue-700 shadow-md transition transform hover:translate-y-[-2px]">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                Eiti į organizacijas
              </router-link>

              <router-link to="/events" class="flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-emerald-600 to-emerald-500 text-white rounded-xl font-semibold hover:from-emerald-700 hover:to-emerald-600 shadow-md transition transform hover:translate-y-[-2px]">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Artimiausieji renginiai
              </router-link>
            </div>

            <div class="mt-6">
              <button @click="logout" class="text-indigo-600 hover:text-indigo-800 text-sm font-medium transition">
                Atsijungti
              </button>
            </div>
          </div>

          <!-- Unauthenticated Buttons -->
          <div v-else class="animate-fadeUp animation-delay-1200">
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <router-link to="/login" class="flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-xl font-semibold hover:from-indigo-700 hover:to-blue-700 shadow-md transition transform hover:translate-y-[-2px]">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                Prisijungti
              </router-link>

              <router-link to="/register" class="flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-gray-700 to-gray-800 text-white rounded-xl font-semibold hover:from-gray-800 hover:to-gray-900 shadow-md transition transform hover:translate-y-[-2px]">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
                Registruotis
              </router-link>

              <router-link to="/register-organizer" class="flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-xl font-semibold hover:from-amber-600 hover:to-amber-700 shadow-md transition transform hover:translate-y-[-2px]">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                Organizatoriaus registracija
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="max-w-5xl mx-auto px-4 py-12 md:py-20 animate-fadeUp animation-delay-1500">
      <h2 class="text-2xl md:text-3xl font-bold text-center text-gray-800 mb-12">Ką siūlome?</h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition">
          <div class="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center mb-4 mx-auto">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 text-center mb-2">Bendruomenė</h3>
          <p class="text-gray-600 text-center">Susipažinkite su kitais žaidėjais ir dalinkitės patirtimi įvairiuose renginiuose.</p>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition">
          <div class="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center mb-4 mx-auto">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 text-center mb-2">Renginiai</h3>
          <p class="text-gray-600 text-center">Dalyvaukite reguliariuose žaidimų renginiuose organizuojamuose jūsų mieste.</p>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition">
          <div class="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center mb-4 mx-auto">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 text-center mb-2">Organizacijos</h3>
          <p class="text-gray-600 text-center">Kurkite ir valdykite savo organizacijas bei kvieskite žaidėjus prisijungti.</p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-indigo-900 text-white py-8 mt-12">
      <div class="max-w-5xl mx-auto px-4 text-center">
        <p>© {{ currentYear }} Žaidimų Bendruomenė | Visos teisės saugomos</p>
        <p class="mt-2 text-indigo-200">Sukurta su ❤️ Lietuvos stalo žaidimų entuziastams</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../api/axios'

const router = useRouter()
const username = ref('')
const currentYear = new Date().getFullYear()

// Statistiniai duomenys
const stats = reactive({
  organizationCount: 0,
  eventCount: 0,
  memberCount: 0
})

// Animuojame skaičius
const animateNumbers = () => {
  let duration = 2000
  let orgTarget = Math.floor(Math.random() * 20) + 10 // Random between 10-30
  let eventTarget = Math.floor(Math.random() * 50) + 20 // Random between 20-70
  let memberTarget = Math.floor(Math.random() * 100) + 50 // Random between 50-150

  const startTime = Date.now()

  const updateNumbers = () => {
    const currentTime = Date.now()
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)

    stats.organizationCount = Math.floor(orgTarget * progress)
    stats.eventCount = Math.floor(eventTarget * progress)
    stats.memberCount = Math.floor(memberTarget * progress)

    if (progress < 1) {
      requestAnimationFrame(updateNumbers)
    }
  }

  updateNumbers()
}

// Bandome gauti statistiką iš API, jei nesėkminga - naudojame atsitiktinius skaičius
const fetchStats = async () => {
  try {
    const response = await axios.get('/stats/')
    stats.organizationCount = response.data.organizations || 0
    stats.eventCount = response.data.events || 0
    stats.memberCount = response.data.users || 0
  } catch (error) {
    console.log('Naudojame atsitiktinius skaičius statistikai')
    animateNumbers()
  }
}

// Atsijungimo funkcija
const logout = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  router.push('/login')
}

onMounted(() => {
  const access = localStorage.getItem('access')
  if (access) {
    try {
      const payload = JSON.parse(atob(access.split('.')[1]))
      username.value = payload.username || 'žaidėjau'
    } catch {
      username.value = 'žaidėjau'
    }
    fetchStats()
  } else {
    animateNumbers()
  }
})

const isAuthenticated = computed(() => !!localStorage.getItem('access'))

const greetingTitle = computed(() =>
  isAuthenticated.value ? `Sveikas sugrįžęs, ${username.value}!` : 'Prisijunk prie stalo žaidimų bendruomenės!'
)

const greetingSubtitle = computed(() =>
  isAuthenticated.value
    ? 'Suplanuok savo kitą žaidimų sesiją ir prisijunk prie artėjančių renginių.'
    : 'Atrask naujus žaidimus, susipažink su bendraminčiais ir pradėk linksmintis jau šiandien!'
)
</script>

<style scoped>
@keyframes blob {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -30px) scale(1.1);
  }
  50% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  75% {
    transform: translate(30px, 30px) scale(1.05);
  }
}

@keyframes fadeDown {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animate-fadeDown {
  animation: fadeDown 0.6s forwards;
}

.animate-fadeUp {
  animation: fadeUp 0.6s forwards;
}

.animation-delay-300 {
  animation-delay: 0.3s;
}

.animation-delay-600 {
  animation-delay: 0.6s;
}

.animation-delay-900 {
  animation-delay: 0.9s;
}

.animation-delay-1200 {
  animation-delay: 1.2s;
}

.animation-delay-1500 {
  animation-delay: 1.5s;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
