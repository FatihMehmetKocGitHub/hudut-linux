# Hudut Linux Güncelleme Altyapısı

Hudut Linux güncelleme mantığı GitHub deposu ve LXC/LXD container katmanı üzerine kurulacaktır.

## V1 Güncelleme Yaklaşımı

- Ana sistem temiz tutulur
- Proje dosyaları GitHub üzerinden güncellenir
- Araçlar mümkün olduğunca LXC container içinde çalıştırılır
- Container güncellemelerinden önce snapshot alınır
- Hata durumunda rollback yapılır

## Hedef

Güncellemeler kontrollü, kayıtlı ve geri alınabilir olmalıdır.
