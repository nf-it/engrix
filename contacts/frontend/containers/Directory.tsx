import React, {createRef} from 'react'
import {Box, Dialog, EntityList, IconButton, MaterialIcon, Tab, Tabs, Typography} from 'system/components'
import {TeamContactModel} from '../types'
import {ScreenProps} from 'system/types'
import {gettext} from 'system/l10n'
import {api} from 'system/api'
import {RequestApiPath} from 'system/routing'
import ContactCard from './ContactCard'
import {contactsApi} from '../providers'
import {notifications} from 'system/notification'


const objectsPath: RequestApiPath = api.entityPath('contacts', 'Team')


type DirectoryScreenState = {
  entityKey?: string | null
  tab?: string
}


type ContactReqsProps = {
  item: TeamContactModel
}

type ContactIconedReqProps = {
  value: string
  icon: string
  tag?: string
  proto?: string
}


const ContactIconedReq = (props: ContactIconedReqProps): JSX.Element => (
  <Box display={'flex'} alignItems={'center'}>
    <MaterialIcon icon={props.icon} size={16} mr={1} color={'#0008'} />
    <MaterialIcon icon={props.tag ?? 'more_horiz'} size={16} mr={1} color={props.tag ? '#0004' : '#0002'} />
    <Typography variant={'subtitle2'}>
      {props.proto !== undefined ? (
        <a
          href={`${props.proto !== 'url' ? props.proto : ''}${props.value}`}
          target={'_blank'}
          style={{
            textDecoration: 'none',
            color: '14b'
          }}
        >{props.value}</a>
      ) : props.value}
    </Typography>
  </Box>
)



const ContactReqs = (props: ContactReqsProps): JSX.Element | null => {
  const item: TeamContactModel = props.item
  const reqs: JSX.Element[] = []

  if (item.company) {
    reqs.push(<ContactIconedReq value={item.company} icon={'business'} />)
  }

  if (item.position) {
    reqs.push(<ContactIconedReq value={item.position} icon={'work'} />)
  }

  if (item.emails.length) {
    item.emails.forEach(el => {
      let value: string
      let tag: string | undefined
      if (typeof el == 'string') {
        value = el
        tag = undefined
      } else {
        value = el.value
        tag = el.tag
      }
      reqs.push(<ContactIconedReq value={value} icon={'email'} tag={tag} proto={'mailto:'} />)
    })
  }

  if (item.phones.length) {
    item.phones.forEach(el => {
      let value: string
      let tag: string | undefined
      if (typeof el == 'string') {
        value = el
        tag = undefined
      } else {
        value = el.value
        tag = el.tag
      }
      reqs.push(<ContactIconedReq value={value} icon={'phone'} tag={tag} proto={'tel:'} />)
    })
  }

  if (!reqs.length)
    return null

  return (
    <Box>
      {reqs}
    </Box>
  )
}


export default class DirectoryScreen extends React.Component<ScreenProps> {
  state: DirectoryScreenState = {
    entityKey: undefined,
    tab: 'team'
  }

  private listRef = createRef<EntityList>()

  private handlePinClick = (item: TeamContactModel): void => {
    if (item.pinned && item.contactId !== null) {
      contactsApi.unpin(item.contactId).then(() => {
        this.listRef.current?.update()
      }).catch(err => {
        notifications.showRequestError(err)
      })
    } else if (!item.pinned) {
      contactsApi.pin(
        item.contactId,
        item.contactId === null ? item.userId : null
      ).then(() => {
        this.listRef.current?.update()
      }).catch(err => {
        notifications.showRequestError(err)
      })
    }
  }

  render() {
    return (
      <React.Fragment>
        <Box mt={1}>
          <Typography variant={'h4'} paddingBottom={2}>{gettext('Contacts', 'contacts')}</Typography>

          <Box mb={2}>
            <Tabs
              value={this.state.tab}
              onChange={(event: React.ChangeEvent<{}>, newValue: number) => this.setState({tab: newValue})}
            >
              <Tab
                label={gettext("Team", 'contacts')}
                value={'team'}
                disableFocusRipple
                wrapped
              />
            </Tabs>
          </Box>

          <EntityList
            ref={this.listRef}
            requestPath={objectsPath}

            avatarColor
            avatarField={'avatar'}
            primaryField={'name'}
            renderItemCardHeaderActions={(item: TeamContactModel) => [
              <IconButton
                color={item.pinned ? 'primary' : undefined}
                size={'small'}
                onClick={() => this.handlePinClick(item)}
              >
                <MaterialIcon icon={'push_pin'} color={item.pinned ? 'primary' : '#0002'} />
              </IconButton>,
              <IconButton size={'small'}>
                <MaterialIcon icon={'chat'} color={'#0007'} />
              </IconButton>
            ]}
            renderSecondaryField={(item: TeamContactModel) => (
              <ContactReqs item={item} />
            )}

            search
            variant={'cards'}
          />
        </Box>

        <Dialog open={this.state.entityKey !== undefined} maxWidth={'md'}>
          {this.state.entityKey !== undefined && (
            <ContactCard
              entityKey={this.state.entityKey}
              onClose={() => {
                this.setState({entityKey: undefined})
              }}
              onAfterDelete={() => {
                this.listRef.current?.update()
                this.setState({entityKey: undefined})
              }}
              onAfterSubmit={() => {
                this.listRef.current?.update()
                this.setState({entityKey: undefined})
              }}
            />
          )}
        </Dialog>
      </React.Fragment>
    )
  }
}
