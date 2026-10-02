export type InfluencerStatus = 'QUALIFIED' | 'FAILED' | 'PENDING'

export interface Influencer {
  _id: string
  platform: string
  platformId: string
  name: string
  profileUrl?: string | null
  description?: string | null
  followerCount?: number
  engagementRate?: number | null
  niche?: string | null
  contentThemes?: string[]
  contentStyle?: string | null
  recentContent?: string[]
  contactEmail?: string
  emailSource?: string | null
  website?: string | null
  instagramUrl?: string | null
  youtubeUrl?: string | null
  tiktokUrl?: string | null
  audienceAge?: string | null
  audienceGender?: string | null
  audienceGeography?: string | null
  qualificationStatus?: InfluencerStatus
  qualificationScore?: number
  qualificationReasons?: string[]
  brandFitScore?: number
  contentRelevanceScore?: number
  discoverySource?: string | null
  discoveredAt?: string | null
  createdAt?: string
  updatedAt?: string
}

export interface DiscoveryRun {
  _id: string
  niche: string
  queries: string[]
  candidatesFound: number
  duplicatesFound: number
  storedCount: number
  qualifiedCount: number
  failedCount: number
  status: string
  startedAt?: string
  completedAt?: string
  error?: string | null
}

export interface MessageRecord {
  _id: string
  influencerId: string
  emailSubject: string
  emailBody: string
  emailWordCount?: number
  instagramDm: string
  dmWordCount?: number
  personalizationSignals?: string[]
  model?: string
  promptVersion?: string
  status?: string
  createdAt?: string
  updatedAt?: string
}

export interface OutreachLog {
  _id: string
  influencerId: string
  channel: string
  recipient: string
  messageId?: string
  status: string
  sentAt?: string | null
  failureReason?: string | null
  attemptCount?: number
  createdAt?: string
  updatedAt?: string
}

export interface DashboardStats {
  totalInfluencers: number
  qualifiedInfluencers: number
  failedInfluencers: number
  emailsFound: number
  messagesGenerated: number
  emailsSent: number
  emailsSimulated: number
  failedOutreach: number
  recentDiscoveryRuns?: DiscoveryRun[]
  recentOutreach?: OutreachLog[]
}
