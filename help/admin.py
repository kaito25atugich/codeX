from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import News
from .models import Site
from .models import UsageExamples


class Newsadmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(News, Newsadmin)
admin.site.register(Site)
admin.site.register(UsageExamples)
