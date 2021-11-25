import {api} from 'system/api'
import {NoContentResponse, Response} from 'system/response'
import {CommonKey} from 'system/types'


export type contactsAPI = {
  pin(contactId?: CommonKey | null, userId?: CommonKey | null): Response<NoContentResponse>
  unpin(contactId: CommonKey): Response<NoContentResponse>
}


export const contactsApi: contactsAPI = {
  pin(contactId?, userId?) {
    const entityId: string = contactId !== undefined && contactId !== null
      ? String(contactId)
      : `u_${String(userId)}`
    return api.post(api.pathWithParams({
      app: 'contacts',
      path: 'pin/{entityId}',
      version: 1
    }, {
      entityId
    }))
  },

  unpin(contactId) {
    return api.delete(api.pathWithParams({
      app: 'contacts',
      path: 'pin/{contactId}',
      version: 1
    }, {
      contactId
    }))
  }
}

