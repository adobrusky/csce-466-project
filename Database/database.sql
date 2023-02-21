CREATE DATABASE store;

USE store;

CREATE TABLE customers (
  id int(11) NOT NULL AUTO_INCREMENT,
  first_name varchar(256),
  last_name varchar(256),
  address varchar(256),
  city varchar(256),
  state varchar(256),
  postal_code varchar(256),
  country varchar(256),
  email varchar(256),
  success boolean,
  message varchar(256),
  PRIMARY KEY (id)
);

CREATE TABLE products (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(256),
  price float,
  success boolean,
  message varchar(256),
  PRIMARY KEY (id)
);
 
CREATE TABLE transactions (
  id int(11) NOT NULL AUTO_INCREMENT,
  customer_id int(11) NOT NULL,
  date date,
  success boolean,
  message varchar(256),
  FOREIGN KEY (customer_id) REFERENCES customers (id),
  PRIMARY KEY (id)
);

CREATE TABLE product_transactions (
  product_id int(11) NOT NULL,
  transaction_id int(11) NOT NULL,
  quantity int(11),
  success boolean,
  message varchar(256),
  FOREIGN KEY (product_id) REFERENCES products (id),
  FOREIGN KEY (transaction_id) REFERENCES transactions (id),
  PRIMARY KEY (product_id, transaction_id)
);

INSERT INTO customers(
  id,
  first_name, 
  last_name, 
  address, 
  city, 
  state, 
  postal_code, 
  country, 
  email, 
  success, 
  message
) VALUES
  (1, 'David', 'Garcia', '181 East Avenue', 'Tempe', 'AZ', '85281', 'USA', 'DavidMGarcia@teleworm.us', NULL, NULL),
  (2, 'Pabil', 'Rico', 'BRAVO 390', 'REFORMA', 'SINALOA', NULL,'Mexico', 'PabilZamudioRico@dayrep.com', NULL, NULL),
  (3, 'Sheryl', 'Pruitt', '3970 Dominion St', 'Williamsburg', 'ON', 'K0C 2H0', 'Canada', 'SherylAPruitt@teleworm.us', NULL, NULL),
  (4, 'Hubert', 'Allen', '4139 Chestnut Street', 'Saint Petersburg', 'FL', '33710', 'USA', 'HubertLAllen@rhyta.com', NULL, NULL),
  (5, 'Miguel', 'Brown', '2425 Bassel Street', 'New Orleans', 'LA', '70113', 'USA', NULL, NULL, NULL),
  (6, 'Lillian', 'Eckstein', '1843 Lynden Road', 'Gormley', 'ON', 'L0H 1G0', 'Canada', 'LillianCEckstein@armyspy.com', NULL, NULL),
  (7, 'Chris', 'Riggs', '3121 Abia Martin Drive', 'Ronkonkoma', 'NY', '11779', 'USA', 'ChrisLRiggs@armyspy.com', NULL, NULL),
  (8, 'Marco', 'Begley', '1421 Ashton Lane', 'Austin', 'TX', '78744', 'USA', 'MarcoKBegley@rhyta.com', NULL, NULL),
  (9, 'Richard', 'Montes', '3473 Elgin Street', 'Lansdowne', 'ON', 'K0E 1L0', 'Canada', 'RichardEMontes@dayrep.com', NULL, NULL),
  (10, 'Guy', 'Kramer', '4344 Central Pkwy', 'Mississauga', 'ON', 'L5L 5S1', 'Canada', NULL, NULL, NULL),
  (11, 'Lynda', 'Lang', '31 Benson Park Drive', 'Oklahoma City', 'OK', '73109', 'USA', 'JoaneRHorton@jourrapide.com', NULL, NULL),
  (12, 'Salvador', 'Zambrano', 'EMILIO CARRANZA 1222 A', 'REFORMA', 'Oaxaca', NULL,'Mexico', 'SalvadorAguileraZambrano@rhyta.com', NULL, NULL);

INSERT INTO products(
  id,
  name,
  price,
  success, 
  message
) VALUES
(1, 'Large Chocolate Chip Cookie', 3.99, NULL, NULL),
(2, 'Large M&M Cookie', 3.99, NULL, NULL),
(3, 'Large Peanut Butter Cookie', 3.99, NULL, NULL),
(4, '12-oz Frappuccino', 6.5, NULL, NULL),
(5, '8-oz Frappuccino', 5.99, NULL, NULL),
(6, '12-oz Cappuccino', 6.5, NULL, NULL),
(7, '8-oz Cappuccino', 5.99, NULL, NULL),
(8, '12-oz Iced Latte', 6.5, NULL, NULL),
(9, '8-oz Iced Latte', 5.99, NULL, NULL),
(10, 'Croissant', 1.99, NULL, NULL),
(11, 'Bagel', 1.99, NULL, NULL),
(12, 'Banana Bread Muffin', 1.99, NULL, NULL),
(13, 'Breakfast Sandwich', 4.99, NULL, NULL),
(14, 'Glazed Donut', 1.99, NULL, NULL),
(15, 'Large Oatmeal Raisin Cookie', 3.99, NULL, NULL),
(16, 'Apple Fritter', 2.99, NULL, NULL),
(17, 'Large Sugar Cookie', 3.99, NULL, NULL),
(18, 'Chocolate Cupcake', 2.99, NULL, NULL),
(19, 'Strawberry Cupcake', 2.99, NULL, NULL);

INSERT INTO transactions(
  id,
  customer_id,
  date,
  success,
  message
) VALUES
(1, 1, '2022-02-09', NULL, NULL),
(2, 2, '2022-02-10', NULL, NULL),
(3, 3, '2022-02-10', NULL, NULL),
(4, 2, '2022-02-10', NULL, NULL),
(5, 4, '2022-02-12', NULL, NULL),
(6, 4, '2022-02-12', NULL, NULL),
(7, 10, '2022-02-12', NULL, NULL),
(8, 10, '2022-02-15', NULL, NULL),
(9, 12, '2022-02-15', NULL, NULL),
(10, 6, '2022-02-15', NULL, NULL),
(11, 8, '2022-02-15', NULL, NULL),
(12, 3, '2022-02-23', NULL, NULL),
(13, 7, '2022-02-23', NULL, NULL),
(14, 2, '2022-02-23', NULL, NULL),
(15, 1, '2022-02-23', NULL, NULL),
(16, 6, '2022-02-28', NULL, NULL),
(17, 11, '2022-02-28', NULL, NULL),
(18, 12, '2022-02-28', NULL, NULL),
(19, 2, '2022-03-05', NULL, NULL),
(20, 6, '2022-03-05', NULL, NULL),
(21, 12, '2022-03-08', NULL, NULL),
(22, 2, '2022-03-08', NULL, NULL),
(23, 3, '2022-03-09', NULL, NULL),
(24, 2, '2022-03-09', NULL, NULL),
(25, 6, '2022-03-14', NULL, NULL),
(26, 9, '2022-03-14', NULL, NULL),
(27, 4, '2022-03-14', NULL, NULL),
(28, 12, '2022-03-21', NULL, NULL),
(29, 2, '2022-03-21', NULL, NULL),
(30, 10, '2022-03-25', NULL, NULL),
(31, 1, '2022-03-25', NULL, NULL),
(32, 2, '2022-03-25', NULL, NULL),
(33, 3, '2022-03-25', NULL, NULL),
(34, 2, '2022-03-29', NULL, NULL),
(35, 4, '2022-03-29', NULL, NULL),
(36, 4, '2022-03-29', NULL, NULL),
(37, 10, '2022-04-02', NULL, NULL),
(38, 10, '2022-04-02', NULL, NULL),
(39, 12, '2022-04-02', NULL, NULL),
(40, 6, '2022-04-03', NULL, NULL),
(41, 8, '2022-04-03', NULL, NULL),
(42, 3, '2022-04-03', NULL, NULL),
(43, 7, '2022-04-05', NULL, NULL),
(44, 2, '2022-04-05', NULL, NULL),
(45, 1, '2022-04-05', NULL, NULL),
(46, 6, '2022-04-07', NULL, NULL),
(47, 11, '2022-04-07', NULL, NULL),
(48, 12, '2022-04-07', NULL, NULL),
(49, 2, '2022-04-07', NULL, NULL),
(50, 6, '2022-04-09', NULL, NULL),
(51, 2, '2022-04-09', NULL, NULL),
(52, 2, '2022-04-10', NULL, NULL),
(53, 3, '2022-04-10', NULL, NULL),
(54, 2, '2022-04-13', NULL, NULL),
(55, 6, '2022-04-12', NULL, NULL),
(56, 9, '2022-04-12', NULL, NULL),
(57, 4, '2022-04-14', NULL, NULL),
(58, 12, '2022-04-14', NULL, NULL),
(59, 2, '2022-04-14', NULL, NULL),
(60, 10, '2022-04-14', NULL, NULL),
(61, 1, '2022-04-15', NULL, NULL),
(62, 2, '2022-04-15', NULL, NULL),
(63, 3, '2022-04-15', NULL, NULL),
(64, 2, '2022-04-16', NULL, NULL),
(65, 4, '2022-04-17', NULL, NULL),
(66, 4, '2022-04-17', NULL, NULL),
(67, 10, '2022-04-18', NULL, NULL),
(68, 10, '2022-04-18', NULL, NULL),
(69, 12, '2022-04-18', NULL, NULL),
(70, 6, '2022-04-18', NULL, NULL),
(71, 8, '2022-04-19', NULL, NULL),
(72, 3, '2022-04-19', NULL, NULL),
(73, 7, '2022-04-21', NULL, NULL),
(74, 2, '2022-04-21', NULL, NULL),
(75, 1, '2022-04-21', NULL, NULL),
(76, 6, '2022-04-24', NULL, NULL),
(77, 11, '2022-04-24', NULL, NULL),
(78, 12, '2022-04-24', NULL, NULL),
(79, 2, '2022-04-24', NULL, NULL),
(80, 6, '2022-04-24', NULL, NULL),
(81, 3, '2022-04-26', NULL, NULL),
(82, 2, '2022-04-26', NULL, NULL),
(83, 3, '2022-04-26', NULL, NULL),
(84, 2, '2022-04-28', NULL, NULL),
(85, 6, '2022-04-28', NULL, NULL),
(86, 9, '2022-04-28', NULL, NULL),
(87, 4, '2022-05-01', NULL, NULL),
(88, 12, '2022-05-01', NULL, NULL),
(89, 2, '2022-05-01', NULL, NULL),
(90, 10, '2022-05-01', NULL, NULL);

INSERT INTO product_transactions(
  product_id,
  transaction_id,
  quantity,
  success,
  message
) VALUES
(1, 1, 3, NULL, NULL),
(1, 31, 3, NULL, NULL),
(1, 61, 3, NULL, NULL),
(2, 1, 1, NULL, NULL),
(2, 10, 1, NULL, NULL),
(2, 13, 2, NULL, NULL),
(2, 18, 3, NULL, NULL),
(2, 30, 8, NULL, NULL),
(2, 31, 1, NULL, NULL),
(2, 40, 1, NULL, NULL),
(2, 43, 2, NULL, NULL),
(2, 48, 3, NULL, NULL),
(2, 60, 8, NULL, NULL),
(2, 61, 1, NULL, NULL),
(2, 70, 1, NULL, NULL),
(2, 73, 2, NULL, NULL),
(2, 78, 3, NULL, NULL),
(2, 90, 8, NULL, NULL),
(3, 1, 2, NULL, NULL),
(3, 7, 1, NULL, NULL),
(3, 17, 5, NULL, NULL),
(3, 26, 4, NULL, NULL),
(3, 31, 2, NULL, NULL),
(3, 37, 1, NULL, NULL),
(3, 47, 5, NULL, NULL),
(3, 56, 4, NULL, NULL),
(3, 61, 2, NULL, NULL),
(3, 67, 1, NULL, NULL),
(3, 77, 5, NULL, NULL),
(3, 86, 4, NULL, NULL),
(4, 2, 1, NULL, NULL),
(4, 13, 2, NULL, NULL),
(4, 18, 2, NULL, NULL),
(4, 20, 5, NULL, NULL),
(4, 32, 1, NULL, NULL),
(4, 43, 2, NULL, NULL),
(4, 48, 2, NULL, NULL),
(4, 50, 5, NULL, NULL),
(4, 62, 1, NULL, NULL),
(4, 73, 2, NULL, NULL),
(4, 78, 2, NULL, NULL),
(4, 80, 5, NULL, NULL),
(5, 8, 2, NULL, NULL),
(5, 11, 2, NULL, NULL),
(5, 38, 2, NULL, NULL),
(5, 41, 2, NULL, NULL),
(5, 68, 2, NULL, NULL),
(5, 71, 2, NULL, NULL),
(6, 12, 2, NULL, NULL),
(6, 26, 2, NULL, NULL),
(6, 42, 2, NULL, NULL),
(6, 56, 2, NULL, NULL),
(6, 72, 2, NULL, NULL),
(6, 86, 2, NULL, NULL),
(7, 16, 1, NULL, NULL),
(7, 26, 2, NULL, NULL),
(7, 46, 1, NULL, NULL),
(7, 56, 2, NULL, NULL),
(7, 76, 1, NULL, NULL),
(7, 86, 2, NULL, NULL),
(8, 3, 2, NULL, NULL),
(8, 8, 2, NULL, NULL),
(8, 11, 4, NULL, NULL),
(8, 20, 2, NULL, NULL),
(8, 29, 3, NULL, NULL),
(8, 33, 2, NULL, NULL),
(8, 38, 2, NULL, NULL),
(8, 41, 4, NULL, NULL),
(8, 50, 2, NULL, NULL),
(8, 59, 3, NULL, NULL),
(8, 63, 2, NULL, NULL),
(8, 68, 2, NULL, NULL),
(8, 71, 4, NULL, NULL),
(8, 80, 2, NULL, NULL),
(8, 89, 3, NULL, NULL),
(9, 5, 1, NULL, NULL),
(9, 35, 1, NULL, NULL),
(9, 65, 1, NULL, NULL),
(10, 4, 2, NULL, NULL),
(10, 9, 6, NULL, NULL),
(10, 14, 6, NULL, NULL),
(10, 23, 2, NULL, NULL),
(10, 34, 2, NULL, NULL),
(10, 39, 6, NULL, NULL),
(10, 44, 6, NULL, NULL),
(10, 53, 2, NULL, NULL),
(10, 64, 2, NULL, NULL),
(10, 69, 6, NULL, NULL),
(10, 74, 6, NULL, NULL),
(10, 83, 2, NULL, NULL),
(11, 10, 3, NULL, NULL),
(11, 40, 3, NULL, NULL),
(11, 70, 3, NULL, NULL),
(12, 5, 3, NULL, NULL),
(12, 11, 4, NULL, NULL),
(12, 20, 2, NULL, NULL),
(12, 23, 3, NULL, NULL),
(12, 35, 3, NULL, NULL),
(12, 41, 4, NULL, NULL),
(12, 50, 2, NULL, NULL),
(12, 53, 3, NULL, NULL),
(12, 65, 3, NULL, NULL),
(12, 71, 4, NULL, NULL),
(12, 80, 2, NULL, NULL),
(12, 83, 3, NULL, NULL),
(13, 20, 4, NULL, NULL),
(13, 30, 5, NULL, NULL),
(13, 50, 4, NULL, NULL),
(13, 60, 5, NULL, NULL),
(13, 80, 4, NULL, NULL),
(13, 90, 5, NULL, NULL),
(14, 6, 4, NULL, NULL),
(14, 15, 1, NULL, NULL),
(14, 19, 8, NULL, NULL),
(14, 24, 1, NULL, NULL),
(14, 36, 4, NULL, NULL),
(14, 45, 1, NULL, NULL),
(14, 49, 8, NULL, NULL),
(14, 54, 1, NULL, NULL),
(14, 66, 4, NULL, NULL),
(14, 75, 1, NULL, NULL),
(14, 79, 8, NULL, NULL),
(14, 84, 1, NULL, NULL),
(15, 6, 2, NULL, NULL),
(15, 15, 1, NULL, NULL),
(15, 23, 3, NULL, NULL),
(15, 27, 1, NULL, NULL),
(15, 36, 2, NULL, NULL),
(15, 45, 1, NULL, NULL),
(15, 53, 3, NULL, NULL),
(15, 57, 1, NULL, NULL),
(15, 66, 2, NULL, NULL),
(15, 75, 1, NULL, NULL),
(15, 83, 3, NULL, NULL),
(15, 87, 1, NULL, NULL),
(16, 6, 1, NULL, NULL),
(16, 16, 2, NULL, NULL),
(16, 21, 2, NULL, NULL),
(16, 36, 1, NULL, NULL),
(16, 46, 2, NULL, NULL),
(16, 51, 2, NULL, NULL),
(16, 66, 1, NULL, NULL),
(16, 76, 2, NULL, NULL),
(16, 81, 2, NULL, NULL),
(17, 21, 3, NULL, NULL),
(17, 28, 2, NULL, NULL),
(17, 51, 3, NULL, NULL),
(17, 58, 2, NULL, NULL),
(17, 81, 3, NULL, NULL),
(17, 88, 2, NULL, NULL),
(18, 21, 1, NULL, NULL),
(18, 25, 4, NULL, NULL),
(18, 51, 1, NULL, NULL),
(18, 55, 4, NULL, NULL),
(18, 81, 1, NULL, NULL),
(18, 85, 4, NULL, NULL),
(19, 22, 1, NULL, NULL),
(19, 25, 4, NULL, NULL),
(19, 52, 1, NULL, NULL),
(19, 55, 4, NULL, NULL),
(19, 82, 1, NULL, NULL),
(19, 85, 4, NULL, NULL);
