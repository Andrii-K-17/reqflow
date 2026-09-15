export interface UserStory {
  id: string
  project_id: string
  code: string
  role: string
  goal: string
  benefit: string
  acceptance_criteria: string[]
  created_at: string
  updated_at: string
}

export interface UserStoryCreatePayload {
  role: string
  goal: string
  benefit: string
  acceptance_criteria: string[]
}
