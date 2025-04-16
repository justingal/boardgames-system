<template>
  <div class="repeat-date-picker">
    <div class="calendar-container border rounded-lg overflow-hidden">
      <FullCalendar
        ref="fullCalendarRef"
        :options="calendarOptions"
      />
    </div>
    <div class="mt-2 text-sm text-gray-600" v-if="selectedDates.length">
      Pasirinktos dienos: {{ formattedDaysOfMonth }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})
const emit = defineEmits(['update:modelValue'])

const fullCalendarRef = ref(null)
const selectedDates = ref([])

// Konfigūruojame kalendoriaus nustatymus kaip objektą
const calendarOptions = {
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  selectable: true,
  locale: 'lt',
  firstDay: 1, // Pirmadienis kaip savaitės pradžia
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: ''
  },
  buttonText: {
    today: 'Šiandien'
  },
  dayHeaderFormat: { weekday: 'short' },
  titleFormat: { month: 'long', year: 'numeric' },
  dateClick: handleDateClick,
  events: computed(() => {
    return selectedDates.value.map(date => ({
      title: '✓',
      start: date,
      allDay: true,
      backgroundColor: '#4CAF50',
      borderColor: '#4CAF50',
      textColor: 'white'
    }))
  }),
  height: 'auto'
}

// Konvertuojame dienų skaičius į pilnas datos eilutes
function convertDayNumbersToFullDates(dayNumbers) {
  const currentDate = new Date();
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  return dayNumbers.map(day => {
    const date = new Date(year, month, parseInt(day));
    return formatDate(date);
  });
}

// Formatuojame datą į YYYY-MM-DD formatą
function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// Inicializuojame kalendorių kai komponentas užsikrauna
onMounted(() => {
  // Jei turime pradinių reikšmių
  if (props.modelValue && props.modelValue.length) {
    // Konvertuojame dienų skaičius į pilnas datas
    selectedDates.value = convertDayNumbersToFullDates(props.modelValue);
  }
})

// Reaguojame į modelValue pakeitimus
watch(() => props.modelValue, (newVal) => {
  // Jei modelValue pasikeičia iš išorės ir skiriasi nuo dabartinių pasirinktų dienų skaičių
  if (newVal && newVal.length) {
    const currentDayNumbers = selectedDates.value.map(d => new Date(d).getDate());

    // Tikriname, ar masyvai skirtingi
    const isDifferent = !arraysEqual(
      [...newVal].sort((a, b) => a - b),
      [...currentDayNumbers].sort((a, b) => a - b)
    );

    if (isDifferent) {
      selectedDates.value = convertDayNumbersToFullDates(newVal);
    }
  } else if (newVal && newVal.length === 0) {
    selectedDates.value = [];
  }
}, { deep: true })

// Reaguojame į selectedDates pakeitimus
watch(() => selectedDates.value, (newVal) => {
  // Išgauname tik dienų skaičius (1-31) iš pilnų datų
  const dayNumbers = newVal.map(dateStr => new Date(dateStr).getDate());
  emit('update:modelValue', dayNumbers);
}, { deep: true })

// Patikrina ar du masyvai yra lygūs
function arraysEqual(a, b) {
  if (a.length !== b.length) return false;
  return a.every((val, idx) => val === b[idx]);
}

// Apdoroja datos paspaudimą kalendoriuje
function handleDateClick(info) {
  const clickedDate = info.dateStr; // YYYY-MM-DD formatas

  // Ieškome ar ši data jau yra pasirinkta
  const index = selectedDates.value.findIndex(dateStr => dateStr === clickedDate);

  if (index > -1) {
    // Jei data jau pasirinkta, pašaliname ją
    selectedDates.value.splice(index, 1);
  } else {
    // Jei data dar nepasirinkta, pridedame ją
    selectedDates.value.push(clickedDate);
  }
}

// Formatuojame dienas rodymui
const formattedDaysOfMonth = computed(() => {
  if (!selectedDates.value.length) return '';

  const days = selectedDates.value
    .map(dateStr => new Date(dateStr).getDate())
    .sort((a, b) => a - b);

  return days.join(', ');
})
</script>

<style scoped>
.repeat-date-picker {
  margin-bottom: 1rem;
}

.calendar-container {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

:deep(.fc-event) {
  cursor: pointer;
}

:deep(.fc-daygrid-day) {
  cursor: pointer;
}

:deep(.fc-daygrid-day:hover) {
  background-color: #f0f9ff;
}

:deep(.fc-event-title) {
  font-weight: bold;
}

:deep(.fc-header-toolbar) {
  margin-bottom: 0.5rem !important;
  padding: 0.5rem;
}

:deep(.fc-toolbar-title) {
  font-size: 1.2rem !important;
}
</style>
