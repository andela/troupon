import datetime
from haystack import indexes
from deals.models import Deal


class DealIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.ChartField(model_attr='title')
    date_created = indexes.DateTimeField(model_attr='date_created')

    def get_model(self):
        return Deal

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date_created__lte=datetime.datetime.now())
