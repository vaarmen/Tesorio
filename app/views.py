# Create your views here.
from django.views.generic import TemplateView

class BaseView(TemplateView):
    def render(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        return context

class IndexView(BaseView):
    template_name = "index.jinja"

    def get(self, request, *args, **kwargs):
        return self.render()

# class IndexView(TemplateView):
#     template_name = "index.jinja"

#     def get(self, request, *args, **kwargs):
#         return self.render_to_response(self.get_context_data(lol="what is this"))

#     def get_context_data(self, **kwargs):

#         context = super(IndexView, self).get_context_data(**kwargs)
#         # context['first_names'] = ['Nathan', 'Richard']

#         return context


# class SearchPageView(FormView):
#     template_name = 'search/search.html'

#     def get(self, request, *args, **kwargs):
#         self.bookmarks = []
#         self.show_results = False
#         form = SearchForm(self.request.GET or None)
#         if form.is_valid():
#             self.show_results = True
#             self.bookmarks = Bookmark.objects.filter(title__icontains=form.cleaned_data['query'])[:10]

#         return self.render_to_response(self.get_context_data(form=form))


#     def get_context_data(self, **kwargs):
#         context = super(SearchPageView, self).get_context_data(**kwargs)
#         context.update({
#             'show_tags': True,
#             'show_user': True,
#             'show_results': self.show_results,
#             'bookmarks': self.bookmarks
#         })
#         return context