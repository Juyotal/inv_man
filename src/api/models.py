from django.db import models
from django.db.models.signals import post_delete, post_save
# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)
    inventory_count = models.IntegerField(null=True, blank=True, default=0)
    probable_profit = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    cost_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    markup = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    count_in_stock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.name

    @property
    def profit(self):
        return ((self.markup/100) * self.cost_price)
    
    @property
    def selling_price(self):
        return (self.profit + self.cost_price)

    @property
    def total_selling_price(self):
        return (self.selling_price * self.count_in_stock)

    @property
    def total_profit(self):
        return (self.profit * self.count_in_stock)


def save_item(sender, instance, **kwargs):
    item = instance
    banana = 0
    mango = 0
    items = Item.objects.filter(store=item.store)
    store = Store.objects.get(_id=item.store._id)
    
    for i in items:
        banana += i.total_profit
        mango += i.count_in_stock
    store.probable_profit = banana
    store.inventory_count  = mango
    store.save()
    print(store.inventory_count)

post_save.connect(save_item, sender=Item)
post_delete.connect(save_item, sender=Item)
