import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.loading import get_model
from haystack.backends import BaseEngine, BaseSearchBackend, BaseSearchQuery, log_query, EmptyResults
from haystack.constants import ID, DJANGO_CT, DJANGO_ID
from haystack.exceptions import MissingDependency
from haystack.models import SearchResult
from haystack.utils import get_identifier
try:
    from django.db.models.sql.query import get_proxied_model
except ImportError:
    # Likely on Django 1.0
    get_proxied_model = None
try:
    import pyes
except ImportError:
    raise MissingDependency("The 'elasticsearch' backend requires the installation of 'pyes'. Please refer to the documentation.")


class ElasticSearchBackend(BaseSearchBackend):
    # Word reserved by Elasticsearch for special use.
    RESERVED_WORDS = (
        'AND',
        'NOT',
        'OR',
        'TO',
    )

    # Characters reserved by Elasticsearch for special use.
    # The '\\' must come first, so as not to overwrite the other slash replacements.
    RESERVED_CHARACTERS = (
        '\\', '+', '-', '&&', '||', '!', '(', ')', '{', '}',
        '[', ']', '^', '"', '~', '*', '?', ':',
    )

    def __init__(self, connection_alias, **connection_options):
        super(ElasticSearchBackend, self).__init__(connection_alias, **connection_options)

        if not 'URL' in connection_options:
            raise ImproperlyConfigured("You must specify a 'URL' in your settings for connection '%s'." % connection_alias)

        if not 'INDEX_NAME' in connection_options:
            raise ImproperlyConfigured("You must specify a 'INDEX_NAME' in your settings for connection '%s'." % connection_alias)

        self.conn = pyes.ES(["%s:9200" % connection_options['URL']], timeout=self.timeout)
        self.index_name = connection_options['INDEX_NAME']
        self.log = logging.getLogger('haystack')

    def update(self, index, iterable, commit=True):
        docs = []

        try:
            for obj in iterable:
                prepped_data = index.full_prepare(obj)
                # FIXME: Not sure this is right.
                self.conn.index(prepped_data, self.index_name, 'modelresult', prepped_data[ID])
        except pyes.connection.ElasticSearchException:
            if not self.silently_fail:
                raise

            self.log.error("Failed to add documents to Elasticsearch: %s", e)

    def remove(self, obj_or_string, commit=True):
        doc_id = get_identifier(obj_or_string)

        try:
            self.conn.delete(self.index_name, 'modelresult', doc_id)
        except pyes.connection.ElasticSearchException, e:
            if not self.silently_fail:
                raise

            self.log.error("Failed to remove document '%s' from Elasticsearch: %s", solr_id, e)

    def clear(self, models=[], commit=True):
        try:
            if not models:
                # *:* matches all docs in Solr
                self.conn.delete_index(self.index_name)
            else:
                models_to_delete = []

                for model in models:
                    models_to_delete.append("%s:%s.%s" % (DJANGO_CT, model._meta.app_label, model._meta.module_name))

                self.conn.deleteByQuery(self.index_name, 'modelresult', {'query_string': {'query': " OR ".join(models_to_delete)}}) #, commit=commit)
        except pyes.connection.ElasticSearchException, e:
            if not self.silently_fail:
                raise

            if len(models):
                self.log.error("Failed to clear Elasticsearch index of models '%s': %s", ','.join(models_to_delete), e)
            else:
                self.log.error("Failed to clear Elasticsearch index: %s", e)

    @log_query
    def search(self, query_string, sort_by=None, start_offset=0, end_offset=None,
               fields='', highlight=False, facets=None, date_facets=None, query_facets=None,
               narrow_queries=None, spelling_query=None,
               limit_to_registered_models=None, result_class=None, **kwargs):
        if len(query_string) == 0:
            return {
                'results': [],
                'hits': 0,
            }

        kwargs = {

        }

        # The body we should build (not URL query params!):
        {
            'query_string': {
                'fields': ['text', 'author^2'], # For field boosting.
                'query': '(django_ct:myapp.mymodel AND (hello AND world)',
                'boost': 1.0, # Hrm, not sure this is what we want...
                'default_field': 'text', # But make it the right thing.
                'default_operator': 'AND', # But make it the right thing.
                'analyze_wildcard': True,
                'auto_generate_phrase_queries': True, # Maybe?
            },
            'filtered': {}, # Maybe the ``fq`` equivalent? Maybe not. :/
            'more_like_this_field': {
                'text': { # But make it the right thing.
                    'like_text': '...', # Going to need to ``get`` the text first, then resubmit as part of the body.
                    'stop_words': [], # Maybe needed. :/
                }
            },
            'range': {
                'from': start_offset,
                'size': end_offset - start_offset,
            },
            'facets': {
                'field_name': {
                    'terms': {
                        'field': 'field_name',
                    },
                },
                'query_name': {
                    'query': {
                        'query': 'custom ish here', # I think this nesting is needed?
                    },
                },
                'date_field_name': {
                    'date_histogram': {
                        'field': 'date_field_name',
                        'interval': 'day', # 'year', 'month', 'week', 'day', 'hour', 'minute'
                    }
                }
            },
            'highlight': {
                'fields': {
                    'text': {'store': 'yes'}, # The safe default
                    # 'text': {"store" : "yes", "term_vector" : "with_positions_offsets"}, # If we setup a mapping, this is faster.
                }
            },
            # Spelling suggestions aren't present yet. Maybe aspell or just leave it out?
            # Alterantively, maybe the fuzzy query DSL bits might be able to help?
        }
        # End body.

        if fields:
            kwargs['fl'] = fields

        if sort_by is not None:
            kwargs['sort'] = sort_by

        if start_offset is not None:
            kwargs['from'] = start_offset

        if end_offset is not None:
            kwargs['size'] = end_offset - start_offset

        if highlight is True:
            kwargs['hl'] = 'true'
            kwargs['hl.fragsize'] = '200'

        # if self.include_spelling is True:
        #     kwargs['spellcheck'] = 'true'
        #     kwargs['spellcheck.collate'] = 'true'
        #     kwargs['spellcheck.count'] = 1

        #     if spelling_query:
        #         kwargs['spellcheck.q'] = spelling_query

        if facets is not None:
            kwargs['facet'] = 'on'
            kwargs['facet.field'] = facets

        if date_facets is not None:
            kwargs['facet'] = 'on'
            kwargs['facet.date'] = date_facets.keys()
            kwargs['facet.date.other'] = 'none'

            for key, value in date_facets.items():
                kwargs["f.%s.facet.date.start" % key] = self.conn._from_python(value.get('start_date'))
                kwargs["f.%s.facet.date.end" % key] = self.conn._from_python(value.get('end_date'))
                gap_by_string = value.get('gap_by').upper()
                gap_string = "%d%s" % (value.get('gap_amount'), gap_by_string)

                if value.get('gap_amount') != 1:
                    gap_string += "S"

                kwargs["f.%s.facet.date.gap" % key] = '+%s/%s' % (gap_string, gap_by_string)

        if query_facets is not None:
            kwargs['facet'] = 'on'
            kwargs['facet.query'] = ["%s:%s" % (field, value) for field, value in query_facets]

        if limit_to_registered_models is None:
            limit_to_registered_models = getattr(settings, 'HAYSTACK_LIMIT_TO_REGISTERED_MODELS', True)

        if limit_to_registered_models:
            # Using narrow queries, limit the results to only models handled
            # with the current routers.
            if narrow_queries is None:
                narrow_queries = set()

            registered_models = self.build_models_list()

            if len(registered_models) > 0:
                narrow_queries.add('%s:(%s)' % (DJANGO_CT, ' OR '.join(registered_models)))

        if narrow_queries is not None:
            kwargs['fq'] = list(narrow_queries)

        try:
            raw_results = self.conn.search(query_string, **kwargs)
        except (IOError, SolrError), e:
            if not self.silently_fail:
                raise

            self.log.error("Failed to query Solr using '%s': %s", query_string, e)
            raw_results = EmptyResults()

        return self._process_results(raw_results, highlight=highlight, result_class=result_class)

    def more_like_this(self, model_instance, additional_query_string=None,
                       start_offset=0, end_offset=None,
                       limit_to_registered_models=None, result_class=None, **kwargs):
        from haystack import connections

        # Handle deferred models.
        if get_proxied_model and hasattr(model_instance, '_deferred') and model_instance._deferred:
            model_klass = get_proxied_model(model_instance._meta)
        else:
            model_klass = type(model_instance)

        index = connections[self.connection_alias].get_unified_index().get_index(model_klass)
        field_name = index.get_content_field()
        params = {
            'fl': '*,score',
        }

        if start_offset is not None:
            params['start'] = start_offset

        if end_offset is not None:
            params['rows'] = end_offset

        narrow_queries = set()

        if limit_to_registered_models is None:
            limit_to_registered_models = getattr(settings, 'HAYSTACK_LIMIT_TO_REGISTERED_MODELS', True)

        if limit_to_registered_models:
            # Using narrow queries, limit the results to only models handled
            # with the current routers.
            if narrow_queries is None:
                narrow_queries = set()

            registered_models = self.build_models_list()

            if len(registered_models) > 0:
                narrow_queries.add('%s:(%s)' % (DJANGO_CT, ' OR '.join(registered_models)))

        if additional_query_string:
            narrow_queries.add(additional_query_string)

        if narrow_queries:
            params['fq'] = list(narrow_queries)

        query = "%s:%s" % (ID, get_identifier(model_instance))

        try:
            raw_results = self.conn.more_like_this(query, field_name, **params)
        except (IOError, SolrError), e:
            if not self.silently_fail:
                raise

            self.log.error("Failed to fetch More Like This from Solr for document '%s': %s", query, e)
            raw_results = EmptyResults()

        return self._process_results(raw_results, result_class=result_class)

    def _process_results(self, raw_results, highlight=False, result_class=None):
        from haystack import connections
        results = []
        hits = raw_results.hits
        facets = {}
        spelling_suggestion = None

        if result_class is None:
            result_class = SearchResult

        if hasattr(raw_results, 'facets'):
            facets = {
                'fields': raw_results.facets.get('facet_fields', {}),
                'dates': raw_results.facets.get('facet_dates', {}),
                'queries': raw_results.facets.get('facet_queries', {}),
            }

            for key in ['fields']:
                for facet_field in facets[key]:
                    # Convert to a two-tuple, as Solr's json format returns a list of
                    # pairs.
                    facets[key][facet_field] = zip(facets[key][facet_field][::2], facets[key][facet_field][1::2])

        if self.include_spelling is True:
            if hasattr(raw_results, 'spellcheck'):
                if len(raw_results.spellcheck.get('suggestions', [])):
                    # For some reason, it's an array of pairs. Pull off the
                    # collated result from the end.
                    spelling_suggestion = raw_results.spellcheck.get('suggestions')[-1]

        unified_index = connections[self.connection_alias].get_unified_index()
        indexed_models = unified_index.get_indexed_models()

        for raw_result in raw_results.docs:
            app_label, model_name = raw_result[DJANGO_CT].split('.')
            additional_fields = {}
            model = get_model(app_label, model_name)

            if model and model in indexed_models:
                for key, value in raw_result.items():
                    index = unified_index.get_index(model)
                    string_key = str(key)

                    if string_key in index.fields and hasattr(index.fields[string_key], 'convert'):
                        additional_fields[string_key] = index.fields[string_key].convert(value)
                    else:
                        additional_fields[string_key] = self.conn._to_python(value)

                del(additional_fields[DJANGO_CT])
                del(additional_fields[DJANGO_ID])
                del(additional_fields['score'])

                if raw_result[ID] in getattr(raw_results, 'highlighting', {}):
                    additional_fields['highlighted'] = raw_results.highlighting[raw_result[ID]]

                result = result_class(app_label, model_name, raw_result[DJANGO_ID], raw_result['score'], **additional_fields)
                results.append(result)
            else:
                hits -= 1

        return {
            'results': results,
            'hits': hits,
            'facets': facets,
            'spelling_suggestion': spelling_suggestion,
        }

    def build_schema(self, fields):
        content_field_name = ''
        schema_fields = []

        for field_name, field_class in fields.items():
            field_data = {
                'field_name': field_class.index_fieldname,
                'type': 'text',
                'indexed': 'true',
                'stored': 'true',
                'multi_valued': 'false',
            }

            if field_class.document is True:
                content_field_name = field_class.index_fieldname

            # DRL_FIXME: Perhaps move to something where, if none of these
            #            checks succeed, call a custom method on the form that
            #            returns, per-backend, the right type of storage?
            if field_class.field_type in ['date', 'datetime']:
                field_data['type'] = 'date'
            elif field_class.field_type == 'integer':
                field_data['type'] = 'slong'
            elif field_class.field_type == 'float':
                field_data['type'] = 'sfloat'
            elif field_class.field_type == 'boolean':
                field_data['type'] = 'boolean'
            elif field_class.field_type == 'ngram':
                field_data['type'] = 'ngram'
            elif field_class.field_type == 'edge_ngram':
                field_data['type'] = 'edge_ngram'

            if field_class.is_multivalued:
                field_data['multi_valued'] = 'true'

            if field_class.stored is False:
                field_data['stored'] = 'false'

            # Do this last to override `text` fields.
            if field_class.indexed is False:
                field_data['indexed'] = 'false'

                # If it's text and not being indexed, we probably don't want
                # to do the normal lowercase/tokenize/stemming/etc. dance.
                if field_data['type'] == 'text':
                    field_data['type'] = 'string'

            # If it's a ``FacetField``, make sure we don't postprocess it.
            if hasattr(field_class, 'facet_for'):
                # If it's text, it ought to be a string.
                if field_data['type'] == 'text':
                    field_data['type'] = 'string'

            schema_fields.append(field_data)

        return (content_field_name, schema_fields)


class ElasticSearchQuery(BaseSearchQuery):
    pass


class ElasticSearchEngine(BaseEngine):
    backend = ElasticSearchBackend
    query = ElasticSearchQuery
