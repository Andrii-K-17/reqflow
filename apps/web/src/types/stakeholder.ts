export type StakeholderCategory = 'PRIMARY' | 'SECONDARY' | 'EXTERNAL'

export interface Stakeholder {
  id: string
  project_id: string
  name: string
  category: StakeholderCategory
  interest_description: string | null
  created_at: string
  updated_at: string
}
