from django.urls import path

from documents.views import (AddDocumentView, DocumentInstanceView,
                             DocumentsView, delete_document)

app_name = 'documents'

urlpatterns = [
    path('', DocumentsView.as_view(), name='documents'),
    path('page/<int:page>', DocumentsView.as_view(), name='documents'),
    path('add_document/', AddDocumentView.as_view(), name='add_document'),
    path('<int:document_id>', DocumentInstanceView.as_view(), name='document'),
    path('delete_document/<int:document_id>', delete_document, name='delete_document'),
]
