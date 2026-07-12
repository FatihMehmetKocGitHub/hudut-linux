# Hudut Linux V1 Project Overview

## Proje Tanımı

Hudut Linux V1, Xubuntu 24.04 tabanlı güvenli OSINT ve siber istihbarat çalışma istasyonudur.

## Hedef

Yerel, düzenli, savunulabilir ve rapor odaklı bir intelligence workstation oluşturmak.

## Yol Haritası

| Sürüm | Odak |
|---|---|
| V1 | Manuel güvenli workstation ve raporlama |
| V2 | Otomasyon |
| V3 | Yapay zekâ destekli analiz |

## V1 Mimarisi

```text
Hudut Linux V1
├── Hudut Shield
├── Proxy Manager
├── Firefox OSINT Profile
├── Tor Research Workflow
├── LXD / LXC Lab
├── LXC Manager
├── Tool Installer
├── Control Panel
├── Intelligence Workspace
└── Report Templates
```

## LXC Containerları

| Container | Amaç |
|---|---|
| hudut-osint | Açık kaynak istihbaratı |
| hudut-socmint | Sosyal medya istihbaratı |
| hudut-cti | Siber tehdit istihbaratı |
| hudut-techint | DNS, IP, ASN ve teknik altyapı |
| hudut-geoint | GEOINT / IMINT |
| hudut-dev | Python ve geliştirme |
| hudut-sandbox | Güvenli test ve genel lab |

## Raporlama Standardı

Her rapor şunları içermelidir:

- Kapsam
- Metodoloji
- Bulgular
- Göstergeler
- Zaman çizelgesi
- Risk değerlendirmesi
- Öneriler
- Etik ve yasal not
