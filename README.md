# godaddy-dns-updater
updates GoDaddy DNS records automatically

## Setup:
create a `settings_local.py`` file:

```python
GODADDY_PUBLIC_KEY = 'xxx'
GODADDY_SECRET_KEY = 'xxx'

DOMAINS = {
    'example.com': [
        '@', # domain itself
        'foo' # subdomain
    ]
}
```
