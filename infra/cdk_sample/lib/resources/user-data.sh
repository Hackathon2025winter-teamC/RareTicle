#!/bin/bash

yum -y update
yum -y install php httpd mysql

PHP_VERSION=`php -v | head -n 1 | awk '{print $2}' | awk -F "." '{print $1}'`
while [  ${PHP_VERSION} -ne 7 ]
do
amazon-linux-extras install php7.4 -y
PHP_VERSION=`php -v | head -n 1 | awk '{print $2}' | awk -F "." '{print $1}'`
done

yum -y install php-mbstring php-xml

wget http://ja.wordpress.org/latest-ja.tar.gz -P /tmp/
tar zxvf /tmp/latest-ja.tar.gz -C /tmp
cp -r /tmp/wordpress/* /var/www/html/
chown apache:apache -R /var/www/html

systemctl enable httpd.service
systemctl start httpd.service