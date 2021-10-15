import  json

from django.shortcuts import render

from django.shortcuts import redirect, render

from transactions.models import Transaction
from transactions.bcschain import BCSNetManager

bcsnet = BCSNetManager()

def index(request):
    return render(request, "application/index.html", {
        'doc_title': "Transactions", 
        'transactions': Transaction.objects.all()
        })

def update(request):

    signed_tx = bcsnet.createsignedtx(
        "Kwg1kex9gQ1nVrTLUFYUGfn1AykDWNAY1JaPurouBdgFUCn2vAdS",
        [(bcsnet.getnewaddress(), 1)]
    )

    
    answer = bcsnet.sendrawtransaction(signed_tx) # server always returns  <TransportError for bcs_tester:iLoveBCS@45.32.232.25:3669/: 500 Internal Server Error>
    decoded_tx = bcsnet.decoderawtransaction(signed_tx)

    Transaction(
        transaction_id = decoded_tx['txid'],
        value = 0.00000001,
        jsontext = json.dumps(decoded_tx)
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
