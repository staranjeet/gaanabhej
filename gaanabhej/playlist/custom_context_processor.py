from playlist.models import SuggestedSongs

def unseen_suggestions(request):
	unseen = SuggestedSongs.objects.filter(suggestedTo=request.user.id,isSeen=False).count()
	return {
		'unseen' : unseen,
	}
