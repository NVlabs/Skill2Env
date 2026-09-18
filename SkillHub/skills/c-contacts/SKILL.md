---
name: c-contacts
description: macOS Contacts — search, list, and look up contact details via AppleScript.
tags: [contacts, address-book, people, phone]
---

# Contacts — Address Book

Access macOS Contacts app via AppleScript. No CLI tool needed.

## Commands

```bash
# Search for a contact by name
osascript -e 'tell application "Contacts"
  set results to (every person whose name contains "John")
  set output to ""
  repeat with p in results
    set output to output & name of p & linefeed
    repeat with e in emails of p
      set output to output & "  Email: " & value of e & linefeed
    end repeat
    repeat with ph in phones of p
      set output to output & "  Phone: " & value of ph & linefeed
    end repeat
    set output to output & linefeed
  end repeat
  return output
end tell'

# Get all contact names
osascript -e 'tell application "Contacts" to get name of every person'

# Get a specific contact's email
osascript -e 'tell application "Contacts"
  set p to first person whose name is "John Smith"
  get value of every email of p
end tell'

# Get a specific contact's phone
osascript -e 'tell application "Contacts"
  set p to first person whose name is "John Smith"
  get value of every phone of p
end tell'

# Count contacts
osascript -e 'tell application "Contacts" to count every person'

# Search by email
osascript -e 'tell application "Contacts"
  set results to (every person whose value of emails contains "john@")
  get name of results
end tell'
```

## Guidelines

- Always search by partial name (uses `contains`) to be flexible
- Return name, email, and phone by default
- If multiple matches, list all and let the user pick
- Contacts app does not need to be running — AppleScript handles it
- Never store contact details in memory files for privacy
- If asked "what's [name]'s number?", search contacts first, then memory
