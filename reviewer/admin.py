from django.contrib import admin
from .models import CodeReview

@admin.register(CodeReview)
class CodeReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'score', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('original_code', 'summary', 'fixed_code')
    readonly_fields = ('created_at',)
