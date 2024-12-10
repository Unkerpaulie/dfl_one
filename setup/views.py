from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from core.models import DealStatus, Currency, IdentificationType
from account.models import User
from setup.models import CurrencyStock, BankFee
from core.utils import get_currency_balance

def check_admin(user):
   return user.is_authenticated and user.role == "admin"

def non_admin_redirect(request):
    messages.warning(request, "You must log in with an admin account to view this page.")
    return redirect('core:home')  # Replace 'home' with your actual home page URL pattern

# list users
@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def list_users(req):
    users = User.objects.all()
    context = {"page_title": "User Management"}
    context["section"] = "setup"
    context["users"] = users
    return render(req, 'setup/list_users.html', context)

# add user  
@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def add_user(req):
    context = {"page_title": "Add User"}
    context["section"] = "setup"
    context["roles"] = User.ROLE_CHOICES
    context["form_purpose"] = "add"
    if req.method == 'POST':
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        email = req.POST['email']
        role = req.POST['role']
        password = "ChangeMe!"
        try:
            new_user = User.objects.create_user(email, password, first_name=first_name, last_name=last_name, role=role)
            new_user.save()
            messages.success(req, 'User added successfully')
            messages.warning(req, 'User password is "ChangeMe!". User must change their password at next login')
            return redirect("setup:list_users")
        except:
            messages.warning(req, 'Error adding user')
            return render(req, 'setup/user_form.html', context)
    else:
        return render(req, 'setup/user_form.html', context)

# reset user password
@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def reset_user_password(req, user_id):
    if req.method == 'POST':
        user = User.objects.get(id=user_id)
        password = "ChangeMe!"
        user.set_password(password)
        user.needs_password_change = True
        user.save()
        messages.warning(req, 'Password reset to "ChangMe!". User must change their password at next login')
        return redirect("setup:list_users")


@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def edit_user(req, user_id):
    user = User.objects.get(id=user_id)
    context = {"page_title": "Edit User"}
    context["section"] = "setup"
    context["roles"] = User.ROLE_CHOICES
    context["form_purpose"] = "edit"
    context["formdata"] = {
        'first_name': user.first_name, 
        'last_name': user.last_name, 
        'email': user.email, 
        'role': user.role,
        'is_active': user.is_active
        }
    if req.method == 'POST':
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        email = req.POST['email']
        role = req.POST['role']
        is_active = req.POST['is_active'] == "on"

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.role = role
        user.is_active = is_active
        user.save()
        messages.success(req, 'User updated successfully')
        return redirect("setup:list_users")
    else:
        return render(req, 'setup/user_form.html', context)


# list currencies
@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def list_currencies(req):
    currencies = Currency.objects.all()
    context = {"page_title": "Currency List"}
    context["section"] = "setup"
    context |= {'currencies': currencies}
    return render(req, 'setup/list_currencies.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def add_currency(req):
    context = {"page_title": "Add Currency"}
    context["section"] = "setup"
    if req.method == 'POST':
        currency_name = req.POST['currency_name']
        currency_code = req.POST['currency_code']
        # symbol = req.POST['symbol']
        try:
            currency = Currency(
                currency_name=currency_name, 
                currency_code=currency_code, 
                # symbol=symbol
                )
            currency.save()
            messages.success(req, 'Currency added successfully')
            return redirect("setup:list_currencies")
        except:
            messages.warning(req, 'Error adding currency')
            return render(req, 'setup/currency_form.html', context)
    else:
        return render(req, 'setup/currency_form.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def edit_currency(req, currency_id):
    currency = Currency.objects.get(id=currency_id)
    context = {"page_title": "Edit Currency"}
    context["section"] = "setup"
    context["formdata"] = {'currency_name': currency.currency_name, 'currency_code': currency.currency_code,'symbol': currency.symbol}
    if req.method == 'POST':
        currency_name = req.POST['currency_name']
        currency_code = req.POST['currency_code']
        # symbol = req.POST['symbol']

        currency.currency_name = currency_name
        currency.currency_code = currency_code
        # currency.symbol = symbol
        currency.save()
        messages.success(req, 'Currency updated successfully')
        return redirect("setup:list_currencies")
    else:
        context |= {'currency': currency}
        return render(req, 'setup/currency_form.html', context)


# list deal status
@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def list_deal_status(req):
    deal_status = DealStatus.objects.all()
    context = {"page_title": "Deal Statuses"}
    context["section"] = "setup"
    context |= {'deal_status': deal_status}
    return render(req, 'setup/list_deal_status.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def add_deal_status(req):
    context = {"page_title": "Add Deal Status"}
    context["section"] = "setup"
    if req.method == 'POST':
        status_name = req.POST['status_name']
        try:
            deal_status = DealStatus(status_name=status_name)
            deal_status.save()
            messages.success(req, 'Deal status added successfully')
            return redirect("setup:list_deal_status")
        except:
            messages.warning(req, 'Error adding deal status')
            return render(req, 'setup/deal_status_form.html', context)
    else:
        return render(req, 'setup/deal_status_form.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def edit_deal_status(req, deal_status_id):
    deal_status = DealStatus.objects.get(id=deal_status_id)
    context = {"page_title": "Edit Deal Status"}
    context["section"] = "setup"
    context["formdata"] = {'status_name': deal_status.status_name}
    if req.method == 'POST':
        status_name = req.POST['status_name']
        deal_status.status_name = status_name
        deal_status.save()
        messages.success(req, 'Deal status updated successfully')
        return redirect("setup:list_deal_status")
    else:
        return render(req, 'setup/deal_status_form.html', context)

# list identification types
@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def list_identification_types(req):
    identification_types = IdentificationType.objects.all()
    context = {"page_title": "Identification Types"}
    context["section"] = "setup"
    context |= {'identification_types': identification_types}
    return render(req, 'setup/list_identification_types.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def add_identification_type(req):
    context = {"page_title": "Add Identification Type"}
    context["section"] = "setup"
    if req.method == 'POST':
        id_type = req.POST['id_type']
        try:
            identification_type = IdentificationType(id_type=id_type)
            identification_type.save()
            messages.success(req, 'Identification type added successfully')
            return redirect("setup:list_identification_types")
        except:
            messages.warning(req, 'Error adding identification type')
            return render(req, 'setup/identification_type_form.html', context)
    else:
        return render(req, 'setup/identification_type_form.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def edit_identification_type(req, identification_type_id):
    identification_type = IdentificationType.objects.get(id=identification_type_id)
    context = {"page_title": "Edit Identification Type"}
    context["section"] = "setup"
    context["formdata"] = {'id_type': identification_type.id_type}
    if req.method == 'POST':
        id_type = req.POST['id_type']
        identification_type.id_type = id_type
        identification_type.save()
        messages.success(req, 'Identification type updated successfully')
        return redirect("setup:list_identification_types")
    else:
        context |= {'identification_type': identification_type}
        return render(req, 'setup/identification_type_form.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def show_currency_inventory(req):
    currencies = Currency.objects.all()
    context = {"page_title": "Currency Inventory"}
    context["section"] = "setup"
    context["stock"] = []
    for currency in currencies:
        currency_adjustments = CurrencyStock.objects.filter(currency=currency)
        total_adjustment = [c.adjustment_type * c.amount for c in currency_adjustments] 
        this_cur  = model_to_dict(currency)
        this_cur['balance'] = sum(total_adjustment)
        context["stock"] += [this_cur]
    return render(req, 'setup/currency_stock.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def add_currency_adjustment(req):    
    currencies = Currency.objects.all()
    context = {"page_title": "Add Currency Adjustment"}
    context["section"] = "setup"
    context |= {'currencies': currencies}
    if req.method == 'POST':
        currency = int(req.POST['currency'])
        adjustment_type = req.POST['adjustment_type']
        amount = req.POST['amount']
        comment = req.POST['comment']
        try:
            currency_adjustment = CurrencyStock(
                currency=Currency.objects.get(id=currency), 
                amount=amount,
                adjustment_source="M", 
                adjustment_type=int(adjustment_type), 
                comment=comment,
                entered_by=req.user
            )
            currency_adjustment.save()
            messages.success(req, 'Currency adjustment added successfully')
            return redirect("setup:show_currency_inventory")
        except:
            messages.warning(req, 'Error adding currency adjustment')
            return render(req, 'setup/currency_adjust.html', context)
    else:
        return render(req, 'setup/currency_adjust.html', context)

        
@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def adjust_currency(req, currency_id):    
    currency = Currency.objects.get(id=currency_id)
    context = {"page_title": "Adjust Currency"}
    context["section"] = "setup"
    context["currency"] = currency
    context["balance"] = get_currency_balance(currency_id)
    if req.method == 'POST':
        adjustment_type = req.POST['adjustment_type']
        amount = req.POST['amount']
        comment = req.POST['comment']
        try:
            currency_adjustment = CurrencyStock(
                currency=currency, 
                amount=amount,
                adjustment_source="M", 
                adjustment_type=int(adjustment_type), 
                comment=comment,
                entered_by=req.user
            )
            currency_adjustment.save()
            messages.success(req, 'Currency adjustment added successfully')
            return redirect("setup:show_currency_inventory")
        except:
            messages.warning(req, 'Error adding currency adjustment')
            return render(req, 'setup/currency_adjust.html', context)
    else:
        return render(req, 'setup/currency_adjust.html', context)

@user_passes_test(check_admin, login_url=reverse_lazy('setup:restricted'))
def update_bank_fee(req):
    fee = BankFee.objects.get(id=1)
    context = {"page_title": "Update Bank Fee"}
    context["section"] = "setup"
    context["formdata"] = {'bank_fee': fee.bank_fee}
    if req.method == 'POST':
        bank_fee = req.POST['bank_fee']
        fee.bank_fee = bank_fee
        fee.save()
        messages.success(req, 'Bank fee updated successfully')
        return redirect("setup:update_bank_fee")
    else:
        context |= {'fee': fee}
        return render(req, 'setup/bank_fee_form.html', context)

