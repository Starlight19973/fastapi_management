import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1219e7bc4501'
down_revision = '247c869fa4b3'
branch_labels = None
depends_on = None


def upgrade():
    # Шаг 1. Создаем новый ENUM тип
    order_status_enum = postgresql.ENUM('IN_PROGRESS', 'SHIPPED', 'DELIVERED', name='orderstatusenum')
    order_status_enum.create(op.get_bind(), checkfirst=True)

    # Шаг 2. Добавляем новый столбец с типом ENUM
    op.add_column('orders', sa.Column('status_enum', order_status_enum, nullable=True))

    # Шаг 3. Копируем данные из старого столбца в новый с использованием правильного преобразования
    op.execute(
        """
        UPDATE orders
        SET status_enum = CASE
            WHEN status = 'IN_PROGRESS' THEN 'IN_PROGRESS'::orderstatusenum
            WHEN status = 'SHIPPED' THEN 'SHIPPED'::orderstatusenum
            WHEN status = 'DELIVERED' THEN 'DELIVERED'::orderstatusenum
            ELSE NULL
        END
        """
    )

    # Шаг 4. Удаляем старый столбец
    op.drop_column('orders', 'status')

    # Шаг 5. Переименовываем новый столбец
    op.alter_column('orders', 'status_enum', new_column_name='status')


def downgrade():
    # Шаг отката изменений
    order_status_enum = postgresql.ENUM('IN_PROGRESS', 'SHIPPED', 'DELIVERED', name='orderstatusenum')

    # Возвращение старого столбца
    op.add_column('orders', sa.Column('status', sa.String(), nullable=True))

    # Копируем данные обратно из нового столбца в старый
    op.execute("UPDATE orders SET status = status::TEXT")

    # Удаляем новый столбец
    op.drop_column('orders', 'status_enum')

    # Удаляем тип ENUM
    order_status_enum.drop(op.get_bind(), checkfirst=True)