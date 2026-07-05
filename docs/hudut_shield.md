# Hudut Shield Security Center

Hudut Shield, Hudut Linux'un güvenlik durum kontrol ve profil yönetim sistemidir.

## Amaç

Hudut Linux üzerinde firewall, DNS, MAC randomization, IPv6 privacy, proxy, Tor Browser, Bluetooth, mikrofon, kamera, SSH, AppArmor, kernel hardening, LXC, açık portlar, disk şifreleme ve honeypot durumunu kontrol etmek.

## V1 Komutları

    hudut-shield status
    hudut-shield report
    hudut-shield profiles
    hudut-shield menu

    hudut-shield apply normal
    hudut-shield apply secure
    hudut-shield apply osint
    hudut-shield apply tor-research
    hudut-shield apply public-wifi
    hudut-shield apply honeypot-lab
    hudut-shield apply lab

    hudut-shield network status
    hudut-shield network report
    hudut-shield network renew-ipv4
    hudut-shield network dns normal
    hudut-shield network dns secure
    hudut-shield network dns osint
    hudut-shield network dns lab
    hudut-shield network mac stable
    hudut-shield network mac random
    hudut-shield network mac permanent

## Kontrol Alanları

- Firewall
- DNS
- Proxy
- Tor Browser
- Bluetooth
- Mikrofon
- Kamera
- SSH
- AppArmor
- Kernel Hardening
- LXC/LXD
- Açık portlar
- Disk şifreleme
- Honeypot
- MAC randomization
- IPv6 privacy

## Mikrofon ve Kamera Kontrolü

Hudut Shield V1 içinde mikrofon ve kamera kontrolü bulunur.

Her profil uygulanırken:

- Mikrofon kaynakları mute edilir
- Kamera modülü kapatılmaya çalışılır
- Durum hudut-shield status çıktısında gösterilir

İlgili dokümantasyon:

- docs/privacy_devices.md
- docs/hudut_shield_profiles.md

## Kernel Hardening

Kernel hardening ayarları şurada tutulur:

    security/kernel/99-hudut-kernel-hardening.conf

Uygulama:

    ./scripts/apply_kernel_hardening.sh

Kontrol:

    ./scripts/check_kernel_hardening.sh
    hudut-shield status

## VPN Notu

Hudut Linux V1 içinde VPN otomasyonu aktif kullanılmayacaktır. VPN konusu V2 aşamasına ayrılmıştır.

## Etik Sınır

Hudut Shield iz kaybettirme, yetkisiz erişim veya saldırı gizleme aracı değildir.

Amaç; güvenli çalışma ortamı, public Wi-Fi koruması, lab ayrımı, yasal OSINT araştırması ve raporlanabilir güvenlik durumudur.
