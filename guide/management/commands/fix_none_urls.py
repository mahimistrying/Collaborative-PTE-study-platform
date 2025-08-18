from django.core.management.base import BaseCommand
from guide.models import Content

class Command(BaseCommand):
    help = 'Fix any "None" string values in URL fields'

    def handle(self, *args, **options):
        # Fix youtube_url fields
        youtube_fixed = Content.objects.filter(youtube_url='None').update(youtube_url=None)
        self.stdout.write(f"Fixed {youtube_fixed} youtube_url fields")
        
        # Fix external_url fields
        external_fixed = Content.objects.filter(external_url='None').update(external_url=None)
        self.stdout.write(f"Fixed {external_fixed} external_url fields")
        
        # Also check for 'null' string values
        youtube_null_fixed = Content.objects.filter(youtube_url='null').update(youtube_url=None)
        self.stdout.write(f"Fixed {youtube_null_fixed} youtube_url 'null' fields")
        
        external_null_fixed = Content.objects.filter(external_url='null').update(external_url=None)
        self.stdout.write(f"Fixed {external_null_fixed} external_url 'null' fields")
        
        self.stdout.write(self.style.SUCCESS('URL fields cleanup complete!'))