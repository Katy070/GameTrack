from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from reviews.models import Review
from .models import Developer, Genre, Platform, GameStatus
from .models import Game
from reviews.forms import ReviewForm
from .forms import GameForm, GameStatusForm
from tracking.models import TimePlayed


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    paginate_by = 6

    def get_queryset(self):
        queryset = Game.objects.all().order_by('-release_date')
        q = self.request.GET.get('q')
        genre = self.request.GET.get('genre')
        platform = self.request.GET.get('platform')
        developer = self.request.GET.get('developer')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(genre__name__icontains=q) |
                Q(platform__name__icontains=q) |
                Q(developer__name__icontains=q)
            ).distinct()

        if genre:
            queryset = queryset.filter(genre__id=genre)

        if platform:
            queryset = queryset.filter(platform__id=platform)

        if developer:
            queryset = queryset.filter(developer__id=developer)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['platforms'] = Platform.objects.all()
        context['developers'] = Developer.objects.all()
        return context

@method_decorator(login_required, name='post')
class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object

        context['form'] = ReviewForm()
        context['reviews'] = game.reviews.all()

        if self.request.user.is_authenticated:
            user_game_status, _ = GameStatus.objects.get_or_create(user=self.request.user, game=game)
            context['status_form'] = GameStatusForm(instance=user_game_status)
            context['user_game_status'] = user_game_status
        else:
            context['status_form'] = None
            context['user_game_status'] = None

        if self.request.user.is_authenticated:
            try:
                time_played = TimePlayed.objects.get(user=self.request.user, game=game)
                context['user_time_played'] = time_played.total_hours()
            except TimePlayed.DoesNotExist:
                context['user_time_played'] = 0
        else:
            context['user_time_played'] = None

        context['all_time_played'] = TimePlayed.objects.filter(game=game).select_related('user')

        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        game = self.object

        form = ReviewForm(request.POST)
        status_form = GameStatusForm(request.POST)

        if 'status_submit' in request.POST:
            user_game_status, created = GameStatus.objects.get_or_create(user=request.user, game=game)
            status_form = GameStatusForm(request.POST, instance=user_game_status)

            if status_form.is_valid():
                status_form.save()
                messages.success(request, "Game status updated!")
                return redirect('games:game_detail', pk=game.pk)
            else:
                messages.error(request, "Failed to update game status.")

        if form.is_valid():
            if Review.objects.filter(game=game, user=request.user).exists():
                messages.error(request, "You've already reviewed this game.")
            else:
                review = form.save(commit=False)
                review.game = game
                review.user = request.user
                review.save()
                messages.success(request, "Your review has been posted!")
            return redirect('games:game_detail', pk=game.pk)

        context = self.get_context_data(form=form, status_form=status_form)
        return self.render_to_response(context)

def game_list(request):
    games = Game.objects.all().order_by('-release_date')  # Latest first
    return render(request, 'games/game_list.html', {'games': games})


@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.added_by = request.user
            game.save()
            form.save_m2m()  # Needed for ManyToMany fields!
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm()
    return render(request, 'games/add_game.html', {'form': form})


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('games:game_list')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid:")
        print(form.errors)
        return super().form_invalid(form)


class GameUpdateView(UpdateView):
    model = Game
    fields = ['title', 'description', 'release_date']  # Add more if needed
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('games:game_list')


class GameDeleteView(DeleteView):
    model = Game
    template_name = 'games/game_confirm_delete.html'
    success_url = reverse_lazy('games:game_list')


@login_required
def toggle_favorite(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    profile = request.user.profile

    if game in profile.favorite_games.all():
        profile.favorite_games.remove(game)
    else:
        profile.favorite_games.add(game)

    return redirect('game_detail', pk=game.id)