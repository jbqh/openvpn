#openvpn.sql

drop database if exists openvpn;
create database if not exists openvpn;
grant all privileges on openvepn.* to 'openvpn'@'localhost' identified by 'vdin1234';
grant all privileges on openvepn.* to 'openvepn'@'172.16.172.%' identified by 'vdin1234';

drop table if exists openvpn.users;
create table if not exists openvpn.users (
	id int(11) unsigned auto_increment,
	username varchar(20) not null,
	password varchar(50) not null default '',
	display_name varchar(20) not null,
	logins int(11) unsigned not null default 0,
	locked varchar(1) not null default '0',
	allow_login datetime not null,
	deration int(11) unsigned not null default 0,
	received int(11) unsigned not null default 0,
	sent int(11) unsigned not null default 0,
	last_login datetime not null,
	last_ip char(15) not null default '0.0.0.0',
	quota int(11) unsigned not null default 0,
	primary key (id) 
	) engine=innodb;
	
drop table if exists openvpn.logins;
create table if not exists openvpn.logins (
	id int(11) unsigned auto_increment,
	username varchar(20) not null,
	login_time datetime not null,
	login_ip varchar(15) not null default '0.0.0.0',
	logout_time datetime not null,
	received int(11) unsigned not null default 0,
	sent int(11) unsigned not null default 0,
	primary key (id)
	) engine=innodb;
	
drop table if exists openvpn.logs;
create table if not exists openvpn.logs (
	id int(11)  unsigned auto_increment,
	log_type varchar(20) not null,
	log_time datetime not null,
	log_opt varchar(20) not null,
	log_memo varchar(255) not null,
	primary key (id)
	) engine=innodb;

drop table if exists openvpn.routes;
create table if not exists openvpn.routes (
	id int(11) unsigned auto_increment,
	network char(13) not null default '0.0.0.0',
	net_prefix tinyint not null default 24,
	used varchar(255) not null,
	primary key (id)
	) engine=innodb;

drop table if exists openvpn.routings;
create table if not exists openvpn.routings (
	id int(11) unsigned auto_increment,
	routeid int (11) unsigned,
	users varchar(20),
	primary key (id)
	) engine=innodb;
