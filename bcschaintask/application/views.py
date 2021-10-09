from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from application.models import Transaction
from application.api import make_transaction

def index(request):
    return render(request, "application/index.html", {
        'doc_title': "Transactions", 
        'transactions': Transaction.objects.all()
        })

def update(request):
    
    Transaction(
        transaction_id = make_transaction(),
        value = 0.00000001
    ).save()

    return redirect("/")

def tx(request, txid):
    return render(
        request,
        'application/tx.html', 
        { 
            'txobject': Transaction.objects.get(transaction_id=txid)
        }
    )
