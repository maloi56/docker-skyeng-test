from django.contrib import admin

from documents.models import Codereview, Document


@admin.register(Document)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'file')
    readonly_fields = ('updated', 'status', 'filename',)


@admin.register(Codereview)
class Codereview(admin.ModelAdmin):
    list_display = ('id', 'document',)
    # readonly_fields = ('updated', 'status', 'filename', )
