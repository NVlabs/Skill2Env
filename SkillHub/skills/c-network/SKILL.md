---
name: c-network
description: DNS lookups with doggo and readable HTTP requests with httpie — modern networking tools for the terminal.
tags: [dns, http, networking, api]
---

# Networking

## doggo (DNS client)

```bash
# Basic DNS lookup
doggo example.com

# Specific record type
doggo example.com MX
doggo example.com AAAA
doggo example.com TXT
doggo example.com NS
doggo example.com CNAME

# Use specific nameserver
doggo example.com --nameserver 1.1.1.1
doggo example.com --nameserver 8.8.8.8

# DNS over HTTPS
doggo example.com --class IN --type A --nameserver https://cloudflare-dns.com/dns-query

# JSON output
doggo example.com --json
```

## httpie (HTTP client)

Human-friendly alternative to curl:

```bash
# GET request
http GET api.example.com/users

# POST with JSON body
http POST api.example.com/users name=John email=john@example.com

# Headers
http GET api.example.com Authorization:"Bearer token123"

# Download file
http --download https://example.com/file.zip

# Form upload
http --form POST api.example.com file@photo.jpg

# With auth
http -a user:password GET api.example.com/protected

# Follow redirects
http --follow GET example.com

# Show only response headers
http --headers GET example.com

# Verbose (show request + response)
http --verbose GET example.com
```

## Guidelines

- Use `doggo` for DNS debugging instead of `dig` or `nslookup`
- Use `http` (httpie) for API testing instead of curl — output is colorized and formatted
- For POST requests, httpie auto-detects JSON vs form data
- `key=value` sends as JSON string, `key:=123` sends as JSON number
