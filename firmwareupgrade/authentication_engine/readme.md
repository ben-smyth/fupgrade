# Authentication Engine

The auth engine is designed to allow for pluggable authentication methods. Any additional authentication method should be added in the form of a folder. It should inherit from `baseclass.BaseAuthentication`

Each authentication type may require different environment variables, so a `readme` should be included in each one.