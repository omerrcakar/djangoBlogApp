from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserProfileForm
from .models import UserProfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            # Eğer UserProfile nesnesi yoksa, oluştur
            user_profile = UserProfile.objects.create(user=request.user)
        
        form = UserProfileForm(instance=user_profile)
        friends = user_profile.friends.all()
        return render(request, self.template_name, {'form': form, 'friends': friends})


    def post(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()

            # Kullanıcı adını güncelleniyor ( first name e ne yazarsak kullancıı adı o olucak)
            new_username = form.cleaned_data['first_name']
            request.user.username = new_username
            request.user.save()

            # UserProfile nesnesini güncelleme
            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.email = form.cleaned_data['email']
            user_profile.save()
            return redirect('blogs:list')

            

        return render(request, self.template_name, {'form': form})

# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request,user)
            return redirect("blogs:list")
    else:

    
        form = UserCreationForm()
    return render(request,"accounts/signup.html",{"form":form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in the user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get("next"))
            else:

                return redirect("blogs:list")
    
    else:
        form = AuthenticationForm()
    return render(request,"accounts/login.html",{"form":form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("blogs:list")
        
@login_required(login_url="/accounts/login/")
def add_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)

    if request.user.id != friend_id:
        user_profile = request.user.userprofile
        user_profile.friends.add(friend.userprofile)
        user_profile.save()

    return JsonResponse({'status': 'OK'})