from haystack import *
from haystack import indexes
from tager_www.models import *
from haystack import site
from haystack.indexes import *
from haystack.query import SearchQuerySet
from haystack.indexes import SearchIndex 

# Nadeem Barakat :This class points to which models will be indexed , this index the post class .
class PostIndex(SearchIndex):
    text = indexes.EdgeNgramField(document=True, use_template=True)  ## The text field with its template will be used for full text search on Solr. 
    author = indexes.CharField(model_attr='seller')  ## The other two fields will be used to faceted (drill down) navigation
    description = indexes.CharField(model_attr='description',null=True)
    content_auto = indexes.EdgeNgramField(model_attr='title')
   
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Post.objects.filter(pub_date__lte=datetime.now())
    
    def get_queryset(self):
        return Post.objects.all()  


site.register(Post, PostIndex)


class UserProfileIndex(SearchIndex):
    text = indexes.EdgeNgramField(document=True, use_template=True)  ## The text field with its template will be used for full text search on Solr. 


    def get_queryset(self):
        return UserProfile.objects.all()

site.register(UserProfile, UserProfileIndex)

class ChannelIndex(SearchIndex):
    text = indexes.EdgeNgramField(document=True, use_template=True)  ## The text field with its template will be used for full text search on Solr. 

    
    def get_queryset(self):
        return Channel.objects.all()
site.register(Channel, ChannelIndex)
