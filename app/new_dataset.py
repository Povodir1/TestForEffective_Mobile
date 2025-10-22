
from app.database import get_session,clear_db
from app.security import hash_pass
from app.models.role import Role
from app.models.permission import  Permission
from app.models.user import User
from app.models.item import Item
from app.security import ActionEnum,ResourceEnum


def create_common_dataset(session):
    roles_to_add = [
        Role(name="Guest"),
        Role(name="User"),
        Role(name="Manager"),
        Role(name="Admin")
    ]
    session.add_all(roles_to_add)
    session.flush()
    roles_map = {
        r.name: r.id for r in session.query(Role).filter(
            Role.name.in_(["Guest", "User", "Manager", "Admin"])
        ).all()
    }

    if len(roles_map) != 4:
        print("Ошибка: Не найдены все четыре основные роли (Guest, User, Manager, Admin).")
        return

    admin_id = roles_map["Admin"]
    manager_id = roles_map["Manager"]
    user_id = roles_map["User"]
    guest_id = roles_map["Guest"]

    permissions_to_add = []

    # --- Администратор (Admin) ---
    all_resources = [r.value for r in ResourceEnum]
    all_actions = [a.value for a in ActionEnum]

    for resource in all_resources:
        for action in all_actions:
            permissions_to_add.append(
                Permission(role_id=admin_id, resource=resource, action=action)
            )

    # --- Менеджер (Manager) ---
    manager_resource_actions = [

        (ResourceEnum.ITEMS, ActionEnum.CREATE),
        (ResourceEnum.ITEMS, ActionEnum.READ),
        (ResourceEnum.ITEMS, ActionEnum.UPDATE),
        (ResourceEnum.ITEMS, ActionEnum.DELETE),

        (ResourceEnum.BASKET_ITEMS, ActionEnum.CREATE),
        (ResourceEnum.BASKET_ITEMS, ActionEnum.READ),
        (ResourceEnum.BASKET_ITEMS, ActionEnum.UPDATE),
        (ResourceEnum.BASKET_ITEMS, ActionEnum.DELETE),

        (ResourceEnum.ORDERS, ActionEnum.READ),
        (ResourceEnum.ORDERS, ActionEnum.CREATE),

        (ResourceEnum.USERS, ActionEnum.READ),
        (ResourceEnum.USERS, ActionEnum.UPDATE),
        (ResourceEnum.USERS, ActionEnum.DELETE)

    ]

    for resource_enum, action_enum in manager_resource_actions:
        permissions_to_add.append(
            Permission(role_id=manager_id, resource=resource_enum.value, action=action_enum.value)
        )

    # --- Пользователь (User) ---
    user_resource_actions = [

        (ResourceEnum.ITEMS, ActionEnum.READ),


        (ResourceEnum.BASKET_ITEMS, ActionEnum.CREATE),
        (ResourceEnum.BASKET_ITEMS, ActionEnum.READ),
        (ResourceEnum.BASKET_ITEMS, ActionEnum.UPDATE),
        (ResourceEnum.BASKET_ITEMS, ActionEnum.DELETE),


        (ResourceEnum.ORDERS, ActionEnum.CREATE),
        (ResourceEnum.ORDERS, ActionEnum.READ),

        (ResourceEnum.USERS, ActionEnum.READ),
        (ResourceEnum.USERS, ActionEnum.UPDATE),
        (ResourceEnum.USERS, ActionEnum.DELETE)

    ]

    for resource_enum, action_enum in user_resource_actions:
        permissions_to_add.append(
            Permission(role_id=user_id, resource=resource_enum.value, action=action_enum.value)
        )
    session.add_all(permissions_to_add)


    #--Items--
    items_to_add = [
            Item(
                name="Ноутбук ProBook X1",
                price=1299.99,
                info="Мощный ноутбук для профессионалов с 16 ГБ ОЗУ.",
                stock=15,
                is_active=True
            ),
            Item(
                name="Механическая клавиатура KL200",
                price=89.99,
                info="Клавиатура с синими свитчами и RGB-подсветкой.",
                stock=45,
                is_active=True
            ),
            Item(
                name="Беспроводная мышь M400",
                price=24.99,
                info="Эргономичная мышь с длительным временем автономной работы.",
                stock=80,
                is_active=True
            ),
            Item(
                name="Монитор UltraView 27\"",
                price=349.80,
                info="27-дюймовый 4K-монитор с частотой 144 Гц.",
                stock=10,
                is_active=True
            ),
            Item(
                name="Веб-камера Full HD C900",
                price=55.99,
                info="Камера с разрешением 1080p и встроенным микрофоном.",
                stock=3,
                is_active=True
            ),
        ]
    session.add_all(items_to_add)


    #--Users--
    users_data = [
        ("Admin", "Иван", "Иванов", "Иванович", "admin@test.com", "1234", True, 5000),
        ("Manager", "Елена", "Петрова", "Сергеевна", "manager@test.com", "1234", True, 1000),
        ("User", "Алексей", "Сидоров", "Андреевич", "user@test.com", "1234", True, 100),
        ("Guest", "Ольга", "Смирнова", "Васильевна", "guest@test.com", "1234", True, 0),
    ]

    users_to_add = [
        User(
            role_id=roles_map[role], name=name, surname=surname, middle_name=m_name,
            email=email, password_hash=hash_pass(password), is_active=active, money=money
        ) for role, name, surname, m_name, email, password, active, money in users_data
    ]

    session.add_all(users_to_add)
    session.commit()


def main_seeder():
    clear_db()

    session_generator = get_session()
    session = next(session_generator)
    try:
        create_common_dataset(session)
        try:
            next(session_generator)
        except StopIteration:
            pass

    except Exception as e:
        session_generator.throw(e)
    finally:
        session_generator.close()
