# godaddy-dns-updater
updates GoDaddy DNS records automatically

## Setup:
create a `settings_local.py`` file:

```python
# credentials (https://developer.godaddy.com/keys/)
GODADDY_PUBLIC_KEY = ''
GODADDY_SECRET_KEY = ''

# domains
# {
#     'example.com': [
#         '@', # domain itself
#         'foo' # subdomain
#     ]
# }
DOMAINS = {}

# time to live (optional)
DOMAIN_TTL = 600

# log-file (optional)
LOG_FILE = 'godaddy.log'
```
