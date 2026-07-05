# Hudut Firefox OSINT Custom Settings

Hudut Firefox OSINT profili, kişisel Firefox profilinden ayrılmış özel bir açık web araştırma profilidir.

Bu profil Tor değildir. Trafik normal internet üzerinden gider.

## Profil Bilgisi

Profil adı:

hudut-osint

Profil yolu:

$HOME/snap/firefox/common/.mozilla/firefox/hudut-osint

## Amaç

Bu profil şu amaçlarla oluşturulmuştur:

- Kişisel Firefox profili ile OSINT araştırmasını ayırmak
- Parola kaydı ve form doldurma riskini azaltmak
- WebRTC kaynaklı IP sızıntısı riskini azaltmak
- Kamera, mikrofon ve konum izinlerini kapatmak
- İndirme dosyalarını ayrı OSINT klasöründe toplamak
- Açık web araştırmaları için daha kontrollü bir Firefox ortamı sağlamak

## Uygulanan Özel Ayarlar

Firefox OSINT profili user.js dosyası üzerinden ayarlanır.

Uygulanan başlıca ayarlar:

- Proxy kapalı / direct mode
- Password saving kapalı
- Form autofill kapalı
- Search suggestions kapalı
- Tracking protection açık
- HTTPS-only açık
- WebRTC kapalı
- Konum izni kapalı
- Kamera izni kapalı
- Mikrofon izni kapalı
- Telemetry azaltılmış
- Pocket kapalı
- Çıkışta cookie, cache ve session temizliği açık
- resistFingerprinting açık

## Proxy Kararı

Firefox OSINT profili proxy kullanmaz.

Bu profil:

- Tor değildir
- Sistem Tor servisine bağlanmaz
- Normal açık web araştırmaları için kullanılır

## Hudut Shield Entegrasyonu

Hudut Shield menüsüne şu seçenekler eklenmiştir:

30. Firefox OSINT durumunu göster
31. Firefox OSINT profilini hazırla
32. Firefox OSINT profilini aç
33. Firefox OSINT raporu üret

CLI komutları:

hudut-shield firefox-osint status
hudut-shield firefox-osint prepare
hudut-shield firefox-osint launch
hudut-shield firefox-osint report

## Açma Komutu

Firefox OSINT profili şu mantıkla açılır:

firefox --new-instance --profile $HOME/snap/firefox/common/.mozilla/firefox/hudut-osint

Bu yöntem Snap Firefox ortamında daha sağlamdır çünkü profil adını değil doğrudan profil klasörünü kullanır.

## Kullanım Kuralları

Firefox OSINT profilinde:

- Kişisel hesaplara giriş yapılmaz
- Parola kaydedilmez
- Normal Firefox geçmişi içe aktarılmaz
- Araştırma ile kişisel kullanım karıştırılmaz
- İndirilen dosyalar kontrol edilmeden açılmaz
- Tor araştırması için Tor Browser veya hassas kullanımda Tails USB tercih edilir

## Özet

Firefox OSINT profili:

- Kişisel Firefox değildir
- Tor Browser değildir
- Anonimlik garantisi vermez
- Açık web OSINT için ayrılmış özel araştırma profilidir
