from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Todo


def todo_list(request):
    """Display list of all todos"""
    todos = Todo.objects.all()
    return render(request, 'todo/home.html', {'todos': todos})


def todo_create(request):
    """Create a new todo"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        todo = Todo.objects.create(
            title=title,
            description=description,
            due_date=due_date if due_date else None
        )
        return redirect('todo_list')
    
    return render(request, 'todo/base.html')


def todo_edit(request, pk):
    """Edit an existing todo"""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        todo.due_date = due_date if due_date else None
        todo.save()
        return redirect('todo_list')
    
    return render(request, 'todo/base.html', {'todo': todo})


def todo_delete(request, pk):
    """Delete a todo"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list')


def todo_toggle(request, pk):
    """Toggle todo completion status"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')
