# Sample Phishing Intelligence Report

## 1. Yönetici Özeti

Bu örnek rapor, `secure-login-example.test` gibi hayali bir phishing göstergesinin nasıl analiz edileceğini gösterir.

Amaç, Hudut Linux V1 içinde phishing göstergelerinin yasal ve savunma odaklı biçimde nasıl raporlanacağını göstermektir.

## 2. Araştırma Kapsamı

- Örnek domain: `secure-login-example.test`
- Örnek URL: `https://secure-login-example.test/auth`
- Analiz türü: Domain adı, URL yapısı, DNS göstergesi, kullanıcı kandırma riski
- Sınır: Siteye saldırı, form gönderimi, brute force veya yetkisiz test yoktur.

## 3. Metodoloji

- Domain adı kalıp analizi yapıldı.
- URL yol yapısı incelendi.
- Olası sosyal mühendislik dili değerlendirildi.
- IOC formatında örnek göstergeler çıkarıldı.

## 4. Bulgular

| No | Gösterge | Tür | Risk | Açıklama |
|---|---|---|---|---|
| 1 | `secure-login-example.test` | Domain | Yüksek | Güvenli giriş algısı oluşturan isim |
| 2 | `/auth` | URL path | Orta | Giriş sayfası taklidi izlenimi |
| 3 | `login`, `secure`, `verify` | Anahtar kelime | Orta | Kullanıcıyı işlem yapmaya zorlama dili |

## 5. IOC Listesi

| Tür | Değer |
|---|---|
| Domain | `secure-login-example.test` |
| URL | `https://secure-login-example.test/auth` |
| Keyword | `secure`, `login`, `verify` |

## 6. Değerlendirme

Bu örnek göstergeler, phishing senaryolarında sık görülen marka taklidi ve güven telkini kalıplarını temsil eder.

## 7. Öneriler

- Benzer domainler izlenmelidir.
- Kullanıcılara resmi giriş adresleri duyurulmalıdır.
- Şüpheli URL raporlama kanalı oluşturulmalıdır.
- IOC listeleri savunma sistemlerine aktarılmalıdır.

## 8. Etik ve Yasal Not

Bu rapor eğitim amaçlıdır. Gerçek phishing altyapısı analiz edilmemiştir.
