from django.conf import settings
from django.contrib import messages
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from main.utils import get_client_ip
from main.forms import CreateFeedbackForm


def index(request):
    context = {"title": "Главная | БиоКормЭксперт"}

    return render(request, "main/index.html", context)


def about(request):
    context = {"title": "О нас | БиоКормЭксперт"}

    return render(request, "main/about.html", context)


def contacts(request):
    context = {"title": "Контакты | БиоКормЭксперт"}

    return render(request, "main/contacts.html", context)


def feedback(request):

    if request.method == 'POST':
        form = CreateFeedbackForm(data=request.POST)
        if form.is_valid():
            ip_address = get_client_ip(request)

            feedback_form = form.save(commit=False)
            feedback_form.ip_address = ip_address
            form.save()

            first_name = form.cleaned_data["first_name"]
            user_email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]

            recipients = [settings.EMAIL_ADMIN]

            message = render_to_string('feedback_email_send.html', {
                'first_name': first_name,
                'email': user_email,
                'phone_number': phone_number,
                'content': content,
                'ip_address': ip_address,
            })

            try:
                email = EmailMessage(subject, message, settings.SERVER_EMAIL, recipients)
                email.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, "Сообщение отправлено!")
            return JsonResponse({'success': True})

        else:
            feedback_html = render_to_string(
                "includes/popup.html", {"form": form}, request=request
            )

            response_data = {
                'success': False,
                "feedback_html": feedback_html,
            }

            return JsonResponse(response_data)
    else:
        form = CreateFeedbackForm()

        feedback_html = render_to_string('includes/popup_form.html', {"form": form}, request=request)
        return JsonResponse({'feedback_html': feedback_html})
