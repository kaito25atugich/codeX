import json

from django.db.models import Q
from django.shortcuts import render

from .models import Comment
from .models import Introduction
from .models import News
from .models import Tag
from .models import TopImages
from .models import SNSTwitter
from .models import YourEmail


def top(request):
    try: 
        top_image = TopImages.objects.using('db_kucg').get(id=1)
    except:
        top_image = False
    try:
        introduction = Introduction.objects.using('db_kucg').get(id=1)
    except:
        introduction = False
    try:
        sns = SNSTwitter.objects.using('db_kucg').get(id=1)
    except:
        sns = False

    news = News.objects.using('db_kucg').all().order_by('-date')[0:5]
    
    news_filtered = News.objects.using('db_kucg').all()
    news_img = []
    news_img_title = []
    for some in reversed(news_filtered):
        if some.img:
            news_img.append(some)
            news_img_title.append(some.title)
    tag_colors = {}
    news_img_title_enced = json.dumps(news_img_title[0:5])
    i = 0
    for tag in news:
        tag_colors[f"{i}"] = tag.tag.all()[0].color
        i += 1   
    tag_colors_json = json.dumps(tag_colors)
    context = {
        "top_image":top_image,
        "introduction":introduction,
        "news":news,
        "sns": sns,
        "tag_colors_json":tag_colors_json,
        "news_img":news_img[0:5],
        "news_img_title_enced":news_img_title_enced
    }
    return render(request,'kucg/top.html',context)

def activity(request,page):
    startpage = (page -1 )*9
    endpage = page * 9
    activityTitle = "最新の投稿"
    if request.method=="POST" and "search_input" in request.POST:
        news = News.objects.filter(Q(message__icontains=request.POST['search_input']) | Q(title__icontains=request.POST['search_input']) | Q(tag__tag__icontains=request.POST['search_input']))
        if len(news) == 0:
            activityTitle = f"'{request.POST['search_input']}'の検索結果はありません"
        else:
            activityTitle = f"'{request.POST['search_input']}'の検索結果 {len(news)}件ヒット"
    else:
        news = News.objects.using('db_kucg').all().order_by('-date')

    
    page_count = int(len(news) / 9) + 1
    if endpage >= len(news):
        news = news[startpage:len(news)]
    else:
        news = news[startpage:endpage]

    tagColors = {}
    i = 0
    for tag in news:
        tagColors[f"{i}"] = tag.tag.all()[0].color
        i += 1
    tagColorsJson = json.dumps(tagColors)
    try:
        sns = SNSTwitter.objects.using('db_kucg').get(id=1)
    except:
        sns = False

    context = {
        "news":news,
        "page":page,
        "page_count":page_count,
        "tagColorsJson":tagColorsJson,
        "activityTitle":activityTitle,
        "sns": sns,
    }
    return render(request,'kucg/activity.html',context)


def article_str(request,page,search_word):
    startpage = (page -1 )*9
    endpage = page * 9
    activityStrTitle = "最新の投稿"
    
    try:
        news = News.objects.using('db_kucg').filter(Q(message__icontains=search_word) | Q(title__icontains=search_word) | Q(tag__tag__icontains=search_word))
        if len(news) == 0:
            activityStrTitle = f"'{search_word}'の検索結果はありません"
        else:
            activityStrTitle = f"'{search_word}'のタグ関連記事は{len(news)}件あります"
        
        page_count = int(len(news) / 9) + 1
        if endpage >= len(news):
            news = news[startpage:len(news)]
        else:
            news = news[startpage:endpage]

        tagColors = {}
        i = 0
        for tag in news:
            tagColors[f"{i}"] = tag.tag.all()[0].color
            i += 1
        tagColorsJson = json.dumps(tagColors)
    except:
        page_cout = 1
        activityStrTitle = f"'{search_word}'の検索結果はありません"
        tagColors = {}
        tagColorsJson = json.dumps(tagColors)
    try:
        sns = SNSTwitter.objects.using('db_kucg').get(id=1)
    except:
        sns = False
    context = {
        "news":news,
        "page":page,
        "page_count":page_count,
        "tagColorsJson":tagColorsJson,
        "activityStrTitle":activityStrTitle,
        "search_word":search_word,
        "sns": sns,
    }
    return render(request,'kucg/activity.html',context)


def archive(request,year,month,page):
    startpage = (page -1 )*9
    endpage = page * 9
    archiveTitle = f"{year}年{month}月の投稿"
    tagColors = {}

    news = News.objects.using('db_kucg').filter(date__year=year,date__month=month)
    page_count = int(len(news) / 9) 
    print(page_count % 9)
    if len(news) % 9 != 0:
         page_count += 1
    if endpage >= len(news):
        news = news[startpage:len(news)]
    else:
        news = news[startpage:endpage]
   
    i = 0
    for tag in news:
        tagColors[f"{i}"] = tag.tag.all()[0].color
        i += 1
    tagColorsJson = json.dumps(tagColors)
    try:
        sns = SNSTwitter.objects.using('db_kucg').get(id=1)
    except:
        sns = False
    context = {
        "news":news,
        "page":page,
        "page_count":page_count,
        "tagColorsJson":tagColorsJson,
        "archiveTitle":archiveTitle,
        "year":year,
        "month":month,
        "sns":sns,
    }
    return render(request,'kucg/activity.html',context)


def article(request,article_id):
    article = News.objects.using('db_kucg').get(id=article_id)
    try:
        sns = SNSTwitter.objects.using('db_kucg').get(id=1)
    except:
        sns = False
    # 動画、画像、記事のみの種類を選別するもの
    type_number = 0
    # 動画のみ
    if article.mov:
        type_number = 1
        # サムネイル付き動画
        if article.img :
            type_number = 2
    # 画像のみ
    elif article.img :
        type_number = 3

    news = News.objects.using('db_kucg').all().order_by('-date')[0:3]

    if request.method == "POST":
        if request.POST["commentform"] != "":
            name = request.POST["nameform"]
            if name == "":
                name = "Commenter"

            comment_obj = Comment.objects.using('db_kucg').create(
                news=article,
                name=name,
                comment=request.POST["commentform"],
                site=article.site 
            )
    
    comments = Comment.objects.using('db_kucg').filter(news=article)
    archives = News.objects.using('db_kucg').dates('date', 'month', order='DESC')
    archives_count = []
    # for i in archives:
    #     counter = News.objects.filter(date__year=i.year,date__month=i.month)

    tagColors = {}
    i = 0
    for tag in article.tag.all():
        tagColors[f"{i}"] = tag.color
        i += 1

    tagColorsJson = json.dumps(tagColors)
    
    context = {
        "article":article,
        "type_number":type_number,
        "news":news,
        "comments":comments,
        "archives":archives,
        "archives_count":archives_count,
        "tagColorsJson":tagColorsJson,
        "sns": sns,
    }
    return render(request,'kucg/article.html',context) 


def contact(request):
    context = {}
    try:
        sns = SNSTwitter.objects.using('db_kucg').get(id=1)
    except:
        sns = False
    try:
        email = YourEmail.objects.using('db_kucg').get(id=1)
    except:
        email = False
    context['sns'] = sns
    context['email'] = email
    return render(request,'kucg/contact.html', context)