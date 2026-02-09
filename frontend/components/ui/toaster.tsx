'use client';

import { useEffect, useState } from 'react';
import { ToastOptions } from './use-toast';
import { cn } from '@/lib/utils';

const TOAST_EVENT = 'worklog-toast';

export function Toaster() {
  const [toasts, setToasts] = useState<Array<ToastOptions & { id: number }>>([]);

  useEffect(() => {
    const handler = (e: CustomEvent<ToastOptions>) => {
      const options = e.detail;
      const id = Date.now();
      setToasts((prev) => [...prev.slice(-4), { ...options, id }]);
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => (t as { id: number }).id !== id));
      }, 4000);
    };
    window.addEventListener(TOAST_EVENT, handler as EventListener);
    return () => window.removeEventListener(TOAST_EVENT, handler as EventListener);
  }, []);

  if (toasts.length === 0) return null;

  return (
    <div
      className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full"
      aria-live="polite"
    >
      {toasts.map((t) => {
        const item = t as ToastOptions & { id: number };
        return (
          <div
            key={item.id}
            className={cn(
              'rounded-lg border px-4 py-3 shadow-lg text-sm',
              item.variant === 'destructive'
                ? 'border-red-200 bg-red-50 text-red-900'
                : 'border-gray-200 bg-white text-gray-900'
            )}
          >
            {item.title && <p className="font-medium">{item.title}</p>}
            {item.description && <p className="mt-0.5 text-gray-600">{item.description}</p>}
          </div>
        );
      })}
    </div>
  );
}
