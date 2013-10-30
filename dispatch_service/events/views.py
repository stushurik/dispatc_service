from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib import messages

from events.models import Event


class CreateEventView(CreateView):

    model = Event
    template_name = 'events/edit_event.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.has_perm('events.add_event'):
            return super(CreateEventView, self).get(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.INFO, 'You can`t add event')
            return HttpResponseRedirect(reverse('home'))

    def get_success_url(self):
        return reverse('events-list')

    def get_context_data(self, **kwargs):

        context = super(CreateEventView, self).get_context_data(**kwargs)
        context['action'] = reverse('events-new')

        return context


class ListEventView(ListView):

    model = Event
    template_name = 'events/event_list.html'
    paginate_by = 10
    queryset = Event.objects.all().order_by('-priority')


class ListUserEventView(ListEventView):

    def get_queryset(self):
        query = super(ListEventView, self).get_queryset()
        user = self.request.user
        return query.filter(executor=user)


class UpdateEventView(UpdateView):

    model = Event
    template_name = 'events/edit_event.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.has_perm('events.change_event'):
            return super(UpdateEventView, self).get(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.INFO, 'You can`t change event')
            return HttpResponseRedirect(reverse('home'))

    def get_success_url(self):
        return reverse('events-list')

    def get_context_data(self, **kwargs):

        context = super(UpdateEventView, self).get_context_data(**kwargs)
        context['action'] = reverse('events-edit',
                                    kwargs={'pk': self.get_object().id})

        return context