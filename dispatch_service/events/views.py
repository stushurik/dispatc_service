from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, UpdateView

from events.models import Event


class CreateEventView(CreateView):

    model = Event
    template_name = 'events/edit_event.html'

    def get_success_url(self):
        return reverse('events-list')

    def get_context_data(self, **kwargs):

        context = super(CreateEventView, self).get_context_data(**kwargs)
        context['action'] = reverse('events-new')

        return context


class ListEventView(ListView):

    model = Event
    template_name = 'events/event_list.html'


class UpdateEventView(UpdateView):

    model = Event
    template_name = 'events/edit_event.html'

    def get_success_url(self):
        return reverse('events-list')

    def get_context_data(self, **kwargs):

        context = super(UpdateEventView, self).get_context_data(**kwargs)
        context['action'] = reverse('events-edit',
                                    kwargs={'pk': self.get_object().id})

        return context