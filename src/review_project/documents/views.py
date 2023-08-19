from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import error
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, ListView, UpdateView

from common.view import TitleMixin
from documents.forms import ChangeDocForm, CreateDocForm
from documents.models import Document


class DocumentsView(TitleMixin, LoginRequiredMixin, ListView):
    template_name = 'documents/documents.html'
    title = 'CodeReview - Мои документы'
    model = Document
    context_object_name = 'documents'
    login_url = reverse_lazy('users:login')
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset(). \
            filter(owner=self.request.user). \
            exclude(status=Document.DELETED). \
            order_by('-updated')
        return queryset


class DocumentInstanceView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = Document
    template_name = 'documents/document_instance.html'
    pk_url_kwarg = 'document_id'
    context_object_name = 'document'
    form_class = ChangeDocForm
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy('documents:document', args=(self.kwargs['document_id'],))

    def get_object(self, queryset=None):
        instance = super().get_object(queryset=None)
        self.title = f'CodeReview - {instance.filename}'
        return instance

    def form_invalid(self, form):
        error(self.request, form.errors)
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user != Document.objects.get(pk=kwargs['document_id']).owner:
            return HttpResponseRedirect(reverse('documents:documents'))
        return super().get(request, *args, **kwargs)


class AddDocumentView(TitleMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Document
    form_class = CreateDocForm
    success_url = reverse_lazy('documents:documents')
    template_name = 'documents/add_document.html'
    login_url = reverse_lazy('users:login')
    title = 'CodeReview - Добавление нового файла'
    success_message = 'Ваш файл сохранен!'

    def form_invalid(self, form):
        error(self.request, form.errors)
        return HttpResponseRedirect(reverse('documents:add_document'))

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@login_required
def delete_document(request, document_id):
    instance = Document.objects.get(pk=document_id)
    if request.user == instance.owner:
        instance.status = Document.DELETED
        instance.updated = now()
        instance.save()
        messages.success(request, 'Файл удален!')
    return HttpResponseRedirect(reverse('documents:documents'))
