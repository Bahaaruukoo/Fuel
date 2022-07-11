from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from accounts.models import Profile
from .models import Audited, Gas_offer, DailyUsage, Gasstation, log_table, Fuel, Compensation
from .forms import AuditForm, SearchForm, UpdateForm, PromoCodeForm, PaymentForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic import CreateView
from django.conf import settings

# Create your views here.
@login_required
def updateView(request, pk, fuel_typ):
    #if request.user.is_staff or request.user.is_superuser:
    if request.user.is_superuser:
        message = "You have no previlage"
        emoji = "9940"#"128532"
        return render(request, 'echo.html', {'message':message, 'emoji':emoji})
        
    if request.user.profile.role !='cashier' and request.user.profile.role !='manager':
        message = "You have no previlage"
        emoji = "9940"#"128532"
        return render(request, 'echo.html', {'message':message, 'emoji':emoji})
        
    offer = get_object_or_404(Gas_offer, pk=pk)
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
           if DailyUsage.objects.filter(vehicle= offer, date=today).exists():
                usage = DailyUsage.objects.get(vehicle= offer, date=today)
                usage.used_amount = usage.used_amount + filled_amount
                if usage.left_amount < 0:
                    over = -filled_amount
                usage.left_amount = usage.left_amount - filled_amount
                usage.user = request.user
                if usage.left_amount < 0 and over == 0:
                    over = usage.left_amount
           else:
                left = offer.permited_amount - filled_amount 
                usage = DailyUsage.objects.create(vehicle = offer, used_amount = filled_amount, left_amount = left, user = request.user)                       
                if left < 0:
                    over = left
           usage.save()         
           fl = Fuel.objects.get(id = fuel_typ)
           log = log_table.objects.create(user=request.user, vehicle = offer, fuel = fl, gasstation=request.user.profile.gasstation, date=today, filled_amount= filled_amount, over_draw=over)
           log.save()
           price = filled_amount * fl.price
           discount = filled_amount * fl.subsidy_amount
           final =  price - discount
           
           if 'ctx' in request.session:
                del request.session['ctx']
           ctx = { 'price':str(price) , 'discount': str(discount), 'final': str(final)         
           }
           request.session['ctx'] = ctx

           return redirect('updateSucceed') #render(request, 'success.html', {'result':offer, 'usage':usage})
    return render(request, 'updateOffer.html', {'form':form})
def updateSucceed(request):
    message = "Successfully Updated"
    return render(request, 'success.html', {'message': message})

def echo(request):
    message = "Successfully Completed"    
    emoji = '9989'
    return render(request, 'echo.html', {'message': message})

def searchView(request):

    message = "Not subsidy previlaged"
    form1 = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            today = date.today()
            searchWord = form.cleaned_data['search']
            if Gas_offer.objects.filter(plate_number=searchWord).exists():
                result = Gas_offer.objects.get(plate_number=searchWord)
            else:
                return render(request, 'noDiscount.html', {'message':message, 'emoji':'128532'})
            if result.status == True:
                if DailyUsage.objects.filter(vehicle = result, date = today).exists():
                    todaysBalance = DailyUsage.objects.get(vehicle = result, date = today)
                    return render(request, 'home.html', {'result':result, 'used':todaysBalance.used_amount, 'left':todaysBalance.left_amount})    
                else:                     
                    return render(request, 'home.html', {'result':result, 'used':0, 'left':result.permited_amount})    
        print(settings.PATH_DIRS)
    return render(request, 'home.html', {'form':form1})

@login_required
def addPromotion(request):    
    if request.user.is_staff or request.user.is_superuser:# or request.user == 'active':       
        form = PromoCodeForm(request.POST)
        if request.method == 'POST':            
            if form.is_valid():
                plate = form.cleaned_data['plate_number']
                permited = form.cleaned_data['permited_amount']
                fuel = form.cleaned_data['fuel']   
                status = form.cleaned_data['status']                
                added = request.user
                cupon = Gas_offer.objects.create(plate_number=plate, permited_amount = permited, fuel= fuel, status=status, added_by= added)
                cupon.save()
                message="Successfully added"
                form = PromoCodeForm()
                return render(request, 'addPromotion.html', {'message':message, 'form':form})
        return render(request, 'addPromotion.html', {'form':form})
    else:
        form = PromoCodeForm()
        message="Account has no permission"
        return render(request, 'addPromotion.html', {'message':message,'form':form})
 
def getOverdraw_asManager(request, id):
    today = date.today()
    cashier = Profile.objects.get(id=id)
    overd = log_table.objects.filter(user = cashier.user, over_draw__lt = 0, date = today, gasstation = request.user.profile.gasstation)
    return render(request, 'overdraw.html', {'overd':overd})

def dailyBalanceWork(request, id):   
    net_ben =0
    net_pet = 0 
    today = date.today()
    cashier = Profile.objects.get(id=id)
    todaySalesVolume = log_table.objects.filter(user=cashier.user, date=today, dailyBalanceDone = 0)
    benz =todaySalesVolume.filter(fuel=1).aggregate(Total=Sum('filled_amount'), Loss=Sum('over_draw'))
    petr =todaySalesVolume.filter(fuel=2).aggregate(Total=Sum('filled_amount'), Loss=Sum('over_draw'))
    
    if benz['Total'] is not None:
        net_ben = benz['Total'] 
        if benz['Loss'] is not None:
            net_ben = net_ben + benz['Loss']
    
    if petr['Total'] is not None:
        net_pet =petr['Total']
        if petr['Loss'] is not None:
            net_pet = net_pet + petr['Loss']
    return render(request, 'balance.html', {'id':id,'cashier':cashier, 'net_ben':net_ben,'net_pet':net_pet, 'today':today, 'benz':benz, 'petr':petr, 'result':todaySalesVolume})

def approve(request, id):
    today = date.today()
    cashier = Profile.objects.get(id=id)
    todaySalesVolume = log_table.objects.filter(user=cashier.user, date=today, dailyBalanceDone = False).update(dailyBalanceDone=1)#.aggregate(Total=Sum('filled_amount'), Loss=Sum('over_draw'))
    message = "Approved "# + str(todaySalesVolume.Total) + " - " + str(todaySalesVolume.Loss)
    return render(request, 'echo.html', {'message':message, 'todaySalesVolume':todaySalesVolume })

def getOverdraw_asAuditor(request):
    today = date.today()
    overd = log_table.objects.filter(over_draw__lt = 0, date = today)
    return render(request, 'overdraw.html', {'overd':overd})
   
def unaudited(request):
    form = AuditForm()
    if request.method == 'POST':
        form = AuditForm(request.POST)
        if form.is_valid():
            gas_station = form.cleaned_data['gasstation']
            startD = form.cleaned_data['start_date']
            endD = form.cleaned_data['end_date']
            unaudited_result = log_table.objects.filter(gasstation = gas_station, date__gte= startD, date__lte=endD, audited__isnull = True)#.values('vehicle', 'gasstation', 'date', 'filled_amount', 'over_draw', 'fuel')
            ben_totalfill = unaudited_result.filter(fuel =1).aggregate(Total=Sum('filled_amount'), Loss=Sum('over_draw'))
            pet_totalfill = unaudited_result.filter(fuel =2).aggregate(Total=Sum('filled_amount'), Loss=Sum('over_draw'))
            #ben_totalfill = log_table.objects.filter(gasstation = gas_station, date__gte= startD, date__lte=endD, audited__isnull = True, fuel = 1).aggregate(Total=Sum('filled_amount'), Loss=Sum('over_draw'))
            #pet_totalfill = log_table.objects.filter(gasstation = gas_station, date__gte= startD, date__lte=endD, audited__isnull = True, fuel = 2).aggregate(Total=Sum('filled_amount'), Loss=Sum('over_draw'))
            
            ben_final = 0
            if ben_totalfill['Total'] != None:
                ben_final = ben_totalfill['Total']
            if ben_totalfill['Loss'] != None:
                if ben_totalfill['Loss'] < 0:
                    ben_final = ben_final + ben_totalfill['Loss']

            pet_final = 0
            if pet_totalfill['Total'] != None:
                pet_final = pet_totalfill['Total']
            if pet_totalfill['Loss'] != None:
                if pet_totalfill['Loss'] < 0:
                    pet_final = pet_final + pet_totalfill['Loss']

            return render(request, 'audit2.html', { 'pet_final':pet_final,'pet_totalfill':pet_totalfill, 'ben_final':ben_final,'ben_totalfill':ben_totalfill, 'startD':startD,'endD':endD,'gasstation': gas_station, 'result':unaudited_result})
    #todaysSale = log_table.objects.filter(compsated = False, date = today)
    return render(request, 'audit.html', {'form':form})

def approveAudit(request ,pk, start_date, end_date):
    ##return render(request, 'echo.html', {'message':'Coming soon'})

    today = date.today()
    gasst_id = pk #request.get('pk')
    startD = start_date #request.get('start_date')
    endD = end_date #request.get('end_date')    
    ben_compensation = 0
    pet_compensation = 0
    fuelData = Fuel.objects.all()
    for data in fuelData:
        if data.fuel_type == 'benzene':
            ben_compensation = data.subsidy_amount
        elif data.fuel_type == 'petrol':
            pet_compensation = data.subsidy_amount

    gas_station = Gasstation.objects.get(id = gasst_id)
    unaudited_result = log_table.objects.filter(gasstation = gas_station, date__gte= startD, date__lte=endD, audited__isnull = True)
    compensated_ben = 0
    compensated_pet = 0
    for result in unaudited_result:
        if result.fuel.fuel_type == 'benzene':
            compensated_ben +=  result.filled_amount + result.over_draw     
        elif result.fuel.fuel_type == 'petrol':
            compensated_pet +=  result.filled_amount + result.over_draw
    compensated_fuel = compensated_ben + compensated_pet
    money_for_ben = compensated_ben * ben_compensation
    money_for_pet = compensated_pet * pet_compensation
    money_compansated = money_for_ben + money_for_pet

    audit = Audited.objects.create(user=request.user, date=today, 
    compensated_benzen= compensated_ben, money_for_benzene= money_for_ben,
    compensated_petrol= compensated_pet, money_for_petrol= money_for_pet, 
    total_compensated_fuel= compensated_fuel, total_money_compansated=money_compansated, 
    audit_date_from= startD, audit_date_to =endD, gasstation=gas_station)

    unaudited_result.update(audited= audit)
    message = "Records Audited"
    return render(request, 'echo.html', {'message':message, 'result':unaudited_result})
    
def paymentRequests(request):
    result = Audited.objects.filter(compansating_agent__isnull = True)
    return render(request, 'payments.html', {'result':result})
    
def paymentDetail(request, id):    
    form = PaymentForm()
    result = Audited.objects.filter(id = id)
    myObj = result.first()
    if request.method == 'POST':
        today = date.today()
        form = PaymentForm(request.POST)
        if form.is_valid():            
            money_reciever = form.cleaned_data['money_reciever']
            result.update(money_reciever = money_reciever, compensated_date = today, compansating_agent = request.user)
            
            Compn = Compensation.objects.create(
               financer = request.user,
               total_money = myObj.total_money_compansated,
               audit = myObj,
               gasstation = myObj.gasstation
            )
            Compn.save()
            if 'ctx' in request.session:
                del request.session['ctx']
            ctx = { 'money_reciever':money_reciever ,
            'financer':Compn.financer.first_name +" " + Compn.financer.last_name ,
            'total_money':str(Compn.total_money),
            'audit': str(Compn.audit.id),
            'gasstation': Compn.gasstation.name,
            'startD':str(myObj.audit_date_from), 
            'endD':str(myObj.audit_date_to),
            'date': str(today),
            'serial': str(myObj.id) }
            request.session['ctx'] = ctx
            return redirect('confirmation')
            #return render(request, 'paymentConfirm.html',{ 'money_reciever':money_reciever ,'Compn':Compn})
    return render(request, 'paymentDetail.html', {'result':result, 'form':form})

def confirmation(request):
    return render(request, 'paymentConfirm.html')

class addGasStaion(CreateView):    
    model = Gasstation
    fields = '__all__'
    template_name= 'addStaions.html'
    success_url = '/addgasstaion/'


def readme(request):
    return render(request, 'readme.html')

def recordSale(request):
    return render(request, 'recordSale.html')