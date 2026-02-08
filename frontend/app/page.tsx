// app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api/client';

export default function Home() {
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    apiClient.get('/').then((res) => {
      setStatus(res.data);
    });
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-4">WorkLog</h1>
      
      {status ? (
        <div className="text-center">
          <p className="text-xl">✅ Backend Connected</p>
          <pre className="mt-4 p-4 bg-gray-100 rounded">
            {JSON.stringify(status, null, 2)}
          </pre>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </main>
  );
}