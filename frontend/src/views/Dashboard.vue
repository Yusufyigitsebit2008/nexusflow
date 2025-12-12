<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-blue-900 font-sans text-slate-100 flex flex-col">
    
    <header class="bg-black/20 backdrop-blur-md border-b border-white/10 p-4 px-8 flex justify-between items-center z-20">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-gradient-to-tr from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/30">N</div>
        <h1 class="text-xl font-bold tracking-wide">NexusFlow</h1>
      </div>
      
      <div class="flex items-center gap-4">
        <div 
            @click="$router.push('/profile')"
            class="flex items-center gap-3 cursor-pointer hover:bg-white/10 p-2 rounded-lg transition"
        >
            <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-xs">
                {{ user?.username?.charAt(0).toUpperCase() }}
            </div>
            <span class="text-sm text-slate-400 hidden md:block">
                Hoş geldin, <b class="text-white">{{ user?.username }}</b>
            </span>
        </div>

        <button @click="handleLogout" class="bg-white/10 hover:bg-red-500/20 hover:text-red-400 text-slate-300 px-3 py-1.5 rounded-lg text-sm transition border border-white/5">Çıkış Yap</button>
      </div>
    </header>

    <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
      <div class="max-w-7xl mx-auto space-y-8">

        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="bg-white/5 backdrop-blur-md border border-white/10 p-5 rounded-2xl flex items-center gap-4 hover:bg-white/10 transition group">
                <div class="w-12 h-12 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-2xl group-hover:scale-110 transition">📂</div>
                <div>
                    <h3 class="text-slate-400 text-xs uppercase font-bold tracking-wider">Toplam Pano</h3>
                    <p class="text-2xl font-bold text-white">{{ totalBoards }}</p>
                </div>
            </div>
            <div class="bg-white/5 backdrop-blur-md border border-white/10 p-5 rounded-2xl flex items-center gap-4 hover:bg-white/10 transition group">
                <div class="w-12 h-12 rounded-full bg-orange-500/20 text-orange-400 flex items-center justify-center text-2xl group-hover:scale-110 transition">🔥</div>
                <div>
                    <h3 class="text-slate-400 text-xs uppercase font-bold tracking-wider">Acil İşler</h3>
                    <p class="text-2xl font-bold text-white">3</p>
                </div>
            </div>
            <div class="bg-white/5 backdrop-blur-md border border-white/10 p-5 rounded-2xl flex items-center gap-4 hover:bg-white/10 transition group">
                <div class="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl group-hover:scale-110 transition">✅</div>
                <div>
                    <h3 class="text-slate-400 text-xs uppercase font-bold tracking-wider">Tamamlanan</h3>
                    <p class="text-2xl font-bold text-white">12</p>
                </div>
            </div>
            <div class="bg-white/5 backdrop-blur-md border border-white/10 p-5 rounded-2xl flex items-center gap-4 hover:bg-white/10 transition group">
                <div class="w-12 h-12 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center text-2xl group-hover:scale-110 transition">🚀</div>
                <div>
                    <h3 class="text-slate-400 text-xs uppercase font-bold tracking-wider">Verimlilik</h3>
                    <p class="text-2xl font-bold text-white">%92</p>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <div class="lg:col-span-2 space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white/5 backdrop-blur-md border border-white/10 p-6 rounded-2xl min-h-[300px] flex flex-col">
                        <h3 class="text-white font-bold mb-4 flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-blue-500"></span> İş Dağılımı
                        </h3>
                        <div class="flex-1 relative">
                            <Doughnut :data="chartDataPie" :options="chartOptions" />
                        </div>
                    </div>
                    <div class="bg-white/5 backdrop-blur-md border border-white/10 p-6 rounded-2xl min-h-[300px] flex flex-col">
                        <h3 class="text-white font-bold mb-4 flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Haftalık Aktivite
                        </h3>
                        <div class="flex-1 relative">
                            <Bar :data="chartDataBar" :options="chartOptions" />
                        </div>
                    </div>
                </div>

                <div 
                    @click="showCreateModal = true"
                    class="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 p-6 rounded-2xl flex items-center justify-between cursor-pointer hover:bg-blue-600/30 transition group"
                >
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 rounded-xl bg-blue-500 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-blue-500/40 group-hover:scale-110 transition">+</div>
                        <div>
                            <h3 class="text-lg font-bold text-white">Yeni Pano Oluştur</h3>
                            <p class="text-slate-400 text-sm">Takımın için yeni bir çalışma alanı yarat.</p>
                        </div>
                    </div>
                    <span class="text-slate-400 group-hover:translate-x-2 transition">Başla ➔</span>
                </div>
            </div>

            <div class="bg-white/5 backdrop-blur-md border border-white/10 p-6 rounded-2xl h-fit">
                <h3 class="text-slate-300 font-bold uppercase text-xs tracking-wider mb-4 border-b border-white/10 pb-2">Çalışma Alanlarım</h3>
                
                <div v-if="loading" class="text-center py-10">
                    <div class="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
                </div>

                <div v-else class="space-y-6">
                    <div v-for="ws in workspaces" :key="ws.id">
                        <div class="flex items-center gap-2 mb-3">
                            <span class="text-xl">🏢</span>
                            <h4 class="text-white font-bold">{{ ws.name }}</h4>
                        </div>
                        
                        <div class="space-y-2 pl-4 border-l-2 border-white/5">
                            <div 
                                v-for="board in (ws.boards || [])" 
                                :key="board.id"
                                @click="$router.push(`/board/${board.id}`)"
                                class="bg-white/5 hover:bg-white/10 p-3 rounded-lg cursor-pointer transition flex items-center justify-between group"
                            >
                                <span class="text-slate-300 text-sm font-medium group-hover:text-white">{{ board.name }}</span>
                                <span class="text-slate-500 text-xs group-hover:translate-x-1 transition">➔</span>
                            </div>
                            <div v-if="!ws.boards || ws.boards.length === 0" class="text-slate-500 text-xs italic px-3">Henüz pano yok.</div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
      </div>
    </div>

    <div v-if="showCreateModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-slate-800 border border-slate-700 p-6 rounded-2xl w-full max-w-md shadow-2xl relative animate-fade-in-up">
            <button @click="showCreateModal = false" class="absolute top-4 right-4 text-slate-400 hover:text-white">✕</button>
            <h3 class="text-xl font-bold text-white mb-6">✨ Yeni Pano</h3>
            
            <form @submit.prevent="createBoard">
                <div class="mb-4">
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-2">Pano İsmi</label>
                    <input v-model="newBoardName" type="text" class="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-white focus:border-blue-500 outline-none" placeholder="Örn: Pazarlama Projesi">
                </div>
                <div class="mb-6">
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-2">Workspace Seç</label>
                    <select v-model="selectedWorkspace" class="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-white focus:border-blue-500 outline-none">
                        <option v-for="ws in workspaces" :key="ws.id" :value="ws.id">{{ ws.name }}</option>
                    </select>
                </div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition">Oluştur</button>
            </form>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useToast } from "vue-toastification";
import api from '../utils/axios';
import { useRouter } from 'vue-router';

// Chart.js Importları
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  Title
} from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Title)

const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();
const user = computed(() => authStore.user);

const workspaces = ref([]);
const loading = ref(true);
const showCreateModal = ref(false);
const newBoardName = ref('');
const selectedWorkspace = ref(null);

// --- GRAFİK VERİLERİ (DEMO) ---
const chartDataPie = ref({
  labels: ['Yapılacak', 'Sürüyor', 'Bitti'],
  datasets: [{
    backgroundColor: ['#64748b', '#3b82f6', '#10b981'],
    data: [5, 8, 3],
    borderWidth: 0
  }]
});

const chartDataBar = ref({
  labels: ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
  datasets: [{
    label: 'Tamamlanan Görevler',
    backgroundColor: '#8b5cf6',
    data: [1, 3, 2, 5, 4, 2, 6],
    borderRadius: 5
  }]
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: '#cbd5e1' } }
  },
  scales: {
      y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
      x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
  }
});

// --- VERİ ÇEKME ---
onMounted(async () => {
    try {
        const res = await api.get('workspaces/');
        // Gelen veride boards yoksa boş dizi olarak kabul et (Backend düzeltilse bile garanti olsun)
        workspaces.value = res.data.map(ws => ({
            ...ws,
            boards: ws.boards || []
        }));
        
        if(workspaces.value.length > 0) selectedWorkspace.value = workspaces.value[0].id;
    } catch (error) {
        console.error(error);
        // Oturum düşmüşse sessizce login'e atılabilir
    } finally {
        loading.value = false;
    }
});

// --- HATA ÇIKARAN COMPUTED (DÜZELTİLDİ) ---
const totalBoards = computed(() => {
    if (!workspaces.value) return 0;
    
    // GÜVENLİ HESAPLAMA: (ws.boards || []).length
    return workspaces.value.reduce((acc, ws) => acc + (ws.boards ? ws.boards.length : 0), 0);
});

// --- PANO OLUŞTURMA ---
const createBoard = async () => {
    if(!newBoardName.value.trim()) return toast.warning("İsim giriniz!");
    try {
        await api.post('boards/', {
            name: newBoardName.value,
            workspace: selectedWorkspace.value
        });
        toast.success("Pano oluşturuldu! 🎉");
        showCreateModal.value = false;
        newBoardName.value = '';
        
        // Listeyi yenile
        const res = await api.get('workspaces/');
        workspaces.value = res.data.map(ws => ({ ...ws, boards: ws.boards || [] }));
        
    } catch (error) {
        toast.error("Hata oluştu.");
    }
};

const handleLogout = () => {
    authStore.logout();
    router.push('/login');
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #475569; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}
</style>