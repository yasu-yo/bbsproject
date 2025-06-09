from django.shortcuts import render
from django.views import generic
from .models import Article
from django.urls import reverse_lazy
from .forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin   # LoginRequiredMixinをインポート
from django.core.exceptions import PermissionDenied    # PermissionDeniedをインポート

class IndexView(generic.ListView):
    model = Article
    template_name = 'bbs/index.html'

class DetailView(generic.DetailView):
    model = Article
    template_name = 'bbs/detail.html'

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    template_name = 'bbs/create.html'
    fields = ['content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    template_name = 'bbs/create.html'
    fields = ['content']
    
        # dispatchメソッドで権限チェックを追加
    def dispatch(self, request, *args, **kwargs):
        # 編集対象の投稿オブジェクトを取得
        obj = self.get_object()
        # 投稿者と現在のユーザーが一致しない場合は403エラーを発生
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません。')
        # 親クラスのdispatchを呼び出して通常の処理を継続
        return super(UpdateView, self).dispatch(request, *args, **kwargs)
       # カスタム403のビュー(アクセス権限が無い場合)
def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {'error_message': str(exception)}, status=403)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    template_name = 'bbs/delete.html'
    success_url = reverse_lazy('bbs:index')

def search(request):
    articles = None
    searchform = SearchForm(request.GET)

    if searchform.is_valid():
        query = searchform.cleaned_data['words']
        articles = Article.objects.filter(content__icontains=query)
        return render(request, 'bbs/results.html', {'articles':articles, 'searchform':searchform})
    
# Create your views here.