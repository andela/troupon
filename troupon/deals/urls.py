
from django.conf.urls import url, include
from .views import DealSearchView, DealSearchCityView, DealView, DealsView, \
    CategoryView, DealCategoryView, DealSlugView, AdvertiserView, \
    DealAdvertiserView


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^search/entry/$', DealSearchView.as_view(), name = 'dealsearch'),
    url(r'^search/cities/$', DealSearchCityView.as_view(), name ='dealsearchcity'),
    # /deals/
    url(r'^$', DealsView.as_view(), name='deals'),
    # /deals/:id/
    url(r'^(?P<deal_id>[0-9]+)/$', DealView.as_view(), name='deal'),
    # /deals/categories/
    url(r'^categories/$',
        CategoryView.as_view(),
        name='deal-categories'),
    # /deals/advertisers/
    url(r'^merchants/$',
        AdvertiserView.as_view(),
        name='deal-advertisers'),
    # /deals/:slug/
    url(r'^(?P<deal_slug>[\w-]+)/$',
        DealSlugView.as_view(),
        name='deal-with-slug'),
    # /deals/category/:slug/
    url(r'^category/(?P<category_slug>[\w-]+)/$',
        DealCategoryView.as_view(),
        name='deal-category-with-slug'),
    # /deals/advertiser/:slug/
    url(r'^merchant/(?P<advertiser_slug>[\w-]+)/$',
        DealAdvertiserView.as_view(),
        name='deal-advertiser-with-slug'),
]
