
from app.models.item import Item
from app.models.basket_item import BasketItem
from app.schemas.basket_item import BasketSchema,ItemInBasketScheme
from app.schemas.item import ItemShortSchema
from sqlalchemy.orm import joinedload
from app.exceptions import ObjectNotFoundError

def db_add_to_basket(user_id:int,item_id:int,count:int ,session):
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise ObjectNotFoundError("Предмет не найден")
    existing_item = session.query(BasketItem).filter(BasketItem.user_id==user_id,
                                                     BasketItem.item_id==item_id).first()

    if existing_item:
        existing_item.count += count
        basket_item = existing_item
    else:
        basket_item = BasketItem(user_id=user_id,item_id=item_id,count=count)
        session.add(basket_item)
    session.flush()
    item = basket_item.items


    return ItemInBasketScheme(item = ItemShortSchema(id = item.id,name = item.name,
                                                          price=item.price,info=item.info,stock=item.stock),count=count)


def db_get_basket_items(user_id,session):
    basket_items = session.query(BasketItem).options(
    joinedload(BasketItem.items)).filter(BasketItem.user_id == user_id).all()
    items_data = []
    res_price = 0
    for b_item in basket_items:
        item = b_item.items
        res_item = ItemInBasketScheme(item=ItemShortSchema(id=item.id, name=item.name,
                                                            price=item.price, info=item.info, stock=item.stock),
                                       count=b_item.count)
        res_price += b_item.count*item.price
        items_data.append(res_item)
    res_data = BasketSchema(items = items_data,
                                     full_price = res_price)
    return res_data


def db_delete_from_basket(item_id:int,user_id:int,session):
    item = session.query(BasketItem).filter(BasketItem.user_id==user_id,
                                            BasketItem.item_id==item_id).first()
    if not item:
        raise ObjectNotFoundError("Предмет не найден")
    session.delete(item)



