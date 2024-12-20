CREATE TABLE Module (
    Id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL
);

CREATE TABLE Accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    moduleId INT,
    FOREIGN KEY (moduleId) REFERENCES Module(Id)
);

CREATE TABLE History (
    accountId INT,
    amount DECIMAL(15, 2) NOT NULL,
    pru DECIMAL(15, 2),
    capitalGain DECIMAL(15, 2),
    date DATE NOT NULL,
    FOREIGN KEY (accountId) REFERENCES Accounts(id)
);