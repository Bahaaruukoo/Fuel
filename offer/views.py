from email import message
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import gas_offer, dailyUsage, log_table
from .forms import SearchForm, UpdateForm, PromoCodeForm
from datetime import date
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def updateView(request, pk):
    offer = get_object_or_404(gas_offer, pk=pk)
    if offer.status == False:
        message = "There is an error. Contact your admin"
        return render(request, 'echo.html', {'message':message})
    form = UpdateForm()
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
           filled_amount = form.cleaned_data['filled_amount']
           today = date.today()
           over = 0
           if dailyUsage.objects.filter(vehicle= offer, date=today).exists():
                usage = dailyUsage.objects.get(vehicle= offer, date=today)
                usage.used_amount = usage.used_amount + filled_amount
                usage.left_amount = usage.left_amount - filled_amount
                usage.user = request.user
                if usage.left_amount < 0:
                    over = usage.left_amount
           else:
                left = offer.permited_amount - filled_amount 
                usage = dailyUsage.objects.create(vehicle = offer, used_amount = filled_amount, left_amount = left, user = request.user)                       
                if left < 0:
                    over = left
           usage.save()         
           log = log_table.objects.create(user=request.user, vehicle = offer,gasstation=request.user.profile.gasstation, date=today, filled_amount= filled_amount, over_draw=over)
           log.save()
           return redirect('echo') #render(request, 'success.html', {'result':offer, 'usage':usage})
    return render(request, 'updateOffer.html', {'form':form})

def echo(request):
    message = "Successfully completed"
    return render(request, 'echo.html', {'message': message})

def searchView(request):
    message = "Not subsidy previlage"
    form1 = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            today = date.today()
            searchWord = form.cleaned_data['search']
            if gas_offer.objects.filter(plate_number=searchWord).exists():
                result = gas_offer.objects.get(plate_number=searchWord)
            else:
                return render(request, 'echo.html', {'message':message, 'form':form1})
            if result.status == True:
                if dailyUsage.objects.filter(vehicle = result, date = today).exists():
                    todaysBalance = dailyUsage.objects.get(vehicle = result, date = today)
                    return render(request, 'home.html', {'result':result, 'todaysBalance':todaysBalance})    
                else:                     
                    return render(request, 'home.html', {'result':result})    
        
    return render(request, 'home.html', {'form':form1})

@login_required
def addPromotion(request):    
    if request.user.is_staff or request.user.is_superuser:# or request.user == 'active':       
        form = PromoCodeForm(request.POST)
        if request.method == 'POST':            
            if form.is_valid():
                plate = form.cleaned_data['plate_number']
                permited = form.cleaned_data['permited_amount']
                status = form.cleaned_data['status']
                added = request.user
                cupon = gas_offer.objects.create(plate_number=plate, permited_amount = permited, status=status, added_by= added)
                cupon.save()
                message="Successfully added"
                return render(request, 'addPromotion.html', {'message':message, 'form':form})
        return render(request, 'addPromotion.html', {'form':form})
    else:
        form = PromoCodeForm()
        message="Account has no permission"
        return render(request, 'addPromotion.html', {'message':message,'form':form})

def getOverdraw_asStaff(request):
    today = date.today()
    overd = log_table.objects.filter(over_draw__lt = 0, date = today)
    return render(request, 'overdraw.html', {'overd':overd})
    
def getOverdraw_asManager(request):
    today = date.today()
    overd = log_table.objects.filter(over_draw__lt = 0, date = today, gasstation = request.user.profile.gasstation)
    return render(request, 'overdraw.html', {'overd':overd})
    