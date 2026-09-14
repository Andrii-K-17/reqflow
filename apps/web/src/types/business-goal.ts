export type Priority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'

export interface BusinessGoal {
  id: string
  project_id: string
  title: string
  description: string | null
  priority: Priority
  created_at: string
  updated_at: string
}
