from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Todo, Category, Tag, TodoTag, Priority


class TodoModelTest(TestCase):
    """Test cases for Todo model"""

    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(name='Work', color='#667eea')
        self.todo = Todo.objects.create(
            title='Test Todo',
            description='Test Description',
            due_date=date.today() + timedelta(days=7),
            priority=Priority.HIGH,
            category=self.category
        )

    def test_todo_creation(self):
        """Test creating a todo with all fields"""
        self.assertEqual(self.todo.title, 'Test Todo')
        self.assertEqual(self.todo.description, 'Test Description')
        self.assertFalse(self.todo.completed)
        self.assertEqual(self.todo.priority, Priority.HIGH)
        self.assertEqual(self.todo.category, self.category)

    def test_todo_minimal_creation(self):
        """Test creating a todo with only required fields"""
        minimal_todo = Todo.objects.create(title='Minimal Todo')
        self.assertEqual(minimal_todo.title, 'Minimal Todo')
        self.assertEqual(minimal_todo.description, '')
        self.assertIsNone(minimal_todo.due_date)
        self.assertFalse(minimal_todo.completed)
        self.assertEqual(minimal_todo.priority, Priority.MEDIUM)  # default

    def test_todo_str_method(self):
        """Test __str__ method returns title"""
        self.assertEqual(str(self.todo), 'Test Todo')

    def test_is_overdue_property_false(self):
        """Test is_overdue returns False for future due date"""
        self.assertFalse(self.todo.is_overdue)

    def test_is_overdue_property_true(self):
        """Test is_overdue returns True for past due date"""
        overdue_todo = Todo.objects.create(
            title='Overdue Todo',
            due_date=date.today() - timedelta(days=1)
        )
        self.assertTrue(overdue_todo.is_overdue)

    def test_is_overdue_completed_todo(self):
        """Test is_overdue returns False for completed todos"""
        overdue_todo = Todo.objects.create(
            title='Completed Overdue',
            due_date=date.today() - timedelta(days=1),
            completed=True
        )
        self.assertFalse(overdue_todo.is_overdue)

    def test_is_overdue_no_due_date(self):
        """Test is_overdue returns False when no due date"""
        no_date_todo = Todo.objects.create(title='No Date')
        self.assertFalse(no_date_todo.is_overdue)

    def test_mark_complete_method(self):
        """Test mark_complete sets completed and completed_at"""
        self.assertFalse(self.todo.completed)
        self.assertIsNone(self.todo.completed_at)
        
        self.todo.mark_complete()
        
        self.assertTrue(self.todo.completed)
        self.assertIsNotNone(self.todo.completed_at)

    def test_mark_incomplete_method(self):
        """Test mark_incomplete resets completion"""
        self.todo.mark_complete()
        self.assertTrue(self.todo.completed)
        
        self.todo.mark_incomplete()
        
        self.assertFalse(self.todo.completed)
        self.assertIsNone(self.todo.completed_at)

    def test_todo_ordering(self):
        """Test todos are ordered by created_at descending"""
        todo1 = Todo.objects.create(title='First')
        todo2 = Todo.objects.create(title='Second')
        todo3 = Todo.objects.create(title='Third')
        
        todos = list(Todo.objects.all())
        self.assertEqual(todos[0], todo3)  # Most recent first
        self.assertEqual(todos[1], todo2)
        self.assertEqual(todos[2], todo1)


class CategoryModelTest(TestCase):
    """Test cases for Category model"""

    def test_category_creation(self):
        """Test creating a category"""
        category = Category.objects.create(name='Personal', color='#764ba2')
        self.assertEqual(category.name, 'Personal')
        self.assertEqual(category.color, '#764ba2')

    def test_category_str_method(self):
        """Test __str__ method returns name"""
        category = Category.objects.create(name='Work')
        self.assertEqual(str(category), 'Work')

    def test_category_default_color(self):
        """Test category has default color"""
        category = Category.objects.create(name='Test')
        self.assertEqual(category.color, '#667eea')

    def test_category_unique_name(self):
        """Test category name must be unique"""
        Category.objects.create(name='Duplicate')
        with self.assertRaises(Exception):
            Category.objects.create(name='Duplicate')


class TagModelTest(TestCase):
    """Test cases for Tag model"""

    def test_tag_creation(self):
        """Test creating a tag"""
        tag = Tag.objects.create(name='urgent')
        self.assertEqual(tag.name, 'urgent')

    def test_tag_str_method(self):
        """Test __str__ method returns hashtag format"""
        tag = Tag.objects.create(name='important')
        self.assertEqual(str(tag), '#important')

    def test_tag_unique_name(self):
        """Test tag name must be unique"""
        Tag.objects.create(name='duplicate')
        with self.assertRaises(Exception):
            Tag.objects.create(name='duplicate')


class TodoTagModelTest(TestCase):
    """Test cases for TodoTag model"""

    def setUp(self):
        """Set up test data"""
        self.todo = Todo.objects.create(title='Test Todo')
        self.tag = Tag.objects.create(name='test')

    def test_todotag_creation(self):
        """Test creating a todo-tag relationship"""
        todo_tag = TodoTag.objects.create(todo=self.todo, tag=self.tag)
        self.assertEqual(todo_tag.todo, self.todo)
        self.assertEqual(todo_tag.tag, self.tag)

    def test_todotag_str_method(self):
        """Test __str__ method"""
        todo_tag = TodoTag.objects.create(todo=self.todo, tag=self.tag)
        self.assertEqual(str(todo_tag), 'Test Todo - test')

    def test_todotag_unique_together(self):
        """Test same todo-tag combination can't be added twice"""
        TodoTag.objects.create(todo=self.todo, tag=self.tag)
        with self.assertRaises(Exception):
            TodoTag.objects.create(todo=self.todo, tag=self.tag)


class TodoListViewTest(TestCase):
    """Test cases for todo_list view"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.url = reverse('todo_list')

    def test_todo_list_view_get(self):
        """Test GET request returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_todo_list_uses_correct_template(self):
        """Test view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todo/home.html')

    def test_todo_list_displays_todos(self):
        """Test view displays all todos"""
        Todo.objects.create(title='Todo 1')
        Todo.objects.create(title='Todo 2')
        
        response = self.client.get(self.url)
        self.assertContains(response, 'Todo 1')
        self.assertContains(response, 'Todo 2')

    def test_todo_list_empty_state(self):
        """Test view shows empty state when no todos"""
        response = self.client.get(self.url)
        self.assertContains(response, 'No todos yet')


class TodoCreateViewTest(TestCase):
    """Test cases for todo_create view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('todo_create')

    def test_todo_create_view_get(self):
        """Test GET request returns form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/base.html')

    def test_todo_create_post_valid(self):
        """Test POST creates new todo and redirects"""
        data = {
            'title': 'New Todo',
            'description': 'Description',
            'due_date': '2025-12-31'
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('todo_list'))
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_todo_create_post_minimal(self):
        """Test POST with only title"""
        data = {'title': 'Minimal Todo'}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)
        todo = Todo.objects.get(title='Minimal Todo')
        self.assertEqual(todo.description, '')
        self.assertIsNone(todo.due_date)

    def test_todo_create_empty_due_date(self):
        """Test POST handles empty due_date correctly"""
        data = {
            'title': 'No Date Todo',
            'description': 'Test',
            'due_date': ''
        }
        response = self.client.post(self.url, data)
        
        todo = Todo.objects.get(title='No Date Todo')
        self.assertIsNone(todo.due_date)


class TodoEditViewTest(TestCase):
    """Test cases for todo_edit view"""

    def setUp(self):
        """Set up test client and todo"""
        self.client = Client()
        self.todo = Todo.objects.create(
            title='Original Title',
            description='Original Description',
            due_date=date.today()
        )
        self.url = reverse('todo_edit', args=[self.todo.pk])

    def test_todo_edit_view_get(self):
        """Test GET returns form with todo data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/base.html')
        self.assertContains(response, 'Original Title')

    def test_todo_edit_post_valid(self):
        """Test POST updates todo"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'due_date': '2025-12-25'
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.description, 'Updated Description')

    def test_todo_edit_nonexistent(self):
        """Test editing non-existent todo returns 404"""
        url = reverse('todo_edit', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoDeleteViewTest(TestCase):
    """Test cases for todo_delete view"""

    def setUp(self):
        """Set up test client and todo"""
        self.client = Client()
        self.todo = Todo.objects.create(title='To Delete')
        self.url = reverse('todo_delete', args=[self.todo.pk])

    def test_todo_delete_view(self):
        """Test DELETE removes todo and redirects"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())

    def test_todo_delete_nonexistent(self):
        """Test deleting non-existent todo returns 404"""
        url = reverse('todo_delete', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoToggleViewTest(TestCase):
    """Test cases for todo_toggle view"""

    def setUp(self):
        """Set up test client and todo"""
        self.client = Client()
        self.todo = Todo.objects.create(title='Toggle Test', completed=False)
        self.url = reverse('todo_toggle', args=[self.todo.pk])

    def test_todo_toggle_incomplete_to_complete(self):
        """Test toggling from incomplete to complete"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)

    def test_todo_toggle_complete_to_incomplete(self):
        """Test toggling from complete to incomplete"""
        self.todo.completed = True
        self.todo.save()
        
        response = self.client.get(self.url)
        
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.completed)

    def test_todo_toggle_nonexistent(self):
        """Test toggling non-existent todo returns 404"""
        url = reverse('todo_toggle', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoIntegrationTest(TestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_complete_workflow(self):
        """Test complete CRUD workflow"""
        # Create
        create_data = {
            'title': 'Integration Test Todo',
            'description': 'Test Description',
            'due_date': '2025-12-31'
        }
        self.client.post(reverse('todo_create'), create_data)
        todo = Todo.objects.get(title='Integration Test Todo')
        
        # Read
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'Integration Test Todo')
        
        # Update
        edit_data = {
            'title': 'Updated Todo',
            'description': 'Updated',
            'due_date': '2026-01-01'
        }
        self.client.post(reverse('todo_edit', args=[todo.pk]), edit_data)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Todo')
        
        # Toggle
        self.client.get(reverse('todo_toggle', args=[todo.pk]))
        todo.refresh_from_db()
        self.assertTrue(todo.completed)
        
        # Delete
        self.client.get(reverse('todo_delete', args=[todo.pk]))
        self.assertFalse(Todo.objects.filter(pk=todo.pk).exists())

    def test_todo_with_category(self):
        """Test creating todo with category"""
        category = Category.objects.create(name='Work', color='#667eea')
        todo = Todo.objects.create(
            title='Work Todo',
            category=category
        )
        
        self.assertEqual(todo.category, category)
        self.assertIn(todo, category.todos.all())
