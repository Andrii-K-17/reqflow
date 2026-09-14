export type RequirementType = 'BUSINESS' | 'USER' | 'FUNCTIONAL' | 'NONFUNCTIONAL' | 'SYSTEM'
export type RequirementStatus = 'DRAFT' | 'REVIEWED' | 'APPROVED' | 'REJECTED'
export type Priority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'

export interface Requirement {
  id: string
  project_id: string
  code: string
  type: RequirementType
  title: string
  description: string | null
  priority: Priority
  status: RequirementStatus
  verifiable: boolean
  rationale: string | null
  source: string | null
  created_at: string
  updated_at: string
}

export interface RequirementPage {
  items: Requirement[]
  total: number
  page: number
  page_size: number
}

export interface RequirementFilters {
  type?: RequirementType
  status?: RequirementStatus
  priority?: Priority
  page?: number
  page_size?: number
}

export interface RequirementCreatePayload {
  type: RequirementType
  title: string
  description?: string
  priority: Priority
  verifiable: boolean
  rationale?: string
  source?: string
}

export type RequirementUpdatePayload = Partial<
  Omit<RequirementCreatePayload, 'type'> & { status: RequirementStatus }
>
