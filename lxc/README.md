# Hudut LXD / LXC Lab

Hudut Linux V1 içinde LXD / LXC katmanı, ana sistemi temiz tutmak ve OSINT / CTI / TECHINT / DEV çalışmalarını izole etmek için kullanılır.

## V1 Container Listesi

| Container | Amaç |
|---|---|
| `hudut-osint` | OSINT / SOCMINT araştırma araçları |
| `hudut-cti` | CTI kaynakları, IOC analizleri ve tehdit istihbaratı yardımcıları |
| `hudut-techint` | DNS, WHOIS, ASN, IP, HTTP header, SSL ve network analizleri |
| `hudut-dev` | Python araç geliştirme, raporlama scriptleri ve otomasyon denemeleri |
| `hudut-sandbox` | Yeni araçları ana sisteme bulaştırmadan test etme ortamı |
| `honeypot-lab` | İzole honeypot demo ve log analiz ortamı |

## Ana Mantık

- Ana sistem sadece yönetim, GUI, dokümantasyon ve güvenlik profilleri için temiz kalır.
- Araç kurulumları mümkün oldukça container içine alınır.
- Her büyük güncellemeden önce snapshot alınır.
- Bozulan container silinir veya snapshot'tan geri döndürülür.
- Public GitHub reposuna API key, kanıt dosyası, kişisel not veya gerçek hedef verisi eklenmez.

## Script Sırası

```bash
bash lxc/scripts/01_install_lxd.sh
bash lxc/scripts/02_create_containers.sh
bash lxc/scripts/03_snapshot_all.sh
bash lxc/scripts/06_container_status.sh
bash lxc/scripts/07_create_desktop_lxc_folders.sh
