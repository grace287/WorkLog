// components/task/EditTaskDialog.tsx
'use client';

import { useEffect, useState } from 'react';
import { useUpdateTask } from '@/hooks/useTasks';
import { Task, TaskPriority, TaskStatus } from '@/types';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { format } from 'date-fns';

interface EditTaskDialogProps {
  task: Task | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function EditTaskDialog({
  task,
  open,
  onOpenChange,
}: EditTaskDialogProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<TaskPriority>('medium');
  const [status, setStatus] = useState<TaskStatus>('todo');
  const [dueDate, setDueDate] = useState('');

  const updateTask = useUpdateTask();

  // task가 바뀔 때마다 폼 업데이트
  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || '');
      setPriority(task.priority);
      setStatus(task.status);
      
      // ISO 8601 → datetime-local 포맷
      if (task.due_date) {
        const date = new Date(task.due_date);
        const formatted = format(date, "yyyy-MM-dd'T'HH:mm");
        setDueDate(formatted);
      } else {
        setDueDate('');
      }
    }
  }, [task]);

  if (!task) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    updateTask.mutate(
      {
        taskId: task.id,
        data: {
          title,
          description: description || null,
          priority,
          status,
          due_date: dueDate || null,
        },
      },
      {
        onSuccess: () => {
          onOpenChange(false);
        },
      }
    );
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>태스크 수정</DialogTitle>
          <DialogDescription>
            태스크 정보를 변경하세요
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* 제목 */}
          <div className="space-y-2">
            <Label htmlFor="edit-title">
              제목 <span className="text-red-500">*</span>
            </Label>
            <Input
              id="edit-title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>

          {/* 설명 */}
          <div className="space-y-2">
            <Label htmlFor="edit-description">설명</Label>
            <Textarea
              id="edit-description"
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          {/* 우선순위 & 상태 */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="edit-priority">우선순위</Label>
              <Select
                value={priority}
                onValueChange={(value) => setPriority(value as TaskPriority)}
              >
                <SelectTrigger id="edit-priority">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="high">🔴 높음</SelectItem>
                  <SelectItem value="medium">🟡 보통</SelectItem>
                  <SelectItem value="low">🟢 낮음</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="edit-status">상태</Label>
              <Select
                value={status}
                onValueChange={(value) => setStatus(value as TaskStatus)}
              >
                <SelectTrigger id="edit-status">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="todo">⬜ 할 일</SelectItem>
                  <SelectItem value="doing">🔄 진행 중</SelectItem>
                  <SelectItem value="done">✅ 완료</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* 마감일 */}
          <div className="space-y-2">
            <Label htmlFor="edit-dueDate">마감일</Label>
            <Input
              id="edit-dueDate"
              type="datetime-local"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
          </div>

          {/* 버튼 */}
          <div className="flex justify-end gap-2 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
            >
              취소
            </Button>
            <Button type="submit" disabled={updateTask.isPending}>
              {updateTask.isPending ? '저장 중...' : '저장'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}