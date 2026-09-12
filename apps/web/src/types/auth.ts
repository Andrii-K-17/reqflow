export interface User {
  id: string
  email: string
  full_name: string
}

export interface TokenPair {
  access_token: string
  refresh_token: string
  token_type: string
}
