<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-blue-100 px-4 py-8">
    <div class="w-full max-w-2xl bg-white rounded-xl shadow-lg p-8 animate-fadeIn">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-indigo-100 text-indigo-600 rounded-full mx-auto mb-4 flex items-center justify-center">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">Registracija – Organizatoriui</h2>
        <p class="text-gray-500 mt-1">Sukurkite organizatoriaus paskyrą ir organizaciją</p>
      </div>

      <form @submit.prevent="submit" class="space-y-6">
        <!-- Vartotojo informacija sekcija -->
        <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
          <h3 class="text-lg font-semibold mb-4 text-indigo-700 flex items-center border-b pb-2">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Asmeninė informacija
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block mb-1 text-sm font-medium text-gray-700">Vartotojo vardas</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input
                  v-model="form.username"
                  placeholder="Vartotojo vardas"
                  required
                  class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            </div>

            <div>
              <label class="block mb-1 text-sm font-medium text-gray-700">El. paštas</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <input
                  v-model="form.email"
                  type="email"
                  placeholder="El. paštas"
                  required
                  class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            </div>

            <div>
              <label class="block mb-1 text-sm font-medium text-gray-700">Slaptažodis</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input
                  v-model="form.password"
                  type="password"
                  placeholder="Slaptažodis"
                  required
                  class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            </div>

            <div class="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block mb-1 text-sm font-medium text-gray-700">Vardas</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <input
                    v-model="form.first_name"
                    placeholder="Vardas"
                    required
                    class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label class="block mb-1 text-sm font-medium text-gray-700">Pavardė</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <input
                    v-model="form.last_name"
                    placeholder="Pavardė"
                    required
                    class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Organizacijos informacija sekcija -->
        <div class="bg-indigo-50 rounded-lg p-6 border border-indigo-100">
          <h3 class="text-lg font-semibold mb-4 text-indigo-700 flex items-center border-b pb-2">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Kuriama organizacija
          </h3>

          <div class="space-y-4">
            <div>
              <label class="block mb-1 text-sm font-medium text-gray-700">Organizacijos pavadinimas</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                </div>
                <input
                  v-model="form.organization.name"
                  placeholder="Organizacijos pavadinimas"
                  required
                  class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            </div>

            <div>
              <label class="block mb-1 text-sm font-medium text-gray-700">Aprašymas</label>
              <div class="relative">
                <div class="absolute top-3 left-3 flex items-start pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
                  </svg>
                </div>
                <textarea
                  v-model="form.organization.description"
                  placeholder="Aprašymas"
                  rows="3"
                  class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                ></textarea>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block mb-1 text-sm font-medium text-gray-700">Viešumas</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </div>
                  <select
                    v-model="form.organization.privacy"
                    required
                    class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="public">🔓 Vieša</option>
                    <option value="protected">🔐 Apsaugota</option>
                    <option value="private">🚫 Privati</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              <div>
                <label class="block mb-1 text-sm font-medium text-gray-700">Kategorija</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                  </div>
                  <select
                    v-model="form.organization.category"
                    required
                    class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option disabled value="">-- Pasirinkite kategoriją --</option>
                    <option v-for="cat in categories" :key="cat.value" :value="cat.value">{{ cat.name }}</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              <div>
                <label class="block mb-1 text-sm font-medium text-gray-700">Miestas</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <select
                    v-model="form.organization.city"
                    required
                    class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="vilnius">Vilnius</option>
                    <option value="kaunas">Kaunas</option>
                    <option value="klaipeda">Klaipėda</option>
                    <option value="siauliai">Šiauliai</option>
                    <option value="panevezys">Panevėžys</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Informacinė žinutė -->
        <div class="p-4 bg-blue-50 rounded-lg border border-blue-100">
          <div class="flex">
            <div class="mr-3 flex-shrink-0">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-sm text-blue-800">
              <p class="font-medium">Svarbi informacija</p>
              <p class="mt-1">Sukūrę organizatoriaus paskyrą, galėsite kurti ir valdyti žaidimų renginius, kviesti dalyvius ir plėsti bendruomenę.</p>
            </div>
          </div>
        </div>

        <!-- Registracijos mygtukas -->
        <button
          type="submit"
          class="w-full bg-gradient-to-r from-indigo-600 to-blue-600 text-white font-semibold py-3 px-4 rounded-lg hover:from-indigo-700 hover:to-blue-700 shadow-md transition flex items-center justify-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
          Registruotis
        </button>
      </form>

      <div class="mt-6 pt-4 border-t border-gray-200 text-center">
        <p class="text-sm text-gray-600">
          Jau užsiregistravote?
          <router-link to="/login" class="text-indigo-600 hover:text-indigo-800 font-medium">Prisijungti čia</router-link>
        </p>
        <p class="text-sm text-gray-600 mt-2">
          Reikia pagalbos?
          <a href="#" class="text-indigo-600 hover:text-indigo-800 font-medium">Susisiekite su mumis</a>
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

// Hardcoded categories matching backend CATEGORY_CHOICES
const categories = [
  { value: 'classic_strategic', name: 'Klasikiniai & Strateginiai' },
  { value: 'rpg', name: 'RPG (Role-playing games)' },
  { value: 'miniature_games', name: 'Miniatiūrų žaidimai' },
  { value: 'party_social', name: 'Vakarėlių ir socialiniai žaidimai' },
  { value: 'children_games', name: 'Vaikų žaidimai' },
  { value: 'educational', name: 'Edukaciniai žaidimai' }
]

const form = ref({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  organization: {
    name: '',
    description: '',
    privacy: 'protected',
    category: 'classic_strategic',
    city: 'vilnius',
  }
})

const submit = async () => {
  try {
    await axios.post('/register/organizer/', form.value)
    alert('Registracija sėkminga! Dabar prisijunkite.')
    router.push('/login')
  } catch (error) {
    if (error.response && error.response.data.password) {
      alert('Slaptažodžio klaida: ' + error.response.data.password.join(', '))
    }
    else if (error.response && error.response.data.username) {
      alert('Vartotojo vardo klaida: ' + error.response.data.username.join(', '))
    } else if (error.response && error.response.data.email) {
      alert('El. pašto klaida: ' + error.response.data.email.join(', '))
    } else if (error.response && error.response.data.organization) {
      alert('Organizacijos klaida: ' + error.response.data.organization.join(', '))
    } else {
      console.error('Nežinoma klaida:', error)
      alert('Įvyko klaida registruojantis.')
    }
  }
}
</script>
