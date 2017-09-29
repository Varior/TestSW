CREATE DATABASE Users;

USE Users;

CREATE TABLE `Users`.`user_list` (
  `user_id` INT AUTO_INCREMENT,
  `user_name` VARCHAR(45),
  `user_email` VARCHAR(30),
  `user_phone` VARCHAR(15) NULL,
  `user_m_phone` VARCHAR(15) NULL,
  `user_status` TINYINT NULL, 
  PRIMARY KEY (`user_id`));

CREATE TABLE `Users`.`courses` (
  `course_id` INT AUTO_INCREMENT,
  `course_name` VARCHAR(45),
  `code` VARCHAR(10),
  `id_user` INT,
  PRIMARY KEY (`course_id`),
  FOREIGN KEY (id_user) REFERENCES user_list (user_id));


DELIMITER $$
CREATE PROCEDURE `create_user`(
  IN u_name VARCHAR(45),
  IN u_email VARCHAR(30),
  IN u_phone VARCHAR(15),
  IN u_m_phone VARCHAR(15),
  IN u_status TINYINT
)
BEGIN
  INSERT INTO user_list(`user_name`,`user_email`,`user_phone`,`user_m_phone`,`user_status`)
  VALUES(u_name,u_email,u_phone,u_m_phone,u_status);
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `create_course`(
  IN c_name VARCHAR(45),
  IN c_code VARCHAR(10),
  IN user_id INT
)
BEGIN
  INSERT INTO courses(`course_name`,`code`,`id_user`)
  VALUES(c_name,c_code,user_id);
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `find_all`()
BEGIN
  SELECT *
  FROM user_list
  ORDER BY user_id;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `select_user`(    
  IN user_uid INT
)
BEGIN
  SELECT * 
  FROM user_list
  WHERE user_id=user_uid;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `find_course`(
   IN user_uid INT
)
BEGIN
  SELECT *
  FROM courses
  WHERE id_user=user_uid;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `find_user`(
  IN f_name VARCHAR(45)
)
BEGIN
  SET @f = CONCAT(f_name,'%');
  SET @f_query:=CONCAT("SELECT * 
  FROM user_list
  WHERE user_name LIKE '", @f,"'");
  PREPARE f_query FROM @f_query;
  EXECUTE f_query;
  DEALLOCATE PREPARE f_query;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `update_user`(    
  IN user_uid INT,
  IN u_email VARCHAR(30),
  IN u_phone VARCHAR(15),
  IN u_m_phone VARCHAR(15),
  IN u_status VARCHAR(1)
)
BEGIN
  UPDATE user_list SET `user_email`= u_email,`user_phone`=u_phone,`user_m_phone`=u_m_phone,`user_status`=u_status
  WHERE user_id=user_uid;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `delete_course`(    
  IN id_course INT
)
BEGIN
  DELETE FROM courses
  WHERE course_id=user_uid;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `delete_user`(    
  IN id_duser INT
)
BEGIN
  DELETE FROM user_list
  WHERE user_id=id_duser;
  DELETE FROM courses
  WHERE id_user=id_duser;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `pagination`(    
  IN start INT,
  IN records INT
)
BEGIN
  SET @page_query:=CONCAT("SELECT * 
  FROM user_list
  ORDER BY user_id
  LIMIT ",start,", ",records);
  PREPARE page_query FROM @page_query;
  EXECUTE page_query;
  DEALLOCATE PREPARE page_query;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `count_all`()
BEGIN 
  SELECT COUNT(*)
  FROM user_list;
END$$
DELIMITER ;