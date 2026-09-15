export interface AlternativeFlow {
  name: string
  condition: string
  steps: string[]
}

export interface UseCase {
  id: string
  project_id: string
  code: string
  title: string
  actors: string[]
  preconditions: string | null
  postconditions: string | null
  main_flow: string[]
  alternative_flows: AlternativeFlow[]
  created_at: string
  updated_at: string
}

export interface UseCaseCreatePayload {
  title: string
  actors: string[]
  preconditions?: string
  postconditions?: string
  main_flow: string[]
  alternative_flows: AlternativeFlow[]
}
