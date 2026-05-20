mysql ``` CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo ENUM('aluno', 'professor', 'coordenador') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE andar (
    id_andar INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL
);

CREATE TABLE sala (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    capacidade INT,
    tipo VARCHAR(50),

    status ENUM('ativa', 'manutencao') DEFAULT 'ativa',

    horario_inicio TIME,
    horario_fim TIME,

    id_andar INT NOT NULL,

    FOREIGN KEY (id_andar)
        REFERENCES andar(id_andar)
        ON DELETE CASCADE
);

-- =========================
-- DISCIPLINA
-- =========================
CREATE TABLE disciplina (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20)
);
CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,

    data_inicio DATETIME NOT NULL,
    data_fim DATETIME NOT NULL,

    descricao TEXT,

    status ENUM('ativa', 'cancelada', 'concluida') DEFAULT 'ativa',

    id_sala INT NOT NULL,
    id_usuario INT NOT NULL,
    id_disciplina INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_sala)
        REFERENCES sala(id_sala)
        ON DELETE CASCADE,

    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE,

    FOREIGN KEY (id_disciplina)
        REFERENCES disciplina(id_disciplina)
        ON DELETE SET NULL,

    CONSTRAINT chk_datas_validas
        CHECK (data_fim > data_inicio)
);

CREATE TABLE evento (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,

    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,

    data_inicio DATETIME NOT NULL,
    data_fim DATETIME NOT NULL,

    tipo VARCHAR(50),
    destaque BOOLEAN DEFAULT FALSE,

    id_sala INT NOT NULL,
    id_usuario INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_sala)
        REFERENCES sala(id_sala)
        ON DELETE CASCADE,

    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE SET NULL,

    CONSTRAINT chk_datas_evento
        CHECK (data_fim > data_inicio)

);

CREATE TABLE usuario_evento (
    id_usuario INT NOT NULL,
    id_evento INT NOT NULL,

    data_participacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id_usuario, id_evento),

    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE,

    FOREIGN KEY (id_evento)
        REFERENCES evento(id_evento)
        ON DELETE CASCADE
);

CREATE INDEX idx_reserva_sala_tempo
ON reserva (id_sala, data_inicio, data_fim);

CREATE INDEX idx_reserva_usuario
ON reserva (id_usuario);

CREATE INDEX idx_evento_sala
ON evento (id_sala);```