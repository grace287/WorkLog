/**
 * classNames 유틸 (조건부 클래스 병합)
 */
export function cn(...classes: (string | undefined | false | null)[]): string {
  return classes.filter(Boolean).join(' ');
}
