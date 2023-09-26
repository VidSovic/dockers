FROM python:3.11-alpine

RUN apk update && \
    apk add --no-cache \
    supervisor \
    curl \
    vim \
    nano \
    openssh

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
WORKDIR /usr/sbin/
RUN ssh-keygen -A && mkdir -p /run/sshd
WORKDIR /

RUN adduser -D -u 1001 -g 1001 -s /bin/sh www

COPY ./app /app

COPY config/supervisord.conf /etc/supervisord.conf
COPY config/id_rsa.pub /root/.ssh/authorized_keys

RUN chmod 700 /root/.ssh
RUN chmod 600 /root/.ssh/authorized_keys

RUN chown -R www:www /app

USER www
WORKDIR /app

USER root
RUN pip3 install -r requirements.txt

RUN find /app -type d -exec chmod 755 {} \;
RUN find /app -type f -exec chmod 644 {} \;

# Expose port 8000 for the Tornado server
EXPOSE 22 8889

# Run server.py when the container launches
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]