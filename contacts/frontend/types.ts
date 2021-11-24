import {CommonKey} from 'system/types'

export type ContactReq = string | {
  value: string
  tag: string
}

export type ContactReqs = ContactReq[]

export type TeamContactModel = {
  contactId: CommonKey | null
  userId: CommonKey | null
  name: string
  avatar: string | null
  nickname: string
  birthdate: string | null
  emails: ContactReqs
  phones: ContactReq
  im: ContactReqs
  company: string
  position: string
  homeAddress: string
  workAddress: string
  notes: string
}
