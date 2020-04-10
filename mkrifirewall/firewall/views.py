import json
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from firewall.forms import NFTablesConfigForm
from firewall.sys_utils.nftables import NFTables, NFTablesException

# Create your views here.
old_data = None


def home(request):
    return render(request, 'firewall/home.html')


def stats(request):
    global old_data
    old_data = process_nftables_data(NFTables.get_stats())
    chart1_max = next(iter(old_data.keys()))
    for key, val in old_data.items():
        if old_data[chart1_max] < val:
            chart1_max = key
    context = {
        'chart1': old_data,
        'chart1_max_key': chart1_max
    }
    return render(request, 'firewall/stats.html', context)


def get_traffic_stats(request):
    global old_data
    data = NFTables.get_stats()
    data = process_nftables_data(data)
    data_diff = {k: v - old_data[k] for k, v in data.items()}
    old_data = data
    return JsonResponse(data_diff, status=200)


# @login_required(login_url='/account/login/')
def rules(request):
    if request.method == 'POST':
        form = NFTablesConfigForm(request.POST)
        form.is_valid()
        conf = form.cleaned_data['nft_config']
        try:
            NFTables.apply_current_conf(conf)
        except NFTablesException as e:
            messages.warning(request, "There is an error in your configuration!")
        except Exception as e:
            messages.warning(request, "Unknown error occurs")
            messages.warning(request, e)
        else:
            messages.success(request, "Configuration successfully applied.")

    else:  # == GET
        curr_conf = ""
        try:
            curr_conf = NFTables.get_current_configuration()
        except NFTablesException as e:
            messages.warning(request, "There is an error in your configuration!")
            messages.warning(request, e)
        except FileNotFoundError:
            messages.warning(request, 'NFT program is not installed')

        form = NFTablesConfigForm(initial={'nft_config': curr_conf})

    return render(request, 'firewall/rules.html', {'form': form})


def process_nftables_data(data):
    return data
