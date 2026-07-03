# Hudut Privacy Devices

Hudut Shield V1 içinde mikrofon ve kamera güvenlik kontrolü bulunur.

## Amaç

Mikrofon ve kamera gibi yerel cihazların güvenli araştırma profillerinde kapalı tutulmasını sağlamak.

Bu özellik iz gizleme amacıyla değil; mahremiyet, güvenli çalışma ortamı ve kurumsal güvenlik profili amacıyla eklenmiştir.

## Hudut Shield Davranışı

Her profil uygulanırken:

- Mikrofon kaynakları mute edilmeye çalışılır
- Kamera için uvcvideo modülü kapatılmaya çalışılır
- Sonuç hudut-shield status çıktısında raporlanır

## Etkilenen Profiller

| Profil | Mikrofon | Kamera | Amaç |
|---|---|---|---|
| normal | Kapatılır / mute | Kapatılır | Günlük güvenli kullanım |
| secure | Kapatılır / mute | Kapatılır | En güçlü temel güvenlik |
| osint | Kapatılır / mute | Kapatılır | Yasal OSINT araştırması |
| tor-research | Kapatılır / mute | Kapatılır | Tor Browser araştırma hazırlığı |
| public-wifi | Kapatılır / mute | Kapatılır | Ortak ağ güvenliği |
| lab | Kapatılır / mute | Kapatılır | Yerel test ortamı |
| honeypot-lab | Kapatılır / mute | Kapatılır | İzole honeypot hazırlığı |

## Komutlar

Durum kontrolü:

    hudut-shield status

Menüden manuel kapatma:

    17. Mikrofon/Kamera kapat

Profil uygulama:

    hudut-shield apply secure
    hudut-shield apply osint
    hudut-shield apply public-wifi

## Geri Açma

Mikrofonu geri açmak için:

    pactl list short sources 2>/dev/null | awk '{print $1}' | while read src; do pactl set-source-mute "$src" 0 2>/dev/null || true; done

Kamerayı geri açmak için:

    sudo modprobe uvcvideo

## Not

Bazı kameralar uvcvideo dışında farklı sürücülerle çalışabilir. Bu durumda Hudut Shield kamera durumunu ayrıca raporlar.
