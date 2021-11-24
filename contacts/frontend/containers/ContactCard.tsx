import React from 'react'
import {
  Box,
  EntityForm
} from 'system/components'
import {gettext} from 'system/l10n'
import {api} from 'system/api'
import {RequestApiPath} from 'system/routing'


const objectPath: RequestApiPath = api.entityObjectPath('contacts', 'Contact')


export type ContactCardProps = {
  entityKey: string | null
  onAfterDelete: () => void
  onAfterSubmit: () => void
  onClose: () => void
}

type ContactCardState = {
  data: any  /* typed model may be used here */
}

export default class ContactCard extends React.Component<ContactCardProps, ContactCardState> {
  state: ContactCardState = {
    data: {
      id: null,
      /* initial model data here */
    }
  }

  render() {
    const key: string | null = this.props.entityKey

    return (
      <EntityForm
        entityKey={key}
        requestPath={objectPath}

        data={this.state.data}
        onUpdateData={(data, cb) => this.setState({data}, cb)}
        requiredForSubmit={[]}
        submitFieldsModel={[]}

        submit
        delete={key !== null}
        title={key === null ? gettext("Create") : this.state.data.name}
        windowed

        onAfterDelete={this.props.onAfterDelete}
        onAfterSubmit={this.props.onAfterSubmit}
        onClose={this.props.onClose}
      >
        <Box>

        {/* the Card contents here */}

        </Box>
      </EntityForm>
    )
  }
}

