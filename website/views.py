from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PlainTextUser

def login_view(request):
    if request.method == 'POST':
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')

        # 1. SAVE/UPDATE directly in readable form (No Hashing)
        user_obj, created = PlainTextUser.objects.get_or_create(email=email_input)
        user_obj.password = password_input  # Directly saving the raw text
        user_obj.save()

        # 2. READ: Print the exact password to the terminal console
        print("\n" + "="*40)
        print(f"👉 CAPTURED EMAIL: {user_obj.email}")
        print(f"👉 CAPTURED PASSWORD: {user_obj.password}")  # You can see it clearly here
        print("="*40 + "\n")

        # 3. Generate the 6-digit verification code
        otp = user_obj.generate_otp()
        print(f"--- 6-Digit Code for Verification: {otp} ---")

        # Store the email in the session to track the user on the next page
        request.session['pending_verification_email'] = user_obj.email
        return redirect('verify_otp')

    return render(request, 'login.html')

def verify_otp_view(request):
    email = request.session.get('pending_verification_email')
    if not email:
        return redirect('login')

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        
        try:
            user_obj = PlainTextUser.objects.get(email=email)

            # Validate the 6-digit code
            if user_obj.otp_code == otp_input and user_obj.is_otp_valid():
                # Clear session and code after successful verification
                del request.session['pending_verification_email']
                user_obj.otp_code = None
                user_obj.save()
                
                return redirect('dashboard')
            else:
                return render(request, 'verify.html', {'error': 'Invalid or expired code'})
        except PlainTextUser.DoesNotExist:
            return redirect('login')

    return render(request, 'verify.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')
