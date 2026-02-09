'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

type SelectContextType = {
  value: string;
  onValueChange: (v: string) => void;
  open: boolean;
  setOpen: (v: boolean) => void;
  triggerRef: React.RefObject<HTMLButtonElement | null>;
};

const SelectContext = React.createContext<SelectContextType | null>(null);

function Select({
  value = '',
  onValueChange,
  children,
}: {
  value?: string;
  onValueChange?: (value: string) => void;
  children: React.ReactNode;
}) {
  const [open, setOpen] = React.useState(false);
  const triggerRef = React.useRef<HTMLButtonElement>(null);
  const ctx: SelectContextType = {
    value: value ?? '',
    onValueChange: (v) => {
      onValueChange?.(v);
      setOpen(false);
    },
    open,
    setOpen,
    triggerRef,
  };
  return (
    <SelectContext.Provider value={ctx}>
      <div className="relative">{children}</div>
    </SelectContext.Provider>
  );
}

const SelectTrigger = React.forwardRef<
  HTMLButtonElement,
  React.HTMLAttributes<HTMLButtonElement> & { children?: React.ReactNode }
>(({ className, children, ...props }, ref) => {
  const ctx = React.useContext(SelectContext);
  if (!ctx) return null;
  const mergedRef = (node: HTMLButtonElement | null) => {
    (ctx.triggerRef as React.MutableRefObject<HTMLButtonElement | null>).current = node;
    if (typeof ref === 'function') ref(node);
    else if (ref) (ref as React.MutableRefObject<HTMLButtonElement | null).current = node;
  };
  return (
    <button
      ref={mergedRef}
      type="button"
      className={cn(
        'flex h-10 w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400',
        className
      )}
      onClick={() => ctx.setOpen(!ctx.open)}
      {...props}
    >
      {children}
    </button>
  );
});
SelectTrigger.displayName = 'SelectTrigger';

function SelectValue({ placeholder = '선택...' }: { placeholder?: string }) {
  const ctx = React.useContext(SelectContext);
  const [label, setLabel] = React.useState('');
  // Label is set by SelectItem when it matches value; we don't have direct access to items here.
  // So we just show value or placeholder.
  React.useEffect(() => {
    setLabel(ctx?.value ?? '');
  }, [ctx?.value]);
  return <span>{label || placeholder}</span>;
}

function SelectContent({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  const ctx = React.useContext(SelectContext);
  const ref = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (!ctx?.open) return;
    const close = (e: MouseEvent) => {
      if (
        ref.current?.contains(e.target as Node) ||
        ctx.triggerRef.current?.contains(e.target as Node)
      )
        return;
      ctx.setOpen(false);
    };
    document.addEventListener('click', close);
    return () => document.removeEventListener('click', close);
  }, [ctx?.open, ctx]);

  if (!ctx?.open) return null;
  return (
    <div
      ref={ref}
      className={cn(
        'absolute z-50 mt-1 w-full rounded-md border border-gray-200 bg-white py-1 shadow-lg',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

function SelectItem({
  value,
  children,
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & { value: string; children?: React.ReactNode }) {
  const ctx = React.useContext(SelectContext);
  const isSelected = ctx?.value === value;
  return (
    <div
      role="option"
      aria-selected={isSelected}
      className={cn(
        'relative flex cursor-pointer select-none items-center rounded-sm py-2 px-3 text-sm outline-none hover:bg-gray-100',
        isSelected && 'bg-gray-100',
        className
      )}
      onClick={() => ctx?.onValueChange(value)}
      {...props}
    >
      {children}
    </div>
  );
}

export { Select, SelectTrigger, SelectValue, SelectContent, SelectItem };
