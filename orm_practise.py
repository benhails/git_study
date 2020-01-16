import peewee as pw
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase

# db = pw.SqliteDatabase('orm_practise.db')
db = PostgresqlExtDatabase('orm_practice_dev')


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = db
        legacy_table_names = False


class Store(BaseModel):
    name = pw.CharField(unique=True)


class Warehouse(BaseModel):
    store = pw.ForeignKeyField(Store, backref='warehouses', unique=True)
    location = pw.TextField()


class Product(BaseModel):
    name = pw.CharField(index=True)
    description = pw.TextField()
    warehouse = pw.ForeignKeyField(Warehouse, backref='products')
    color = pw.CharField(null=True)


# CODE FOR CHALLENGES

# 2. Retrieve all stores and in python loop through them and print out their names

def print_all_stores():
    for store in Store.select():
        print(f"{store.name}")

# 3. Retrieve only the FIRST store

def print_first_store_a():
    print(f"{Store.select().dicts()[0]}") # returns first store as a complete dictionary

def print_first_store_b():
    print(f"{Store.select()[0]}") # returns first store id

def print_first_store_c():
    print(f"{Store.select()[0].name}") # returns first store name

# 4. Retrieve a store by the name of the store e.g. "Store 3"

def get_store_by_name_a(store_name):
    print(f"{Store.get(Store.name == store_name).name}")
        
def get_store_by_name_b(store_name):  
    result = Store.select().dicts().where(Store.name == store_name)
    print(result)

# 5. Retrieve a store by id

def get_store_by_id(store_id):
    print(f"{Store.get_by_id(store_id).name}") # (returns the name of the store)

# 6. Retrieve all the warehouses for the store you created in the previous lesson (use join)

def get_warehouses_for_store_a(store_id):
    for warehouse in Warehouse.select().where(Warehouse.store_id == store_id):
        print(warehouse.location)

def get_warehouses_and_products_for_store_b(store_id):
    for w in Store.get_by_id(store_id).warehouses:
        print(w.location)
        for p in w.products:
            print(p.name)

# 7. Retrieve all the products for the store you created in the previous lesson (use join)

# def get_products_for_store(store_id):
#     for product in Product.select().join(Warehouse).where(product.warehouse.store_id == store_id):
#         print(product.name)

def get_products_for_store_a(store_id):
    for warehouse in Warehouse.select().join(Product).where(Warehouse.store_id == store_id):
        for product in Product.select().where(Product.warehouse_id == warehouse.id):
            print(f"{product.name}")

# 8. For the only product in your database, retrieve the warehouse it belongs to (use join)

def get_warehouse_for_product_a(product_id):
    wh_id = Product.get_by_id(product_id).warehouse_id
    print(f"{Warehouse.get_by_id(wh_id).location}")

def get_warehouse_for_product_b(product_id):
    for warehouse in Warehouse.select().join(Product).where(Product.id == product_id):
        print(warehouse.location)

# 9. For the only product in your database, retrieve which store it belongs to (use join)

# NB. how do you do a join with GET? You can't. It's all such a fuck on to use select when you're only looking for one record - not worth spending the time on it.
# Simpler solution below

def get_store_for_product_b(product_id):  
    print(Product.get_by_id(product_id).warehouse.store.name)

# 1. Update the product name

def update_product_name(product_id, new_name):
    Product.update(name = new_name).where(Product.id == product_id).execute()

# def update_product_name(product_id, new_name):
#     Product.update({Product.name: new_name}).where(Product.id == product_id).execute()

# 2. Move the product to a new warehouse

def update_product_wh(product_id, new_wh_id):
    Product.update(warehouse_id = new_wh_id).where(Product.id == product_id).execute()

# 1. A product was sold, delete the product

def delete_product(product_id):
    Product.get_by_id(product_id).delete_instance()

# 2. usiness isn't going well, delete a warehouse

def delete_warehouse(warehouse_id):
    Warehouse.get_by_id(warehouse_id).delete_instance()