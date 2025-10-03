-- Este script cria a tabela para armazenar as leituras dos sensores.


CREATE TABLE IF NOT EXISTS leituras_sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Chave primária: um número único para cada linha, gerado automaticamente.
    timestamp INTEGER NOT NULL,            -- O timestamp original que coletamos (em ms). Não pode ser nulo.
    temperatura REAL NOT NULL,             -- O valor da temperatura. REAL é um número com casas decimais. Não pode ser nulo.
    umidade REAL NOT NULL,                 -- O valor da umidade. Não pode ser nulo.
    data_leitura TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- A data e hora exatas em que o dado foi inserido no banco.
);