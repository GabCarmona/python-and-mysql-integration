-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS FILMES_EP_DB2;
USE FILMES_EP_DB2;

-- Criação das tabelas
CREATE TABLE Evento (
    IDEvento INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Nacionalidade VARCHAR(255) NOT NULL,
    AnoInicio YEAR NOT NULL,
    Tipo VARCHAR(255) NOT NULL CHECK (Tipo IN ('Academia', 'Festival', 'Concurso'))
);

CREATE TABLE Edicao (
    IDEdicao INT AUTO_INCREMENT PRIMARY KEY,
    IDEvento INT NOT NULL,
    Ano YEAR NOT NULL,
    Localizacao VARCHAR(255) NOT NULL,
    DataRealizacao DATE NOT NULL,
    FOREIGN KEY (IDEvento) REFERENCES Evento(IDEvento)
);

CREATE TABLE Premio (
    IDPremio INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Tipo VARCHAR(255) NOT NULL,
    NomeConhecido VARCHAR(255),
    IDEdicao INT NOT NULL,
    FOREIGN KEY (IDEdicao) REFERENCES Edicao(IDEdicao)
);

CREATE TABLE Pessoa (
    IDPessoa INT AUTO_INCREMENT PRIMARY KEY,
    NomeArt VARCHAR(255),
    NomeReal VARCHAR(255) NOT NULL,
    Sexo CHAR(1) NOT NULL CHECK (Sexo IN ('M', 'F')),
    AnoNasc YEAR NOT NULL,
    Website VARCHAR(255),
    AnoInicio YEAR NOT NULL,
    Situacao VARCHAR(255) NOT NULL,
    AnosAtividade INT CHECK (AnosAtividade >= 0),
    UNIQUE (NomeArt)
);

CREATE TABLE Filme (
    IDFilme INT AUTO_INCREMENT PRIMARY KEY,
    TituloOriginal VARCHAR(255) NOT NULL,
    AnoProd INT NOT NULL,
    DataEstreia DATE NOT NULL,
    TituloNoBrasil VARCHAR(255),
    Classe VARCHAR(255) NOT NULL    ,
    IdiomaOriginal VARCHAR(255) NOT NULL,
    ArrecadacaoAnoInicial DECIMAL(19,2)
);

CREATE TABLE Pessoas_Nomeadas (
    IDNomeacao INT AUTO_INCREMENT PRIMARY KEY,
    IDEdicao INT NOT NULL,
    IDFilme INT NOT NULL,
    IDPremio INT NOT NULL,
    IDPessoa INT NOT NULL,
    Ganhou CHAR(1) NOT NULL CHECK (Ganhou IN ('S', 'N')),
    FOREIGN KEY (IDEdicao) REFERENCES Edicao(IDEdicao),
    FOREIGN KEY (IDFilme) REFERENCES Filme(IDFilme),
    FOREIGN KEY (IDPessoa) REFERENCES Pessoa(IDPessoa),
    FOREIGN KEY (IDPremio) REFERENCES Premio(IDPremio)
);

CREATE TABLE Filmes_Nomeados (
    IDNomeacaoFilme INT AUTO_INCREMENT PRIMARY KEY,
    IDEdicao INT NOT NULL,
    IDFilme INT NOT NULL,
    IDPremio INT NOT NULL,
    Premiado CHAR(1) NOT NULL CHECK (Premiado IN ('S', 'N')),
    FOREIGN KEY (IDEdicao) REFERENCES Edicao(IDEdicao),
    FOREIGN KEY (IDFilme) REFERENCES Filme(IDFilme),
    FOREIGN KEY (IDPremio) REFERENCES Premio(IDPremio)
);

CREATE TABLE Jurados (
    ID_edicao_pessoas INT AUTO_INCREMENT PRIMARY KEY,
    IDPessoa INT NOT NULL,
    IDEdicao INT NOT NULL,
    FOREIGN KEY (IDPessoa) REFERENCES Pessoa(IDPessoa),
    FOREIGN KEY (IDEdicao) REFERENCES Edicao(IDEdicao)
);

CREATE TABLE ProdutorFilme (
    IDProdutorFilme INT AUTO_INCREMENT PRIMARY KEY,
    IDPessoa INT NOT NULL,
    IDFilme INT NOT NULL,
    FOREIGN KEY (IDPessoa) REFERENCES Pessoa(IDPessoa),
    FOREIGN KEY (IDFilme) REFERENCES Filme(IDFilme)
);

CREATE TABLE RoteiristaFilme (
    IDRoteiristaFilme INT AUTO_INCREMENT PRIMARY KEY,
    IDPessoa INT NOT NULL,
    IDFilme INT NOT NULL,
    FOREIGN KEY (IDPessoa) REFERENCES Pessoa(IDPessoa),
    FOREIGN KEY (IDFilme) REFERENCES Filme(IDFilme)
);

CREATE TABLE DiretorFilme (
    IDDiretorFilme INT AUTO_INCREMENT PRIMARY KEY,
    IDPessoa INT NOT NULL,
    IDFilme INT NOT NULL,
    Principal BOOLEAN NOT NULL,
    FOREIGN KEY (IDPessoa) REFERENCES Pessoa(IDPessoa),
    FOREIGN KEY (IDFilme) REFERENCES Filme(IDFilme)
);

CREATE TABLE AtorFilme (
    IDAtorFilme INT AUTO_INCREMENT PRIMARY KEY,
    IDPessoa INT NOT NULL,
    IDFilme INT NOT NULL,
    Principal BOOLEAN NOT NULL,
    FOREIGN KEY (IDPessoa) REFERENCES Pessoa(IDPessoa),
    FOREIGN KEY (IDFilme) REFERENCES Filme(IDFilme)
);

CREATE TABLE Filmes_Locais_Estreia (
    IDLocalEstreia INT AUTO_INCREMENT PRIMARY KEY,
    IDFilme INT NOT NULL,
    LocalizacaoEstreia VARCHAR(255) NOT NULL,
    FOREIGN KEY (IDFilme) REFERENCES Filme(IDFilme)
);

-- Triggers
DELIMITER //

CREATE TRIGGER CheckDocumentaryActors BEFORE INSERT ON AtorFilme
FOR EACH ROW
BEGIN
    DECLARE filme_classe VARCHAR(255);
    SELECT Classe INTO filme_classe FROM Filme WHERE IDFilme = NEW.IDFilme;
    IF filme_classe = 'Documentario' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Um filme documentário não pode ter atores associados.';
    END IF;
END;
//

CREATE TRIGGER CheckJuradoBeforeInsert BEFORE INSERT ON Jurados
FOR EACH ROW
BEGIN
    DECLARE filme_participacao INT;
    SELECT COUNT(*) INTO filme_participacao FROM Pessoas_Nomeadas WHERE IDPessoa = NEW.IDPessoa AND IDEdicao = NEW.IDEdicao;
    IF filme_participacao > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Uma pessoa não pode ser jurado se participar de um filme indicado na mesma edição do evento.';
    END IF;
END;
//

CREATE TRIGGER CheckNomeacaoBeforeInsert BEFORE INSERT ON Pessoas_Nomeadas
FOR EACH ROW
BEGIN
    DECLARE jurado_participacao INT;
    SELECT COUNT(*) INTO jurado_participacao FROM Jurados WHERE IDPessoa = NEW.IDPessoa AND IDEdicao = NEW.IDEdicao;
    IF jurado_participacao > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Não é possível nomear uma pessoa que é jurado na mesma edição do evento.';
    END IF;
END;
//

DELIMITER ;
