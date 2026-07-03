# Hudut Shield Menü Açıklamaları

## Menü Seçenekleri

| No | Menü seçeneği | Ne işe yarar? | Sistemde neyi değiştirir? | Ne zaman kullanılır? | Risk |
|---:|---|---|---|---|---|
| 1 | Genel güvenlik durumu | Sistemin güvenlik özetini gösterir. | Değişiklik yapmaz. | İlk kontrol için. | Güvenli |
| 2 | Ağ durumu göster | IP, DNS, MAC, IPv6, VPN, Bluetooth ve portları gösterir. | Değişiklik yapmaz. | Ağ kontrolü için. | Güvenli |
| 3 | Profil tablolarını göster | Profillerin ne yaptığını açıklar. | Değişiklik yapmaz. | Profil seçmeden önce. | Güvenli |
| 4 | Normal profil uygula | Günlük güvenli profil. | Firewall açar, DNS normale döner. | Normal kullanım. | Düşük |
| 5 | Secure profil uygula | Güçlü güvenlik profili. | Firewall açar, SSH/Bluetooth kapatır, Secure DNS ve stable MAC uygular. | Güvenli çalışma. | Orta |
| 6 | OSINT profil uygula | OSINT araştırma profili. | Firewall, OSINT DNS, stable MAC, research/reports klasörleri. | Yasal OSINT. | Orta |
| 7 | Tor Research profil uygula | Tor araştırma hazırlığı. | Bluetooth bloklar, stable MAC yapar, Tor klasörleri oluşturur. | Tor Browser araştırması. | Orta |
| 8 | Public Wi-Fi profil uygula | Ortak ağ koruması. | Firewall, SSH kapatma, Bluetooth bloklama, Secure DNS, random MAC. | Kafe/otel Wi-Fi. | Orta-yüksek |
| 9 | Lab profil uygula | Lab/test profili. | Lab DNS, stable MAC, lab klasörü. | LXC/VM testleri. | Orta |
| 10 | IPv4 DHCP yenile | IPv4 adresini yeniler. | Aktif bağlantıyı kapatıp açar. | Ağ sorunu varsa. | Orta |
| 11 | DNS secure uygula | Güvenli DNS uygular. | DNS adreslerini değiştirir. | Daha güvenli DNS için. | Düşük-orta |
| 12 | MAC stable random uygula | Sabit rastgele MAC ayarı. | MAC modunu stable yapar. | Günlük güvenli kullanım. | Orta |
| 13 | MAC random uygula | Rastgele MAC ayarı. | MAC modunu random yapar. | Public Wi-Fi. | Orta-yüksek |
| 14 | Network raporu üret | Ağ raporu oluşturur. | reports/network içine dosya yazar. | Kanıt/portföy. | Güvenli |
| 15 | Security raporu üret | Güvenlik raporu oluşturur. | reports/security içine dosya yazar. | Sistem güvenlik kaydı. | Güvenli |
| 0 | Çıkış | Menüden çıkar. | Değişiklik yapmaz. | İş bitince. | Güvenli |

## Profil Mantığı

Hudut Shield profilleri yasal, etik ve raporlanabilir güvenlik çalışmaları için hazırlanmıştır. Amaç iz gizlemek veya yetkisiz erişim değildir. Amaç güvenli çalışma ortamı, public Wi-Fi koruması, lab ayrımı ve araştırma düzenidir.
