from django.contrib import admin
from .models import Section, Content, Tag, ContentTag, UserProgress, SimpleUser, WhiteboardImage

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'created_at', 'updated_at']
    list_filter = ['name', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'content_type', 'is_active', 'order', 'created_at']
    list_filter = ['section', 'content_type', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'text_content']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('section', 'title', 'content_type', 'description', 'order', 'is_active')
        }),
        ('Content', {
            'fields': ('youtube_url', 'text_content', 'external_url'),
            'description': 'Fill in the appropriate field based on the content type selected above.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(ContentTag)
class ContentTagAdmin(admin.ModelAdmin):
    list_display = ['content', 'tag', 'created_at']
    list_filter = ['tag', 'created_at']
    search_fields = ['content__title', 'tag__name']
    readonly_fields = ['created_at']

@admin.register(SimpleUser)
class SimpleUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'last_login']
    list_filter = ['created_at', 'last_login']
    search_fields = ['name']
    readonly_fields = ['created_at', 'last_login', 'pin_hash']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'is_completed', 'is_favorited', 'updated_at']
    list_filter = ['is_completed', 'is_favorited', 'content__section', 'created_at']
    search_fields = ['user__name', 'content__title', 'notes']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(WhiteboardImage)
class WhiteboardImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['title', 'created_by__name']
    readonly_fields = ['created_at', 'image_data']
