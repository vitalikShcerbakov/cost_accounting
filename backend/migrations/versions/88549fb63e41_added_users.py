"""added users

Revision ID: 88549fb63e41
Revises: 56228cf7f8df
Create Date: 2025-08-18 08:00:59.527754

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '88549fb63e41'
down_revision: Union[str, None] = '56228cf7f8df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу пользователей
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=50), nullable=True, comment='Электронная почта'),
        sa.Column('name', sa.String(length=50), nullable=True, comment='Имя'),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('false'), nullable=True, comment='Признак актива ли запись'),
        sa.Column('hashed_password', sa.String(), nullable=True, comment='ХЭШ пароля'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)

    # Добавляем столбцы user_id в существующие таблицы и создаем внешние ключи
    with op.batch_alter_table('categories_expenses') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_categories_expenses_user_id_users', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('categories_incomes') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_categories_incomes_user_id_users', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('expense_types') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_expense_types_user_id_users', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('expenses') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_expenses_user_id_users', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('incomes') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_incomes_user_id_users', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    # Удаляем связи и столбцы user_id
    with op.batch_alter_table('incomes') as batch_op:
        batch_op.drop_constraint('fk_incomes_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('expenses') as batch_op:
        batch_op.drop_constraint('fk_expenses_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('expense_types') as batch_op:
        batch_op.drop_constraint('fk_expense_types_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('categories_incomes') as batch_op:
        batch_op.drop_constraint('fk_categories_incomes_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('categories_expenses') as batch_op:
        batch_op.drop_constraint('fk_categories_expenses_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    # Удаляем таблицу пользователей
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
