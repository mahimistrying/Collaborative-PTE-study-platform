from django.core.management.base import BaseCommand
from guide.models import Tag

class Command(BaseCommand):
    help = 'Add tags for new PTE task types'

    def handle(self, *args, **options):
        new_tags = [
            # New Speaking Tasks
            {'name': 'Group Discussion', 'color': '#28a745', 'description': 'New speaking task - summarize group discussion'},
            {'name': 'Respond to Situation', 'color': '#17a2b8', 'description': 'New speaking task - respond appropriately to situations'},
            
            # Task-specific tags
            {'name': 'Personal Introduction', 'color': '#6f42c1', 'description': 'Speaking personal introduction'},
            {'name': 'Read Aloud', 'color': '#007bff', 'description': 'Reading aloud tasks'},
            {'name': 'Repeat Sentence', 'color': '#28a745', 'description': 'Sentence repetition tasks'},
            {'name': 'Describe Image', 'color': '#ffc107', 'description': 'Image description tasks'},
            {'name': 'Re-tell Lecture', 'color': '#dc3545', 'description': 'Lecture retelling tasks'},
            {'name': 'Answer Short Question', 'color': '#6c757d', 'description': 'Short answer questions'},
            
            # Writing tasks
            {'name': 'Summarize Written Text', 'color': '#fd7e14', 'description': 'Written text summarization'},
            {'name': 'Essay Writing', 'color': '#e83e8c', 'description': 'Essay writing tasks'},
            
            # Reading tasks
            {'name': 'Single Answer', 'color': '#20c997', 'description': 'Multiple choice single answer'},
            {'name': 'Multiple Answers', 'color': '#6f42c1', 'description': 'Multiple choice multiple answers'},
            {'name': 'Re-order Paragraphs', 'color': '#fd7e14', 'description': 'Paragraph reordering'},
            {'name': 'Reading Fill Blanks', 'color': '#dc3545', 'description': 'Reading fill in the blanks'},
            {'name': 'Reading & Writing Fill Blanks', 'color': '#ffc107', 'description': 'Combined reading and writing fill blanks'},
            
            # Listening tasks
            {'name': 'Summarize Spoken Text', 'color': '#007bff', 'description': 'Spoken text summarization'},
            {'name': 'Listening Fill Blanks', 'color': '#28a745', 'description': 'Listening fill in the blanks'},
            {'name': 'Highlight Correct Summary', 'color': '#17a2b8', 'description': 'Select correct summary'},
            {'name': 'Select Missing Word', 'color': '#6c757d', 'description': 'Choose the missing final word'},
            {'name': 'Highlight Incorrect Words', 'color': '#dc3545', 'description': 'Identify words that differ from audio'},
            {'name': 'Write from Dictation', 'color': '#e83e8c', 'description': 'Type exactly what you hear'},
            
            # Time-based tags
            {'name': '2024 Update', 'color': '#ff6b6b', 'description': 'Updated for 2024 PTE format'},
            {'name': 'New Task', 'color': '#4ecdc4', 'description': 'Newly added task type'},
        ]

        for tag_data in new_tags:
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

        self.stdout.write(self.style.SUCCESS('New task tags added successfully!'))