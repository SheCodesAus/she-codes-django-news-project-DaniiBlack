from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import NewsStory
from .forms import StoryForm, CommentForm, SearchForm, FilterForm
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()
class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'all_stories'

    def get_queryset(self):
        '''Return all news stories.'''
        qs = NewsStory.objects.all()
        form = FilterForm(self.request.GET)
        order_by = "-pub_date"
        if form.is_valid():
            order = form.cleaned_data.get('order')
            if order == "oldfirst":
                order_by = "pub_date"


            if author := form.cleaned_data.get('author'):
                qs = qs.filter(author=author)

            if search := form.cleaned_data.get('search'):
                qs = qs.filter(Q(title__icontains=search) | Q(content__icontains=search))


        return qs.order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_stories'] = NewsStory.objects.all()[:4]
        context['author_list'] = User.objects.all()
        context['form'] = FilterForm(self.request.GET)
        return context

class StoryView(generic.DetailView):
    model = NewsStory
    template_name = 'news/story.html' # default: news/newsstory_detail.html
    context_object_name = 'story' # default: newsstory


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["form_action"] = reverse_lazy("news:addComment", kwargs={"pk": self.kwargs.get('pk')})
        return context

@login_required
def like_post(request, pk):
    story = get_object_or_404(NewsStory, pk=pk)
    user = request.user
    if story.liked_by.filter(id=user.id).exists():
        story.liked_by.remove(user)
    else:
        story.liked_by.add(user)
    return redirect('news:story', pk=story.id)

@login_required
def like(request, pk):
    news_story = get_object_or_404(NewsStory, pk=pk)
    if news_story.favourited_by.filter(username=request.user.username).exists():
        news_story.favourited_by.remove(request.user)
    else:
        news_story.favourited_by.add(request.user)
    return redirect(reverse_lazy('news:story', kwargs={'pk': pk}))

class AddStoryView(generic.CreateView):
    form_class = StoryForm
    context_object_name = 'storyForm'
    template_name = 'news/newsstory_form.html'
    success_url = reverse_lazy('news:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StoryEditView(LoginRequiredMixin, generic.UpdateView):
    model = NewsStory
    fields = ['title', 'pub_date', 'content']

    def get_success_url(self) -> str:
        return reverse_lazy('news:story', kwargs={"pk":self.kwargs['pk']})

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class StoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = NewsStory
    success_url = reverse_lazy('news:index')

    def get_queryset(self):
        """ filter to only allow delete of own stories """
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)
    

class AddCommentView(generic.CreateView):
    form_class = CommentForm
    template_name = "news/createComment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        pk = self.kwargs.get("pk")
        story = get_object_or_404(NewsStory, pk=pk)
        form.instance.story = story
        return super().form_valid(form)

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk")
        return reverse_lazy("news:story", kwargs={"pk":pk})