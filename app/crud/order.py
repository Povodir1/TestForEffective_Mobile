from app.models import Order,BasketItem,OrderItem,User
from app.schemas.order import OrderSchema,OrderItemSchema
from app.exceptions import ObjectNotFoundError,NoMoneyError


def db_create_order(user_id:int,session):
    #задать пустой заказ
    order = Order(user_id = user_id)
    session.add(order)
    session.flush()

    #добавить товары в заказ
    basket_items = session.query(BasketItem).filter(BasketItem.user_id == user_id).all()

    if not basket_items:
        raise ObjectNotFoundError("Корзина пуста")

    res_price = 0
    for item in basket_items:
        order_item = OrderItem(item_id = item.item_id,order_id = order.id,count = item.count,
                               item_price = item.items.price)
        session.add(order_item)
        res_price += item.items.price*item.count

    #оплата заказа юзером
    user = session.query(User).filter(User.id ==user_id).first()
    if not user:
        raise ObjectNotFoundError("Пользователь не найден")

    if user.money < res_price:
        raise NoMoneyError("Недостаточно средств")

    user.money -= res_price

    #убрать товары из корзины
    for item in basket_items:
        session.delete(item)


    order_items = session.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    res_item_arr = [(OrderItemSchema(item_id = item.item_id,item_name=item.items.name,
                                            count = item.count,item_price = item.items.price)) for item in order_items]

    return OrderSchema(id = order.id, items = res_item_arr,price = res_price)




def db_get_all_orders(user_id:int,session):
    orders = session.query(Order).filter(Order.user_id == user_id).all()
    orders_arr = []
    for order in orders:
        res_item_arr = []
        res_price = 0
        for item in order.order_items:
            res_item_arr.append(OrderItemSchema(item_id = item.item_id,item_name=item.items.name,
                                                count = item.count,item_price = item.items.price))
            res_price += item.items.price*item.count
        orders_arr.append(OrderSchema(id = order.id, items = res_item_arr,price = res_price))
    return orders_arr
