create database XYZ;
USE  XYZ;
drop table EMPLOYEE;


INSERT INTO employee(ID, NAME, SALARY)
values
(1, "adam", 25000),
(2, "bob", 30000),
(3, "casey", 40000);
select * from employee;

create table flights(
id INT PRIMARY KEY,
NAME VARCHAR(50),
CAPACITY int

);

INSERT INTO flights
VALUES
(1002,"indigo", 10000),
(1003,"VISTARA", 20000),
(1004,"AKASA", 30000);
DROP table flights;
select * from flights;

CREATE TABLE student(
ID INT PRIMARY KEY,
NAME VARCHAR(50)
);



INSERT INTO student(ID, NAME)
values
(101, "adam"),
(102, "bob" ),
(103, "casey");
truncate table student; 

CREATE TABLE course(
ID INT PRIMARY KEY,
 course VARCHAR(50)
);
INSERT INTO course(ID, course)
values
(102, "english"),
(105, "science" ),
(103, "maths"),
(107,"computer science");

select * from student
inner join course
on student.id=course.id;
select * 
from student as s
left join course as c
on s.id = c.id;

select * 
from student as s
right join course as c
on s.id = c.id;
select * from student;
select * from course;
select * from student as a
left join course as b
on a.id=b.id
union 
select * from student as a
right join course as b
on a.id =  b.id;

select * from student as a
left join course as b
on a.id=b.id
where b.id is null;

select * from student as a
right join course as b
on a.id=b.id
where a.id is null;

select * from student as a
left join course as b
on a.id=b.id
where b.id is null
Union
select * from student as a
right join course as b
on a.id=b.id
where a.id is null;

CREATE TABLE EMPLOYEE(
ID INT PRIMARY KEY,
NAME VARCHAR(50),
manager_id INT
);
select * from employee;
insert into EMPLOYEE(ID, NAME, manager_id)
values
(101,"adam",103),
(102,"bob",104),
(103,"casey",NULL),
(104,"donald",103);

select a.name as manager_name, b.name
from employee as a
join employee as b
on a.id =  b.manager_id;

select name from employee
union all
select name from student;
