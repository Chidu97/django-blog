from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.

def post_list(request):
    all_post = Post.published.all()
    
    paginator = Paginator(all_post, 5)
    page = request.GET.get('page')


    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the last page of results
        posts = paginator.page(paginator.num_pages)



    data = {
        'posts':posts
    }

    return render (request, 'blog/post/list.html', data)







def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month, publish__day=day)

    #List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render (request, 'blog/post/detail.html', {'post':post,
      'comments':comments,
      'new_comment':new_comment,
      'comment_form':comment_form})



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')

    sent=False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        # Form was submitted
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments:{cd['comments']}"

            send_mail(subject, message, "Ralu from Astroverse <admin@admin.com>", [cd['recepient']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', 
                      {'post':post,
                      'form':form,
                      'sent':sent})

def create_post(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('content'):
            post=Post()
            post.title = request.POST.get('title')
            post.body = request.POST.get('content')
            post.person = request.POST.get('author_name')
            post.slug=post.title.lower().replace(" ","-")
            post.save()

            return redirect('blog:post_list')
        else:
            pass
    return render(request, 'create.html')


