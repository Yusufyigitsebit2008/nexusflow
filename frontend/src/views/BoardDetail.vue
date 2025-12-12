<template>
  <div 
    :class="['h-screen flex flex-col font-sans overflow-hidden transition-colors duration-300', 
    isDarkMode ? 'bg-gradient-to-br from-slate-900 to-blue-950 text-slate-100' : 'bg-gradient-to-br from-blue-50 to-white text-slate-800']"
  >
    
    <header 
        :class="['backdrop-blur-md border-b h-16 flex items-center justify-between px-6 shadow-lg z-20 flex-shrink-0 transition-colors duration-300', 
        isDarkMode ? 'bg-slate-900/50 border-white/10' : 'bg-white/80 border-slate-200']"
    >
      <div class="flex items-center gap-4">
        <button 
          @click="$router.push('/dashboard')" 
          :class="['group flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all border', 
          isDarkMode ? 'bg-white/5 hover:bg-white/10 text-slate-300 border-white/5 hover:border-white/20' : 'bg-white hover:bg-slate-50 text-slate-600 border-slate-200 shadow-sm']"
        >
          <span class="group-hover:-translate-x-1 transition-transform">⬅</span> 
          <span>Dashboard</span>
        </button>
        
        <div class="h-6 w-px mx-2" :class="isDarkMode ? 'bg-white/10' : 'bg-slate-300'"></div>

        <div v-if="board" class="flex flex-col">
            <h1 class="text-lg font-bold tracking-wide leading-tight">{{ board.name }}</h1>
            <span class="text-[10px] uppercase tracking-widest font-semibold opacity-60">
                Workspace Görünümü
            </span>
        </div>
      </div>

      <div class="flex items-center gap-4">
         
         <div class="relative group">
            <button 
                class="px-3 py-1.5 rounded-lg text-xs font-bold border transition flex items-center gap-2"
                :class="isDarkMode ? 'bg-black/30 border-white/10 text-slate-300 hover:text-white' : 'bg-white border-slate-200 text-slate-600 hover:text-blue-600'"
            >
                <span v-if="filterMode === 'all'">🔍 Tümü</span>
                <span v-else-if="filterMode === 'me'">👤 Bana Ait</span>
                <span v-else>🔥 Acil</span>
            </button>
            
            <div 
                class="absolute top-full right-0 mt-2 w-48 rounded-xl shadow-xl border p-2 z-50 invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all transform origin-top-right scale-95 group-hover:scale-100"
                :class="isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'"
            >
                <div class="text-[10px] font-bold uppercase mb-2 px-2 opacity-50">Filtrele</div>
                <div @click="filterMode = 'all'" :class="['p-2 rounded cursor-pointer text-sm mb-1 transition', filterMode === 'all' ? 'bg-blue-500/20 text-blue-500' : 'hover:bg-slate-500/10']">Tüm Kartlar</div>
                <div @click="filterMode = 'me'" :class="['p-2 rounded cursor-pointer text-sm mb-1 transition', filterMode === 'me' ? 'bg-blue-500/20 text-blue-500' : 'hover:bg-slate-500/10']">Bana Atananlar</div>
                <div @click="filterMode = 'urgent'" :class="['p-2 rounded cursor-pointer text-sm transition', filterMode === 'urgent' ? 'bg-blue-500/20 text-blue-500' : 'hover:bg-slate-500/10']">Sadece Acil İşler</div>
            </div>
         </div>

         <div class="flex rounded-lg p-1 border" :class="isDarkMode ? 'bg-black/30 border-white/10' : 'bg-slate-100 border-slate-200'">
            <button 
                @click="viewMode = 'kanban'"
                :class="['px-3 py-1.5 rounded-md text-xs font-bold transition flex items-center gap-2', viewMode === 'kanban' ? 'bg-blue-600 text-white shadow-lg' : 'opacity-60 hover:opacity-100']"
            >
                <span>📊</span>
            </button>
            <button 
                @click="viewMode = 'calendar'"
                :class="['px-3 py-1.5 rounded-md text-xs font-bold transition flex items-center gap-2', viewMode === 'calendar' ? 'bg-blue-600 text-white shadow-lg' : 'opacity-60 hover:opacity-100']"
            >
                <span>📅</span>
            </button>
         </div>

         <button 
            @click="toggleTheme" 
            class="w-8 h-8 flex items-center justify-center rounded-full transition hover:bg-white/10 text-lg"
            :title="isDarkMode ? 'Aydınlık Mod' : 'Karanlık Mod'"
         >
            {{ isDarkMode ? '☀️' : '🌑' }}
         </button>

         <button @click="fetchActivities" :class="['px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-2 border', isDarkMode ? 'bg-white/10 hover:bg-white/20 text-white border-white/10' : 'bg-white hover:bg-slate-50 text-slate-600 border-slate-200']">
            <span>📜</span> Geçmiş
         </button>

         <transition name="fade" mode="out-in">
             <span v-if="saving" class="flex items-center gap-2 text-xs text-yellow-500 bg-yellow-500/10 border border-yellow-500/20 px-3 py-1 rounded-full font-bold">
                Kaydediliyor...
             </span>
             <span v-else class="flex items-center gap-2 text-xs text-emerald-500 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full font-bold">
                ✓ Senkronize
             </span>
         </transition>
         
         <div 
            class="flex items-center gap-2 px-3 py-1.5 rounded-full border transition-colors cursor-help" 
            :class="isDarkMode ? 'bg-black/40 border-white/10' : 'bg-white border-slate-200'"
            :title="socketConnected ? 'Canlı Bağlantı Aktif' : 'Bağlantı Koptu'"
         >
             <span class="text-[10px] font-mono font-bold tracking-wider opacity-70">LIVE</span>
             <span v-if="socketConnected" class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse"></span>
             <span v-else class="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)]"></span>
         </div>
      </div>
    </header>

    <div v-if="loading" class="flex-1 flex flex-col items-center justify-center gap-6 z-50 absolute inset-0 backdrop-blur-sm" :class="isDarkMode ? 'bg-slate-900/80 text-white' : 'bg-white/80 text-slate-800'">
        <div class="relative">
            <div class="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center font-bold text-xs animate-pulse">NF</div>
        </div>
        <p class="text-sm font-medium opacity-80">Pano verileri yükleniyor...</p>
    </div>

    <div v-else-if="board && viewMode === 'kanban'" class="flex-1 overflow-x-auto overflow-y-hidden p-6 relative w-full" :class="isDarkMode ? 'bg-pattern-dark' : 'bg-pattern-light'">
      <div class="flex h-full items-start gap-6 pb-4">
        
        <draggable 
            v-model="board.lists" 
            group="lists" 
            item-key="id" 
            direction="horizontal"
            @change="onListMove"
            class="flex h-full items-start gap-6"
            ghost-class="ghost-list"
            handle=".list-handle" 
        >
            <template #item="{element: list}">
                <div :class="['group/list w-80 flex-shrink-0 backdrop-blur-sm rounded-xl flex flex-col max-h-full shadow-2xl border-t-[3px] border-blue-600 transition-all duration-300', isDarkMode ? 'bg-slate-900/90' : 'bg-slate-100/90']">
                    
                    <div class="list-handle p-3 px-4 font-bold flex justify-between items-center rounded-t-xl border-b cursor-grab active:cursor-grabbing" :class="isDarkMode ? 'text-slate-200 border-slate-700 bg-white/5' : 'text-slate-700 border-slate-200 bg-white/60'">
                        <span class="truncate">{{ list.title }}</span>
                        <span class="text-[10px] font-mono px-2 py-0.5 rounded-full min-w-[20px] text-center" :class="isDarkMode ? 'bg-slate-800 text-slate-400' : 'bg-slate-200 text-slate-600'">
                            {{ list.cards.length }}
                        </span>
                    </div>

                    <div class="flex-1 overflow-y-auto p-2 custom-scrollbar" :class="isDarkMode ? 'bg-slate-900/50' : 'bg-slate-100'">
                        <draggable 
                            v-model="list.cards" 
                            group="cards" 
                            item-key="id" 
                            @change="onCardMove($event, list.id)"
                            class="space-y-2 min-h-[50px]"
                            ghost-class="ghost-card"
                            drag-class="drag-card"
                        >
                            <template #item="{element: card}">
                                <div 
                                    v-show="shouldShowCard(card)"
                                    @click="openEditModal(card)"
                                    @contextmenu.prevent="showContextMenu($event, card)" 
                                    :class="['p-3 rounded-lg shadow-sm border cursor-pointer hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 group relative overflow-hidden', 
                                    isDarkMode ? 'bg-slate-800 border-slate-700 hover:border-blue-500' : 'bg-white border-slate-200 hover:border-blue-400']"
                                >
                                    <div :class="['absolute left-0 top-0 bottom-0 w-1', getPriorityColorClass(card.priority)]"></div>
                                    
                                    <div class="pl-2.5">
                                        <div v-if="card.labels && card.labels.length > 0" class="flex flex-wrap gap-1 mb-2">
                                            <span v-for="label in card.labels" :key="label" :class="['text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-wider', getLabelColor(label)]">
                                                {{ label }}
                                            </span>
                                        </div>

                                        <h4 class="font-medium text-sm leading-snug mb-3 transition-colors" :class="isDarkMode ? 'text-slate-200 group-hover:text-blue-400' : 'text-slate-700 group-hover:text-blue-600'">
                                            {{ card.title }}
                                        </h4>
                                        
                                        <div v-if="card.checklist_items && card.checklist_items.length > 0" class="mb-3">
                                            <div class="flex items-center gap-1 text-[10px] mb-1 font-medium opacity-60">
                                                <span>☑️</span>
                                                <span>{{ card.checklist_items.filter(i => i.is_done).length }}/{{ card.checklist_items.length }}</span>
                                            </div>
                                            <div class="w-full rounded-full h-1" :class="isDarkMode ? 'bg-slate-700' : 'bg-slate-200'">
                                                <div 
                                                    class="bg-emerald-500 h-1 rounded-full transition-all duration-300" 
                                                    :style="{ width: (card.checklist_items.filter(i => i.is_done).length / card.checklist_items.length) * 100 + '%' }"
                                                ></div>
                                            </div>
                                        </div>

                                        <div v-if="card.attachments && card.attachments.length > 0" class="mb-2">
                                            <div v-if="isImage(card.attachments[0].file)" class="h-20 w-full rounded-md overflow-hidden border relative group/img" :class="isDarkMode ? 'border-slate-700' : 'border-slate-100'">
                                                <img :src="card.attachments[0].file" class="w-full h-full object-cover">
                                                <div class="absolute inset-0 bg-black/10 group-hover/img:bg-transparent transition"></div>
                                            </div>
                                            <div v-else class="text-[10px] border p-1.5 rounded flex items-center gap-1 font-medium" :class="isDarkMode ? 'bg-slate-900 border-slate-700 text-slate-400' : 'bg-slate-50 border-slate-200 text-slate-500'">
                                                <span>📎</span> {{ card.attachments.length }} Dosya
                                            </div>
                                        </div>

                                        <div class="flex justify-between items-center mt-2 pt-2 border-t" :class="isDarkMode ? 'border-slate-700' : 'border-slate-100'">
                                            <div class="flex items-center gap-2">
                                                <span class="text-[10px] font-mono opacity-50">#{{ String(card.id).slice(0,4) }}</span>
                                                <div v-if="card.comments && card.comments.length > 0" class="flex items-center gap-0.5 text-[10px] opacity-70">
                                                    <span>💬</span> {{ card.comments.length }}
                                                </div>
                                            </div>
                                            
                                            <div v-if="card.due_date" class="flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded font-bold border" :class="getDueDateClass(card.due_date)">
                                                <span>📅</span>
                                                {{ new Date(card.due_date).toLocaleDateString('tr-TR', {day: 'numeric', month:'short'}) }}
                                            </div>

                                            <div class="flex -space-x-1.5">
                                                <div v-for="u in card.assignees" :key="u.id" class="w-5 h-5 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-[9px] text-white border border-white shadow-sm font-bold uppercase" :title="u.username">
                                                    {{ u.username.charAt(0) }}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </draggable>
                    </div>

                    <div class="p-2 rounded-b-xl" :class="isDarkMode ? 'bg-slate-800' : 'bg-slate-100'">
                        <div v-if="addingCardToList === list.id" class="p-2 rounded-lg shadow-sm border border-blue-400 animate-in fade-in zoom-in duration-200" :class="isDarkMode ? 'bg-slate-700' : 'bg-white'">
                            <textarea 
                                :id="'card-input-' + list.id"
                                v-model="newCardTitle"
                                @keydown.enter.prevent="createCard(list.id)"
                                @keydown.esc="cancelAddCard"
                                class="w-full text-sm resize-none outline-none bg-transparent p-1"
                                :class="isDarkMode ? 'text-white placeholder-slate-400' : 'text-slate-700 placeholder-slate-400'"
                                rows="2"
                                placeholder="Kart başlığı giriniz..."
                            ></textarea>
                            <div class="flex items-center gap-2 mt-2 justify-end">
                                <button @click="cancelAddCard" class="text-xs opacity-70 hover:opacity-100">İptal</button>
                                <button @click="createCard(list.id)" class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-1.5 rounded shadow-sm transition">Ekle</button>
                            </div>
                        </div>
                        <button v-else @click="showAddCardForm(list.id)" class="w-full text-left p-2 rounded-lg text-sm transition flex items-center gap-2 font-medium group" :class="isDarkMode ? 'text-slate-400 hover:bg-slate-700 hover:text-white' : 'text-slate-500 hover:bg-slate-200 hover:text-slate-700'">
                            <span class="text-lg leading-none opacity-50 group-hover:text-blue-500 transition-colors">+</span> Kart Ekle
                        </button>
                    </div>
                </div>
            </template>
        </draggable>

        <div class="w-80 flex-shrink-0">
            <div v-if="isAddingList" class="p-3 rounded-xl shadow-lg border border-blue-500 animate-in fade-in zoom-in duration-200" :class="isDarkMode ? 'bg-slate-800' : 'bg-white'">
                <input
                    ref="newListInput"
                    v-model="newListTitle"
                    @keydown.enter="createList"
                    @keydown.esc="isAddingList = false"
                    class="w-full border rounded-lg p-2 text-sm outline-none focus:border-blue-500 mb-2"
                    :class="isDarkMode ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400' : 'bg-white border-slate-300 text-slate-700 placeholder-slate-400'"
                    placeholder="Liste adı..."
                >
                <div class="flex items-center gap-2 justify-end">
                    <button @click="isAddingList = false" class="text-xs font-medium opacity-70 hover:opacity-100">İptal</button>
                    <button @click="createList" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">Kaydet</button>
                </div>
            </div>

            <div
                v-else
                @click="startAddingList"
                class="hover:bg-white/10 backdrop-blur-sm rounded-xl p-4 cursor-pointer transition border border-dashed flex items-center justify-center gap-2 h-16 group select-none"
                :class="isDarkMode ? 'bg-white/5 text-white/50 hover:text-white border-white/10 hover:border-white/30' : 'bg-white/40 text-slate-500 hover:text-slate-700 border-slate-300 hover:border-slate-400'"
            >
                <span class="text-2xl group-hover:scale-110 transition-transform">+</span>
                <span class="font-medium text-sm">Yeni Liste Ekle</span>
            </div>
        </div>

      </div>
    </div>

    <div v-else-if="board && viewMode === 'calendar'" class="flex-1 p-6 overflow-hidden animate-fade-in-up">
        <BoardCalendar 
            :lists="board.lists" 
            @openCard="openEditModal" 
        />
    </div>

    <div 
        v-if="contextMenu.visible" 
        :style="{ top: contextMenu.y + 'px', left: contextMenu.x + 'px' }" 
        class="fixed z-[100] w-48 rounded-lg shadow-xl border overflow-hidden animate-scale-in origin-top-left"
        :class="isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'"
    >
        <div class="p-1">
            <button @click="openEditModal(contextMenu.card); closeContextMenu()" class="w-full text-left px-3 py-2 text-xs hover:bg-blue-500 hover:text-white rounded transition flex items-center gap-2" :class="isDarkMode ? 'text-slate-300' : 'text-slate-700'">
                ✏️ Düzenle
            </button>
            <button @click="duplicateCard(contextMenu.card); closeContextMenu()" class="w-full text-left px-3 py-2 text-xs hover:bg-blue-500 hover:text-white rounded transition flex items-center gap-2" :class="isDarkMode ? 'text-slate-300' : 'text-slate-700'">
                📑 Kopyala
            </button>
            <div class="h-px my-1" :class="isDarkMode ? 'bg-slate-700' : 'bg-slate-200'"></div>
            <button @click="deleteCardDirectly(contextMenu.card); closeContextMenu()" class="w-full text-left px-3 py-2 text-xs hover:bg-red-500 hover:text-white rounded transition flex items-center gap-2 text-red-500 font-bold">
                🗑 Sil
            </button>
        </div>
    </div>
    <div v-if="contextMenu.visible" @click="closeContextMenu" class="fixed inset-0 z-[90]"></div>

    <transition name="modal-fade">
    <div v-if="showModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div 
            class="rounded-2xl shadow-2xl w-full max-w-5xl h-[85vh] flex flex-col md:flex-row overflow-hidden relative animate-modal-slide"
            :class="isDarkMode ? 'bg-slate-900 text-white' : 'bg-white text-slate-800'"
        >
            <button @click="closeModal" class="absolute top-4 right-4 z-50 p-2 rounded-full transition shadow-sm border" :class="isDarkMode ? 'text-slate-400 hover:text-white bg-slate-800 border-slate-700' : 'text-slate-400 hover:text-red-500 bg-white border-slate-100'">✕</button>

            <div class="flex-1 p-8 overflow-y-auto custom-scrollbar relative" :class="isDarkMode ? 'bg-slate-900' : 'bg-white'">
                <div class="mb-6">
                    <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider mb-3 opacity-60">
                        <span class="px-2 py-1 rounded border" :class="isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-200'">#{{ String(activeCardId).slice(0,8) }}</span>
                        <span>•</span>
                        <span>Listesi: <span class="text-blue-500 underline decoration-dotted cursor-pointer">{{ getListName(activeListId) }}</span></span>
                    </div>
                    <input v-model="form.title" class="text-3xl font-extrabold w-full outline-none border-b-2 border-transparent focus:border-blue-500 rounded-t px-2 py-1 -ml-2 bg-transparent transition" placeholder="Kart başlığı...">
                </div>

                <div class="mb-6">
                    <h4 class="text-sm font-bold opacity-70 mb-2">🏷️ Etiketler</h4>
                    <div class="flex flex-wrap gap-2">
                        <button 
                            v-for="tag in ['Bug', 'Feature', 'Design', 'Urgent']" 
                            :key="tag" 
                            @click="toggleLabel(tag)"
                            :class="['px-3 py-1 rounded-full text-xs font-bold transition border', 
                            form.labels.includes(tag) ? getLabelColor(tag) + ' border-transparent scale-105' : 'bg-transparent border-slate-500 text-slate-500 hover:border-blue-500 hover:text-blue-500']"
                        >
                            {{ tag }}
                        </button>
                    </div>
                </div>

                <div class="mb-6 flex items-center gap-4 p-4 rounded-xl border" :class="isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-200'">
                    <div class="text-2xl">⏱️</div>
                    <div class="flex-1">
                        <h4 class="text-sm font-bold">Zaman Takibi</h4>
                        <p class="text-xs opacity-60">{{ formatTime(timeSpent) }} harcandı</p>
                    </div>
                    <button @click="toggleTimer" :class="['px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2', isTimerRunning ? 'bg-red-500/20 text-red-500 animate-pulse' : 'bg-emerald-500/20 text-emerald-500']">
                        {{ isTimerRunning ? '⏹ Durdur' : '▶ Başlat' }}
                    </button>
                </div>

                <div class="mb-10 group p-5 rounded-2xl border transition-colors" :class="isDarkMode ? 'bg-slate-800/50 border-slate-700 hover:border-blue-500' : 'bg-slate-50/50 border-slate-100 hover:border-blue-200'">
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-sm font-bold flex items-center gap-2 opacity-70">📄 Açıklama</h4>
                        <button 
                            @click="generateAIDescription"
                            :disabled="generatingAI"
                            class="text-xs flex items-center gap-2 px-3 py-1.5 rounded-full font-bold transition-all border shadow-sm select-none"
                            :class="generatingAI ? 'opacity-50 cursor-wait' : 'bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white border-transparent hover:shadow-purple-500/30'"
                        >
                            <span v-if="generatingAI" class="animate-spin">⚙️</span>
                            <span v-else>✨ AI ile Yaz</span>
                        </button>
                    </div>
                    <textarea v-model="form.description" rows="4" class="w-full bg-transparent border-none outline-none resize-none" placeholder="Bu görev hakkında detaylı bilgi ekleyin..."></textarea>
                </div>

                <div class="mb-10">
                    <div class="flex items-center justify-between mb-4">
                        <h4 class="text-sm font-bold opacity-70 flex items-center gap-2">☑️ Kontrol Listesi</h4>
                        <span class="text-xs font-medium px-2 py-1 rounded" :class="isDarkMode ? 'bg-slate-800' : 'bg-slate-100'">
                            {{ completedChecklistCount }}/{{ activeCardChecklist.length }} Tamamlandı
                        </span>
                    </div>
                    
                    <div class="w-full bg-slate-200/20 rounded-full h-2 mb-6 overflow-hidden">
                        <div class="bg-emerald-500 h-2 rounded-full transition-all duration-500 ease-out" :style="{ width: checklistProgress + '%' }"></div>
                    </div>

                    <div class="space-y-2 mb-4">
                        <div v-for="item in activeCardChecklist" :key="item.id" class="flex items-center gap-3 p-2 rounded-lg group transition" :class="isDarkMode ? 'hover:bg-slate-800' : 'hover:bg-slate-50'">
                            <input 
                                type="checkbox" 
                                :checked="item.is_done" 
                                @change="toggleChecklistItem(item)"
                                class="w-5 h-5 text-emerald-600 rounded cursor-pointer"
                            >
                            <span :class="['flex-1 text-sm transition select-none', item.is_done ? 'line-through opacity-50' : '']">{{ item.text }}</span>
                            <button @click="deleteChecklistItem(item.id)" class="opacity-0 group-hover:opacity-100 transition p-1 text-red-500">🗑</button>
                        </div>
                    </div>

                    <div class="flex gap-2">
                        <input 
                            v-model="newChecklistItem" 
                            @keydown.enter.prevent="addChecklistItem" 
                            placeholder="Yeni madde ekle..." 
                            class="flex-1 border rounded-xl px-4 py-2.5 text-sm bg-transparent outline-none focus:border-blue-500"
                            :class="isDarkMode ? 'border-slate-700' : 'border-slate-200'"
                        >
                        <button @click="addChecklistItem" class="px-4 py-2 rounded-xl text-sm font-bold transition" :class="isDarkMode ? 'bg-slate-800 hover:bg-slate-700' : 'bg-slate-100 hover:bg-slate-200'">Ekle</button>
                    </div>
                </div>

                <div class="mb-10">
                    <h4 class="text-sm font-bold opacity-70 mb-4 flex items-center gap-2">📎 Ekler (Attachments)</h4>
                    
                    <div v-if="activeCardAttachments.length > 0" class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                        <div v-for="att in activeCardAttachments" :key="att.id" class="relative group border rounded-xl overflow-hidden hover:shadow-md transition" :class="isDarkMode ? 'border-slate-700 bg-slate-800' : 'border-slate-200 bg-white'">
                            <img v-if="isImage(att.file)" :src="att.file" class="w-full h-32 object-cover">
                            <div v-else class="w-full h-32 flex flex-col items-center justify-center p-4 text-center">
                                <span class="text-2xl mb-2">📄</span>
                                <span class="text-xs truncate w-full opacity-60">{{ att.filename }}</span>
                            </div>
                            
                            <a :href="att.file" target="_blank" class="absolute inset-0 flex items-center justify-center bg-black/60 opacity-0 group-hover:opacity-100 transition text-white font-bold text-sm backdrop-blur-sm">
                                👁️ Görüntüle
                            </a>
                        </div>
                    </div>

                    <div 
                        class="border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition group relative overflow-hidden"
                        :class="isDarkMode ? 'border-slate-700 hover:border-blue-500 hover:bg-slate-800' : 'border-slate-300 hover:border-blue-500 hover:bg-blue-50'"
                    >
                        <input type="file" @change="handleFileUpload" class="absolute inset-0 opacity-0 cursor-pointer" multiple>
                        
                        <div v-if="uploading" class="absolute inset-0 flex flex-col items-center justify-center z-10 backdrop-blur-sm bg-black/50">
                            <span class="text-xs font-bold text-white animate-pulse">Yükleniyor... %{{ uploadProgress }}</span>
                        </div>

                        <div>
                            <span class="text-3xl block mb-3 group-hover:scale-110 transition duration-300">📂</span>
                            <span class="text-sm opacity-60 font-medium group-hover:text-blue-500 transition">
                                Dosyaları buraya sürükle veya <span class="underline decoration-dotted">seçmek için tıkla</span>
                            </span>
                        </div>
                    </div>
                </div>

                <div class="mt-8">
                    <h4 class="text-sm font-bold opacity-70 mb-4 flex items-center gap-2">💬 Aktivite & Yorumlar</h4>
                    <div class="flex gap-4 mb-8">
                        <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0 shadow-md border-2 border-white">BEN</div>
                        <div class="flex-1 relative">
                            <textarea v-model="newCommentText" placeholder="Bir yorum yaz..." class="w-full border rounded-2xl p-4 text-sm focus:border-blue-500 outline-none shadow-sm pr-14 resize-none min-h-[80px] bg-transparent" :class="isDarkMode ? 'border-slate-700' : 'border-slate-300'" @keydown.enter.prevent="addComment"></textarea>
                            <button @click="addComment" class="absolute right-3 bottom-3 p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition shadow-md hover:scale-105 active:scale-95" title="Gönder">➤</button>
                        </div>
                    </div>
                    <div class="space-y-6 pb-4" ref="commentContainer">
                        <transition-group name="list">
                            <div v-for="comment in activeCardComments" :key="comment.id" class="flex gap-4 group animate-fade-in-up">
                                <div class="w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 border-2 border-white shadow-sm uppercase" :class="isDarkMode ? 'bg-slate-700 text-white' : 'bg-slate-100 text-slate-600'">{{ comment.author ? comment.author.username.charAt(0) : '?' }}</div>
                                <div class="flex-1 p-4 rounded-2xl rounded-tl-none text-sm border transition leading-relaxed shadow-sm" :class="isDarkMode ? 'bg-slate-800 border-slate-700 text-slate-300' : 'bg-slate-50 border-slate-100 text-slate-700'">
                                    <div class="flex items-center gap-2 mb-1">
                                        <span class="font-bold">{{ comment.author ? comment.author.username : 'Anonim' }}</span>
                                        <span class="text-xs opacity-50">{{ new Date(comment.created_at).toLocaleString('tr-TR') }}</span>
                                    </div>
                                    {{ comment.text }}
                                </div>
                            </div>
                        </transition-group>
                    </div>
                </div>
            </div>

            <div class="w-full md:w-80 p-8 flex flex-col gap-8 border-l shadow-inner" :class="isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-200'">
                <div class="flex flex-col gap-3">
                    <button @click="submitCard" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-xl font-bold shadow-lg shadow-blue-500/20 transition transform active:scale-95 flex items-center justify-center gap-2">
                        <span>💾</span> Kaydet
                    </button>
                    
                    <button 
                        v-if="isEditing" 
                        @click="deleteCard"
                        class="w-full border py-3 px-4 rounded-xl font-medium transition flex items-center justify-center gap-2 hover:shadow-sm"
                        :class="isDarkMode ? 'border-slate-600 hover:bg-red-900/30 text-red-400' : 'border-red-200 hover:bg-red-50 text-red-500'"
                    >
                        <span>🗑</span> Sil
                    </button>
                </div>

                <hr :class="isDarkMode ? 'border-slate-700' : 'border-slate-200'">

                <div class="space-y-6">
                    <div>
                        <label class="block text-xs font-bold uppercase mb-2 opacity-60">Öncelik</label>
                        <div class="grid grid-cols-2 gap-2">
                            <button 
                                v-for="p in priorities" :key="p.val" 
                                @click="form.priority = p.val" 
                                :class="['px-3 py-2 rounded-lg text-xs font-bold border transition-all duration-200', form.priority === p.val ? p.activeClass + ' ring-2 ring-offset-1' : (isDarkMode ? 'bg-slate-700 border-slate-600' : 'bg-white border-slate-200')]"
                            >
                                {{ p.label }}
                            </button>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-xs font-bold uppercase mb-2 opacity-60">Atanan Kişi</label>
                        <div class="relative">
                            <select v-model="form.assignee" class="w-full border rounded-lg p-3 text-sm outline-none appearance-none cursor-pointer bg-transparent" :class="isDarkMode ? 'border-slate-600' : 'border-slate-300'">
                                <option :value="null">Atanmadı</option>
                                <option v-for="member in board.members" :key="member.id" :value="member.id">
                                    {{ member.username }}
                                </option>
                            </select>
                            <div class="absolute right-3 top-3.5 pointer-events-none opacity-50">▼</div>
                        </div>
                    </div>

                    <div>
                         <label class="block text-xs font-bold uppercase mb-2 opacity-60">Bitiş Tarihi</label>
                         <input v-model="form.due_date" type="date" class="w-full border rounded-lg p-3 text-sm outline-none cursor-pointer bg-transparent" :class="isDarkMode ? 'border-slate-600' : 'border-slate-300'">
                    </div>
                </div>
            </div>

        </div>
    </div>
    </transition>

    <transition name="slide-right">
    <div v-if="showActivity" class="fixed inset-y-0 right-0 w-80 border-l shadow-2xl z-50 p-6 overflow-y-auto" :class="isDarkMode ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
        <div class="flex justify-between items-center mb-6">
            <h3 class="text-lg font-bold">📜 Pano Geçmişi</h3>
            <button @click="showActivity = false" class="opacity-50 hover:opacity-100">✕</button>
        </div>

        <div class="space-y-6">
            <div v-for="act in activities" :key="act.id" class="relative pl-6 border-l-2 pb-2 last:pb-0" :class="isDarkMode ? 'border-slate-700' : 'border-slate-200'">
                <div class="absolute -left-[9px] top-0 w-4 h-4 bg-slate-800 border-2 border-blue-500 rounded-full"></div>
                <div class="flex flex-col gap-1">
                    <span class="text-xs text-blue-500 font-bold">{{ act.actor_name }}</span>
                    <span class="text-sm font-medium opacity-80">{{ act.action_type }}</span>
                    <p class="text-xs opacity-50">{{ act.description }}</p>
                    <span class="text-[10px] opacity-40 mt-1">{{ new Date(act.created_at).toLocaleString('tr-TR') }}</span>
                </div>
            </div>
            <div v-if="activities.length === 0" class="text-center opacity-50 text-sm italic">
                Henüz bir hareket yok.
            </div>
        </div>
    </div>
    </transition>

  </div>
</template>

<script setup>
import { useToast } from "vue-toastification";
const toast = useToast();
import { ref, onMounted, onBeforeUnmount, reactive, nextTick, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useBoardStore } from '../stores/board';
import { useAuthStore } from '../stores/auth'; // Auth Store
import draggable from 'vuedraggable';
import api from '../utils/axios';
import BoardCalendar from '../components/BoardCalendar.vue';

const route = useRoute();
const boardStore = useBoardStore();
const authStore = useAuthStore();

const board = ref(null);
const loading = ref(true);
const saving = ref(false);
const socket = ref(null);
const socketConnected = ref(false);
const viewMode = ref('kanban'); // 'kanban' | 'calendar'
const isDarkMode = ref(true); // 🌗 TEMA DEĞİŞKENİ
const filterMode = ref('all'); // 🔍 FİLTRE DEĞİŞKENİ

const showModal = ref(false);
const isEditing = ref(false);
const activeListId = ref(null);
const activeCardId = ref(null);
const activeCardComments = ref([]);
const activeCardAttachments = ref([]);
const activeCardChecklist = ref([]);
const newChecklistItem = ref('');
const newCommentText = ref('');
const generatingAI = ref(false);
const commentContainer = ref(null);
const uploading = ref(false);
const uploadProgress = ref(0);

// Zaman Takibi
const timeSpent = ref(0);
const isTimerRunning = ref(false);
let timerInterval = null;

// Sağ Tık Menüsü
const contextMenu = ref({ visible: false, x: 0, y: 0, card: null });

const addingCardToList = ref(null);
const newCardTitle = ref('');
const isAddingList = ref(false);
const newListTitle = ref('');
const newListInput = ref(null);

const showActivity = ref(false);
const activities = ref([]);

const form = reactive({
    title: '',
    description: '',
    priority: 'medium',
    assignee: null,
    due_date: '',
    labels: [] // 🏷️ ETİKETLER
});

const priorities = [
    { val: 'low', label: 'Düşük', activeClass: 'bg-emerald-500/20 text-emerald-500 border-emerald-500' },
    { val: 'medium', label: 'Orta', activeClass: 'bg-orange-500/20 text-orange-500 border-orange-500' },
    { val: 'high', label: 'Yüksek', activeClass: 'bg-red-500/20 text-red-500 border-red-500' },
    { val: 'urgent', label: 'Acil', activeClass: 'bg-purple-500/20 text-purple-500 border-purple-500' }
];

onMounted(async () => {
    await refreshBoard();
    connectWebSocket();
});

onBeforeUnmount(() => {
    if (socket.value) socket.value.close();
    if (timerInterval) clearInterval(timerInterval);
});

// TEMA DEĞİŞTİRİCİ
const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value;
};

const refreshBoard = async () => {
    try {
        const boardId = route.params.id;
        board.value = await boardStore.fetchBoardDetail(boardId);
        if (!board.value.lists) board.value.lists = [];
    } catch (e) { console.error(e); } finally { loading.value = false; }
};

// 🔍 FİLTRELEME MANTIĞI
const shouldShowCard = (card) => {
    if (filterMode.value === 'all') return true;
    if (filterMode.value === 'me') {
        return card.assignees.some(u => u.username === authStore.user?.username);
    }
    if (filterMode.value === 'urgent') {
        return card.priority === 'urgent' || card.priority === 'high';
    }
    return true;
};

const connectWebSocket = () => {
    if (socket.value) socket.value.close();
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//127.0.0.1:8000/ws/board/${route.params.id}/`;
    socket.value = new WebSocket(wsUrl);
    socket.value.onopen = () => socketConnected.value = true;
    socket.value.onmessage = (event) => handleSocketMessage(JSON.parse(event.data));
    socket.value.onclose = () => { socketConnected.value = false; setTimeout(connectWebSocket, 3000); };
};

const handleSocketMessage = (data) => {
    if (!board.value) return;
    if (data.action === 'card_updated') updateLocalCard(data.card);
    else if (data.action === 'card_created') { addLocalCard(data.list_id, data.card); toast.info(`Yeni kart: ${data.card.title}`); }
    else if (data.action === 'new_comment') {
        if (activeCardId.value === data.card_id) { activeCardComments.value.push(data.comment); scrollToBottom(); }
    }
};

const updateLocalCard = (updatedCard) => {
    board.value.lists.forEach(list => {
        const index = list.cards.findIndex(c => c.id === updatedCard.id);
        if (index !== -1) list.cards.splice(index, 1);
    });
    const targetList = board.value.lists.find(l => l.id === updatedCard.list);
    if (targetList) { targetList.cards.push(updatedCard); targetList.cards.sort((a, b) => a.position - b.position); }
    if (activeCardId.value === updatedCard.id) {
        activeCardAttachments.value = updatedCard.attachments || [];
        activeCardChecklist.value = updatedCard.checklist_items || [];
    }
};

const addLocalCard = (listId, newCard) => {
    const list = board.value.lists.find(l => l.id === listId);
    if (list) list.cards.push(newCard);
};

// 🖱️ SAĞ TIK MENÜSÜ
const showContextMenu = (e, card) => {
    contextMenu.value = { visible: true, x: e.clientX, y: e.clientY, card: card };
};
const closeContextMenu = () => contextMenu.value.visible = false;

const deleteCardDirectly = async (card) => {
    if(!confirm("Silinsin mi?")) return;
    try { await api.delete(`cards/${card.id}/`); updateLocalCard({...card, list: -1}); refreshBoard(); toast.info("Silindi"); } catch(e){ toast.error("Hata"); }
};

const duplicateCard = async (card) => {
    try {
        await api.post('cards/', { ...card, id: undefined, title: card.title + ' (Kopya)', list: card.list });
        toast.success("Kopyalandı");
        refreshBoard();
    } catch(e){ toast.error("Hata"); }
};

// 🏷️ ETİKETLER
const toggleLabel = (tag) => {
    if (form.labels.includes(tag)) form.labels = form.labels.filter(t => t !== tag);
    else form.labels.push(tag);
};
const getLabelColor = (tag) => {
    switch(tag) {
        case 'Bug': return 'bg-red-500/20 text-red-500 border-red-500';
        case 'Feature': return 'bg-blue-500/20 text-blue-500 border-blue-500';
        case 'Design': return 'bg-purple-500/20 text-purple-500 border-purple-500';
        case 'Urgent': return 'bg-orange-500/20 text-orange-500 border-orange-500';
        default: return 'bg-slate-500/20 text-slate-500 border-slate-500';
    }
};

// ⏱️ ZAMAN SAYACI
const toggleTimer = () => {
    if (isTimerRunning.value) {
        clearInterval(timerInterval);
        isTimerRunning.value = false;
        toast.info(`Süre durduruldu: ${formatTime(timeSpent.value)}`);
    } else {
        isTimerRunning.value = true;
        timerInterval = setInterval(() => { timeSpent.value++; }, 1000);
    }
};
const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h}s ${m}d ${s}sn`;
};

const scrollToBottom = () => nextTick(() => commentContainer.value && (commentContainer.value.scrollTop = commentContainer.value.scrollHeight));
const showAddCardForm = (listId) => { addingCardToList.value = listId; newCardTitle.value = ''; nextTick(() => document.getElementById(`card-input-${listId}`)?.focus()); };
const cancelAddCard = () => { addingCardToList.value = null; newCardTitle.value = ''; };
const createCard = async (listId) => { if (!newCardTitle.value.trim()) return; try { await api.post('cards/', { title: newCardTitle.value, list: listId, description: '', priority: 'medium' }); newCardTitle.value = ''; nextTick(() => document.getElementById(`card-input-${listId}`)?.focus()); } catch (e) { toast.error("Hata"); } };
const startAddingList = () => { isAddingList.value = true; nextTick(() => newListInput.value?.focus()); };
const createList = async () => { if (!newListTitle.value.trim()) return; try { await api.post('lists/', { title: newListTitle.value, board: route.params.id, position: board.value.lists?.length || 0 }); toast.success("Liste eklendi!"); newListTitle.value = ''; isAddingList.value = false; await refreshBoard(); } catch (e) { toast.error("Hata"); } };
const openEditModal = (card) => { isEditing.value = true; activeListId.value = card.list; activeCardId.value = card.id; activeCardComments.value = card.comments || []; activeCardAttachments.value = card.attachments || []; activeCardChecklist.value = card.checklist_items || []; form.title = card.title; form.description = card.description; form.priority = card.priority; form.due_date = card.due_date ? new Date(card.due_date).toISOString().split('T')[0] : ''; form.assignee = (card.assignees && card.assignees.length > 0) ? card.assignees[0].id : null; form.labels = card.labels || []; showModal.value = true; scrollToBottom(); };
const closeModal = () => showModal.value = false;
const submitCard = async () => { const payload = { title: form.title, description: form.description, priority: form.priority, list: activeListId.value, due_date: form.due_date || null, assignees: form.assignee ? [form.assignee] : [], labels: form.labels }; try { if (isEditing.value) { await api.patch(`cards/${activeCardId.value}/`, payload); toast.success("Kaydedildi"); } else { await api.post('cards/', payload); } closeModal(); } catch (e) { toast.error("Hata"); } };
const deleteCard = async () => { if (!confirm("Silinsin mi?")) return; try { await api.delete(`cards/${activeCardId.value}/`); closeModal(); toast.info("Silindi"); } catch (e) { toast.error("Hata"); } };
const addComment = async () => { if (!newCommentText.value.trim()) return; try { const res = await api.post('comments/', { card: activeCardId.value, text: newCommentText.value }); activeCardComments.value.push(res.data); newCommentText.value = ''; scrollToBottom(); } catch(e) { toast.error("Hata"); } };
const onCardMove = async (event, listId) => { if (event.added) { saving.value = true; try { await api.patch(`cards/${event.added.element.id}/`, { list: listId }); } catch(e) { refreshBoard(); } finally { saving.value = false; } } };
const onListMove = async (event) => { if (event.moved) { try { await api.patch(`lists/${event.moved.element.id}/`, { position: event.moved.newIndex }); } catch(e){} } };
const generateAIDescription = async () => { generatingAI.value = true; try { const res = await api.post('cards/ai_generate/', { title: form.title }, { timeout: 60000 }); form.description = res.data.description; toast.success("AI yazdı!"); } catch (e) { toast.error("Hata"); } finally { generatingAI.value = false; } };
const handleFileUpload = async (event) => { const files = event.target.files; if (!files.length) return; uploading.value = true; for (let i = 0; i < files.length; i++) { const formData = new FormData(); formData.append('file', files[i]); formData.append('card', activeCardId.value); try { const res = await api.post('attachments/', formData, { headers: { 'Content-Type': 'multipart/form-data' }, onUploadProgress: (p) => uploadProgress.value = Math.round((p.loaded * 100) / p.total) }); activeCardAttachments.value.push(res.data); } catch (e) { toast.error("Hata"); } } uploading.value = false; refreshBoard(); };
const addChecklistItem = async () => { if (!newChecklistItem.value.trim()) return; try { const res = await api.post('checklists/', { card: activeCardId.value, text: newChecklistItem.value, is_done: false }); activeCardChecklist.value.push(res.data); newChecklistItem.value = ''; refreshBoard(); } catch (e) { toast.error("Hata"); } };
const toggleChecklistItem = async (item) => { try { item.is_done = !item.is_done; await api.patch(`checklists/${item.id}/`, { is_done: item.is_done }); refreshBoard(); } catch (e) { item.is_done = !item.is_done; } };
const deleteChecklistItem = async (id) => { try { await api.delete(`checklists/${id}/`); activeCardChecklist.value = activeCardChecklist.value.filter(i => i.id !== id); refreshBoard(); } catch (e) { toast.error("Hata"); } };
const fetchActivities = async () => { try { const res = await api.get(`activities/?board=${route.params.id}`); activities.value = res.data; showActivity.value = true; } catch (e) { console.error(e); } };

const completedChecklistCount = computed(() => activeCardChecklist.value.filter(i => i.is_done).length);
const checklistProgress = computed(() => activeCardChecklist.value.length === 0 ? 0 : (completedChecklistCount.value / activeCardChecklist.value.length) * 100);
const isImage = (url) => url.match(/\.(jpeg|jpg|gif|png|webp)$/) != null;
const getListName = (id) => board.value ? board.value.lists.find(x => x.id === id)?.title : '';
const getDueDateClass = (date) => { const today = new Date().toISOString().split('T')[0]; if (date < today) return 'text-red-500 bg-red-500/10 border-red-500'; if (date === today) return 'text-orange-500 bg-orange-500/10 border-orange-500'; return 'text-blue-500 bg-blue-500/10 border-blue-500'; };
const getPriorityColorClass = (p) => { if(p==='urgent') return 'bg-purple-600'; if(p==='high') return 'bg-red-500'; if(p==='medium') return 'bg-orange-400'; return 'bg-emerald-400'; }
</script>

<style scoped>
.ghost-card { opacity: 0.5; border: 2px dashed #94a3b8; }
.ghost-list { opacity: 0.5; border: 2px dashed #3b82f6; }
.drag-card { transform: rotate(2deg); cursor: grabbing; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2); }
.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #64748b; border-radius: 10px; }
.bg-pattern-dark { background-image: radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px); background-size: 24px 24px; }
.bg-pattern-light { background-image: radial-gradient(rgba(0, 0, 0, 0.05) 1px, transparent 1px); background-size: 24px 24px; }
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.slide-right-enter-active, .slide-right-leave-active { transition: transform 0.3s ease; }
.slide-right-enter-from, .slide-right-leave-to { transform: translateX(100%); }
.animate-scale-in { animation: scaleIn 0.1s ease-out; }
@keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes modalSlide { from { opacity: 0; transform: translateY(20px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
.animate-modal-slide { animation: modalSlide 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
</style>