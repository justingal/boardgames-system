<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
    <div class="bg-white rounded-xl shadow-2xl p-6 w-full max-w-2xl overflow-y-auto max-h-[90vh] animate-fadeIn">
      <div class="absolute top-3 right-3">
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="text-center mb-6">
        <div class="w-14 h-14 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-3">
          <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">Redaguoti organizaciją</h2>
        <p class="text-gray-500 mt-1">Atnaujinkite organizacijos informaciją</p>
      </div>

      <form class="space-y-5">
        <!-- Pavadinimas -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Pavadinimas</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <input
              v-model="form.name"
              required
              class="w-full border rounded-lg pl-10 pr-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Pvz.: Stalo žaidimų entuziastai"
            />
          </div>
        </div>

        <!-- Aprašymas -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Aprašymas</label>
          <div class="relative">
            <div class="absolute top-3 left-3 flex items-start pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
              </svg>
            </div>
            <textarea
              v-model="form.description"
              class="w-full border rounded-lg pl-10 pr-3 py-2 min-h-[100px] focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Trumpai aprašykite organizaciją, jos tikslus ir veiklą..."
            ></textarea>
          </div>
        </div>

        <!-- Viešumo tipas -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Viešumo tipas</label>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <label class="relative border rounded-lg p-3 flex items-center cursor-pointer hover:bg-gray-50 transition" :class="{'bg-indigo-50 border-indigo-300': form.privacy === 'public'}">
              <input type="radio" v-model="form.privacy" value="public" class="absolute opacity-0 h-0 w-0" />
              <div class="flex items-center">
                <div class="w-10 h-10 rounded-full bg-green-100 text-green-600 flex items-center justify-center mr-3">
                  <span class="text-xl">🔓</span>
                </div>
                <div>
                  <p class="font-medium text-gray-800">Vieša</p>
                  <p class="text-xs text-gray-500">Bet kas gali rasti</p>
                </div>
              </div>
              <div v-if="form.privacy === 'public'" class="absolute top-2 right-2 w-4 h-4 rounded-full bg-indigo-500"></div>
            </label>

            <label class="relative border rounded-lg p-3 flex items-center cursor-pointer hover:bg-gray-50 transition" :class="{'bg-indigo-50 border-indigo-300': form.privacy === 'protected'}">
              <input type="radio" v-model="form.privacy" value="protected" class="absolute opacity-0 h-0 w-0" />
              <div class="flex items-center">
                <div class="w-10 h-10 rounded-full bg-yellow-100 text-yellow-600 flex items-center justify-center mr-3">
                  <span class="text-xl">🔐</span>
                </div>
                <div>
                  <p class="font-medium text-gray-800">Apsaugota</p>
                  <p class="text-xs text-gray-500">Ribota prieiga</p>
                </div>
              </div>
              <div v-if="form.privacy === 'protected'" class="absolute top-2 right-2 w-4 h-4 rounded-full bg-indigo-500"></div>
            </label>

            <label class="relative border rounded-lg p-3 flex items-center cursor-pointer hover:bg-gray-50 transition" :class="{'bg-indigo-50 border-indigo-300': form.privacy === 'private'}">
              <input type="radio" v-model="form.privacy" value="private" class="absolute opacity-0 h-0 w-0" />
              <div class="flex items-center">
                <div class="w-10 h-10 rounded-full bg-red-100 text-red-600 flex items-center justify-center mr-3">
                  <span class="text-xl">🚫</span>
                </div>
                <div>
                  <p class="font-medium text-gray-800">Privati</p>
                  <p class="text-xs text-gray-500">Tik su pakvietimu</p>
                </div>
              </div>
              <div v-if="form.privacy === 'private'" class="absolute top-2 right-2 w-4 h-4 rounded-full bg-indigo-500"></div>
            </label>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- Grupė (kategorija) -->
          <div>
            <label class="block mb-1 font-medium text-gray-700">Grupė (kategorija)</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
              </div>
              <select
                v-model="form.category"
                required
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option v-for="cat in categories" :key="cat.value" :value="cat.value">
                  {{ cat.name }}
                </option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Miestas -->
          <div>
            <label class="block mb-1 font-medium text-gray-700">Miestas</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <select
                v-model="form.city"
                required
                class="w-full border rounded-lg pl-10 pr-10 py-2 appearance-none bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option disabled value="">-- Pasirinkite miestą --</option>
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

        <!-- Organizacijos nuotrauka -->
        <div>
          <label class="block mb-1 font-medium text-gray-700">Organizacijos logotipas</label>
          <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg bg-gray-50 hover:bg-gray-100 transition cursor-pointer">
            <div class="space-y-1 text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div class="flex text-sm text-gray-600 justify-center">
                <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500 px-2 py-1">
                  <span>Įkelti failą</span>
                  <input id="file-upload" name="file-upload" type="file" class="sr-only">
                </label>
                <p class="pl-1 pt-1">arba nuvilkite ir numeskite</p>
              </div>
              <p class="text-xs text-gray-500">
                PNG, JPG, GIF iki 10MB
              </p>
            </div>
          </div>
        </div>

        <!-- Informacija apie organizacijas -->
        <div class="p-4 bg-blue-50 rounded-lg border border-blue-100">
          <div class="flex">
            <div class="mr-3 flex-shrink-0">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-sm text-blue-800">
              <p class="font-medium">Atnaujinimo įspėjimas</p>
              <p class="mt-1">Atnaujinus organizacijos informaciją, pakeitimai iškart bus matomi visiems nariams.</p>
            </div>
          </div>
        </div>

        <!-- Veiksmai -->
        <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition shadow-sm flex items-center gap-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Atšaukti
          </button>
          <button
            type="button"
            @click="submitEdit"
            class="px-5 py-2 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg hover:from-indigo-700 hover:to-blue-700 transition shadow-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Išsaugoti pakeitimus
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from '@/api/axios'

const props = defineProps<{
  visible: boolean
  organization: any
}>()

const emit = defineEmits(['close', 'updated'])

const categories = [
  { value: 'classic_strategic', name: 'Klasikiniai & Strateginiai' },
  { value: 'rpg', name: 'RPG (Role-playing games)' },
  { value: 'miniature_games', name: 'Miniatiūrų žaidimai' },
  { value: 'party_social', name: 'Vakarėlių ir socialiniai žaidimai' },
  { value: 'children_games', name: 'Vaikų žaidimai' },
  { value: 'educational', name: 'Edukaciniai žaidimai' }
]


const form = ref({
  name: '',
  description: '',
  city: '',
  category: '',
  privacy: ''
})

watch(() => props.organization, (org) => {
  if (org) {
    form.value = {
      name: org.name || '',
      description: org.description || '',
      city: org.city || '',
      category: org.category || '',
      privacy: org.privacy || ''
    }
  }
}, { immediate: true })

const submitEdit = async () => {
  try {
    await axios.patch(`/organizations/${props.organization.id}/`, {
      ...form.value,
      category_name: form.value.category // API naudoja šitą lauką
    })
    emit('updated')
    emit('close')
  } catch (err) {
    console.error('❌ Nepavyko atnaujinti organizacijos:', err)
    alert('Nepavyko atnaujinti organizacijos.')
  }
}
</script>
