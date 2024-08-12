from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models.functions import Round
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from app.forms import CommentModelForm
from app.models import Product, Cart, Comment, Profile, AttributeValue, Rating, ProductAttribute, Customer


# Create your views here.


def product_list(request):

    # Fetch all products
    products = Product.objects.all()

    # Handle cart items
    cart_items = Cart.objects.filter(user=request.user.id)

    # Handle profile fetching
    try:
        profile = Profile.objects.get(user=request.user.id)
    except Profile.DoesNotExist:
        profile = None

    # Fetch recent products
    time_threshold = timezone.now() - timedelta(hours=36)
    recent_products = Product.objects.filter(created_at__gte=time_threshold)

    # Pagination
    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cart_items': cart_items,
        'recent_products': recent_products,
        'profile': profile,
    }
    return render(request, 'app/product/products/product-list.html', context)


def product_detail(request, slug):

    # Fetch slug products
    product = get_object_or_404(Product, slug=slug)

    # Handle cart items
    cart_items = Cart.objects.filter(user=request.user.id)

    # Handle profile fetching
    try:
        profile = Profile.objects.get(user=request.user.id)
    except Profile.DoesNotExist:
        profile = None

    attributes = product.get_attributes()
    comments = Comment.objects.filter(product=product).order_by('-created_at')
    avg_rating = Rating.objects.filter(product=product).aggregate(avg_rating=Round(Avg('rating')))

    context = {
        'product': product,
        'attributes': attributes,
        'comments': comments,
        'cart_items': cart_items,
        'profile': profile,
        'avg_rating': avg_rating['avg_rating']
    }
    return render(request, 'app/product/products/product-details.html', context)


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    if created:
        cart.quantity = quantity
    else:
        cart.quantity += quantity
    cart.save()

    return redirect('product_detail', slug=product.slug)


def show_cart(request):

    # Handle profile fetching
    try:
        profile = Profile.objects.get(user=request.user.id)
    except Profile.DoesNotExist:
        profile = None

    cart_items = Cart.objects.filter(user=request.user.id).order_by('-created_at')
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'profile': profile
    }
    return render(request, 'app/product/shopping_cart/shopping-cart.html', context)


def delete_cart_item(request, item_id):
    cart = get_object_or_404(Cart, id=item_id, user=request.user)
    if cart:
        cart.delete()
        return redirect('show_cart')
    context = {
        'cart': cart
    }
    return render(request, 'app/product/shopping_cart/shopping-cart.html', context)


@login_required
def comment(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.username = request.user
            review.product = product
            review.save()
            return redirect('product_detail', slug)
    else:
        form = CommentModelForm()
    return render(request, 'app/product/products/product-details.html', {'form': form, 'product': product})


def like_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.user in product.users_like.all():
        product.users_like.remove(request.user)
    else:
        product.users_like.add(request.user)

    return redirect('product_detail', slug=slug)


def checkout(request):
    return render(request, 'app/product')


def customers(request):
    customer = Customer.objects.all()
    # Handle cart items
    cart_items = Cart.objects.filter(user=request.user.id)

    # Handle profile fetching
    try:
        profile = Profile.objects.get(user=request.user.id)
    except Profile.DoesNotExist:
        profile = None

    # Pagination
    paginator = Paginator(customer, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cart_items': cart_items,
        'profile': profile
    }
    return render(request, 'app/product/customers/customers.html', context)


def customer_detail(request, id):
    customer = get_object_or_404(Customer, id=id)

    # Handle cart items
    cart_items = Cart.objects.filter(user=request.user.id)

    # Handle profile fetching
    try:
        profile = Profile.objects.get(user=request.user.id)
    except Profile.DoesNotExist:
        profile = None

    context = {
        'customer': customer,
        'cart_items': cart_items,
        'profile': profile,
    }
    return render(request, 'app/product/customers/customer-details.html', context)
