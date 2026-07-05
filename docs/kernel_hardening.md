# Hudut Linux Kernel Hardening

Hudut Linux V1, Xubuntu 24.04 üzerinde güvenli ve kırıcı olmayan temel kernel sertleştirme ayarları kullanır.

## Amaç

Kernel seviyesinde bilgi sızıntısını azaltmak, debug ve trace yüzeyini sınırlamak, ağ yönlendirme risklerini düşürmek ve dosya sistemi korumalarını aktif hale getirmek.

## Uygulanan Başlıca Ayarlar

- kernel.kptr_restrict
- kernel.dmesg_restrict
- kernel.yama.ptrace_scope
- kernel.perf_event_paranoid
- kernel.unprivileged_bpf_disabled
- kernel.kexec_load_disabled
- kernel.randomize_va_space
- kernel.sysrq
- fs.protected_hardlinks
- fs.protected_symlinks
- fs.protected_fifos
- fs.protected_regular
- net.ipv4.tcp_syncookies
- IPv4 ve IPv6 redirect engelleme
- rp_filter
- martian packet logging

## Uygulama

    ./scripts/apply_kernel_hardening.sh

## Kontrol

    ./scripts/check_kernel_hardening.sh
    hudut-shield status

## Not

Bu ayarlar saldırı veya iz gizleme amacıyla değil; sistem sertleştirme, güvenli çalışma ortamı ve kurumsal sunuma uygun güvenlik profili oluşturmak için kullanılır.
