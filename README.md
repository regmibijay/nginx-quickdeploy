# NGINX QUICKDEPLOY

## About

Helps you create and deploy websites on nginx quickly. 

## Installation
`pip3 install nginx-quickdeploy` 

## Usage
Variables:
- 'FQDN' : Fully Qualified Domain Name, name of your website
- Nginx config path: Path where your generated config file is stored.
- Ports: Ports to listen to, in format: `<port1> [ssl], <port2> [ssl]`
- Root path: Path where your html files are located
- Proxy: If your actual application is running on some other port, you can proxy pass and use nginx as webserver. For that just use this function, if not leave it empty

## Tips and Examples
Invoke the script with sudo rights if you want to write to `/etc/ngnix/sites-available` as it is write protected for non sudo users.

`# sudo quickdeploy`
```
FQDN of your domain, e.g. example.com or subdomain.example.com without http or https:  www.example.org
Where should the new config file be saved?, default is /etc/nginx/sites-available/www.example.org :
Ports separated by commas(,) in nginx fashion, like 80, [::]:80 etc
For ssl, just add ssl after the port, e.g. 80, 443 ssl, [::]:80, [::]:443 ssl
Enter ports here:
Enter the www root path(default /var/www/html):
Should this server need to proxy_pass, enter the address here:

Your new website was deployed successfully
Restart nginx to serve it via nginx.
```
would yield a config file that looks like this:
```
server {
  root /var/www/html;
  server_name www.example.org;
  listen 80;
   location / {
       try_files $uri $uri/;
   }
}
```
