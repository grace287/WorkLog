// lib/store/auth.ts
import { create } from 'zustand';
import { User } from '@/types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;

  setAuth: (user: User, token: string) => void;
  setUser: (user: User) => void;
  logout: () => void;
  initAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  setAuth: (user, token) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
    set({ user, token, isAuthenticated: true });
  },

  setUser: (user) => {
    set({ user });
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    set({ user: null, token: null, isAuthenticated: false });
  },

  initAuth: () => {
    if (typeof window === 'undefined') return;
    const token = localStorage.getItem('access_token');
    if (token) {
      set({ token, isAuthenticated: true });
    }
  },
}));
