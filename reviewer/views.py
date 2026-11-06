import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CodeReview
from .ai_agent import review_code_with_ai

def index(request):
    """Frontend dark-mode editor page serve karta hai"""
    recent_reviews = CodeReview.objects.all()[:5]
    return render(request, 'reviewer/index.html', {'recent_reviews': recent_reviews})

@csrf_exempt
def review_code_api(request):
    """AJAX POST request se code receive karke AI review run karta hai"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        body = json.loads(request.body)
        code = body.get('code', '').strip()
        language = body.get('language', 'python')

        if not code:
            return JsonResponse({'error': 'Code field cannot be empty'}, status=400)

        # AI Engine ko call karein
        ai_result = review_code_with_ai(source_code=code, language=language)

        score = ai_result.get('score', 0)
        summary = ai_result.get('summary', '')
        issues = ai_result.get('issues', [])
        fixed_code = ai_result.get('fixed_code', '')

        # Database me record save karein
        review_obj = CodeReview.objects.create(
            language=language,
            original_code=code,
            score=score,
            summary=summary,
            issues_json=issues,
            fixed_code=fixed_code
        )

        return JsonResponse({
            'success': True,
            'review_id': review_obj.id,
            'score': score,
            'summary': summary,
            'issues': issues,
            'fixed_code': fixed_code
        })

    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)
