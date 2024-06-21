FROM nginx:1.23

ARG TEMPLATE_NAME=default

COPY ${TEMPLATE_NAME}.conf.template /etc/nginx/templates/default.conf.template
RUN mkdir /statics /media_files
