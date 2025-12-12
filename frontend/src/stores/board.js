import { defineStore } from 'pinia';
import api from '../utils/axios';

export const useBoardStore = defineStore('board', {
    state: () => ({
        workspaces: [],
        loading: false,
        error: null
    }),

    actions: {
        async fetchWorkspaces() {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.get('workspaces/');
                this.workspaces = response.data;
            } catch (err) {
                console.error("Veri çekilemedi:", err);
                this.error = "Veriler yüklenirken bir hata oluştu.";
            } finally {
                this.loading = false;
            }
        },
        async fetchBoardDetail(boardId) {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.get(`boards/${boardId}/`);
                return response.data; 
            } catch (err) {
                console.error("Board detayı çekilemedi:", err);
                this.error = "Board yüklenirken hata oluştu.";
            } finally {
                this.loading = false;
            }
        }
    }
});