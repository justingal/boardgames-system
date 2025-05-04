<template>
  <div class="repeat-date-picker">
    <div class="calendar-container border rounded-lg overflow-hidden">
      <FullCalendar
        ref="fullCalendarRef"
        :options="calendarOptions"
      />
    </div>
    <div class="mt-2 text-sm text-gray-600" v-if="selectedDates.length">
      Pasirinktos datos: {{ formattedSelectedDates }}
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

// Format date to YYYY-MM-DD
function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// Format date for display (YYYY-MM-DD)
function formatDateForDisplay(dateStr) {
  const date = new Date(dateStr);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// Calendar configuration
const calendarOptions = {
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  selectable: true,
  locale: 'lt',
  firstDay: 1, // Monday as first day
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
  datesSet: function(info) {
    // When month is changed, ensure the selected dates are properly displayed
    if (fullCalendarRef.value) {
      fullCalendarRef.value.getApi().render();
    }
  },
  height: 'auto'
}

// Format selected dates for display
const formattedSelectedDates = computed(() => {
  if (!selectedDates.value.length) return '';

  return selectedDates.value
    .sort((a, b) => new Date(a) - new Date(b))
    .map(dateStr => formatDateForDisplay(dateStr))
    .join(', ');
});

// Handle date click in calendar
// Handle date click in calendar
function handleDateClick(info) {
  const clickedDate = info.dateStr; // YYYY-MM-DD format

  // Check if date is already selected
  const index = selectedDates.value.findIndex(dateStr => dateStr === clickedDate);

  if (index > -1) {
    // If already selected, remove it
    selectedDates.value.splice(index, 1);
  } else {
    // If not selected, add it
    selectedDates.value.push(clickedDate);
  }

  // Sort the dates and emit full date strings
  // Svarbu - dabar įsitikiname, kad perduodame tikras datas YYYY-MM-DD formatu,
  // o ne tik dienų skaičius
  const sortedDates = [...selectedDates.value].sort((a, b) => new Date(a) - new Date(b));
  console.log("Perduodamos datos:", sortedDates); // Debugging
  emit('update:modelValue', sortedDates);
}

// React to modelValue changes from outside
watch(() => props.modelValue, (newVal) => {
  if (newVal && newVal.length) {
    // Check if we're getting full date strings or just day numbers
    const allAreDateStrings = newVal.every(item =>
      typeof item === 'string' && item.includes('-')
    );

    if (allAreDateStrings) {
      // They're already full date strings
      selectedDates.value = [...newVal];
    } else {
      // They're day numbers or other format - konvertuojame į YYYY-MM-DD
      if (fullCalendarRef.value) {
        const calendar = fullCalendarRef.value.getApi();
        const currentDate = calendar.getDate();
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        selectedDates.value = newVal.map(day => {
          // Jei tai jau yra dateString formatu, tiesiog grąžiname
          if (typeof day === 'string' && day.includes('-')) {
            return day;
          }
          // Kitu atveju, konvertuojame į datą
          const date = new Date(year, month, parseInt(day));
          return formatDate(date);
        });
      }
    }
  } else if (newVal && newVal.length === 0) {
    selectedDates.value = [];
  }
}, { deep: true });
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
