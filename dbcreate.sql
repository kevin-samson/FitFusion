#DROP database project;
use project;
create database project;

delimiter \\
CREATE TRIGGER calculate_bmi
before INSERT ON user_details
FOR EACH ROW
BEGIN
  SET new.bmi = ROUND(NEW.weight / ((NEW.height / 100) * (NEW.height / 100)), 2);
END\\

delimiter ;

delimiter \\
CREATE TRIGGER update_bmi_on_update
BEFORE UPDATE ON user_details
FOR EACH ROW
BEGIN
  SET NEW.bmi = ROUND(NEW.weight / ((NEW.height / 100) * (NEW.height / 100)), 2);
END\\
delimiter ;

drop TRIGGER update_calculate_bmi;

select * from user;

delete from user_details where user_id=1;
insert into user_details values (1,44,22,null,null);

select * from user_details;

INSERT INTO food (food_name, food_cal) VALUES ('hamburger', 300), ('french fries', 200), ('chicken nuggets', 250), ('onion rings', 400), ('milkshake', 500);
insert into exercise_catogory (exercise_catogory_name) values ("Cross Fit"),("Weight Training"),("HIIT");
insert into exercise (exercise_name,exercise_catogory_id,exercise_cal) values ("Jumping Jacks",2,100);
insert into trainer (trainer_name) values ("Sarah Miller") , ("Jhon Doe"),("Sarah Jay");

select * from exercise natural join exercise_catogory ;