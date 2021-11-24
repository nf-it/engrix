import React, {createRef} from 'react'
import {
  Box,
  Dialog,
  EntityList,
  IconButton, MaterialIcon,
  Tab,
  Tabs,
  Typography
} from 'system/components'
import {TeamContactModel} from '../types'
import {ScreenProps} from 'system/types'
import {gettext} from 'system/l10n'
import {api} from 'system/api'
import {RequestApiPath} from 'system/routing'
import ContactCard from './ContactCard'


const objectsPath: RequestApiPath = api.entityPath('contacts', 'Team')


type DirectoryScreenState = {
  entityKey?: string | null
  tab?: string
}


export default class DirectoryScreen extends React.Component<ScreenProps> {
  state: DirectoryScreenState = {
    entityKey: undefined,
    tab: 'team'
  }

  private listRef = createRef<EntityList>()

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
              <IconButton>
                <MaterialIcon icon={'chat'} />
              </IconButton>
            ]}

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
