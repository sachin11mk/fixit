from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.forms import  SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out

def home(request):
    template = loader.get_template("base.html")
    context = RequestContext( request, {})
    return HttpResponse(template.render(context))


def admin_login(request):
    template = loader.get_template("base.html")
    context = RequestContext( request, {})
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            user = authenticate( username=form.get_user(), \
                    password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user )
            return render_to_response( template_name, {
                'form' : form,
            },context_instance=context )
        else:
            print form.errors
            error_msg = "Invalid Registration no / Password."
            messages.add_message(request, messages.ERROR, error_msg)
            pass
    return HttpResponseRedirect( reverse("list_task"),)

def admin_logout(request):
    template = loader.get_template("base.html")
    context = RequestContext( request, {})
    username = request.user
    success_msg = '%s, You have successfully logged out.'%username
    messages.add_message(request, messages.SUCCESS, success_msg)
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    return HttpResponseRedirect( reverse("list_task"),)

