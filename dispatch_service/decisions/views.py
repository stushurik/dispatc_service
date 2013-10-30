from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from decisions.forms import DecisionForm

from decisions.models import Decision


class CreateDecisionView(CreateView):

    model = Decision
    template_name = 'events/edit_event.html'
    form_class = DecisionForm

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        return super(CreateDecisionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        user = request.user

        if user.has_perm('decisions.add_decision'):
            return super(CreateDecisionView, self).get(request, *args, **kwargs)
        else:
            #messages.add_message(request, messages.INFO, 'You can`t add event')
            return HttpResponseRedirect(reverse('home'))

    def get_initial(self):
        init = super(CreateDecisionView, self).get_initial()
        init['author'] = self.request.user.id
        init['event'] = self.pk
        return init

    def get_success_url(self):
        return reverse('events-list')

    def get_context_data(self, **kwargs):

        context = super(CreateDecisionView, self).get_context_data(**kwargs)
        context['action'] = reverse('decisions-new', kwargs={'pk': self.pk})

        return context
