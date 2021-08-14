# NGINX QUICKDEPLOY

## About

Helps you create and deploy websites on nginx quickly. 

## Installation
`pip3 install nginx-quickdeploy` 

## Usage
### Variables:
- 'FQDN' : Fully Qualified Domain Name, name of your website
- Nginx config path: Path where your generated config file is stored.
- Ports: Ports to listen to, in format: `<port1> [ssl], <port2> [ssl]`
- Root path: Path where your html files are located
- Proxy: If your actual application is running on some other port, you can proxy pass and use nginx as webserver. For that just use this function, if not leave it empty

### JSON input:
Json input is also supported for easier deployment. Following keys are supported:
- url : mandatory : provide FQDN 
- path : optional : provide path to be written config, default /etc/nginx/sites-available/{URL}
- ports : optional, list : provide ports to listen and with ssl or not, default 80 on both interfaces
- root : optional : path to webroot folder, default /var/www/html/{url}
- proxy : optional : path to http proxy if you have an app running behind nginx
- ssl_cert_path : optional : SSL cert path if you have ssl enabled
- ssl_key_path : optional : SSL key path if you have ssl enabled

#### Json example
  ```
  {
    "url": "www.example.org",
    "path": "/usr/shared/www.example.org",
    "ports": ["80", "[::]:80", "443 ssl", "[::]:443 ssl"],
    "root": "/var/www/html",
    "proxy": "https://app.example.org:8080",
    "ssl_cert_path": "/etc/ssl/myexample.org/cert.crt",
    "ssl_key_path": "/etc/ssl/myexample.org/key.pem" 
  }
  ``` 
  yields:
  ```
  server {
  root /var/www/html;
  index index.html index.htm index.nginx-debian.html;
  server_name www.example.org;
  listen 80;
  listen [::]:80;
  listen 443 ssl;
  listen [::]:443 ssl;
  ssl_certificate /etc/ssl/myexample.org/cert.crt;
  ssl_certificate_key /etc/ssl/myexample.org/key.pem;
  location / {
    proxy_pass https://app.example.org:8080;
    }
  }
  ```
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
