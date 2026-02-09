'use client';

export type ToastVariant = 'default' | 'destructive';

export interface ToastOptions {
  title?: string;
  description?: string;
  variant?: ToastVariant;
}

const TOAST_EVENT = 'worklog-toast';

/**
 * 토스트 알림. Toaster가 있으면 UI에 표시, 없으면 console.
 */
export function toast(options: ToastOptions) {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(new CustomEvent(TOAST_EVENT, { detail: options }));
}
