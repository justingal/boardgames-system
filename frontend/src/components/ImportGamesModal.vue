<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-xl max-w-3xl w-full relative">
      <h2 class="text-xl font-bold mb-4">🎲 Pasirink žaidimus, kuriuos atsineši į renginį</h2>

      <div class="flex items-center mb-4">
        <input type="checkbox" id="selectAll" v-model="selectAll" @change="toggleSelectAll" class="mr-2" />
        <label for="selectAll" class="text-sm">Pažymėti visus žaidimus iš kolekcijos</label>
      </div>

      <div class="max-h-[50vh] overflow-y-auto space-y-2">
        <div v-for="item in games" :key="item.id" class="flex items-center gap-3 border rounded px-3 py-2 bg-gray-50">
          <input type="checkbox" v-model="selectedGameIds" :value="item.game.id" />
          <img :src="item.game.thumbnail_url" alt="thumbnail" class="w-12 h-12 object-cover rounded" />
          <div>
            <p class="font-semibold">{{ item.game.title }}</p>
            <p class="text-sm text-gray-600">
              {{ item.game.min_players }}–{{ item.game.max_players }} žaidėjai • {{ item.game.playtime_minutes }} min
            </p>
          </div>
        </div>
      </div>

      <div class="flex justify-end mt-6 gap-3">
        <button @click="$emit('close')" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Atšaukti</button>
        <button
          @click="submitImport"
          :disabled="selectedGameIds.length === 0"
          class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Importuoti pasirinktus žaidimus
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import axios from '@/api/axios'
import { useRoute } from 'vue-router'

const props = defineProps<{ visible: boolean }>()
const emit = defineEmits(['close', 'imported'])

const route = useRoute()
const games = ref<any[]>([])
const selectedGameIds = ref<number[]>([])
const selectAll = ref(false)

const fetchUserCollectionGames = async () => {
  try {
    const res = await axios.get(`/events/${route.params.id}/importable-games/`) // ⬅️ ČIA TAVO ASMENINĖ KOLEKCIJA
    games.value = res.data
  } catch (err) {
    console.error('Klaida gaunant žaidimų kolekciją:', err)
  }
}

const toggleSelectAll = () => {
  selectedGameIds.value = selectAll.value ? games.value.map(item => item.game.id) : []
}

watch(games, () => {
  if (selectAll.value) {
    selectedGameIds.value = games.value.map(item => item.game.id)
  }
})

const submitImport = async () => {
  try {
    await axios.post(`/events/${route.params.id}/import-games/`, {
      game_ids: selectedGameIds.value,
    })
    alert('✅ Žaidimai sėkmingai importuoti į renginį!')
    emit('imported')
    emit('close')
  } catch (err) {
    console.error('Importavimo klaida:', err)
    alert('❌ Nepavyko importuoti žaidimų.')
  }
}

onMounted(fetchUserCollectionGames)
</script>
