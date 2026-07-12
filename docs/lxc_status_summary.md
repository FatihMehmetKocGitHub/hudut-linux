# Hudut LXC Status Summary

Hudut Linux V1 LXC/LXD temel altyapısı tamamlandı.

## Network

- Bridge: lxdbr0
- IPv4: 10.99.10.1/24
- IPv6: disabled
- UFW: active
- LXD DNS/DHCP/route rules: active

## Containers

| Container | IP | Status | Snapshot |
|---|---:|---|---|
| hudut-osint | 10.99.10.10 | RUNNING | clean-base |
| hudut-socmint | 10.99.10.11 | RUNNING | clean-base |
| hudut-cti | 10.99.10.12 | RUNNING | clean-base |
| hudut-techint | 10.99.10.13 | RUNNING | clean-base |
| hudut-geoint | 10.99.10.14 | RUNNING | clean-base |
| hudut-dev | 10.99.10.15 | RUNNING | clean-base |
| hudut-sandbox | 10.99.10.16 | RUNNING | clean-base |

## Result

LXC/LXD lab layer is ready for Hudut Linux V1.
