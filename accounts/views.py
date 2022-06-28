from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UpdateUser, UpdateProfile, UpdateMyCachier,EditProfile
from django.contrib.auth.decorators import login_required
from .models import Profile


@login_required
def register(request):    
    if request.user.profile.role == 'manager':
        id = request.user.id
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            #form_p = CashierRegisterForm(request.POST)
            gasst = request.user.profile.gasstation

            if form.is_valid():# and form_p.is_valid():
                new_user = form.save()
       
                Profile.objects.create(user=new_user,
                    manager_id= id, #form.cleaned_data['manager_id'],
                    gasstation = gasst, #gasstaion_id, #form.cleaned_data['hotel_id'],
                    role = 'cashier', #role, #form.cleaned_data['role'],
                )                
                return redirect('search')
        else:
            form = UserRegisterForm()
            #form_p = CashierRegisterForm()
            
        return render(request, 'accounts/register.html', {'form':form })
        
@login_required
def profileEditor(request, id):
    p = Profile.objects.get(id = id)
    '''manager_p = request.user.profile
    if p.hotel != manager_p.hotel:
        if manager_p.role != 'manager':
            return redirect('dashboard')
     '''       
    if request.method == 'POST':
            u_form = UpdateMyCachier( request.POST, instance = p.user)
            p_form = UpdateProfile( request.POST, request.FILES, instance = p)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                return redirect('profile')
    else:
        u_form = UpdateMyCachier(instance = p.user)
        p_form = UpdateProfile(instance = p)

    form = {'u_form': u_form, 'p_form':p_form }
    return render(request, 'accounts/profile.html', form)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UpdateUser( request.POST, instance = request.user)
        p_form = UpdateProfile( request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            return redirect('profile')
    else:
        u_form = UpdateUser(instance = request.user)
        p_form = UpdateProfile(instance = request.user.profile)

    form = {'u_form': u_form, 'p_form':p_form }
    return render(request, 'accounts/profile.html', form)

@login_required
def agentList(request):
    agents = Profile.objects.filter(manager_id = request.user.id)
    return render(request, 'accounts/agentList.html', {'agents':agents})

@login_required
def addManager(request):    
    form = UserRegisterForm()
    form_p = EditProfile()
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            form_p = EditProfile(request.POST)

            if form.is_valid() and form_p.is_valid():# and form_p.is_valid():
                new_user = form.save()
                gasst = form_p.cleaned_data['gasstation']

                Profile.objects.create(user=new_user,
                    gasstation = gasst, #gasstaion_id, #form.cleaned_data['hotel_id'],
                    role = 'manager', #role, #form.cleaned_data['role'],
                )                
                message = "Account successfully created"
                return render(request, 'accounts/echo.html', {'message':message,'form':form ,'form_p':form_p })
            else:
                message = "Account creation failed"
                return render(request, 'accounts/echo.html', {'message':message,'form':form ,'form_p':form_p })
        else:    
            return render(request, 'accounts/addManager.html', {'form':form ,'form_p':form_p })
    else:
        message = "Account has no permission"
        return render(request, 'accounts/addManager.html', {'message':message,'form':form ,'form_p':form_p })


@login_required   
def addAuditorFinance(request, act):   
    form = UserRegisterForm()
    #form_p = EditProfile()
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            #form_p = EditProfile(request.POST)

            if form.is_valid(): 
                new_user = form.save()

                Profile.objects.create(user=new_user,
                    role = act 
                )                
                message = "Account successfully created"
                return render(request, 'accounts/echo.html', {'message':message,'form':form })
            else:
                message = "Account creation failed"
                return render(request, 'accounts/echo.html', {'message':message,'form':form })
        else:    
            return render(request, 'accounts/addManager.html', {'form':form  })
    else:
        message = "Account has no permission"
        return render(request, 'accounts/addManager.html', {'message':message,'form':form  })


@login_required   
def addAgent(request):   
    form = UserRegisterForm()
    #form_p = EditProfile()
    if request.user.profile.role == 'manager': #or request.user.is_superuser:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            #form_p = EditProfile(request.POST)

            if form.is_valid(): # and form_p.is_valid():# and form_p.is_valid():
                new_user = form.save()
                #gasst = form_p.cleaned_data['gasstation']

                Profile.objects.create(user=new_user,
                    gasstation = request.user.profile.gasstation, # gasst, #gasstaion_id, #form.cleaned_data['hotel_id'],
                    role = 'cashier', #role, #form.cleaned_data['role'],
                    manager_id = request.user.id
                )                
                message = "Account successfully created"
                return render(request, 'accounts/echo.html', {'message':message,'form':form })
            else:
                message = "Account creation failed"
                return render(request, 'accounts/echo.html', {'message':message,'form':form })
        else:    
            return render(request, 'accounts/addManager.html', {'form':form  })
    else:
        message = "Account has no permission"
        return render(request, 'accounts/addManager.html', {'message':message,'form':form  })
