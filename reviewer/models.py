from django.db import models

class CodeReview(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('typescript', 'TypeScript'),
        ('sql', 'SQL'),
        ('html_css', 'HTML/CSS'),
        ('other', 'Other'),
    ]

    language = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, default='python')
    original_code = models.TextField()
    score = models.IntegerField(default=0, help_text="Code Quality Score out of 100")
    summary = models.TextField(blank=True)
    issues_json = models.JSONField(default=list, help_text="List of detected bugs, security warnings")
    fixed_code = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.language.upper()} Review #{self.id} - Score: {self.score}/100"
