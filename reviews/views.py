from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from .models import Review
from .forms import ReviewForm
from games.models import Game
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs['pk'])
        if Review.objects.filter(user=request.user, game=self.game).exists():
            return redirect('game-detail', pk=self.game.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.game = self.game
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game-detail', kwargs={'pk': self.game.pk})

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_success_url(self):
        return reverse('games:game_detail', kwargs={'pk': self.object.game.pk})

    def test_func(self):
        return self.get_object().user == self.request.user

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('games:game_detail', pk=review.game.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/edit_review.html', {'form': form})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def get_success_url(self):
        return reverse('games:game_detail', kwargs={'pk': self.object.game.pk})

    def test_func(self):
        return self.get_object().user == self.request.user

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    game_pk = review.game.pk
    if request.method == 'POST':
        review.delete()
        return redirect('games:game_detail', pk=game_pk)
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})