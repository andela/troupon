from django.shortcuts import render

# Create your views here.


# from django.shortcuts import render
# from django.views.generic.base import RedirectView

# from articles.models import Article

# class IndexRedirectView(RedirectView):

#     permanent = False
#     pattern_name = 'article-detail'

#     def get_redirect_url(self, *args, **kwargs):
#         article = get_object_or_404(Article, pk=kwargs['pk'])
#         article.update_counter()
#         return super(ArticleCounterRedirectView, self).get_redirect_url(*args, **kwargs)
