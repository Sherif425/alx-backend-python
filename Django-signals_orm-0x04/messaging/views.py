from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')  # Or any post-delete page
