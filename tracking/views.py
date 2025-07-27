from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from .models import TimePlayed, TimeSession
from games.models import Game

@csrf_exempt
@login_required
def start_tracking(request, game_id):
    game = Game.objects.get(pk=game_id)
    session, created = TimeSession.objects.get_or_create(user=request.user, game=game)
    session.is_active = True
    session.save()
    return JsonResponse({'status': 'started'})

@require_POST
@login_required
def stop_tracking(request, game_id):
    try:
        data = json.loads(request.body)
        seconds = int(data.get("seconds", 0))

        if seconds <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid seconds'})

        game = Game.objects.get(pk=game_id)
        entry, _ = TimePlayed.objects.get_or_create(user=request.user, game=game)

        minutes = round(seconds / 60)
        entry.total_minutes += minutes
        entry.save()

        return JsonResponse({
            'success': True,
            'total_minutes': entry.total_minutes
        })

    except Game.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Game not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
