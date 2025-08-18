from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import hashlib

class SimpleUser(models.Model):
    name = models.CharField(max_length=50, help_text="Your display name")
    pin_hash = models.CharField(max_length=64, help_text="Hashed PIN for security")
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['name', 'pin_hash']
    
    def __str__(self):
        return self.name
    
    def set_pin(self, pin):
        """Hash and set the PIN"""
        self.pin_hash = hashlib.sha256(f"{self.name}{pin}".encode()).hexdigest()
    
    def check_pin(self, pin):
        """Check if the provided PIN is correct"""
        return self.pin_hash == hashlib.sha256(f"{self.name}{pin}".encode()).hexdigest()
    
    @classmethod
    def authenticate(cls, name, pin):
        """Authenticate user with name and PIN"""
        try:
            user = cls.objects.get(name=name)
            if user.check_pin(pin):
                return user
        except cls.DoesNotExist:
            pass
        return None

class Section(models.Model):
    SECTION_CHOICES = [
        ('speaking', 'Speaking'),
        ('writing', 'Writing'),
        ('reading', 'Reading'),
        ('listening', 'Listening'),
        ('collaborative', 'Collaborative Study'),
    ]
    
    name = models.CharField(max_length=20, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('section_detail', kwargs={'section_name': self.name})

class Content(models.Model):
    CONTENT_TYPES = [
        ('video', 'YouTube Video'),
        ('note', 'Note'),
        ('text', 'Text Content'),
    ]
    
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    description = models.TextField(blank=True)
    
    # For YouTube videos
    youtube_url = models.TextField(blank=True, default='', help_text="YouTube video URL")
    
    # For notes and text content
    text_content = models.TextField(blank=True)
    
    # Common fields
    order = models.PositiveIntegerField(default=0, help_text="Order of display within section")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.section.title} - {self.title}"
    
    def get_youtube_embed_url(self):
        """Convert YouTube URL to embed format"""
        if self.youtube_url and 'youtube.com/watch?v=' in self.youtube_url:
            video_id = self.youtube_url.split('watch?v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif self.youtube_url and 'youtu.be/' in self.youtube_url:
            video_id = self.youtube_url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.youtube_url
    
    def get_tags(self):
        """Get all tags for this content"""
        return [ct.tag for ct in self.content_tags.all()]
    
    def get_difficulty_level(self):
        """Get difficulty level based on tags"""
        difficulty_tags = ['Beginner', 'Intermediate', 'Advanced']
        for tag in self.get_tags():
            if tag.name in difficulty_tags:
                return tag.name
        return None
    
    def is_completed_by_user(self, user):
        """Check if content is completed by user"""
        try:
            progress = self.user_progress.get(user=user)
            return progress.is_completed
        except UserProgress.DoesNotExist:
            return False
    
    def is_favorited_by_user(self, user):
        """Check if content is favorited by user"""
        try:
            progress = self.user_progress.get(user=user)
            return progress.is_favorited
        except UserProgress.DoesNotExist:
            return False

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ContentTag(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='content_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagged_content')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['content', 'tag']
    
    def __str__(self):
        return f"{self.content.title} - {self.tag.name}"

class UserProgress(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, related_name='progress')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    is_favorited = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    favorited_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="User's personal notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'content']
    
    def __str__(self):
        return f"{self.user.name} - {self.content.title}"

class WhiteboardImage(models.Model):
    title = models.CharField(max_length=200, default="Whiteboard Session")
    image_data = models.TextField(help_text="Base64 encoded image data")
    created_by = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, null=True, blank=True, related_name='whiteboards')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
