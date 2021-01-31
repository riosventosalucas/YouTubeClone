# -*- coding: utf-8 -*-

# Python

# Django
from django.contrib.auth.decorators import login_required
from django.core                    import serializers
from django.db.models               import Count
from django.http                    import JsonResponse
from django.shortcuts               import render, redirect
from django.urls                    import reverse_lazy
from django.utils                   import timezone
from django.views.decorators.http   import require_http_methods
from django.views.generic           import ListView, DetailView, View

# Project
from .models                        import Video, Comment
from profiles.models                import History

class VideoListView(ListView):
    model         = Video
    template_name = "videos/list.html"
    paginate_by   =  10

class VideoPopularListView(ListView):
    model               = Video
    template_name       = "videos/popular.html"
    context_object_name = 'videos'

    def get_queryset(self):
        queryset = sorted(Video.objects.all()
            .order_by('-created_at')
            .exclude(created_at=None), 
                key=lambda popularity: popularity.calculate_popularity(), 
                reverse=True)[:5]
        if len(queryset) < 5:
            queryset = sorted(Video.objects.all()
                .order_by('-created_at'), 
                    key=lambda popularity: popularity.calculate_popularity(), 
                    reverse=True)[:5]            
        return queryset

class VideoDetailView(DetailView):
    model=Video
    template_name="videos/detail.html"
    query_set=Video.objects.all()
    slug_field="slug"
    slug_url_kwarg="slug"

    def get_context_data(self, **kwargs):
        ContextOfTheView=super().get_context_data(**kwargs)
        video=self.get_object()
        if self.request.user.is_authenticated:
            History.objects.create(
                user  = self.request.user,
                video = video
            )
        likes = Video.objects.filter(youtube_id=video.youtube_id).aggregate(dislikes_count=Count('dislikes'), likes_count=Count('likes'))
        ContextOfTheView["comments"]= Comment.objects.filter(video=video)
        ContextOfTheView["likes"]   = likes
        return ContextOfTheView



    def render_to_response(self, context, **response_kwargs):
        video       = self.get_object()
        video.views = video.views + 1
        video.save()
        
        return super().render_to_response(context, **response_kwargs)

@require_http_methods(["POST"])
def comment_video(request, youtube_id):
    user_logged = request.user
    video       = Video.objects.get(youtube_id=youtube_id)
    comment_req = request.POST.get("comment")
    
    comment     = Comment.objects.create(
        video   = video,
        user    = user_logged,
        comment = comment_req
    )

    return redirect(reverse_lazy("videos:detail", kwargs={"slug": video.slug}))

@require_http_methods(["POST"])
def like_video(request, youtube_id):
    if request.user.is_authenticated:
        user_logged=request.user
        video=Video.objects.filter(youtube_id=youtube_id).first()

        if not video:
            return JsonResponse({'error': 'invalid video id'}, status=400)

        if not user_logged in video.likes.all():

            video.likes.add(user_logged)
            video.dislikes.remove(user_logged)
            video.save()

            response={
                "status"   :  True,
                "response" : "Like saved"
            }
        else: 
            response = {
                "status"   :  False,
                "response" : "Already Liked"
            }
    else:
        response = {
                "status"   :  False,
                "response" : "Only user can like videos"
        }
    return JsonResponse(response)

@require_http_methods(["POST"])
def dislike_video(request, youtube_id):
    if request.user.is_authenticated:
        user_logged = request.user
        video       = Video.objects.filter(youtube_id=youtube_id).first()

        if not video:
            return JsonResponse({'error': 'invalid video id'}, status=400)    
        
        if not user_logged in video.dislikes.all():

            video.dislikes.add(user_logged)
            video.likes.remove(user_logged)
            video.save()

            response={
                "status"   :  True,
                "response" : "Dislike saved"
            }
        else: 
            response = {
                "status"   :  False,
                "response" : "Already Disliked"
            }
    else:
        response = {
                "status"   :  False,
                "response" : "Only user can dislike videos"
        }

    return JsonResponse(response)
