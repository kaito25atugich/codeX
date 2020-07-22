from django.contrib import admin

# Register your models here.
from kucg.models import Site
from kucg.models import News
from kucg.models import Tag
from kucg.models import TopImages
from kucg.models import Introduction
from kucg.models import Comment
from kucg.models import SNSTwitter
from kucg.models import YourEmail

admin.site.register(Site)
admin.site.register(News)
admin.site.register(Tag)
admin.site.register(TopImages)
admin.site.register(Introduction)
admin.site.register(Comment)
admin.site.register(SNSTwitter)
admin.site.register(YourEmail)

