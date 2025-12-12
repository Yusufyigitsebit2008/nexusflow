<template>
  <div class="h-full bg-white/5 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-white/10 calendar-wrapper">
    <FullCalendar :options="calendarOptions" class="h-full" />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import api from '../utils/axios';
import { useToast } from "vue-toastification";

const props = defineProps(['lists']); // Parent'tan listeleri alıyoruz
const emit = defineEmits(['openCard']); // Kart açma isteğini yukarı iletmek için
const toast = useToast();

// Kartları FullCalendar formatına (Events) çevir
const calendarEvents = computed(() => {
    if (!props.lists) return [];
    
    // Tüm listelerin içindeki kartları tek bir havuzda topla (FlatMap)
    // Sadece 'due_date'i olan kartları alıyoruz.
    const allCards = props.lists.flatMap(list => list.cards);
    
    return allCards
        .filter(card => card.due_date) // Tarihi olmayanları gösterme
        .map(card => ({
            id: card.id,
            title: card.title,
            start: card.due_date, // FullCalendar 'start' bekler
            backgroundColor: getPriorityColor(card.priority),
            borderColor: 'transparent',
            extendedProps: { ...card } // Orijinal veriyi sakla
        }));
});

// Önceliğe göre renk ver
const getPriorityColor = (priority) => {
    switch(priority) {
        case 'urgent': return '#9333ea'; // Mor
        case 'high': return '#ef4444';   // Kırmızı
        case 'medium': return '#f97316'; // Turuncu
        case 'low': return '#10b981';    // Yeşil
        default: return '#3b82f6';       // Mavi
    }
};

// Takvim Ayarları
const calendarOptions = ref({
    plugins: [ dayGridPlugin, interactionPlugin, timeGridPlugin ],
    initialView: 'dayGridMonth',
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek'
    },
    editable: true, // Sürüklemeye izin ver
    droppable: true,
    events: calendarEvents, // Veriyi bağla
    
    // Kart sürüklendiğinde (Tarih Değiştirme)
    eventDrop: async (info) => {
        const newDate = info.event.start.toISOString().split('T')[0]; // YYYY-MM-DD
        const cardId = info.event.id;

        try {
            await api.patch(`cards/${cardId}/`, { due_date: newDate });
            toast.success(`Tarih güncellendi: ${newDate}`);
        } catch (error) {
            toast.error("Tarih değiştirilemedi!");
            info.revert(); // Hata olursa kartı eski yerine geri koy
        }
    },

    // Karta tıklandığında (Detay Açma)
    eventClick: (info) => {
        // Parent bileşene (BoardDetail) "Şu kartı aç" emri gönder
        emit('openCard', info.event.extendedProps);
    }
});

// Veri değişirse takvimi güncelle (Reactivity)
watch(() => props.lists, () => {
    calendarOptions.value.events = calendarEvents.value;
}, { deep: true });

</script>

<style scoped>
/* FullCalendar Dark Theme Özelleştirmesi (Glassmorphism) */
.calendar-wrapper {
    --fc-border-color: rgba(255, 255, 255, 0.1);
    --fc-button-bg-color: rgba(255, 255, 255, 0.1);
    --fc-button-border-color: rgba(255, 255, 255, 0.1);
    --fc-button-text-color: #e2e8f0;
    --fc-button-hover-bg-color: rgba(255, 255, 255, 0.2);
    --fc-button-active-bg-color: #3b82f6;
    --fc-today-bg-color: rgba(59, 130, 246, 0.1);
    --fc-page-bg-color: transparent;
    --fc-neutral-bg-color: transparent;
    --fc-list-event-hover-bg-color: rgba(255, 255, 255, 0.05);
}

:deep(.fc) {
    color: #cbd5e1;
    font-family: inherit;
}

:deep(.fc-col-header-cell-cushion),
:deep(.fc-daygrid-day-number) {
    color: #cbd5e1;
    text-decoration: none;
}

:deep(.fc-daygrid-day.fc-day-today) {
    background-color: rgba(59, 130, 246, 0.1) !important;
}

:deep(.fc-event) {
    cursor: pointer;
    border-radius: 4px;
    padding: 2px 4px;
    font-size: 0.85em;
    font-weight: 600;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>