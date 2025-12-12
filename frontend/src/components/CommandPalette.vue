<template>
  <transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4" @click.self="close">
        
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"></div>

        <div class="relative w-full max-w-xl bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden animate-slide-down">
            
            <div class="flex items-center px-4 border-b border-slate-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                <input 
                    ref="searchInput"
                    v-model="query"
                    @input="performSearch"
                    @keydown.esc="close"
                    class="w-full bg-transparent border-none text-white text-lg px-4 py-4 focus:ring-0 outline-none placeholder-slate-500"
                    placeholder="Ne aramıştın? (Kartlar, Panolar...)"
                >
                <div class="text-xs text-slate-500 font-mono border border-slate-700 rounded px-2 py-1">ESC</div>
            </div>

            <div class="max-h-[60vh] overflow-y-auto custom-scrollbar p-2">
                
                <div v-if="loading" class="text-center py-4 text-slate-500">
                    <span class="animate-pulse">Aranıyor...</span>
                </div>

                <div v-else-if="results.length > 0" class="space-y-1">
                    <div 
                        v-for="(item, index) in results" 
                        :key="index"
                        @click="navigate(item.url)"
                        class="flex items-center gap-3 p-3 rounded-lg hover:bg-blue-600/20 hover:border-blue-500/30 border border-transparent cursor-pointer group transition-all"
                    >
                        <span class="text-xl">{{ item.icon }}</span>
                        <div class="flex-1">
                            <h4 class="text-slate-200 font-medium group-hover:text-blue-100">{{ item.title }}</h4>
                            <p class="text-xs text-slate-500 group-hover:text-blue-300">{{ item.subtitle }}</p>
                        </div>
                        <span class="text-slate-600 text-xs group-hover:text-blue-300">Git ↵</span>
                    </div>
                </div>

                <div v-else-if="query.length > 1" class="text-center py-8 text-slate-500">
                    <p>Sonuç bulunamadı 😔</p>
                </div>

                <div v-else class="text-center py-8 text-slate-600 text-sm">
                    <p>Aramak için yazmaya başla...</p>
                </div>
            </div>

            <div class="bg-slate-800/50 p-2 text-center border-t border-slate-700">
                <p class="text-[10px] text-slate-500">NexusFlow Command Center</p>
            </div>
        </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import api from '../utils/axios';

const isOpen = ref(false);
const query = ref('');
const results = ref([]);
const loading = ref(false);
const searchInput = ref(null);
const router = useRouter();
let debounceTimer = null;

// Klavye Dinleyicisi (Ctrl + K)
const handleKeydown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        isOpen.value = !isOpen.value;
        if (isOpen.value) {
            nextTick(() => searchInput.value?.focus());
        } else {
            reset();
        }
    }
    if (e.key === 'Escape' && isOpen.value) {
        close();
    }
};

const close = () => {
    isOpen.value = false;
    reset();
};

const reset = () => {
    query.value = '';
    results.value = [];
};

const navigate = (url) => {
    close();
    router.push(url);
};

// Arama Fonksiyonu (Debounce ile - Çok hızlı yazınca api boğulmasın diye)
const performSearch = () => {
    if (debounceTimer) clearTimeout(debounceTimer);
    
    if (query.value.length < 2) {
        results.value = [];
        return;
    }

    loading.value = true;
    debounceTimer = setTimeout(async () => {
        try {
            const res = await api.get(`search/?q=${query.value}`);
            results.value = res.data;
        } catch (error) {
            console.error(error);
        } finally {
            loading.value = false;
        }
    }, 300); // 300ms bekle
};

onMounted(() => window.addEventListener('keydown', handleKeydown));
onUnmounted(() => window.removeEventListener('keydown', handleKeydown));
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@keyframes slideDown {
    from { transform: translateY(-20px) scale(0.95); opacity: 0; }
    to { transform: translateY(0) scale(1); opacity: 1; }
}
.animate-slide-down { animation: slideDown 0.2s ease-out; }

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #475569; border-radius: 4px; }
</style>