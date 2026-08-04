# Security

> [!NOTE]
> This document was last reviewed on 2026-08-04.

## Authentication
This API supports authentication via:
- **API keys**
- **Google OAuth**

JWT-based authentication is planned for a future release.

## Hashing
API keys are stored hashed in the database.

## Encryption
The following fields are encrypted at rest (the encryption key is only known to the API):
- Email
- First name
- Last name
- HMAC

### Planned
- Stored messages
- External API keys provided by users

## Data Sharing
All information is processed locally and is **not** shared with third parties, with one exception: message completion requests and model queries are sent to the relevant external AI provider (e.g., Anthropic). Those requests may be logged by said provider per their own policies.

Shared messages are linked to a personal User ID and are not shared with other users.

## Network
It is recommended to run this behind a VPN or on a local network (e.g., Tailscale).