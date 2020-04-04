import json
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from firewall.forms import NFTablesConfigForm
from firewall.sys_utils.nftables import NFTables


# Create your views here.

def home(request):
    return render(request, 'firewall/home.html')


def stats(request):
    return render(request, 'firewall/stats.html', {'chart1': process_nftables_data(NFTables.get_stats())})


# @login_required(login_url='/account/login/')
def rules(request):
    print(request)
    if request.method == 'POST':
        form = NFTablesConfigForm(request.POST)
        try:
            NFTables.apply_current_cong(form['nft_config'])
        except Exception as e:
            messages.warning(request, "There is an error in your configuration!")
        else:
            messages.success(request, "Configuration successfully applied.")

    else:  # == GET
        form = NFTablesConfigForm()
    return render(request, 'firewall/rules.html', {'form': form})


def process_nftables_data(data):
    return data
