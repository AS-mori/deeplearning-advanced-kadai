from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Product
from django.urls import reverse_lazy

class TopView(TemplateView):
# Templateファイルをtemplateフォルダからの相対パスで指定
    template_name = 'top.html'

class ProductListView(ListView):
    model = Product
# ページネーション = 表示件数が多い場合に、1ページあたりに何件表示するか を指定
    paginate_by = 3

# 新規作成フォーム
class ProductCreateView(CreateView):
    model = Product
    fields = '__all__' # 全てのフィールドを表示

# 編集フォーム
class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__' # 全てのフィールドを表示
    template_name_suffix = '_update_form'

# 削除フォーム
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('list')

# 商品詳細ページ
class ProductDetailView(DetailView):
    model = Product