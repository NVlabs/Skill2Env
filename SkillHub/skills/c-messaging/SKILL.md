---
name: c-messaging
description: Send and read messages via imsg (iMessage) and wacli (WhatsApp). Supports sending to individuals or groups, reading recent conversations, and checking unread messages across both platforms.
tags: [messaging, imessage, whatsapp, imsg, wacli, sms]
---

This skill manages messaging via `imsg` (iMessage/SMS) and `wacli` (WhatsApp). Check availability with `which imsg wacli`.

## iMessage & SMS — `imsg`

```bash
imsg send "Phone or Email" "Message text"  # Send a message
imsg send "+14155551234" "Hello!"
imsg send "user@icloud.com" "Hey there"
imsg list                                   # List recent conversations
imsg list --limit 10                        # Last 10 conversations
imsg read "+14155551234"                    # Read conversation with contact
imsg read "+14155551234" --limit 20         # Read last 20 messages
imsg unread                                 # Show unread messages
imsg group send "Group Name" "Message"      # Send to a group chat
imsg group list                             # List group chats
imsg contacts                               # List contacts
```

## WhatsApp — `wacli`

```bash
wacli send "+14155551234" "Message text"    # Send a message
wacli send "Contact Name" "Hello!"          # Send by name (if in contacts)
wacli list                                  # List recent chats
wacli read "+14155551234"                   # Read conversation
wacli read "+14155551234" --limit 20
wacli unread                                # Show unread messages
wacli group list                            # List WhatsApp groups
wacli group send "Group Name" "Message"
wacli status "Your status text"            # Set WhatsApp status
```

## Usage Guidelines

- Use `imsg` for iMessage/SMS to Apple devices or phone numbers.
- Use `wacli` for WhatsApp contacts.
- Phone numbers should include country code (e.g., +1 for US).
- Check `imsg unread` or `wacli unread` before sending follow-ups.
- If a contact name is ambiguous, prefer using the phone number directly.

## Notes

- `imsg` requires macOS and an active iMessage account.
- `wacli` requires WhatsApp to be linked — run `wacli auth` to scan QR code on first use.
- Both tools operate locally; no cloud API credentials required after initial auth.
