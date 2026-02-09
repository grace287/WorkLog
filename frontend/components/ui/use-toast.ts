'use client';

export type ToastVariant = 'default' | 'destructive';

export interface ToastOptions {
  title?: string;
  description?: string;
  variant?: ToastVariant;
}

/**
 * 토스트 알림. (나중에 Toaster UI 연동 가능)
 */
export function toast(options: ToastOptions) {
  const msg = [options.title, options.description].filter(Boolean).join(': ');
  if (typeof window !== 'undefined') {
    if (options.variant === 'destructive') {
      console.error('[Toast]', msg);
    } else {
      console.log('[Toast]', msg);
    }
  }
}
