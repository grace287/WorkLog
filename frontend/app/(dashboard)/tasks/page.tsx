// app/(dashboard)/tasks/page.tsx
'use client';

import { useState } from 'react';
import { useTasks } from '@/hooks/useTasks';
import { Task, TaskStatus, TaskPriority } from '@/types';
import { TaskList } from '@/components/task/TaskList';
import { CreateTaskDialog } from '@/components/task/CreateTaskDialog';
import { EditTaskDialog } from '@/components/task/EditTaskDialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Skeleton } from '@/components/ui/skeleton';
import { Search, X } from 'lucide-react';

export default function TasksPage() {
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // 필터 상태
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<TaskStatus | 'all'>('all');
  const [priority, setPriority] = useState<TaskPriority | 'all'>('all');
  const [page, setPage] = useState(0);
  const limit = 20;

  // API 호출
  const { data, isLoading } = useTasks({
    skip: page * limit,
    limit,
    status: status === 'all' ? undefined : status,
    priority: priority === 'all' ? undefined : priority,
    search: search || undefined,
  });

  // 필터 초기화
  const resetFilters = () => {
    setSearch('');
    setStatus('all');
    setPriority('all');
    setPage(0);
  };

  const hasFilters = search || status !== 'all' || priority !== 'all';

  return (
    <div className="max-w-6xl mx-auto">
      {/* 헤더 */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">모든 태스크</h1>
          <p className="text-gray-600 mt-1">
            총 {data?.total || 0}개의 태스크
          </p>
        </div>
        <CreateTaskDialog />
      </div>

      {/* 필터 영역 */}
      <div className="bg-white rounded-lg border p-4 mb-6">
        <div className="space-y-4">
          {/* 검색 */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="태스크 검색..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9"
            />
          </div>

          {/* 상태 탭 */}
          <div>
            <p className="text-sm font-medium text-gray-700 mb-2">상태</p>
            <Tabs value={status} onValueChange={(v) => setStatus(v as TaskStatus | 'all')}>
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="all">전체</TabsTrigger>
                <TabsTrigger value="todo">할 일</TabsTrigger>
                <TabsTrigger value="doing">진행 중</TabsTrigger>
                <TabsTrigger value="done">완료</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          {/* 우선순위 선택 */}
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-700 mb-2">
                우선순위
              </p>
              <Select
                value={priority}
                onValueChange={(v) => setPriority(v as TaskPriority | 'all')}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">전체</SelectItem>
                  <SelectItem value="high">🔴 높음</SelectItem>
                  <SelectItem value="medium">🟡 보통</SelectItem>
                  <SelectItem value="low">🟢 낮음</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* 필터 초기화 */}
            {hasFilters && (
              <Button
                variant="outline"
                size="sm"
                onClick={resetFilters}
                className="mt-7"
              >
                <X className="h-4 w-4 mr-1" />
                초기화
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* 태스크 목록 */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      ) : (
        <>
          <TaskList
            tasks={data?.items || []}
            onEditTask={setEditingTask}
            emptyMessage="태스크가 없습니다"
          />

          {/* 페이지네이션 */}
          {data && data.total > limit && (
            <div className="flex items-center justify-center gap-2 mt-6">
              <Button
                variant="outline"
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                disabled={page === 0}
              >
                이전
              </Button>
              <span className="text-sm text-gray-600">
                {page + 1} / {Math.ceil(data.total / limit)}
              </span>
              <Button
                variant="outline"
                onClick={() => setPage((p) => p + 1)}
                disabled={!data.has_more}
              >
                다음
              </Button>
            </div>
          )}
        </>
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
