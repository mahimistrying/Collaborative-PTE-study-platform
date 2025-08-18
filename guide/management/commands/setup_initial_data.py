from django.core.management.base import BaseCommand
from guide.models import Section, Content

class Command(BaseCommand):
    help = 'Set up initial sections and sample content'

    def handle(self, *args, **options):
        sections_data = [
            {
                'name': 'speaking',
                'title': 'Speaking',
                'description': 'PTE Speaking section preparation materials including practice questions, tips, and video tutorials.'
            },
            {
                'name': 'writing',
                'title': 'Writing',
                'description': 'PTE Writing section resources with sample essays, templates, and writing strategies.'
            },
            {
                'name': 'reading',
                'title': 'Reading',
                'description': 'PTE Reading section materials including comprehension passages, question types, and techniques.'
            },
            {
                'name': 'listening',
                'title': 'Listening',
                'description': 'PTE Listening section practice with audio materials, note-taking tips, and response strategies.'
            }
        ]

        for section_data in sections_data:
            section, created = Section.objects.get_or_create(
                name=section_data['name'],
                defaults={
                    'title': section_data['title'],
                    'description': section_data['description']
                }
            )
            if created:
                self.stdout.write(f"Created section: {section.title}")
            else:
                self.stdout.write(f"Section already exists: {section.title}")

        sample_content = [
            {
                'section_name': 'speaking',
                'title': 'PTE Speaking Overview',
                'content_type': 'text',
                'description': 'Introduction to PTE Speaking section',
                'text_content': '''The PTE Speaking section tests your ability to understand and speak English in academic settings. 

Key components:
1. Personal Introduction (not scored)
2. Read Aloud
3. Repeat Sentence
4. Describe Image
5. Re-tell Lecture
6. Answer Short Question

Tips for success:
- Speak clearly and at a steady pace
- Use proper pronunciation and intonation
- Practice with a variety of topics
- Time management is crucial'''
            },
            {
                'section_name': 'writing',
                'title': 'Essay Writing Template',
                'content_type': 'note',
                'description': 'Standard template for PTE essays',
                'text_content': '''PTE Essay Writing Template:

Introduction (50-75 words):
- Hook sentence
- Background information
- Thesis statement

Body Paragraph 1 (75-100 words):
- Topic sentence
- Supporting details
- Examples
- Concluding sentence

Body Paragraph 2 (75-100 words):
- Topic sentence
- Supporting details
- Examples
- Concluding sentence

Conclusion (50-75 words):
- Restate thesis
- Summarize main points
- Final thought

Remember: Aim for 200-300 words total'''
            }
        ]

        for content_data in sample_content:
            try:
                section = Section.objects.get(name=content_data['section_name'])
                content, created = Content.objects.get_or_create(
                    section=section,
                    title=content_data['title'],
                    defaults={
                        'content_type': content_data['content_type'],
                        'description': content_data['description'],
                        'text_content': content_data['text_content']
                    }
                )
                if created:
                    self.stdout.write(f"Created content: {content.title}")
                else:
                    self.stdout.write(f"Content already exists: {content.title}")
            except Section.DoesNotExist:
                self.stdout.write(f"Section {content_data['section_name']} not found")

        self.stdout.write(self.style.SUCCESS('Initial data setup complete!'))