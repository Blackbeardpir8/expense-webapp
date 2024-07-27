from django.shortcuts import render,redirect
from django.contrib import messages
from tracker.models import *
from django.db.models import Sum


# Create your views here.
def index(request):
    if request.method =="POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')


        if not description:
            messages.info(request, "Description cannot be empty")
            return redirect('/')
        
        try:
            amount = float(amount)
        except ValueError:
            messages.info(request, "Amount should be a valid number")
            return redirect('/')


        Transactions.objects.create(
            description = description,
            amount = amount,
        )

        messages.success(request, "Transaction added successfully!")
        return redirect('/')
        

    
    context = {'transactions' : Transactions.objects.all(),
               'balance' : Transactions.objects.all().aggregate(total_balance = Sum('amount'))['total_balance'] or 0,
               'income' : Transactions.objects.filter(amount__gte = 0).aggregate(income = Sum('amount'))['income'] or 0,
               'expense' : Transactions.objects.filter(amount__lte = 0).aggregate(expense = Sum('amount'))['expense'] or 0,
               }

    return render(request,'index.html',context)


def deleteTransaction(request,uuid):

    Transactions.objects.get(uuid = uuid).delete()
    return redirect('/')