from app.schemas.item import ItemShortSchema,ItemCreateSchema, ItemPatchSchema
from app.models import Item
from app.exceptions import ObjectNotFoundError


def db_get_all_items(limit_num:int, page:int,session):
    items = session.query(Item).filter(Item.is_active == True).all()
    res_data = [ItemShortSchema(id = item.id,name = item.name,price=item.price,info = item.info,stock = item.stock) for item in items]
    res_data = res_data[(page-1)*limit_num:(page-1)*limit_num+limit_num]
    return res_data

def db_get_item(item_id:int,session):
    item = session.query(Item).filter(Item.is_active == True,Item.id == item_id).first()
    if not item:
        raise ObjectNotFoundError("Item not found")
    return ItemShortSchema(id = item.id,name = item.name,price=item.price,info = item.info,stock = item.stock)

def db_create_item(add_item:ItemCreateSchema,session):
    item = Item(name = add_item.name,info = add_item.info,price = add_item.price,stock = add_item.stock)
    session.add(item)
    session.flush()
    return ItemShortSchema(id = item.id,name = item.name,price = item.price,info= item.info,stock = item.stock)


def db_delete_item(item_id,session):
    item = session.query(Item).filter(Item.id == item_id,
                                      Item.is_active == True).first()
    if not item:
        raise ObjectNotFoundError("Item not found")
    item.is_active = False
    items_in_basket = item.basket_items
    if items_in_basket:
        for i in items_in_basket:
            session.delete(i)


def db_patch_item(item_id:int, new_data:ItemPatchSchema,session):
    item = session.query(Item).filter(Item.id == item_id,
                                      Item.is_active == True).first()
    if not item:
        raise ObjectNotFoundError("Item not found")
    for key,value in new_data.model_dump(exclude_none=True).items():
        setattr(item,key,value)
    session.flush()
    return ItemShortSchema(id = item.id,name = item.name,price = item.price,info= item.info,stock = item.stock)
