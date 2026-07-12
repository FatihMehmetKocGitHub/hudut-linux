# Hudut Tool Installer

Hudut Tool Installer, Hudut Linux V1 içinde araç kurulumlarını container bazlı yönetmek için hazırlanmıştır.

## Amaç

Host sistemi temiz tutmak ve araçları ilgili LXC container içinde çalıştırmak.

## Profiller

| Profil | Container | Amaç |
|---|---|---|
| OSINT Tools | hudut-osint | Genel açık kaynak araştırma |
| SOCMINT Tools | hudut-socmint | Sosyal medya / platform araştırması |
| CTI Tools | hudut-cti | Siber tehdit istihbaratı |
| TECHINT Tools | hudut-techint | DNS / IP / ASN / ağ teknik analiz |
| GEOINT Tools | hudut-geoint | GEOINT / IMINT hazırlığı |
| DEV Tools | hudut-dev | Python geliştirme |
| SANDBOX Tools | hudut-sandbox | İzole test ortamı |

## Güvenlik Çizgisi

Bu araçlar yalnızca yasal araştırma, kendi lab ortamı, kendi sistemlerin ve izinli hedefler için kullanılmalıdır.

Hudut Linux V1 bir saldırı sistemi değil; güvenli araştırma, istihbarat toplama, analiz ve raporlama workstation katmanıdır.
