from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.shortcuts import redirect
from django.shortcuts import render
from django_hosts.resolvers import reverse
from django.urls import reverse_lazy
from urllib.parse import urlencode

from .forms import CodexPasswordChangeForm
from .forms import UserForm
from .models import Site as OriginalSite
from .models import User


class Top(TemplateView):
    """
    Top page
    ユーザに紐づけられたサイトの一覧を表示する。
    """
    template_name = 'X/top.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            sites = OriginalSite.objects.using('default').filter(user=self.request.user)
            context['sites'] = sites
        return context


class Profile(LoginRequiredMixin, TemplateView):
    """
    Profile page
    """
    login_url = '/top/'
    template_name = 'X/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    login_url = '/top/'
    template_name='X/update_profile.html'
    success_url = reverse_lazy('codeX:profile')
    form_class = UserForm


class LoginPage(LoginView):
    """login ビュー"""
    template_name = 'X/login.html'


class Logout(LogoutView):
    """logout ビュー"""
    template_name = 'X/top.html'


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = CodexPasswordChangeForm
    success_url = reverse_lazy('codeX:change_password_done')
    template_name = 'X/change_password.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'X/change_password_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLを送付するページ"""
    subject_template_name = 'X/mail_template/reset_password/subject.txt'
    email_template_name = 'X/mail_template/reset_password/message.txt'
    template_name = 'X/reset_password_form.html'
    success_url = reverse_lazy('codeX:reset_password_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたと表示するページ"""
    template_name = 'X/reset_password_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('codeX:reset_password_complete')
    template_name = 'X/reset_password_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたと表示するページ"""
    template_name = 'X/reset_password_complete.html'


class Edit(LoginRequiredMixin, TemplateView):
    """
    本アプリケーションにおけるメイン機能
    
    """
    login_url = '/top/'
    template_name = 'X/edit.html'
    def get_context_data(self, **kwargs):
        """
        original_site codeX 側のsiteモデルからひっぱてくる(これが基準となる)
        name 上記のsite名を取り出す
        db_name 上記のsite名をもとにデータベース名を推測する(そのためdb名とmodelのサイト名(app_name)は同一にすべき)

        site_command サイト名からそのアプリケーションのmodelをimport する。
            名前が競合した場合最後にimport されたものが優先される様子であったのでこの機能を追加した。

        site 各アプリケーション 側のsiteモデルを代入している。

        それ以降の処理:
            site のget_all_relationを使ってformを絞り込む。
            現段階においてはformの最大値を10と考えそこまでのif文を設定しredirectを行う。
            3/29 追記:
                formの最大値が10個という制限を無くしました

            relations 当該siteに結びついたリレーション
            
        
        try の中
            forms 最終的にreturnするformを格納するリスト
            各リレーションを一つずつ取り出しrelationが
            can_edit()を持っているか確認する
                持っている場合には以下の処理を行いそうでなければ何もせずにbreakする

            for　文内
                Form(数字)をimportしてformsに格納

        exec eval　について
            execだけではスコープに変数が反映されず, evalによって**式**を評価することで
            ローカルスコープに反映？している。
            これについては調査不足の点も否めず、より理想的なコードもあると考えられる。
            上記の説明文も良いものであるとは言い難い。よって改善が必要とされるポイントである。
            
        """
        context = super().get_context_data(**kwargs)
        original_site = OriginalSite.objects.using('default').get(id=self.kwargs['pk'])
        name = original_site.site_name
        db_name = f'db_{name}'
        site_command = f'from {name}.models import Site as _site'
        exec(site_command)
        Site = eval('_site')
        site = Site.objects.using(db_name).get(site_name=name, url=original_site.url)
        
        relations = site.get_all_relation()
        relation_num = str(len(relations))
        try:
            forms = {}
            for i, relation in enumerate(relations):
                form_num = i+1
                form_command = f'from {name}.forms import Form{form_num} as _form{form_num}'
                exec(form_command)
                exec(f'Form{form_num} = eval(\'_form{form_num}\')')
                exec(f'_form = Form{form_num}()')
                form = eval('_form')
                forms[form.return_model_name()]=form
            context['forms'] = forms
        except:
            pass
        try:
            import re
            form = str(context['form'])
            error_mes = re.search(r'<ul class="errorlist">(.*)</ul>', form).group()
            messages.error(self.request, error_mes)
        except:
            pass
        context['site'] = site
        return context

    def post(self, request, **kwargs):
        """
        POSTリクエストに対する処理
        
        req request.POSTの中身
        original_site codeX 側のsiteモデルからひっぱてくる(これが基準となる)
        name 上記のsite名を取り出す
        db_name 上記のsite名をもとにデータベース名を推測する(そのためdb名とmodelのサイト名(app_name)は同一にすべき)
        site_command サイト名からそのアプリケーションのmodelをimport する。
            名前が競合した場合最後にimport されたものが優先される様子であったのでこの機能を追加した。

        site 各アプリケーション 側のsiteモデルを代入している。 relationを求めるために使用する

        relation 各アプリケーションに結びついたモデルをすべて取得する
            _num relationのモデルがいくつ存在するか(Formの数を決める要素)
        
        以降の処理については随時コメントを入れることとする。
        """
        ## 下処理
        req = request.POST
        original_site = OriginalSite.objects.using('default').get(id=self.kwargs['pk'])
        name = original_site.site_name
        db_name = f'db_{name}'
        site_command = f'from {name}.models import Site as _site'
        exec(site_command)
        Site = eval('_site')
        site = Site.objects.using(db_name).get(site_name=name, url=original_site.url)
        relation = site.get_all_relation()
        relation_num = len(relation)

        ## 本処理
        for i in range(0, relation_num):
            try:
                if req[f'form{i+1}_change_or_not']:# もし選択されないとerrorになるのでtryで回避している
                    # form_commandにimport するFormを指定し実行。
                    form_command = f'from {name}.forms import Form{i+1}'
                    exec(form_command)
                    exec(f'_form = Form{i+1}(request.POST or None, request.FILES or None)')
                    form = eval('_form')
                    if form.is_valid():
                        # オブジェクトを生成し、追加処理を行う
                        forms = form.save(commit=False)
                        # 分岐
                        # それぞれのmodelに実装されるis_file_img,is_file_movを用いて
                        # 画像や動画である場合の処理を行う。
                        if request.FILES and forms.is_file_img():
                            try:
                                forms.img = request.FILES['img']
                            except:
                                pass
                        if request.FILES and forms.is_file_mov():
                            try:
                                forms.mov = request.FILES['mov']
                            except:
                                pass
                        else:
                            pass
                        # それぞれのサイトを外部キーとして代入し保存する。
                        forms.site = site
                        forms.save()
                        # 多対多のリレーションがあれば保存する。
                        if forms.check_many_field():
                            form.save_m2m()
                        messages.success(self.request,'保存できました。')
                        return redirect('codeX:edit', self.kwargs['pk'])
                    import re
                    form_mes = str(form)
                    error_mes = re.search(r'<ul class="errorlist">(.*)</ul>', form_mes).group()
                    messages.error(self.request, error_mes)
                    return redirect('codeX:edit', self.kwargs['pk'])
            except:
                pass
        messages.error(self.request, '保存できませんでした。必要な項目が抜けているか、チェックが入っていない可能性があります。')
        return redirect('codeX:edit', self.kwargs['pk'])
            
        
    

class Update(LoginRequiredMixin, TemplateView):
    """
    各アプリケーションのモデルのメソッドであるcan_deleteの返り値がTrueであれば利用可能である。
    利用できない場合は「更新及び削除可能であるものはございません」とのメッセージが表示される。

    """
    login_url = '/login/'
    template_name = 'X/update.html'

    def get_context_data(self, **kwargs):
        """
        ####　の流れは Editのget_context_dataと同じ

        リレーションを獲得したのち
        [[['news1'], ['news2']....], [['img1'], ['img2']....], ....]のようなクエリセットが得られる。
        これをアンパック
            i=0 の時
                [['news1'], ['news2']....]
            i=1　の時
                [['img1'], ['img2']....]
            ....
        して、さらにアンパックを行って、すべての配列に最初の要素だけを取り出す。
        その要素を用いてcan_delete()を確認し、itemに格納。
        itemをreturnして完了。
        """
        context = super().get_context_data(**kwargs)
        ####
        original_site = OriginalSite.objects.using('default').get(id=self.kwargs['pk'])
        name = original_site.site_name
        db_name = f'db_{name}'
        site_command = f'from {name}.models import Site as _site'
        exec(site_command)
        Site = eval('_site')
        site = Site.objects.using(db_name).get(site_name=name, url=original_site.url)
        ####
        relations = site.get_all_relation()
        counter = 0
        items = {}
        model_name = []
        for i, relation in enumerate(relations):
            for model in relation:
                model_name.append(model._meta.object_name)
                name = model.return_model_name()
                if model.can_delete() or model.can_update():
                    item = relations[i]
                    counter += 1
                    items[name] = item
                break
        print(model_name)
        context['model_name'] = model_name
        context['items'] = items
        context['counter'] = counter
        context['site_id'] = original_site.id
        return context


@login_required
def delete(request, *args, **kwargs):
    pk = kwargs['pk']
    mod_id = kwargs['mod_id']
    mod = kwargs['mod']
    ####
    original_site = OriginalSite.objects.using('default').get(id=kwargs['pk'])
    name = original_site.site_name
    db_name = f'db_{name}'
    site_command = f'from {name}.models import Site as _site'
    exec(site_command)
    Site = eval('_site')
    site = Site.objects.using(db_name).get(site_name=name, url=original_site.url)
    ####

    model_command = f'from {name}.models import {mod} as _{mod}'
    exec(model_command)
    exec(f'{mod} = eval(\'_{mod}\')')
    exec(f'_model = {mod}.objects.using(\'{db_name}\').get(id={mod_id})')
    model = eval('_model')
    model.delete()
    messages.success(request, '削除できました。')
    return redirect('codeX:update', kwargs['pk'])


@login_required
def update_page(request, *args, **kwargs):
    pk = kwargs['pk']
    mod_id = kwargs['mod_id']
    mod = kwargs['mod']

    ####  site を定義
    original_site = OriginalSite.objects.using('default').get(id=kwargs['pk'])
    name = original_site.site_name
    db_name = f'db_{name}'
    site_command = f'from {name}.models import Site as _site'
    exec(site_command)
    Site = eval('_site')
    site = Site.objects.using(db_name).get(site_name=name, url=original_site.url)

    ###  form番号を取得するためmodelを呼び出す  ###
    model_command = f'from {name}.models import {mod} as _{mod}'
    exec(model_command)
    exec(f'{mod} = eval(\'_{mod}\')')
    exec(f'_model = eval(\'_{mod}\')')
    model = eval('_model')

    ### form番号を取得する
    num = model.confirm_form_num(model)
    exec(f'_target = {mod}.objects.using(\'{db_name}\').get(id={mod_id})')
    target = eval('_target')

    ###  import form  ###
    form_command = f'from {name}.forms import Form{num}'
    exec(form_command)
    if request.method == "POST":
        exec(f'_form = Form{num}(request.POST or None, request.FILES or None, instance=target)')
        form = eval('_form')
        if form.is_valid():
            s = form.save()
            messages.success(request, '更新しました')
            return redirect('codeX:update_page', pk, mod_id, mod)
        import re
        form_mes = str(form)
        error_mes = re.search(r'<ul class="errorlist">(.*)</ul>', form_mes).group()
        messages.error(request, error_mes)
        return redirect('codeX:update_page', pk, mod_id, mod)
    else:
        exec(f'_form = Form{num}(request.POST or None, request.FILES or None, instance=target)')
        form = eval('_form')
        context = {'form': form, 'num': num,}

        return render(request, 'X/update_page.html', context)


