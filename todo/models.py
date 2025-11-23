from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Priority(models.TextChoices):
    """Priority levels for todos"""
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    URGENT = 'URGENT', 'Urgent'


class Category(models.Model):
    """Categories for organizing todos"""
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#667eea', help_text='Hex color code')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Todo(models.Model):
    """Main todo item model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='todos'
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """Check if todo is overdue"""
        if self.due_date and not self.completed:
            return self.due_date < timezone.now().date()
        return False

    def mark_complete(self):
        """Mark todo as completed"""
        self.completed = True
        self.completed_at = timezone.now()
        self.save()

    def mark_incomplete(self):
        """Mark todo as incomplete"""
        self.completed = False
        self.completed_at = None
        self.save()


class Tag(models.Model):
    """Tags for additional todo organization"""
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'#{self.name}'


class TodoTag(models.Model):
    """Many-to-many relationship between todos and tags"""
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='todo_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='todo_tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('todo', 'tag')
        ordering = ['tag__name']

    def __str__(self):
        return f'{self.todo.title} - {self.tag.name}'
