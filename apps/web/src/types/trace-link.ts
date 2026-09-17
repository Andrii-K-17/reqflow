export type TraceEntityType = 'BUSINESS_GOAL' | 'REQUIREMENT' | 'USE_CASE' | 'USER_STORY'
export type TraceRelation = 'DERIVES_FROM' | 'SATISFIES' | 'CONFLICTS_WITH'

export interface TraceLink {
  id: string
  project_id: string
  from_type: TraceEntityType
  from_id: string
  to_type: TraceEntityType
  to_id: string
  relation: TraceRelation
  created_at: string
}

export interface TraceGraphNode {
  id: string
  type: TraceEntityType
  code: string
  label: string
}

export interface TraceGraphEdge {
  from_id: string
  to_id: string
  relation: TraceRelation
}

export interface TraceGraph {
  nodes: TraceGraphNode[]
  edges: TraceGraphEdge[]
}
