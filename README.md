# Hudut Linux V1

## Secure OSINT Workstation

Hudut Linux, Xubuntu tabanlı; yasal açık kaynak istihbaratı, CTI, GEOINT, SOCMINT, raporlama ve güvenli araştırma süreçleri için geliştirilen bir Linux workstation projesidir.

Bu proje bir saldırı sistemi değildir. Hudut Linux'un amacı; açık kaynak araştırmalarını daha düzenli, kontrollü, raporlanabilir ve güvenli bir çalışma ortamında yürütmektir.

---

## Proje Amacı

Hudut Linux V1'in amacı:

- Yasal OSINT araştırmaları için hazır bir çalışma ortamı oluşturmak
- CTI, GEOINT, SOCMINT ve açık kaynak analiz süreçlerini düzenlemek
- Araştırma notlarını, raporları ve kanıt dosyalarını klasör yapısı içinde toplamak
- Güvenli, izole ve kontrollü bir araştırma profili oluşturmak
- Eğitim, portföy ve kamu yararına siber istihbarat çalışmaları için profesyonel bir temel hazırlamak
- Xubuntu üzerinde hızlı geliştirilebilir, modüler ve sade bir OSINT workstation mimarisi kurmak

---

## Etik Çizgi

Hudut Linux saldırı sistemi değildir.

Bu proje:

- İzinsiz erişim için kullanılmaz
- Doxxing için kullanılmaz
- Kişisel veri yaymak için kullanılmaz
- Zararlı yazılım geliştirmek için kullanılmaz
- Yetkisiz hedeflere karşı saldırı veya istismar amacıyla kullanılmaz
- Yasal açık kaynak araştırma, eğitim, analiz, raporlama ve resmi bildirim süreçleri için kullanılır

Hudut Linux; güvenlik, mahremiyet, araştırma disiplini ve raporlama odaklı bir workstation projesidir.

---

## Mevcut Durum

Hudut Linux V1 şu anda geliştirme aşamasındadır.

Mevcut sürüm hedefi:

```text
Hudut Linux V0.1 Beta
Secure OSINT Workstation Developer Beta

Bu aşamada sistem, Xubuntu üzerine kurulan çalışan bir Hudut güvenlik ve OSINT katmanı olarak geliştirilmektedir.

Tamamlanan Ana Bileşenler
1. Xubuntu Temel Kurulum
Xubuntu tabanı seçildi
Sistem güncelleme süreci planlandı
Git, Python ve temel geliştirme araçları hazırlandı
GitHub SSH bağlantısı kuruldu
Hudut Linux repo yapısı oluşturuldu
2. Proje Klasör Yapısı

Hudut Linux için modüler klasör yapısı oluşturuldu:

apps/
branding/
config/
docs/
intelligence/
launchers/
logs/
lxc/
research/
reports/
scripts/
security/
templates/
tools/

Bu yapı; uygulamalar, güvenlik ayarları, dokümantasyon, araştırma klasörleri, raporlar ve ileride eklenecek lab bileşenleri için temel oluşturur.

3. Görsel Kimlik

Hudut Linux için ilk görsel kimlik altyapısı hazırlandı:

Logo
Wallpaper
GRUB ekranı hazırlığı
Login ekranı hazırlığı
Welcome Center
Masaüstü launcher dosyaları
Autostart yapılandırması
4. Welcome Center

Hudut Linux açılış karşılama ekranı oluşturuldu.

Welcome Center içinde:

Proje tanıtımı
Etik kullanım mesajı
Hudut Linux amacı
Sosyal bağlantılar
GitHub bağlantısı
Kullanıcıyı yönlendiren başlangıç mesajları

yer alır.

5. Hudut Shield

Hudut Shield, Hudut Linux'un güvenlik kontrol merkezidir.

Temel amaç:

Sistem güvenlik durumunu görmek
Araştırma profilleri uygulamak
Ağ, DNS, firewall ve gizlilik kontrollerini yönetmek
Rapor üretmek
OSINT çalışma ortamını daha kontrollü hale getirmek

Hudut Shield menü tabanlı çalışır ve CLI komutlarıyla da kullanılabilir.

Hudut Shield Profilleri

Hudut Shield içinde şu profiller oluşturuldu:

normal
secure
osint
tor-research
public-wifi
honeypot-lab
lab

Bu profiller farklı araştırma ve çalışma senaryolarına göre firewall, DNS, proxy, mahremiyet ve güvenlik kontrollerini yönetmek için tasarlanmıştır.

Güvenlik Kontrolleri

Hudut Shield şu kontrolleri yapabilir:

Firewall durumu
DNS durumu
Proxy durumu
Tor Browser durumu
Tor servis durumu
Bluetooth durumu
Mikrofon durumu
Kamera durumu
SSH durumu
AppArmor durumu
Kernel hardening durumu
LXC/LXD durumu
Açık port kontrolü
Disk şifreleme kontrolü
Honeypot durumu
MAC randomization durumu
IPv6 privacy durumu

Profil uygulandığında sistem sonunda özet çıktı üretir.

Kernel Hardening

Hudut Linux V1 içinde temel kernel hardening ayarları eklendi.

Kontrol edilen başlıca ayarlar:

kernel.kptr_restrict
kernel.dmesg_restrict
kernel.yama.ptrace_scope
kernel.perf_event_paranoid
kernel.unprivileged_bpf_disabled
kernel.kexec_load_disabled
kernel.randomize_va_space
kernel.sysrq
fs.protected_hardlinks
fs.protected_symlinks
fs.protected_fifos
fs.protected_regular
net.ipv4.tcp_syncookies
rp_filter
accept_redirects

Amaç; araştırma workstation ortamında temel sistem sertleştirmesi sağlamaktır.

Proxy Manager

Hudut Proxy Manager eklendi.

Özellikler:

Terminal proxy durumunu gösterir
Terminal için geçici proxy export komutu üretir
Proxy temizleme komutu üretir
Firefox profil proxy durumunu gösterir
Firefox proxy ayarlarını direct moda alabilir
Proxy raporu oluşturabilir

Proxy Manager anonimlik garantisi vermez. Amaç bağlantı durumunu daha kontrollü ve raporlanabilir hale getirmektir.

Firefox OSINT Profili

Hudut Linux V1 içinde kişisel Firefox kullanımından ayrılmış özel Firefox OSINT profili oluşturuldu.

Profil adı:

hudut-osint

Bu profil açık web OSINT araştırmaları için tasarlanmıştır.

Özellikler:

Kişisel Firefox profilinden ayrıdır
Proxy varsayılan olarak kapalıdır
Tor değildir
Password saving kapalıdır
Form autofill kapalıdır
Search suggestions azaltılmıştır
Tracking protection açıktır
HTTPS-only açıktır
WebRTC kapalıdır
Konum izni kapalıdır
Kamera izni kapalıdır
Mikrofon izni kapalıdır
Telemetry azaltılmıştır
Pocket kapalıdır
Çıkışta cookie, cache ve session temizliği açıktır
resistFingerprinting açıktır

Hudut Shield üzerinden yönetilebilir:

hudut-shield firefox-osint status
hudut-shield firefox-osint prepare
hudut-shield firefox-osint launch
hudut-shield firefox-osint report

Hudut Shield menüsünde:

30. Firefox OSINT durumunu göster
31. Firefox OSINT profilini hazırla
32. Firefox OSINT profilini aç
33. Firefox OSINT raporu üret

seçenekleri yer alır.

Tor Research Workflow

Hudut Linux içinde Tor Research workflow eklendi.

Ancak önemli karar:

Hudut Linux, Tails veya Whonix alternatifi değildir.

Hudut içinde Tor Browser:

Eğitim
Demo
Bağlantı testi
Workflow gösterimi

için kullanılabilir.

Aktif ve hassas Tor araştırmaları için Tails USB tercih edilir.

Hudut Shield içinde Tor servis kontrolü bulunur:

hudut-shield tor service-status
hudut-shield tor service-start
hudut-shield tor service-stop

Ama sistem Tor servisi varsayılan olarak açık kalacak şekilde tasarlanmamıştır.

Araştırma Klasörleri

Hudut Linux araştırma süreçlerini düzenlemek için klasör yapısı içerir.

Ana başlıklar:

OSINT
SOCMINT
CTI
GEOINT
IMINT
TECHINT
Disinformation / Misinformation
Fraud Intelligence
Attack Surface Intelligence
Vulnerability Intelligence
Brand Protection
Dark Web / Leak Intelligence
Reporting

Bu yapı V1 içinde araştırma disiplinlerini ayırmak ve ileride araçları modüler şekilde bağlamak için hazırlanmıştır.

Raporlama

Hudut Linux içinde bazı bileşenler rapor üretebilir.

Mevcut rapor türleri:

Network raporu
Security raporu
Proxy raporu
Firefox OSINT profil raporu
Tor Research notları

Yerel araştırma çıktıları ve raporlar public repo için Git dışı bırakılacak şekilde planlanmıştır.

Sistem Kimliği ve Launcher Temizliği

0.1 Beta hazırlığı kapsamında sistem kimliği ve launcher path yapısı temizlendi.

Yapılanlar:

Hostname profesyonel geliştirme kimliğine alındı
Terminal prompt Hudut geliştirme ortamına uygun hale getirildi
Launcher dosyalarında kişisel path kullanımı azaltıldı
Sistem komutları için wrapper mantığı eklendi
Local rapor ve araştırma çıktıları .gitignore içine alındı
Public / Private Repo Mantığı

Hudut Linux geliştirme süreci iki repo mantığıyla yürütülebilir:

Private repo:
aktif geliştirme, test, deneme ve yarım işler

Public repo:
temiz release, demo ve portföy sunumu

Public repo içine kişisel path, local rapor, araştırma notu, evidence, özel test çıktısı veya hassas veri eklenmemelidir.

Kullanım Örneği

Hudut Shield menüsü:

hudut-shield menu

Firefox OSINT durumu:

hudut-shield firefox-osint status

Firefox OSINT profilini açma:

hudut-shield firefox-osint launch

Tor servis durumu:

hudut-shield tor service-status

Kernel hardening kontrolü:

hudut-shield menu

Menüden:

16. Kernel hardening kontrolü

seçilebilir.

0.1 Beta Kapsamı

Hudut Linux 0.1 Beta için mevcut kapsam:

Xubuntu tabanlı geliştirme ortamı
Hudut branding
Welcome Center
Hudut Shield
Güvenlik profilleri
Firewall / DNS / MAC / IPv6 privacy kontrolleri
Mikrofon / kamera gizlilik kontrolleri
Kernel hardening kontrolü
Proxy Manager
Tor Research workflow
Tor servis kontrolü
Firefox OSINT profili
Raporlama altyapısı
Temel dokümantasyon
Etik kullanım sınırları
0.2 Beta Hedefleri

0.2 Beta için planlanan başlıklar:

Ayrı hudut OSINT kullanıcısı
Kişisel kullanıcı ile araştırma kullanıcısı ayrımı
Daha temiz kullanıcı izolasyonu
OSINT araştırma klasörlerinin kullanıcı bazlı düzenlenmesi
Tool installer başlangıcı
OSINT / SOCMINT / GEOINT araçlarının kontrollü eklenmesi
0.3 Beta Hedefleri

0.3 Beta için planlanan başlıklar:

LXC / LXD entegrasyonu
hudut-lab kullanıcısı
Lab ortamı
Honeypot-lab hazırlığı
Araç test ortamları
Daha güçlü raporlama akışı
Proje Durumu

Hudut Linux V1 şu anda erken beta hazırlık aşamasındadır.

Mevcut hedef:

Hudut Linux 0.1 Beta
Secure OSINT Workstation Developer Beta

Bu sürüm, tam ISO final sürümü değil; Xubuntu üzerinde çalışan Hudut güvenlik, OSINT ve araştırma profili katmanıdır.

Yasal Uyarı

Hudut Linux yalnızca yasal ve etik araştırma süreçleri için geliştirilmiştir.

Kullanıcı, bu sistemi kullanırken kendi ülkesindeki yasalara, kurum politikalarına ve etik araştırma kurallarına uymaktan sorumludur.

Bu proje; izinsiz erişim, kişisel veri ihlali, doxxing, zararlı yazılım geliştirme veya saldırı faaliyetleri için tasarlanmamıştır.

Kısa Özet

Hudut Linux V1:

Xubuntu tabanlıdır.
Yasal OSINT ve CTI odaklıdır.
Saldırı sistemi değildir.
Hudut Shield güvenlik merkezi içerir.
Firefox OSINT profili içerir.
Tor için Tails/Whonix alternatifi değildir.
Raporlama ve araştırma düzeni sağlar.
0.1 Beta aşamasına hazırlanmaktadır.

---

## Calamares Installer Demo

Hudut Linux V1 içinde Calamares tabanlı kurulum arayüzü için demo branding hazırlanmıştır.

Mevcut demo başlığı:

```text
Hudut Linux Kurulum
V0.1 Beta
Bu aşamada Calamares gerçek disk kurulum akışı için değil, Hudut Linux installer arayüzü ve branding testi için kullanılmaktadır.

Gerçek kurulum akışı Penguins' eggs ile üretilecek Live ISO üzerinde yapılandırılacaktır.

