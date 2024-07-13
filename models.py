from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.full_name

class Order(models.Model):
    PAYMENT_MODES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Digital Wallet', 'Digital Wallet')
    ]
    orderdatetime = models.DateTimeField(auto_now_add=True)
    paymentmode = models.CharField(max_length=15, choices=PAYMENT_MODES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.pk} by {self.customer.full_name}"

class OrderItem(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} x {self.food.name} for Order {self.order.pk}"
