// app/(dashboard)/page.tsx
'use client';

import { useState } from 'react';
import { useTodayTasks } from '@/hooks/useTasks';
import { Task } from '@/types';
import { TaskList } from '@/components/task/TaskList';
import { CreateTaskDialog } from '@/components/task/CreateTaskDialog';
import { EditTaskDialog } from '@/components/task/EditTaskDialog';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { RefreshCw } from 'lucide-react';

export default function TodayPage() {
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const { data: tasks, isLoading, refetch, isRefetching } = useTodayTasks();

  // 오늘 날짜
  const today = format(new Date(), 'yyyy년 M월 d일 (EEEE)', { locale: ko });

  // 통계
  const totalTasks = tasks?.length || 0;
  const completedTasks = tasks?.filter((t) => t.status === 'done').length || 0;
  const completionRate =
    totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <div className="max-w-4xl mx-auto">
      {/* 헤더 */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-3xl font-bold text-gray-900">오늘 할 일</h1>
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            disabled={isRefetching}
          >
            <RefreshCw
              className={`h-4 w-4 ${isRefetching ? 'animate-spin' : ''}`}
            />
          </Button>
        </div>
        <p className="text-gray-600">{today}</p>
      </div>

      {/* 통계 카드 */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg border p-4">
          <p className="text-sm text-gray-600 mb-1">전체</p>
          <p className="text-2xl font-bold text-gray-900">{totalTasks}</p>
        </div>
        <div className="bg-white rounded-lg border p-4">
          <p className="text-sm text-gray-600 mb-1">완료</p>
          <p className="text-2xl font-bold text-green-600">{completedTasks}</p>
        </div>
        <div className="bg-white rounded-lg border p-4">
          <p className="text-sm text-gray-600 mb-1">완료율</p>
          <p className="text-2xl font-bold text-blue-600">{completionRate}%</p>
        </div>
      </div>

      {/* 새 태스크 버튼 */}
      <div className="mb-6">
        <CreateTaskDialog />
      </div>

      {/* 태스크 목록 */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      ) : (
        <TaskList
          tasks={tasks || []}
          onEditTask={setEditingTask}
          emptyMessage="오늘 할 일이 없습니다 🎉"
        />
      )}

      {/* 수정 다이얼로그 */}
      <EditTaskDialog
        task={editingTask}
        open={!!editingTask}
        onOpenChange={(open) => !open && setEditingTask(null)}
      />
    </div>
  );
}
