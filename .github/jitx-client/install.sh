#!/usr/bin/env bash
set -e

chmod +x /root/.jitx/current/jitx # artifact caching loses permissions somewhere
cp /root/.jitx/current/jitx.config /root/.jitx # missing config file
chmod +x /root/.jitx/current/jstanza
chmod +x /root/.jitx/current/stanza/stanza
apt install -y python3.8
