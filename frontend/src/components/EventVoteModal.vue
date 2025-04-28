<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-xl max-w-3xl w-full relative">
      <h2 class="text-xl font-bold mb-4">🗳️ Sudėliok savo norimų žaisti žaidimų eilę</h2>

      <div v-if="games.length === 0" class="text-center text-gray-600">
        ❌ Šiam renginiui dar neimportuoti jokie žaidimai!
      </div>

      <draggable v-model="games" item-key="game.id" class="space-y-2" handle=".drag-handle">
        <template #item="{ element, index }">
          <div class="flex items-center gap-3 border rounded px-3 py-2 bg-gray-50">
            <span class="drag-handle cursor-move">☰</span>
            <img :src="element.game.thumbnail_url" alt="thumbnail" class="w-12 h-12 object-cover rounded" />
            <div class="flex-1">
              <p class="font-semibold">{{ element.game.title }}</p>
              <p class="text-sm text-gray-600">
                {{ element.game.min_players }}–{{ element.game.max_players }} žaidėjai • {{ element.game.playtime_minutes }} min
              </p>
            </div>
            <span class="text-gray-500 text-sm">#{ { index + 1 } }</span>
          </div>
        </template>
      </draggable>

      <div class="flex justify-end mt-6 gap-3">
        <button @click="$emit('close')" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Atšaukti</button>
        <button @click="submitVotes" :disabled="games.length === 0"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          🗳️ Balsuoti
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'
import axios from '@/api/axios'
import { useRoute } from 'vue-router'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits(['close', 'voted'])
const route = useRoute()

const games = ref<any[]>([])

const fetchAvailableGames = async () => {
  try {
    const res = await axios.get(`/events/${route.params.id}/available-games/`)
    games.value = res.data
  } catch (err) {
    console.error('Klaida gaunant žaidimų sąrašą:', err)
  }
}

const submitVotes = async () => {
  const votes = games.value.map((item, index) => ({
    game_id: item.game.id,
    rank: index + 1,
  }))

  try {
    await axios.post(`/events/${route.params.id}/vote/`, { votes })
    alert('✅ Balsas išsaugotas!')
    emit('voted')
    emit('close')
  } catch (err) {
    console.error('Balsavimo klaida:', err)
    alert('❌ Nepavyko išsaugoti balsavimo.')
  }
}

onMounted(fetchAvailableGames)
</script>
