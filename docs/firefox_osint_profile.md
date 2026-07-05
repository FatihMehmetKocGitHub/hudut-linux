# Hudut Firefox OSINT Profile

Hudut Firefox OSINT Profile, açık web araştırmaları için kişisel Firefox profilinden ayrılmış özel bir araştırma profilidir.

Bu profil Tor değildir.

## Amaç

- Kişisel Firefox kullanımını OSINT araştırmasından ayırmak
- Kaydedilmiş parola, form doldurma ve kişisel hesap riskini azaltmak
- Açık web araştırmalarını ayrı klasör ve ayrı profil düzeninde yürütmek
- Hudut Linux içinde profesyonel araştırma workflow'u sağlamak

## Varsayılan Karar

Firefox OSINT Profile:

- Açık web OSINT için kullanılır
- Normal internet bağlantısı kullanır
- Tor ağına yönlendirilmez
- Kişisel Firefox profilinden ayrıdır
- Kişisel hesaplarla kullanılmaz

## Güvenlik Ayarları

Profil içinde:

- Password saving kapalı
- Form autofill kapalı
- WebRTC kapalı
- HTTPS-only açık
- Tracking protection açık
- Telemetry kapalı
- Pocket kapalı
- Konum/kamera/mikrofon izinleri kapalı
- İndirmeler research/firefox/downloads klasörüne yönlendirilir

## Kullanım

Hazırlama:

```bash
python3 apps/firefox/hudut_firefox_osint.py prepare
