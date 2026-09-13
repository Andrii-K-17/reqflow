export type ProjectRole = 'OWNER' | 'EDITOR' | 'VIEWER'

export interface Project {
  id: string
  name: string
  description: string | null
  owner_id: string
  my_role: ProjectRole
  archived_at: string | null
  created_at: string
  updated_at: string
}
