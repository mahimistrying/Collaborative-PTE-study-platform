from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone
from .models import Section, Content, Tag, ContentTag, UserProgress, SimpleUser, WhiteboardImage
import json
import uuid

EDIT_PASSCODE = "pte2024"  # Change this to your desired passcode

def get_current_user(request):
    """Get the current logged-in SimpleUser or None"""
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return SimpleUser.objects.get(id=user_id)
        except SimpleUser.DoesNotExist:
            request.session.pop('user_id', None)
            request.session.pop('current_user', None)
    return None

def home(request):
    sections = Section.objects.all()
    search_query = request.GET.get('search', '')
    
    # Recent content
    recent_content = Content.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Search functionality
    if search_query:
        search_results = Content.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(text_content__icontains=search_query),
            is_active=True
        ).order_by('-created_at')[:10]
    else:
        search_results = None
    
    context = {
        'sections': sections,
        'recent_content': recent_content,
        'search_query': search_query,
        'search_results': search_results,
    }
    return render(request, 'guide/home.html', context)

def section_detail(request, section_name):
    section = get_object_or_404(Section, name=section_name)
    is_edit_mode = request.session.get('can_edit', False)
    current_user = get_current_user(request)
    
    # Get filter parameters
    content_type = request.GET.get('type', '')
    tag_filter = request.GET.get('tag', '')
    sort_by = request.GET.get('sort', 'order')
    show_completed = request.GET.get('completed', '')
    show_favorites = request.GET.get('favorites', '')
    
    # Base queryset
    contents = section.contents.filter(is_active=True)
    
    # Apply filters
    if content_type:
        contents = contents.filter(content_type=content_type)
    
    if tag_filter:
        contents = contents.filter(content_tags__tag__name=tag_filter)
    
    # Progress filters (only if user is logged in)
    if current_user and show_completed == 'true':
        completed_content_ids = UserProgress.objects.filter(
            user=current_user, 
            is_completed=True
        ).values_list('content_id', flat=True)
        contents = contents.filter(id__in=completed_content_ids)
    elif current_user and show_completed == 'false':
        completed_content_ids = UserProgress.objects.filter(
            user=current_user, 
            is_completed=True
        ).values_list('content_id', flat=True)
        contents = contents.exclude(id__in=completed_content_ids)
    
    if current_user and show_favorites == 'true':
        favorited_content_ids = UserProgress.objects.filter(
            user=current_user, 
            is_favorited=True
        ).values_list('content_id', flat=True)
        contents = contents.filter(id__in=favorited_content_ids)
    
    # Apply sorting
    if sort_by == 'title':
        contents = contents.order_by('title')
    elif sort_by == 'created':
        contents = contents.order_by('-created_at')
    elif sort_by == 'updated':
        contents = contents.order_by('-updated_at')
    else:  # default to order
        contents = contents.order_by('order', 'created_at')
    
    # Get available tags for this section
    available_tags = Tag.objects.filter(
        tagged_content__content__section=section
    ).distinct().order_by('name')
    
    # Get user progress for all content (only if logged in)
    user_progress = {}
    if current_user and contents:
        progress_data = UserProgress.objects.filter(
            user=current_user,
            content__in=contents
        )
        user_progress = {p.content_id: p for p in progress_data}
    
    context = {
        'section': section,
        'contents': contents,
        'is_edit_mode': is_edit_mode,
        'available_tags': available_tags,
        'user_progress': user_progress,
        'current_user': current_user,
        'filters': {
            'content_type': content_type,
            'tag_filter': tag_filter,
            'sort_by': sort_by,
            'show_completed': show_completed,
            'show_favorites': show_favorites,
        }
    }
    return render(request, 'guide/section_detail.html', context)

def authenticate_edit(request):
    if request.method == 'POST':
        passcode = request.POST.get('passcode')
        if passcode == EDIT_PASSCODE:
            request.session['can_edit'] = True
            messages.success(request, 'Authentication successful! You can now edit content.')
        else:
            messages.error(request, 'Invalid passcode.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def logout_edit(request):
    request.session.pop('can_edit', None)
    messages.info(request, 'Logged out of edit mode.')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def edit_content_simple(request, content_id=None):
    if not request.session.get('can_edit', False):
        messages.error(request, 'You need to authenticate first.')
        return redirect('home')
    
    if content_id:
        content = get_object_or_404(Content, id=content_id)
        action = 'Edit'
    else:
        content = None
        action = 'Add'
    
    if request.method == 'POST':
        section_id = request.POST.get('section')
        title = request.POST.get('title')
        content_type = request.POST.get('content_type')
        description = request.POST.get('description', '')
        youtube_url = request.POST.get('youtube_url', '').strip()
        text_content = request.POST.get('text_content', '')
        order = request.POST.get('order', 0)
        
        # Clean up empty URLs
        if not youtube_url:
            youtube_url = ''
        
        # Basic validation
        if not section_id or not title or not content_type:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'guide/edit_content_simple.html', {
                'content': content,
                'sections': Section.objects.all(),
                'action': action,
            })
        
        try:
            section = Section.objects.get(id=section_id)
            
            if content:
                # Update existing content
                content.section = section
                content.title = title
                content.content_type = content_type
                content.description = description
                content.youtube_url = youtube_url
                content.text_content = text_content
                content.order = int(order) if order else 0
                content.save()
                messages.success(request, f'Content "{title}" updated successfully.')
            else:
                # Create new content
                content = Content.objects.create(
                    section=section,
                    title=title,
                    content_type=content_type,
                    description=description,
                    youtube_url=youtube_url,
                    text_content=text_content,
                    order=int(order) if order else 0
                )
                messages.success(request, f'Content "{title}" added successfully.')
            
            return redirect('section_detail', section_name=section.name)
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    sections = Section.objects.all()
    context = {
        'content': content,
        'sections': sections,
        'action': action,
    }
    return render(request, 'guide/edit_content_simple.html', context)

def edit_content(request, content_id=None):
    if not request.session.get('can_edit', False):
        messages.error(request, 'You need to authenticate first.')
        return redirect('home')
    
    if content_id:
        content = get_object_or_404(Content, id=content_id)
        action = 'Edit'
    else:
        content = None
        action = 'Add'
    
    if request.method == 'POST':
        try:
            section_id = request.POST.get('section')
            title = request.POST.get('title')
            content_type = request.POST.get('content_type')
            description = request.POST.get('description', '')
            youtube_url = request.POST.get('youtube_url', '')
            text_content = request.POST.get('text_content', '')
            order = request.POST.get('order', 0)
            
            # Validation
            if not section_id:
                messages.error(request, 'Please select a section.')
                raise ValueError("Section is required")
            
            if not title:
                messages.error(request, 'Title is required.')
                raise ValueError("Title is required")
            
            if not content_type:
                messages.error(request, 'Please select a content type.')
                raise ValueError("Content type is required")
            
            section = get_object_or_404(Section, id=section_id)
            
            if content:
                # Update existing content
                content.section = section
                content.title = title
                content.content_type = content_type
                content.description = description
                content.youtube_url = youtube_url if youtube_url else ''
                content.text_content = text_content
                content.order = int(order) if order else 0
                content.save()
                messages.success(request, f'Content "{title}" updated successfully.')
            else:
                # Create new content
                content = Content.objects.create(
                    section=section,
                    title=title,
                    content_type=content_type,
                    description=description,
                    youtube_url=youtube_url if youtube_url else '',
                    text_content=text_content,
                    order=int(order) if order else 0
                )
                messages.success(request, f'Content "{title}" added successfully.')
            
            return redirect('section_detail', section_name=section.name)
            
        except ValueError as e:
            # Form validation errors - stay on the form page
            pass
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    sections = Section.objects.all()
    context = {
        'content': content,
        'sections': sections,
        'action': action,
    }
    return render(request, 'guide/edit_content.html', context)

def delete_content(request, content_id):
    if not request.session.get('can_edit', False):
        messages.error(request, 'You need to authenticate first.')
        return redirect('home')
    
    content = get_object_or_404(Content, id=content_id)
    section_name = content.section.name
    content.delete()
    messages.success(request, f'Content "{content.title}" deleted successfully.')
    return redirect('section_detail', section_name=section_name)

@csrf_exempt
def toggle_progress(request):
    """Toggle content completion status"""
    if request.method == 'POST':
        current_user = get_current_user(request)
        if not current_user:
            return JsonResponse({'success': False, 'error': 'Please login to track progress'})
        
        data = json.loads(request.body)
        content_id = data.get('content_id')
        action = data.get('action')  # 'complete', 'favorite'
        
        content = get_object_or_404(Content, id=content_id)
        
        progress, created = UserProgress.objects.get_or_create(
            user=current_user,
            content=content,
            defaults={'is_completed': False, 'is_favorited': False}
        )
        
        if action == 'complete':
            progress.is_completed = not progress.is_completed
            progress.completed_at = timezone.now() if progress.is_completed else None
        elif action == 'favorite':
            progress.is_favorited = not progress.is_favorited
            progress.favorited_at = timezone.now() if progress.is_favorited else None
        
        progress.save()
        
        return JsonResponse({
            'success': True,
            'is_completed': progress.is_completed,
            'is_favorited': progress.is_favorited
        })
    
    return JsonResponse({'success': False})

def search_content(request):
    """Search content across all sections"""
    query = request.GET.get('q', '')
    section_filter = request.GET.get('section', '')
    content_type_filter = request.GET.get('type', '')
    
    if not query:
        return render(request, 'guide/search.html', {'query': query})
    
    # Search in title, description, and text content
    results = Content.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(text_content__icontains=query),
        is_active=True
    )
    
    # Apply filters
    if section_filter:
        results = results.filter(section__name=section_filter)
    
    if content_type_filter:
        results = results.filter(content_type=content_type_filter)
    
    results = results.order_by('-created_at')
    
    # Get sections for filter dropdown
    sections = Section.objects.all()
    
    context = {
        'query': query,
        'results': results,
        'sections': sections,
        'section_filter': section_filter,
        'content_type_filter': content_type_filter,
    }
    return render(request, 'guide/search.html', context)

def favorites_view(request):
    """Show user's favorite content"""
    current_user = get_current_user(request)
    if not current_user:
        messages.info(request, 'Please login to view your favorites.')
        return redirect('user_login')
    
    favorites = UserProgress.objects.filter(
        user=current_user,
        is_favorited=True
    ).select_related('content', 'content__section').order_by('-favorited_at')
    
    context = {
        'favorites': favorites,
        'current_user': current_user,
    }
    return render(request, 'guide/favorites.html', context)

def progress_view(request):
    """Show user's progress across all sections"""
    current_user = get_current_user(request)
    if not current_user:
        messages.info(request, 'Please login to view your progress.')
        return redirect('user_login')
    
    # Get progress by section
    sections = Section.objects.all()
    progress_data = {}
    
    for section in sections:
        total_content = section.contents.filter(is_active=True).count()
        completed_content = UserProgress.objects.filter(
            user=current_user,
            content__section=section,
            is_completed=True
        ).count()
        
        progress_data[section.name] = {
            'section': section,
            'total': total_content,
            'completed': completed_content,
            'percentage': (completed_content / total_content * 100) if total_content > 0 else 0
        }
    
    # Recent completed content
    recent_completed = UserProgress.objects.filter(
        user=current_user,
        is_completed=True
    ).select_related('content', 'content__section').order_by('-completed_at')[:10]
    
    context = {
        'progress_data': progress_data,
        'recent_completed': recent_completed,
        'current_user': current_user,
    }
    return render(request, 'guide/progress.html', context)

def debug_edit(request):
    """Debug view to help diagnose edit issues"""
    if not request.session.get('can_edit', False):
        return JsonResponse({'error': 'Not authenticated'})
    
    if request.method == 'POST':
        data = {
            'post_data': dict(request.POST),
            'session_data': dict(request.session),
            'method': request.method,
            'content_type': request.content_type,
        }
        return JsonResponse(data)
    
    return JsonResponse({'message': 'Debug endpoint for edit issues'})

def user_login(request):
    """User login/registration view"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        pin = request.POST.get('pin', '').strip()
        action = request.POST.get('action')
        
        if not name or not pin:
            messages.error(request, 'Please enter both name and PIN.')
            return render(request, 'guide/login.html')
        
        if len(pin) < 4 or len(pin) > 6 or not pin.isdigit():
            messages.error(request, 'PIN must be 4-6 digits.')
            return render(request, 'guide/login.html')
        
        if action == 'login':
            user = SimpleUser.authenticate(name, pin)
            if user:
                request.session['user_id'] = user.id
                request.session['current_user'] = user.name
                user.save()  # Update last_login
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid name or PIN.')
        
        elif action == 'register':
            try:
                user = SimpleUser(name=name)
                user.set_pin(pin)
                user.save()
                request.session['user_id'] = user.id
                request.session['current_user'] = user.name
                messages.success(request, f'Account created successfully! Welcome, {user.name}!')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'This name and PIN combination already exists. Try logging in instead.')
    
    return render(request, 'guide/login.html')

def user_logout(request):
    """User logout view"""
    name = request.session.get('current_user', 'User')
    request.session.pop('user_id', None)
    request.session.pop('current_user', None)
    messages.info(request, f'Goodbye, {name}! Your progress has been saved.')
    return redirect('home')

def whiteboard(request):
    """Collaborative whiteboard view"""
    return render(request, 'guide/whiteboard.html')

def whiteboard_gallery(request):
    """View all saved whiteboards"""
    whiteboards = WhiteboardImage.objects.all()
    context = {
        'whiteboards': whiteboards,
    }
    return render(request, 'guide/whiteboard_gallery.html', context)

@csrf_exempt
def save_whiteboard(request):
    """Save whiteboard image to gallery"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', 'Untitled Whiteboard')
            image_data = data.get('image_data')
            
            if not image_data:
                return JsonResponse({'success': False, 'error': 'No image data provided'})
            
            # Get current user if logged in
            current_user = get_current_user(request)
            
            # Save whiteboard
            whiteboard = WhiteboardImage.objects.create(
                title=title,
                image_data=image_data,
                created_by=current_user
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Whiteboard saved successfully!',
                'whiteboard_id': whiteboard.id
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_whiteboard(request, whiteboard_id):
    """Delete a whiteboard"""
    if request.method == 'POST':
        try:
            whiteboard = get_object_or_404(WhiteboardImage, id=whiteboard_id)
            whiteboard.delete()
            return JsonResponse({'success': True, 'message': 'Whiteboard deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'ok',
        'message': 'PTE Guide is running!',
        'features': [
            'Interactive Whiteboard',
            'User Authentication', 
            'Progress Tracking',
            'Collaborative Study'
        ]
    })
