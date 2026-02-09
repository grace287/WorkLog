'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

type TabsContextType = {
  value: string;
  onValueChange: (v: string) => void;
};

const TabsContext = React.createContext<TabsContextType | null>(null);

function Tabs({
  value,
  onValueChange,
  children,
  className,
  ...props
}: {
  value: string;
  onValueChange: (value: string) => void;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <TabsContext.Provider value={{ value, onValueChange }}>
      <div className={cn(className)} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  );
}

function TabsList({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        'inline-flex h-10 items-center justify-center rounded-md bg-gray-100 p-1 text-gray-600',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

function TabsTrigger({
  value,
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLButtonElement> & { value: string; children?: React.ReactNode }) {
  const ctx = React.useContext(TabsContext);
  const isActive = ctx?.value === value;
  return (
    <button
      type="button"
      role="tab"
      aria-selected={isActive}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-400 disabled:pointer-events-none disabled:opacity-50',
        isActive ? 'bg-white text-gray-900 shadow-sm' : 'hover:bg-gray-200/80',
        className
      )}
      onClick={() => ctx?.onValueChange(value)}
      {...props}
    >
      {children}
    </button>
  );
}

export { Tabs, TabsList, TabsTrigger };
