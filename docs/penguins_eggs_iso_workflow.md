# Hudut Linux Penguins' eggs ISO Workflow

Hudut Linux V1 için ISO/remaster sürecinde Penguins' eggs değerlendirilmektedir.

## Amaç

Penguins' eggs ile hedeflenenler:

- Kurulu Hudut Linux sisteminden ISO üretmek
- Live ortamda Hudut Linux'u test etmek
- Hudut branding, Welcome Center, Hudut Shield ve Firefox OSINT profilini ISO içine taşımak
- Daha sonra Calamares installer ile grafiksel kurulum akışı hazırlamak

## Doğru Sıra

Hudut Linux ISO sürecinde doğru sıra:

1. Hudut Linux geliştirme sistemi hazırlanır
2. Kişisel veriler ve local raporlar temizlenir
3. Penguins' eggs kurulur
4. Sistemden ISO/remaster üretilir
5. Live ISO test edilir
6. Calamares yapılandırması Live ISO içinde hazırlanır
7. Hudut Kurulum kısayolu Live ortamda aktif kullanılır

## Calamares Notu

Calamares tek başına kurulduğunda yeterli değildir.

Calamares şu dosyalardan birini bekler:

```text
/etc/calamares/settings.conf
/usr/share/calamares/settings.conf
