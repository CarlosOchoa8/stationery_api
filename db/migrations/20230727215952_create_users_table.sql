-- migrate:up
CREATE TABLE "user"
(
   id integer generated always as identity primary key,
   first_name varchar(255) not null,
   last_name varchar(255) not null,
   email varchar(255) not null,
   password varchar(255) not null,
   phone_number varchar(13) not null
);

-- migrate:down
DROP TABLE "user"