'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

type DialogContextType = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

const DialogContext = React.createContext<DialogContextType | null>(null);

function Dialog({
  open,
  onOpenChange,
  children,
}: {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: React.ReactNode;
}) {
  const [internalOpen, setInternalOpen] = React.useState(false);
  const isControlled = open !== undefined;
  const isOpen = isControlled ? open : internalOpen;
  const handleOpenChange = React.useCallback(
    (next: boolean) => {
      if (!isControlled) setInternalOpen(next);
      onOpenChange?.(next);
    },
    [isControlled, onOpenChange]
  );
  return (
    <DialogContext.Provider value={{ open: isOpen, onOpenChange: handleOpenChange }}>
      {children}
    </DialogContext.Provider>
  );
}

const DialogTrigger = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement> & { asChild?: boolean }
>(({ children, asChild, onClick, ...props }, ref) => {
  const ctx = React.useContext(DialogContext);
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    ctx?.onOpenChange(true);
    onClick?.(e);
  };
  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children, { ref, onClick: handleClick } as any);
  }
  return (
    <button type="button" ref={ref} onClick={handleClick} {...props}>
      {children}
    </button>
  );
});
DialogTrigger.displayName = 'DialogTrigger';

function DialogContent({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  const ctx = React.useContext(DialogContext);
  if (!ctx?.open) return null;
  return (
    <>
      <div
        className="fixed inset-0 z-50 bg-black/50"
        aria-hidden
        onClick={() => ctx.onOpenChange(false)}
      />
      <div
        className={cn(
          'fixed left-1/2 top-1/2 z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg border shadow-lg p-6 mx-4 max-h-[90vh] overflow-y-auto',
          className
        )}
        {...props}
      >
        {children}
      </div>
    </>
  );
}

function DialogHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('mb-4', className)} {...props} />;
}

function DialogTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h2 className={cn('text-lg font-semibold', className)} {...props} />;
}

function DialogDescription({
  className,
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  return <p className={cn('text-sm text-gray-500 mt-1', className)} {...props} />;
}

export { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription };
