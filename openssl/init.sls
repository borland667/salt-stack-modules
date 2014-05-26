#
# OpenSSL crypto library
#

{% import 'openssl/vars.sls' as ssl with context %}

openssl:
  pkg.installed

{{ ssl.home }}:
  file.directory:
    - user: root
    - group: root
    - mode: 755

{{ ssl.ca }}:
  file.directory:
    - user: root
    - group: root
    - mode: 755
    - require:
      - file: {{ ssl.home }}

{{ ssl.certs }}:
  file.directory:
    - user: root
    - group: root
    - mode: 755
    - require:
      - file: {{ ssl.home }}

{{ ssl.keys }}:
  file.directory:
    - user: root
    - group: root
    - mode: 755
    - require:
      - file: {{ ssl.home }}

{% if 'server' != salt['pillar.get']('net:hosts:%s:vpn'|format(grains['id']), {}) %}
{{ ssl.keys }}/{{ grains['id'] }}.key:
  file.managed:
    - source: salt://keys/{{ grains['id'] }}.key
    - user: root
    - group: root
    - mode: 640
    - makedirs: True

{{ ssl.certs }}/{{ grains['id'] }}.crt:
  file.managed:
    - source: salt://certs/{{ grains['id'] }}.crt
    - user: root
    - group: root
    - mode: 644
    - makedirs: True
{% endif %}

{{ ssl.ca_crt }}:
  file.managed:
    - source: salt://ca/ca.crt
    - user: root
    - group: root
    - mode: 644
    - makedirs: True
