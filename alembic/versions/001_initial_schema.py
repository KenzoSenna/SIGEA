from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'andares',
        sa.Column('id_andar', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('numero', sa.Integer, nullable=False),
        sa.Column('descricao', sa.String(200), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Criar tabela de usuários
    op.create_table(
        'usuarios',
        sa.Column('id_usuario', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('senha_hash', sa.String(255), nullable=False),
        sa.Column('tipo', sa.Enum('aluno', 'professor', 'coordenador', name='tipousuario'), nullable=False, default='aluno'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_usuarios_email', 'usuarios', ['email'])
    
    # Criar tabela de salas
    op.create_table(
        'salas',
        sa.Column('id_sala', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(50), nullable=False),
        sa.Column('capacidade', sa.Integer, nullable=False),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('status', sa.Enum('ativa', 'manutencao', 'inativa', name='statussala'), nullable=False, default='ativa'),
        sa.Column('horario_inicio', sa.Time, nullable=False),
        sa.Column('horario_fim', sa.Time, nullable=False),
        sa.Column('id_andar', sa.Integer, sa.ForeignKey('andares.id_andar'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Criar tabela de eventos
    op.create_table(
        'eventos',
        sa.Column('id_evento', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('descricao', sa.String(255), nullable=True),
        sa.Column('data', sa.Date, nullable=False),
        sa.Column('hora_inicio', sa.Time, nullable=False),
        sa.Column('hora_fim', sa.Time, nullable=False),
        sa.Column('id_sala', sa.Integer, sa.ForeignKey('salas.id_sala'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Criar tabela de reservas
    op.create_table(
        'reservas',
        sa.Column('id_reserva', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('id_sala', sa.Integer, sa.ForeignKey('salas.id_sala'), nullable=False),
        sa.Column('id_disciplina', sa.Integer, nullable=False),
        sa.Column('id_usuario', sa.Integer, sa.ForeignKey('usuarios.id_usuario'), nullable=False),
        sa.Column('descricao', sa.String(255), nullable=True),
        sa.Column('tipo_reserva', sa.Enum('diaria', 'semestral', name='tiporeserva'), nullable=False),
        sa.Column('data', sa.Date, nullable=True),
        sa.Column('horario_inicio', sa.Time, nullable=True),
        sa.Column('horario_fim', sa.Time, nullable=True),
        sa.Column('data_inicio', sa.Date, nullable=True),
        sa.Column('data_fim', sa.Date, nullable=True),
        sa.Column('dias_semana', sa.JSON, nullable=True),
        sa.Column('horarios', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('reservas')
    op.drop_table('eventos')
    op.drop_table('salas')
    op.drop_table('usuarios')
    op.drop_table('andares')
