from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from sshkm.models import Key, KeyGroup, Group
from sshkm.forms import KeyForm

from iota import BadApiResponse, StrictIota, __version__

@login_required
def KeyList(request):
    keys = Key.objects.order_by('name')
    context = {'keys': keys}
    return render(request, 'sshkm/key/list.html', context)

@login_required
def KeyDetail(request):
    if request.method == 'GET' and 'id' in request.GET:
        key = get_object_or_404(Key, pk=request.GET['id'])
        groups = Group.objects.all()
        groups_selected = KeyGroup.objects.all().filter(key_id=request.GET['id'])
        ids_selected = []
        
        for group_selected in groups_selected:
            ids_selected.append(group_selected.group_id)

        groups_not_selected = groups.exclude(id__in=ids_selected)
        
        return render(request, 'sshkm/key/detail.html', {
            'keyform': KeyForm(instance=key),
            'groups': groups,
            'groups_selected': groups_selected,
            'groups_not_selected': groups_not_selected,
        })
    else:
        return render(request, 'sshkm/key/detail.html', {
            'keyform': KeyForm(),
            'groups_not_selected': Group.objects.all(),
        })

@login_required
def KeyDelete(request):
    try:
        keys = Key.objects.filter(id__in=request.GET.getlist('id', request.POST.getlist('id'))) # calls getlist on POST only if getlist of GET is None
        size = len(keys)

        if size > 0:
            messages.add_message(request, messages.SUCCESS, "Keys deleted") if size > 1 else messages.add_message(request, messages.SUCCESS, "Key " + keys.first().name+ " deleted")
            keys.delete()
        else:
            messages.add_message(request, messages.ERROR, "The key could not be deleted. Key does not exist")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The key could not be deleted: "+str(e))

    return HttpResponseRedirect(reverse('KeyList'))

@login_required
def KeySave(request):
    try:
        key = Key(
            id=request.POST.get('id'),
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            firstname=request.POST.get('firstname', False),
            lastname=request.POST.get('lastname', False),
            email=request.POST.get('email'),
            publickey=request.POST.get('publickey', '').replace("\n", "").replace("\r", ""),
        )
        
        if key.id is not None:
            KeyGroup.objects.filter(key_id=key.id).delete()
            
        key.save()

        for group_id in request.POST.getlist('member_of'):
            keygroup = KeyGroup(key_id=key.id, group_id=group_id)
            keygroup.save()

        messages.add_message(request, messages.SUCCESS, "Key " + request.POST.get('name') + " sucessfully saved")
    except AttributeError as e:
        messages.add_message(request, messages.WARNING, "Key " + request.POST.get('name') + " sucessfully saved with warnings")
    except ValueError as e:
        messages.add_message(request, messages.ERROR, "The key could not be saved (ValueError)")
    except IntegrityError as e:
        messages.add_message(request, messages.ERROR, "The key could not be saved. Key already exists.")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The key could not be saved")

    return HttpResponseRedirect(reverse('KeyList'))
