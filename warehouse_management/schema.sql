DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS ProductMovement;

CREATE TABLE Product (
  product_id INTEGER PRIMARY KEY AUTOINCREMENT
  );

CREATE TABLE Location (
  location_id INTEGER PRIMARY KEY AUTOINCREMENT
  );

CREATE TABLE ProductMovement (
  movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  from_location INTEGER ,
  to_location INTEGER ,
  product_id INTEGER NOT NULL,
  qty INTEGER,
  FOREIGN KEY (movement_id) REFERENCES Product (product_id),
  FOREIGN KEY (from_location) REFERENCES Location (location_id),
  FOREIGN KEY (to_location) REFERENCES Location (location_id)
);