# Changelog
## [0.2.0] - Quarterly Planning and Webhooks
- Added new table `quarterly_initiatives` to track larger quarterly initiatives.
- Added `add-initiative`, `list-initiatives`, and `complete-initiative` to the CLI.
- Added a Twilio webhook (`webhook.py`) via Flask to handle incoming SMS/Voice messages dynamically.

## [0.1.0] - Core Implementation
- Bootstrapped project layout.
- Added `cli.py` for tracking daily "One-Minute Goals" via `add`, `list`, and `complete`.
- Added programmable notifications for email and text/voice (via Twilio).

## [0.0.0] - Initial Setup
- Initialized core project documentation.
