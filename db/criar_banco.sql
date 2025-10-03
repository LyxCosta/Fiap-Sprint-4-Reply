-- Tabela para armazenar as leituras dos sensores.


CREATE TABLE IF NOT EXISTS leituras_sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    timestamp INTEGER NOT NULL,            
    temperatura REAL NOT NULL,             
    umidade REAL NOT NULL,                 
    data_leitura TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);