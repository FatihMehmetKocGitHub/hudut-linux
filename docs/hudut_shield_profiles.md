# Hudut Shield Profil Tablosu

Hudut Shield profilleri, Xubuntu tabanlı Hudut Linux sisteminde güvenli çalışma ortamı oluşturmak için kullanılır.

## Profil Özeti

| Profil | Firewall | DNS | MAC | Bluetooth | Mikrofon/Kamera | SSH | Kullanım |
|---|---|---|---|---|---|---|---|
| normal | Açık | Normal DNS | Mevcut ayar | Değiştirilmez | Kapatılır / mute | Değiştirilmez | Günlük güvenli kullanım |
| secure | Açık | Secure DNS | Stable random | Kapatılır | Kapatılır / mute | Kapatılır | En güçlü temel güvenlik |
| osint | Açık | OSINT DNS | Stable random | Kapatılması önerilir | Kapatılır / mute | Kapalı kalmalı | Yasal OSINT araştırması |
| tor-research | Gelen kapalı | Tor Browser ayrı ağ kullanır | Stable random | Kapatılır | Kapatılır / mute | Kapalı önerilir | Tor araştırma hazırlığı |
| public-wifi | Açık | Secure DNS | Random | Kapatılır | Kapatılır / mute | Kapatılır | Ortak Wi-Fi güvenliği |
| lab | Kontrollü | Lab DNS | Stable random | Kapalı önerilir | Kapatılır / mute | Gerekirse açık | Yerel test/lab |
| honeypot-lab | Ana sistem korumalı | Lab DNS | Lab/stable | Kapalı önerilir | Kapatılır / mute | Ana sistemde kapalı | İzole honeypot hazırlığı |

## Her Profilde Ortak Privacy Lock

Her profil uygulanırken Hudut Shield şunları yapar:

- Mikrofon kaynaklarını mute etmeye çalışır
- Kamera için uvcvideo modülünü kapatmaya çalışır
- Mikrofon ve kamera durumunu hudut-shield status içinde raporlar

## V1 İlkesi

Hudut Shield V1; iz kaybettirme, yetkisiz erişim veya saldırı gizleme aracı değildir.

Amaç:

- Güvenli çalışma ortamı
- Public Wi-Fi koruması
- Lab ayrımı
- Yasal OSINT araştırması
- Kernel hardening kontrolü
- Mikrofon/kamera mahremiyeti
- Raporlanabilir güvenlik durumu
