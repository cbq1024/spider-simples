docker run -d -p 27017:27017 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=cxk -e MONGO_INITDB_ROOT_PASSWORD=jntm

docker run -d -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=db  mysql
