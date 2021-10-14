import json
import logging

from django.shortcuts import redirect, render

from application.models import Transaction
from application.bcschain import BCSNetManager

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

    answer = bcsnet.sendrawtransaction(signed_tx)
    logging.warn(answer)

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
