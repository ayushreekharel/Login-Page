create database login_signup;
use login_signup;
create table login_signup(
id int primary key auto_increment,
first_name varchar(20),
middle_name varchar(20) null,
last_name varchar(20),
phone_no decimal(12,2),
email varchar(40),
username varchar(20),
set_password varchar(20),
confirm_password varchar(20)
);

select * from login_signup;




