from django.shortcuts import render, redirect
from .models import Note
from django.http import HttpResponseRedirect


def notes_list(request):
    if request.method == "POST":
        Note.objects.filter(id=request.POST.get("deleteButton")).delete()
    notes_list = Note.objects.filter(owner=request.user.username)
    return render(request, 'notebook.html', {'notes_list': notes_list})


def notes_creating(request):
    if request.method == "POST":
        Note.objects.create(
            title = request.POST.get("noteTitle", ""),
            text = request.POST.get("noteText", ""),
            owner = request.user.username
        )
        return redirect('/notebook')
    else:
        return render(request, 'newNotebook.html')

def notes_logout(request):
    return HttpResponseRedirect('/logout')