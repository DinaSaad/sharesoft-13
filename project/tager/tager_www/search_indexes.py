
from haystack import indexes
from tager.models import Post
from haystack import site
from haystack.indexes import *



# Nadeem Barakat :This class points to which models will be indexed , this index the post class .
class PostIndex(indexes.SearchIndex, indexes.Indexable,):
    text = indexes.CharField(document=True, use_template=True)  ## The text field with its template will be used for full text search on Solr. 
    author = indexes.CharField(model_attr='user')  ## The other two fields will be used to faceted (drill down) navigation
    description = models.CharField(model_attr='description')
    suggestions = indexes.FacetCharField() # for spelling suggestions
   



    # for more filtering we can filter results with as much attributes in the class as we want to get narrower search results
    def index_queryset(self):
        return self.get_model().objects.all()



    def get_model(self):
        return Post


## this method is prededined method by solr search engine for spelling check
    def prepare(self, obj):
        prepared_data = super(PostIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data




site.register(Post, PostIndex)


