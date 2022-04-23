-- init CDN File CDNManager DB

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS cdn_server (
    server_id varchar(100) PRIMARY KEY ,
    server_ip varchar(45),
    server_path text,
    secret_key varchar(36),
    description text,
    is_main boolean,
    stor_path text
);

CREATE TABLE IF NOT EXISTS film_file (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    server_id varchar(100) REFERENCES cdn_server(server_id) ON DELETE CASCADE,
    film_uuid varchar(36),
    quality varchar(10),
    length_sec int,
    url_path text,
    disk_path text
)
