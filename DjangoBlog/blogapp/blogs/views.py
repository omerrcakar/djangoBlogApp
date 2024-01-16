from django.shortcuts import render,redirect, get_object_or_404
from .models import Blog , Comment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator
from .forms import CommentForm

# Create your views here.

def blog_list(request):
    # date e gore tüm blogları listeliyoruz
    blogs = Blog.objects.all().order_by("date")
    return render(request,"blogs/blog_list.html",{"blogs":blogs})

def blog_detail(request,slug):
    #return HttpResponse(slug)
    blog = Blog.objects.get(slug=slug)

    comments = Comment.objects.filter(blog=blog)
    comment_form = CommentForm()

    # yeni eklenen
    # Sadece blogu oluşturan kullanıcı düzenleme ve silme işlemlerini gerçekleştirebilir
    if request.user == blog.author:
        can_edit = True
    else:
        can_edit = False

    return render(request,"blogs/blog_detail.html",{"blog":blog, "can_edit": can_edit, "comments":comments, "comment_form": comment_form})

@login_required(login_url="/accounts/login/")
def blog_create(request):

    if request.method == "POST":
        form = forms.CreateBlog(request.POST, request.FILES)
        if form.is_valid():
            #save blog to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()

            return redirect("blogs:list")
    else:

        form = forms.CreateBlog()
    return render(request, "blogs/blog_create.html",{"form":form})

# yeni eklenen
@login_required(login_url="/accounts/login/")
def blog_edit(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # Sadece blogu oluşturan kullanıcı düzenleme işlemi gerçekleştirebilir
    if request.user == blog.author:
        if request.method == "POST":
            form = forms.CreateBlog(request.POST, request.FILES, instance=blog)
            if form.is_valid():

                # Tarih alanını güncelliyoruz blogu düzenledikten sonra
                blog.date = timezone.now()
                form.save()
                # Blog düzenleme başarılı oldu, tüm blogların listelendiği sayfaya yönlendir
                return redirect("blogs:list")
        else:
            form = forms.CreateBlog(instance=blog)
        return render(request, "blogs/blog_edit.html", {"form": form, "blog": blog})
    else:
        return HttpResponse("Bu blogu düzenleme izniniz yok.")


@login_required(login_url="/accounts/login/")
def blog_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # Sadece blogu oluşturan kullanıcı silme işlemi gerçekleştirebilir
    if request.user == blog.author:
        if request.method == "POST":
            blog.delete()
            return redirect("blogs:list")
        return render(request, "blogs/blog_delete.html", {"blog": blog})
    else:
        return HttpResponse("You are not authorized to delete this blog.")
    

class BlogDetailView(View):
    template_name = 'blogs/blog_detail.html'

    def get(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        comment_form = CommentForm()
        return render(request, self.template_name, {'blog': blog, 'comment_form': comment_form})

    @method_decorator(login_required(login_url='/accounts/login/'))
    def post(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()

        return redirect('blogs:detail', slug=slug)
    
class CommentCreateView(View):
    template_name = 'blogs/blog_detail.html'  # ya da ayrı bir şablon belirleyebilirsiniz, aynı şablonu kullanmak istiyorsanız bu satırı geçebilirsiniz

    @method_decorator(login_required(login_url='/accounts/login/'))
    def post(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()

        return redirect('blogs:detail', slug=slug)