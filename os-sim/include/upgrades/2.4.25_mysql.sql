use ossim;
SET AUTOCOMMIT=0;
BEGIN;

UPDATE `user_config` SET value = 'a:10:{s:2:\"ds\";a:40:{i:440;a:1:{s:5:\"notes\";N;}i:300;a:1:{s:5:\"notes\";s:0:\"\";}i:401;a:1:{s:5:\"notes\";N;}i:121;a:5:{s:3:\"top\";s:2:\"10\";s:10:\"sourcetype\";s:0:\"\";s:8:\"category\";s:1:\"0\";s:11:\"subcategory\";s:1:\"0\";s:5:\"notes\";s:0:\"\";}i:120;a:5:{s:3:\"top\";s:2:\"10\";s:10:\"sourcetype\";s:0:\"\";s:8:\"category\";s:1:\"0\";s:11:\"subcategory\";s:1:\"0\";s:5:\"notes\";s:0:\"\";}i:122;a:5:{s:3:\"top\";s:2:\"10\";s:10:\"sourcetype\";s:0:\"\";s:8:\"category\";s:1:\"0\";s:11:\"subcategory\";s:1:\"0\";s:5:\"notes\";s:0:\"\";}i:123;a:5:{s:3:\"top\";s:2:\"10\";s:10:\"sourcetype\";s:0:\"\";s:8:\"category\";s:1:\"0\";s:11:\"subcategory\";s:1:\"0\";s:5:\"notes\";s:0:\"\";}i:405;a:1:{s:5:\"notes\";N;}i:124;a:5:{s:3:\"top\";s:2:\"15\";s:10:\"sourcetype\";s:0:\"\";s:8:\"category\";s:1:\"0\";s:11:\"subcategory\";s:1:\"0\";s:5:\"notes\";s:0:\"\";}i:400;a:1:{s:5:\"notes\";N;}i:1029;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:406;a:1:{s:5:\"notes\";N;}i:1045;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:407;a:1:{s:5:\"notes\";N;}i:1032;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:408;a:1:{s:5:\"notes\";N;}i:1038;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:409;a:1:{s:5:\"notes\";N;}i:1047;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:410;a:1:{s:5:\"notes\";N;}i:1043;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:403;a:1:{s:5:\"notes\";N;}i:1028;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:404;a:1:{s:5:\"notes\";N;}i:1040;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1034;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1031;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1044;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1039;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1042;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1037;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1041;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1036;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1046;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1030;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1033;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:1099;a:2:{s:3:\"top\";s:2:\"25\";s:5:\"notes\";s:0:\"\";}i:1035;a:3:{s:3:\"top\";s:2:\"25\";s:10:\"sourcetype\";s:0:\"\";s:5:\"notes\";s:0:\"\";}i:402;a:1:{s:5:\"notes\";N;}i:128;a:5:{s:3:\"top\";s:3:\"100\";s:10:\"sourcetype\";s:0:\"\";s:8:\"category\";s:1:\"0\";s:11:\"subcategory\";s:1:\"0\";s:5:\"notes\";s:0:\"\";}}s:5:\"rname\";s:11:\"SIEM Report\";s:9:\"date_from\";s:10:\"2010-06-14\";s:7:\"date_to\";s:10:\"2010-07-14\";s:10:\"date_range\";s:6:\"last30\";s:7:\"profile\";s:7:\"Default\";s:5:\"cdate\";s:19:\"2010-05-07 18:34:28\";s:5:\"mdate\";s:19:\"2010-07-14 08:00:23\";s:4:\"user\";s:1:\"0\";s:6:\"assets\";s:8:\"ALL_ASSETS\";}' WHERE login='admin' AND category='custom_report' AND name='SIEM Report' AND value LIKE "%ENTITY:2%";

-- WARNING! Keep this at the end of this file
-- ATENCION! Keep this at the end of this file
use ossim;
REPLACE INTO config (conf, value) VALUES ('last_update', '2011-04-14');
REPLACE INTO config (conf, value) VALUES ('ossim_schema_version', '2.4.25');
COMMIT;
-- NOTHING BELOW THIS LINE / NADA DEBAJO DE ESTA LINEA
