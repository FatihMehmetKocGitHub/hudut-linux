#!/usr/bin/env bash

echo "HUDUT KERNEL HARDENING STATUS"
echo "========================================"

keys=(
"kernel.kptr_restrict"
"kernel.dmesg_restrict"
"kernel.yama.ptrace_scope"
"kernel.perf_event_paranoid"
"kernel.unprivileged_bpf_disabled"
"kernel.kexec_load_disabled"
"kernel.randomize_va_space"
"kernel.sysrq"
"fs.protected_hardlinks"
"fs.protected_symlinks"
"fs.protected_fifos"
"fs.protected_regular"
"net.ipv4.tcp_syncookies"
"net.ipv4.conf.all.accept_redirects"
"net.ipv4.conf.default.accept_redirects"
"net.ipv6.conf.all.accept_redirects"
"net.ipv6.conf.default.accept_redirects"
"net.ipv4.conf.all.rp_filter"
"net.ipv4.conf.default.rp_filter"
)

for key in "${keys[@]}"; do
    value=$(sysctl -n "$key" 2>/dev/null || echo "N/A")
    printf "%-45s %s\n" "$key" "$value"
done

echo "========================================"
