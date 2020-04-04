from django.shortcuts import render
from django.http import HttpResponse

from firewall.sys_utils.nftables import NFTables


# Create your views here.

def home(request):
    return render(request, 'firewall/home.html')


def stats(request):
    return render(request, 'firewall/stats.html')


def rules(request):
    return render(request, 'firewall/rules.html', {'conf': NFTables.get_current_configuration()})
