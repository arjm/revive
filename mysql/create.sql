CREATE DATABASE IF NOT EXISTS campaign;

CREATE TABLE  IF NOT EXISTS `voucher_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(100) NOT NULL,
  `total_orders` int(11) NOT NULL,
  `voucher_amount` float NOT NULL, 
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
