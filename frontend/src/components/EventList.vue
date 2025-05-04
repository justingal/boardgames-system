<template>
  <div class="space-y-4">
    <div
      v-for="event in events"
      :key="event.id"
      class="border rounded-lg p-4 bg-white shadow-sm"
      :class="{
        'ring-2 ring-blue-400': highlight === 'today',
        'opacity-60': past
      }"
    >
      <h2 class="text-xl font-bold mb-2">{{ event.title }}</h2>
      <p class="text-gray-600 mb-2">{{ event.description }}</p>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-sm text-gray-800"><span class="font-semibold">Adresas:</span> {{ event.address }}</p>
          <p class="text-sm text-gray-800"><span class="font-semibold">Stalo dydis:</span> {{ tableSizeLabels[event.table_size] }}</p>

          <div v-if="event.first_player_is_organizer && event.players_count === 0"
               class="mt-2 mb-2 py-1 px-3 bg-green-100 text-green-800 rounded-full inline-block text-sm font-medium">
            🟢 Laisvas - narių 0 - tapk organizatoriumi!
          </div>
          <p v-else class="text-sm text-gray-800">
            <span class="font-semibold">Dalyviai:</span> {{ event.players_count }}
            <span v-if="event.organizers && event.organizers.length">
              (Organizatorius: {{ getOrganizerNames(event) }})
            </span>
          </p>

          <p class="text-sm text-gray-800"><span class="font-semibold">Viešumas:</span> {{ privacyLabels[event.visibility] }}</p>
        </div>

        <div>
          <p class="text-sm text-gray-800">
            <span class="font-semibold">Pradžia:</span>
            {{ formatDateTime(event.start_time) }}
          </p>
          <p class="text-sm text-gray-800">
            <span class="font-semibold">Pabaiga:</span>
            {{ formatDateTime(event.end_time) }}
          </p>
          <p class="text-sm text-gray-800" v-if="event.perks">
            <span class="font-semibold">Papildomos galimybės:</span> {{ event.perks }}
          </p>

          <div class="mt-4">
            <button
              v-if="event.is_participant"
              @click="$emit('go-to', event.id)"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Eiti į renginį
            </button>
            <button
              v-else
              @click="$emit('join', event.id)"
              class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              {{ event.first_player_is_organizer && event.players_count === 0 ? 'Tapti organizatoriumi' : 'Prisijungti' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  events: Array,
  highlight: String, // 'today' jei šiandienos renginiai
  past: Boolean
})

const emit = defineEmits(['go-to', 'join'])

const tableSizeLabels = {
  S: 'Mažas (2 žmonės) ~ 80x80cm',
  M: 'Vidutinis (4 žmonės) ~ 120x80cm',
  L: 'Didelis (6–8 žmonės) ~ 180x90cm',
  XL: 'Labai didelis (8–10 žmonių) ~ 200x100cm'
}

const privacyLabels = {
  public: '🔓 Vieša – matoma visiems',
  protected: '🔐 Apsaugota – matoma, bet reikia leidimo jungtis',
  private: '🚫 Privati – nematoma, tik pakviestiesiems'
}

function getOrganizerNames(event) {
  if (!event.organizers || !event.organizers.length) return ''
  return event.organizers.map(org => org.username).join(', ')
}

function formatDateTime(datetimeStr) {
  if (!datetimeStr) return ''
  const date = new Date(datetimeStr)
  return date.toLocaleString('lt-LT', {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'UTC'
  })
}
</script>
