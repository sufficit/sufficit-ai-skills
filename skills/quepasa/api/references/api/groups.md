# Joined groups and membership

QuePasa 5.26.1125.1212, canonical API v5.

## Behaviors

- `GET /groups` lists live joined groups for the selected session. A successful response may be served from a ten-minute Redis cache when configured. Send `?refresh=1` to bypass it. `groups` and `total` are omitted for an empty collection.
- Group fields preserve their wire casing. Use `group.JID` (a string such as `123456789@g.us`) and `group.Name`, not lowercase keys. `Participants` can be null or empty for a joined-group summary. Fetch one group when member details are needed.

### List joined group names and JIDs

```bash
curl --fail-with-body --silent --show-error "$QUEPASA_API/groups?refresh=1" \
  -H "X-QUEPASA-USERKEY: $QUEPASA_USER_KEY" \
  -H "X-QUEPASA-TOKEN: $QUEPASA_SESSION_TOKEN" | jq '(.groups // [])[] | {JID, Name}'
```

Leave off `refresh=1` when a cached list is acceptable.

## Operations

### `DELETE /api/v5/groups/invite`

Revoke and regenerate a group invite link.

- Unversioned alias `DELETE /api/groups/invite` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and groupid.
- HTTP 200. `api.InviteResponse`.

### `GET /api/v5/groups`

List joined WhatsApp groups from the linked session.

- Unversioned alias `GET /api/groups` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token for an owned session. Use query refresh=1 to bypass the cache.
- HTTP 200. `Groups`.

### `GET /api/v5/groups/invite`

Read the current invite link for a group.

- Unversioned alias `GET /api/groups/invite` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and groupid.
- HTTP 200. `api.InviteResponse`.

### `GET /api/v5/groups/requests`

List group membership requests.

- Unversioned alias `GET /api/groups/requests` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and groupid.
- HTTP 200. `GroupRequests`.

### `GET /api/v5/me/groups`

Aggregate joined groups across owned sessions.

- Unversioned alias `GET /api/me/groups` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. No request parameters. An individual session can report an error.
- HTTP 200. `UserGroups`.

### `PATCH /api/v5/groups`

Change the group name or description.

- Unversioned alias `PATCH /api/groups` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, groupid and JSON name, topic (description is an alias), or whatsapp.GroupPermissionsPatch fields. Send permissions separately from name or topic.
- Request schemas. `whatsapp.GroupPermissionsPatch`.
- HTTP 200. `SingleGroup`.

### `POST /api/v5/groups`

Create a WhatsApp group and add participants.

- Unversioned alias `POST /api/groups` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and JSON title and participants array.
- HTTP 200. `SingleGroup`.

### `POST /api/v5/groups/get`

Read one WhatsApp group.

- Unversioned alias `POST /api/groups/get` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and groupid.
- HTTP 200. `SingleGroup`.

### `POST /api/v5/groups/invite`

Generate a fresh invite link for a group.

- Unversioned alias `POST /api/groups/invite` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and groupid.
- HTTP 200. `api.InviteResponse`.

### `POST /api/v5/groups/leave`

Leave a WhatsApp group.

- Unversioned alias `POST /api/groups/leave` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and groupid.
- HTTP 200. `Result`.

### `POST /api/v5/groups/requests`

Approve or reject pending group membership requests.

- Unversioned alias `POST /api/groups/requests` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, groupid, action and participants.
- HTTP 200. `GroupRequestMutation`.

### `PUT /api/v5/groups/description`

Set the group description.

- Unversioned alias `PUT /api/groups/description` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, groupid and JSON topic.
- HTTP 200. `SingleGroup`.

### `PUT /api/v5/groups/name`

Set the group name.

- Unversioned alias `PUT /api/groups/name` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, groupid and JSON name.
- HTTP 200. `SingleGroup`.

### `PUT /api/v5/groups/participants`

Add, remove, promote or demote group participants.

- Unversioned alias `PUT /api/groups/participants` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, groupid and JSON action and participants.
- HTTP 200. `Participants`.

### `PUT /api/v5/groups/permissions`

Update group permissions.

- Unversioned alias `PUT /api/groups/permissions` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, groupid and whatsapp.GroupPermissionsPatch JSON.
- Request schemas. `whatsapp.GroupPermissionsPatch`.
- HTTP 200. `SingleGroup`.

### `PUT /api/v5/groups/photo`

Set or remove a group photo.

- Unversioned alias `PUT /api/groups/photo` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, groupid and JSON image_url or remove_img.
- HTTP 200. `PhotoResult`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### GroupInfo

| Field | Type | Presence |
| --- | --- | --- |
| `JID` | string | Required |
| `OwnerJID` | string | Required |
| `OwnerPN` | string | Required |
| `Name` | string | Required |
| `NameSetAt` | date-time | Required |
| `NameSetBy` | string | Required |
| `NameSetByPN` | string | Required |
| `Topic` | string | Required |
| `TopicID` | string | Required |
| `TopicSetAt` | date-time | Required |
| `TopicSetBy` | string | Required |
| `TopicSetByPN` | string | Required |
| `TopicDeleted` | boolean | Required |
| `IsLocked` | boolean | Required |
| `IsAnnounce` | boolean | Required |
| `AnnounceVersionID` | string | Required |
| `IsEphemeral` | boolean | Required |
| `DisappearingTimer` | integer | Required |
| `IsIncognito` | boolean | Required |
| `IsParent` | boolean | Required |
| `DefaultMembershipApprovalMode` | string | Required |
| `LinkedParentJID` | string | Required |
| `IsDefaultSubGroup` | boolean | Required |
| `IsJoinApprovalRequired` | boolean | Required |
| `AddressingMode` | string | Required |
| `GroupCreated` | date-time | Required |
| `CreatorCountryCode` | string | Required |
| `ParticipantVersionID` | string | Required |
| `Participants` | Array of `GroupParticipant` or null | Required |
| `ParticipantCount` | integer | Required |
| `MemberAddMode` | string | Required |
| `Suspended` | boolean | Required |

### GroupJoinRequest

| Field | Type | Presence |
| --- | --- | --- |
| `JID` | string | Required |
| `RequestedAt` | date-time | Required |

### GroupParticipant

| Field | Type | Presence |
| --- | --- | --- |
| `JID` | string | Required |
| `PhoneNumber` | string | Required |
| `LID` | string | Required |
| `Username` | string | Required |
| `IsAdmin` | boolean | Required |
| `IsSuperAdmin` | boolean | Required |
| `DisplayName` | string | Required |
| `Error` | integer | Required |
| `AddRequest` | `GroupParticipantAddRequest` or null | Required |

### GroupParticipantAddRequest

| Field | Type | Presence |
| --- | --- | --- |
| `Code` | string | Required |
| `Expiration` | date-time | Required |

### GroupRequestMutation

`Response`

| Field | Type | Presence |
| --- | --- | --- |
| `total` | integer | Optional |
| `requests` | Array of `GroupParticipant` | Optional |

### GroupRequests

`Response`

| Field | Type | Presence |
| --- | --- | --- |
| `total` | integer | Optional |
| `requests` | Array of `GroupJoinRequest` | Optional |

### Groups

`Response`

| Field | Type | Presence |
| --- | --- | --- |
| `total` | integer | Optional |
| `groups` | Array of `GroupInfo` | Optional |

### Participants

`Response`

| Field | Type | Presence |
| --- | --- | --- |
| `total` | integer | Optional |
| `participants` | Array of `GroupParticipant` | Optional |

### PhotoResult

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `pictureId` | string | Optional |

### Response

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `status` | string | Optional |
| `debug` | Array of string | Optional |

### Result

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |

### SingleGroup

`Response`

| Field | Type | Presence |
| --- | --- | --- |
| `total` | integer | Optional |
| `groupinfo` | `GroupInfo` | Optional |

### UserGroupSession

| Field | Type | Presence |
| --- | --- | --- |
| `token` | string | Required |
| `session_id` | string | Optional |
| `wid` | string | Optional |
| `groups` | Array of `GroupInfo` or null | Required |
| `error` | string | Optional |

### UserGroups

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `sessions` | Array of `UserGroupSession` | Required |

### api.InviteResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `url` | string | Unspecified |

### whatsapp.GroupPermissionsPatch

| Field | Type | Presence |
| --- | --- | --- |
| `admin_approval_required` | boolean | Unspecified |
| `disappearing_timer` | integer | Unspecified |
| `members_can_add_members` | boolean | Unspecified |
| `members_can_edit_group_settings` | boolean | Unspecified |
| `members_can_send_messages` | boolean | Unspecified |
