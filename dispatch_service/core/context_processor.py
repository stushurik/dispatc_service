def events_count_context_processor(request):
    user = request.user
    if user.is_authenticated():
        events_count = user.executors_set.filter(decision=None).count()
        return {'events_count': events_count}
    return {'events_count': None}