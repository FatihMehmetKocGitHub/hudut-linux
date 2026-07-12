# Hudut LXC Manager

Hudut LXC Manager, Hudut Linux V1 içinde LXD/LXC container katmanını yönetmek için hazırlanan basit GUI aracıdır.

## Amaç

- Container durumunu görmek
- Container başlatmak / durdurmak / restart etmek
- Tüm containerları toplu başlatmak / durdurmak
- clean-base snapshot bilgisini görmek
- LXC status raporu üretmek

## V1 Container Listesi

| Container | IP | Amaç |
|---|---:|---|
| hudut-osint | 10.99.10.10 | Genel OSINT |
| hudut-socmint | 10.99.10.11 | Sosyal medya açık kaynak araştırması |
| hudut-cti | 10.99.10.12 | Siber tehdit istihbaratı |
| hudut-techint | 10.99.10.13 | Teknik istihbarat |
| hudut-geoint | 10.99.10.14 | GEOINT / IMINT |
| hudut-dev | 10.99.10.15 | Geliştirme ortamı |
| hudut-sandbox | 10.99.10.16 | Deneme / izole test ortamı |

## Güvenlik Notu

clean-base restore işlemi GUI içinde otomatik yapılmaz. Sadece manuel komut gösterilir.
Bu karar, yanlışlıkla veri kaybını önlemek için alınmıştır.
