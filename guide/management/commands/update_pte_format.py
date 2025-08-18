from django.core.management.base import BaseCommand
from guide.models import Section, Content, Tag, ContentTag

class Command(BaseCommand):
    help = 'Update PTE Guide with new 2024 format and tasks'

    def handle(self, *args, **options):
        # Update section descriptions
        sections_data = [
            {
                'name': 'speaking',
                'title': 'Speaking',
                'description': 'Section 1 – Speaking (30–35 minutes) – Tests spoken English skills in academic contexts.'
            },
            {
                'name': 'writing',
                'title': 'Writing',
                'description': 'Section 2 – Writing (24–32 minutes) – Tests ability to write academically.'
            },
            {
                'name': 'reading',
                'title': 'Reading',
                'description': 'Section 3 – Reading (29–30 minutes) – Tests comprehension and interpretation of written text.'
            },
            {
                'name': 'listening',
                'title': 'Listening',
                'description': 'Section 4 – Listening (30–43 minutes) – Tests comprehension of spoken English.'
            }
        ]

        for section_data in sections_data:
            try:
                section = Section.objects.get(name=section_data['name'])
                section.description = section_data['description']
                section.save()
                self.stdout.write(f"Updated section: {section.title}")
            except Section.DoesNotExist:
                self.stdout.write(f"Section {section_data['name']} not found")

        # Add new content for updated tasks
        new_content = [
            # Speaking Section - Updated Tasks
            {
                'section_name': 'speaking',
                'title': 'Speaking Section Overview (2024 Format)',
                'content_type': 'text',
                'description': 'Complete overview of the updated Speaking section tasks',
                'text_content': '''PTE Speaking Section - New Format (30-35 minutes)

Tasks Include:

1. Personal Introduction (not scored)
   - 1 minute to prepare, 30 seconds to record
   - Introduce yourself to the admissions officer

2. Read Aloud (6-7 items)
   - 30-40 seconds to prepare, 35-40 seconds to record
   - Read the text aloud clearly and fluently

3. Repeat Sentence (10-12 items)
   - Listen and repeat exactly what you hear
   - 15 seconds to record

4. Describe Image (6-7 items)
   - 25 seconds to prepare, 40 seconds to record
   - Describe the image in detail

5. Re-tell Lecture (3-4 items)
   - 90 seconds audio, 40 seconds to record
   - Summarize the key points from the lecture

6. Answer Short Question (10-12 items)
   - Listen to the question and give a brief answer
   - 10 seconds to record

7. Summarize Group Discussion (NEW)
   - Listen to a group discussion
   - Summarize the main points and opinions

8. Respond to a Situation (NEW)
   - Listen to a situation description
   - Provide an appropriate response

Tips for Success:
- Speak clearly with natural rhythm
- Use proper intonation and stress
- Don't rush - maintain steady pace
- Practice pronunciation of difficult words
- Stay calm and confident'''
            },
            
            # Writing Section
            {
                'section_name': 'writing',
                'title': 'Writing Section Overview (2024 Format)',
                'content_type': 'text',
                'description': 'Complete overview of the Writing section tasks',
                'text_content': '''PTE Writing Section (24-32 minutes)

Tasks Include:

1. Summarize Written Text (2-3 items)
   - 10 minutes each
   - Read a passage and write a one-sentence summary
   - 5-75 words, must be grammatically correct

2. Essay (1-2 items)
   - 20 minutes each
   - Write a 200-300 word essay
   - Present a clear argument with examples

Key Skills Tested:
- Reading comprehension
- Writing fluency
- Grammar and vocabulary
- Critical thinking
- Time management

Essay Types:
- Argumentative essays
- Problem-solution essays
- Advantages/disadvantages essays
- Opinion essays

Success Strategies:
- Plan before writing (2-3 minutes)
- Use clear paragraph structure
- Include specific examples
- Check grammar and spelling
- Manage time effectively'''
            },
            
            # Reading Section
            {
                'section_name': 'reading',
                'title': 'Reading Section Overview (2024 Format)',
                'content_type': 'text',
                'description': 'Complete overview of the Reading section tasks',
                'text_content': '''PTE Reading Section (29-30 minutes)

Tasks Include:

1. Multiple-choice, Choose Single Answer (2-3 items)
   - Read text and select the best answer
   - Tests detailed comprehension

2. Multiple-choice, Choose Multiple Answers (2-3 items)
   - Select all correct answers
   - Partial credit scoring

3. Re-order Paragraphs (2-3 items)
   - Arrange paragraphs in logical order
   - Tests understanding of text structure

4. Reading: Fill in the Blanks (4-5 items)
   - Drag words to complete the text
   - Tests vocabulary and grammar

5. Reading & Writing: Fill in the Blanks (5-6 items)
   - Type the missing words
   - Tests both reading and writing skills

Key Skills:
- Reading comprehension
- Vocabulary knowledge
- Grammar understanding
- Logical reasoning
- Text organization

Time Management:
- Don't spend too long on one question
- Use skimming and scanning techniques
- Read questions before the passage
- Eliminate wrong answers systematically'''
            },
            
            # Listening Section
            {
                'section_name': 'listening',
                'title': 'Listening Section Overview (2024 Format)',
                'content_type': 'text',
                'description': 'Complete overview of the Listening section tasks',
                'text_content': '''PTE Listening Section (30-43 minutes)

Tasks Include:

1. Summarize Spoken Text (2-3 items)
   - Listen to audio (60-90 seconds)
   - Write 50-70 word summary
   - 10 minutes to complete

2. Multiple-choice, Choose Multiple Answers (2-3 items)
   - Select all correct answers
   - Listen for specific information

3. Fill in the Blanks (2-3 items)
   - Type missing words while listening
   - Tests listening and writing skills

4. Highlight Correct Summary (2-3 items)
   - Choose the best summary of the audio
   - Tests main idea comprehension

5. Multiple-choice, Choose Single Answer (2-3 items)
   - Select the best answer
   - Tests detailed understanding

6. Select Missing Word (2-3 items)
   - The audio cuts off, select the final word
   - Tests prediction skills

7. Highlight Incorrect Words (2-3 items)
   - Click on words that don't match audio
   - Tests detailed listening

8. Write from Dictation (3-4 items)
   - Type exactly what you hear
   - Tests listening and spelling

Listening Tips:
- Take notes while listening
- Focus on keywords and main ideas
- Don't panic if you miss something
- Practice with various accents
- Use context clues for unknown words'''
            }
        ]

        # Add the new content
        for content_data in new_content:
            try:
                section = Section.objects.get(name=content_data['section_name'])
                content, created = Content.objects.get_or_create(
                    section=section,
                    title=content_data['title'],
                    defaults={
                        'content_type': content_data['content_type'],
                        'description': content_data['description'],
                        'text_content': content_data['text_content'],
                        'order': 0  # Put these at the top
                    }
                )
                if created:
                    self.stdout.write(f"Created content: {content.title}")
                    
                    # Add tags
                    important_tag = Tag.objects.get(name='Important')
                    overview_tag, _ = Tag.objects.get_or_create(
                        name='Overview',
                        defaults={'color': '#6f42c1', 'description': 'Section overviews'}
                    )
                    updated_tag, _ = Tag.objects.get_or_create(
                        name='2024 Format',
                        defaults={'color': '#fd7e14', 'description': 'Updated 2024 PTE format'}
                    )
                    
                    for tag in [important_tag, overview_tag, updated_tag]:
                        ContentTag.objects.get_or_create(content=content, tag=tag)
                        
                else:
                    self.stdout.write(f"Content already exists: {content.title}")
            except Section.DoesNotExist:
                self.stdout.write(f"Section {content_data['section_name']} not found")

        self.stdout.write(self.style.SUCCESS('PTE format update complete!'))