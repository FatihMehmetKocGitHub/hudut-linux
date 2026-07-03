#!/usr/bin/env bash
xfce4-terminal \
  --title="Hudut Shield" \
  --command="bash -lc 'hudut-shield menu; echo; echo Kapatmak için herhangi bir tuşa basın.; read -n 1 -s -r'"
