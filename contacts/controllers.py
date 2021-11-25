from typing import *
from wefram import aaa, api, requests
from .models import Contact, Pin


@api.handle_post('/pin/{contact_id}', version=1)
@aaa.requires_authenticated()
async def v1_pin_contact(request: requests.Request) -> requests.NoContentResponse:
    contact_id: str = request.path_params['contact_id']

    # If the contact have been identified by corresponding system.User.id,
    # then trying to fetch the corresponding contant and if there is no
    # corresponding contact exists - create the new one.
    if contact_id.startswith('u_'):
        user_id: str = contact_id[2:]
        contact: Optional[Contact] = await Contact.ensure_for_user(user_id)
        contact_id = contact.id

    await Pin.pin(contact_id)

    return requests.NoContentResponse()


@api.handle_delete('/pin/{contact_id}', version=1)
@aaa.requires_authenticated()
async def v1_unpin_contact(request: requests.Request) -> requests.NoContentResponse:
    contact_id: str = request.path_params['contact_id']

    # If the contact have been identified by corresponding system.User.id,
    # then trying to fetch the corresponding contant and if there is no
    # corresponding contact exists - create the new one.
    if contact_id.startswith('u_'):
        user_id: str = contact_id[2:]
        contact: Optional[Contact] = await Contact.ensure_for_user(user_id)
        contact_id = contact.id

    await Pin.unpin(contact_id)

    return requests.NoContentResponse()


# Place controllers and routes in this module.


# A couple examples are located below:
#
# @requests.route('/my_get_controller/{some_id}', methods=['GET'])
# async def my_get_controller(request: requests.Request) -> requests.Response:
#     some_id: str = request.path_params['some_id']
#     query_args: Dict[str, Union[str, List[str]]] = request.scope['query_args']
#
#     # some kind of work here :-)
#
#     return requests.JSONResponse({
#         'key1': 'value1',
#         'key2': 'value2'
#     })
#
#
# @requests.route('/my_post_controller/{some_id}', methods=['POST'])
# @aaa.requires('some_permission')
# async def my_post_controller(request: requests.Request) -> requests.Response:
#     some_id: str = request.path_params['some_id']
#     payload: Any = request.scope['payload']  # the payload (data) of the POST/PUT request
#
#     # some kind of work here :-)
#
#     return requests.NoContentResponse(204)


# A couple API controllers' examples are located below:

# @api.handle_get('/my_entity/{id}')
# @aaa.requires_authenticated()
# async def my_entity_get(request: requests.Request) -> requests.Response:
#
#     # some kind of work here :-)
#
#     return requests.PlainTextResponse("OK")
#
#
# @api.handle_post('/my_entity')
# @aaa.requires('some_permission')
# async def my_entity_post(request: requests.Request) -> requests.Response:
#
#     # some kind of work here :-)
#
#     return requests.NoContentResponse()

