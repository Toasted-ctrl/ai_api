# Authentication
This API currently requires authentication in the form of an API key. At a later stage authentication using a JWT will also be added.

# Hashing
API keys are stored hashed in the database.

# Encryption
Sensitive details (i.e., email, first name, last name, HMAC) are currently encrypted, the encryption key is only known to the API. This will later on also extend to stored messages, as well as external API keys provided. Shared messages are linked to a personal User ID and will not be shared with others.

# VPN / Local Network
I recommend running this on a local network / VPN only (i.e., TailScale).

# Processing
All information is processed locally and not shared with third parties, with the exception of message completion requests and model queries regarding external AI providers. I.e., your requests for which you may be using an API key (such as with Anthropic), may be sent to Anthropic's API, and those details may be logged with said Provider.