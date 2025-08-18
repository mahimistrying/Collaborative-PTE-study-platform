from django.core.management.base import BaseCommand
from guide.models import Tag

class Command(BaseCommand):
    help = 'Set up default tags for content organization'

    def handle(self, *args, **options):
        tags_data = [
            # Difficulty levels
            {'name': 'Beginner', 'color': '#28a745', 'description': 'Content suitable for beginners'},
            {'name': 'Intermediate', 'color': '#ffc107', 'description': 'Content for intermediate level'},
            {'name': 'Advanced', 'color': '#dc3545', 'description': 'Advanced level content'},
            
            # Content categories
            {'name': 'Tips', 'color': '#17a2b8', 'description': 'Tips and strategies'},
            {'name': 'Practice', 'color': '#6f42c1', 'description': 'Practice exercises'},
            {'name': 'Templates', 'color': '#fd7e14', 'description': 'Templates and formats'},
            {'name': 'Examples', 'color': '#20c997', 'description': 'Sample answers and examples'},
            {'name': 'Vocabulary', 'color': '#e83e8c', 'description': 'Vocabulary building'},
            {'name': 'Grammar', 'color': '#6c757d', 'description': 'Grammar rules and usage'},
            
            # Question types
            {'name': 'Multiple Choice', 'color': '#007bff', 'description': 'Multiple choice questions'},
            {'name': 'Fill Blanks', 'color': '#28a745', 'description': 'Fill in the blanks exercises'},
            {'name': 'Essay', 'color': '#dc3545', 'description': 'Essay writing'},
            {'name': 'Summary', 'color': '#ffc107', 'description': 'Summary tasks'},
            
            # Priority
            {'name': 'Important', 'color': '#ff6b6b', 'description': 'Important content to focus on'},
            {'name': 'Quick Review', 'color': '#4ecdc4', 'description': 'Quick review materials'},
        ]

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults={
                    'color': tag_data['color'],
                    'description': tag_data['description']
                }
            )
            if created:
                self.stdout.write(f"Created tag: {tag.name}")
            else:
                self.stdout.write(f"Tag already exists: {tag.name}")

        self.stdout.write(self.style.SUCCESS('Default tags setup complete!'))