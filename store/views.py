from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CheckoutForm, RegistrationForm
from .models import Order, OrderItem, Product


def home(request):
    products = Product.objects.all()
    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()
    if search:
        products = products.filter(name__icontains=search)
    if category:
        products = products.filter(category__iexact=category)
    categories = Product.objects.values_list("category", flat=True).distinct()
    return render(request, "store/home.html", {
        "products": products,
        "search": search,
        "selected_category": category,
        "categories": categories,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def _cart_items(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = int(quantity)
        except (Product.DoesNotExist, ValueError, TypeError):
            continue
        if quantity < 1:
            continue
        subtotal = product.price * quantity
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
        total += subtotal
    return items, total


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.stock < 1:
        messages.error(request, "This product is currently out of stock.")
        return redirect("product_detail", pk=product.pk)
    cart = request.session.get("cart", {})
    key = str(product.pk)
    new_quantity = int(cart.get(key, 0)) + 1
    if new_quantity > product.stock:
        messages.error(request, "You cannot add more than the available stock.")
    else:
        cart[key] = new_quantity
        request.session["cart"] = cart
        messages.success(request, f"{product.name} was added to your cart.")
    return redirect("cart")


def cart(request):
    items, total = _cart_items(request)
    return render(request, "store/cart.html", {"items": items, "total": total})


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_data = request.session.get("cart", {})
    try:
        quantity = int(request.POST.get("quantity", "1"))
    except ValueError:
        quantity = 0
    if quantity <= 0:
        cart_data.pop(str(product_id), None)
    elif quantity > product.stock:
        messages.error(request, f"Only {product.stock} unit(s) of {product.name} are available.")
    else:
        cart_data[str(product_id)] = quantity
        messages.success(request, "Cart updated.")
    request.session["cart"] = cart_data
    return redirect("cart")


@require_POST
def remove_from_cart(request, product_id):
    cart_data = request.session.get("cart", {})
    cart_data.pop(str(product_id), None)
    request.session["cart"] = cart_data
    messages.success(request, "Product removed from cart.")
    return redirect("cart")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("home")
    return render(request, "store/register.html", {"form": form})


@login_required
def checkout(request):
    items, total = _cart_items(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart")
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                locked_products = []
                for item in items:
                    product = Product.objects.select_for_update().get(pk=item["product"].pk)
                    if product.stock < item["quantity"]:
                        raise ValueError(f"Insufficient stock for {product.name}.")
                    locked_products.append((product, item["quantity"]))

                fresh_total = sum(
                    (product.price * quantity for product, quantity in locked_products),
                    Decimal("0.00")
                )
                order = Order.objects.create(
                    user=request.user,
                    total_amount=fresh_total,
                    address=form.cleaned_data["address"],
                )
                for product, quantity in locked_products:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )
                    product.stock -= quantity
                    product.save(update_fields=["stock"])
        except (ValueError, Product.DoesNotExist) as exc:
            messages.error(request, str(exc))
            return redirect("cart")

        request.session["cart"] = {}
        return render(request, "store/order_success.html", {"order": order})
    return render(request, "store/checkout.html", {"form": form, "items": items, "total": total})


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "store/orders.html", {"orders": user_orders})
