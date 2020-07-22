from django.conf import settings
from django_hosts import host
from django_hosts import patterns


host_patterns = patterns('',
    host(r'', settings.ROOT_URLCONF, name='www'),
    host(r'help', 'help.urls', name='help'),
    host(r'kucg-official', 'kucg.urls', name='kucg'),
)
