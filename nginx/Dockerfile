FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 443

COPY ssl/ /etc/ssl/
COPY webapp.conf /etc/nginx/conf.d/
