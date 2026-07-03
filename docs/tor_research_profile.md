# Hudut Tor Research Profile

Hudut Tor Research Profile, Tor Browser ile yasal araştırma, açık kaynak doğrulama ve gizlilik farkındalığı için hazırlanmış V1 profilidir.

## Amaç

Tor Research profili şunları sağlar:

- Tor Browser varlığını kontrol eder
- Tor araştırma klasörlerini hazırlar
- Uyarı dosyalarını oluşturur
- Araştırma notu şablonu verir
- Proxy Manager ile Tor Browser'ı karıştırmaz
- Tüm sistemi Tor'a yönlendirmez

## V1 Kararı

Hudut Linux V1 içinde tüm sistem Tor ağına zorla yönlendirilmez.

Bunun nedeni:

- DNS, proxy, tarayıcı ve sistem trafiği karışabilir
- Yanlış güven hissi oluşabilir
- Tor Browser zaten kendi güvenlik modeline sahiptir
- V1 hedefi kontrollü ve raporlanabilir araştırma ortamıdır

## Komutlar

Tor Research durum kontrolü:

    hudut-shield tor status

Tor Research klasörlerini hazırla:

    hudut-shield tor prepare

Yeni araştırma notu oluştur:

    hudut-shield tor note

## Klasör Yapısı

    research/tor/
    ├── downloads/
    ├── notes/
    ├── screenshots/
    ├── reports/
    ├── evidence/
    ├── warnings.md
    └── tor_research_template.md

## Güvenlik Notu

Tor Browser gizlilik sağlar ama hatalı kullanım gizliliği zayıflatabilir.

Riskli davranışlar:

- Kişisel hesaplara giriş yapmak
- Eklenti kurmak
- Torrent kullanmak
- Dosya indirip ana sistemde açmak
- Kişisel tarayıcıyla aynı araştırmayı sürdürmek
- Kimlik bilgisi paylaşmak
- İndirilen belgelerin metadata bilgisini kontrol etmemek

## Etik Sınır

Bu profil saldırı, yetkisiz erişim, doxxing veya kişisel veri yayma amacıyla kullanılmaz.
