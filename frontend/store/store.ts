import { create } from 'zustand'
import axios from 'axios';

const URL = "http://127.0.0.1:8080"

export const useChatStore = create((set: any) => ({
    isLoading: false,
    cats: [],
    userId: 1,
    page: 1,
    totalPage: 0,
    activeTab: "Features",
    query: "",
    selectedBreed: "",

    setQuery: (query: string) => set((state: any) => ({ query: query })),
    setSelectedBreed: (breed: string) => set((state: any) => ({ selectedBreed: breed })),
    setActiveTab: (tab: string) => set((state: any) => ({ activeTab: tab })),
    setIsLoading : () => set((state: any) => ({ isLoading: !state.isLoading})),
    setPage: (page: number) => set((state: any) => ({ page: page })),
    setTotalPage: (page: number) => set((state: any) => ({ totalPage: page })),

    fetchAllCats: async () => {
        set({ isLoading: true });
        try {
            const { data } = await axios.get(`${URL}/cats?page=${useChatStore.getState().page}&user_id=${useChatStore.getState().userId}`);
            set({ page: data.current_page, totalPage: data.total_pages, cats: data.cats, isLoading: false });
        } catch (error) {
            console.log(error);
            set({ isLoading: false });
        }
    },
    addOrRemoveFavorite: async (imageId: number, favorite: boolean, body: any) => {
        try {
            set((state: any) => ({ cats: state.cats.map((cat: any) => cat.id === imageId ? { ...cat, favorite: !cat.favorite } : cat) }));
            if(!favorite) {
                const { data } = await axios.post(`${URL}/cats`, { user_id: useChatStore.getState().userId, ...body });
            } else {
                const { data } = await axios.delete(`${URL}/cats?image_id=${imageId}&user_id=${useChatStore.getState().userId}`);
            }
        } catch (error) {
            console.log(error);
        }
    },
    fetchFavoriteCats: async () => {
        set({ isLoading: true });
        try {
            const { data } = await axios.get(`${URL}/cats/favorite?user_id=${useChatStore.getState().userId}`);
            console.log(data)
            set({ page: data.current_page, totalPage: data.total_pages, cats: data.cats, isLoading: false });
        } catch (error) {
            console.log(error);
            set({ isLoading: false });
        }
    },

    fetchQuery: async (query: string, breed: string) => {
        set({ isLoading: true });
        if(!breed || breed === "All") breed = "";
        try {
            const { data } = await axios.get(`${URL}/cats?page=${useChatStore.getState().page}&user_id=${useChatStore.getState().userId}&query=${query}&breed=${breed}`);
            set({ page: data.current_page, totalPage: data.total_pages, cats: data.cats, isLoading: false });
        } catch (error) {
            console.log(error);
            set({ isLoading: false });
        }
    },

    editPreference: async (id: number, description: string, breed: string) => {
        try {
            await axios.put(`${URL}/cats/${id}`, { description: description, name: breed });
        } catch (error) {
            console.log(error)
        }
    }

  }));