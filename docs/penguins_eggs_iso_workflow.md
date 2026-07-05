# Hudut Linux Penguins' eggs ISO Workflow

Hudut Linux V1 için ISO/remaster sürecinde Penguins' eggs kullanılacaktır.

## Doğru Sıra

1. Hudut Linux geliştirme sistemi hazırlanır
2. Kişisel veriler ve local raporlar temizlenir
3. Penguins' eggs kurulur
4. Sistemden Live ISO/remaster üretilir
5. Live ISO test edilir
6. Calamares yapılandırması Live ISO içinde hazırlanır
7. Hudut Kurulum kısayolu Live ortamda aktif kullanılır

## Eggs Amacı

Penguins' eggs ile hedeflenenler:

- Kurulu Hudut sisteminden ISO üretmek
- Hudut branding, Welcome Center, Hudut Shield ve Firefox OSINT profilini ISO içine taşımak
- Live ortamda sistemi test etmek
- Daha sonra Calamares ile grafiksel kurulum hazırlamak

## Güvenlik Notu

ISO içine SSH key, GitHub token, kişisel tarayıcı oturumları, çerezler, local raporlar, evidence dosyaları, kişisel notlar, Machine ID / Boot ID ve kişisel kullanıcı geçmişi dahil edilmemelidir.
