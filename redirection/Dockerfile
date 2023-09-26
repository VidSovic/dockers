FROM ubuntu:22.04

RUN apt clean && apt update \
	&& TZ=Europe/Ljubljana DEBIAN_FRONTEND=noninteractive apt install -y supervisor ssh curl vim nano

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - \
	&& apt install -y nodejs \
	&& apt autoclean

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
WORKDIR /usr/sbin/
RUN ssh-keygen -A && mkdir -p /run/sshd
WORKDIR /

RUN useradd -d /home/www -m -s /bin/bash www

COPY app/ /app
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/id_rsa.pub /root/.ssh/authorized_keys

RUN chmod 700 /root/.ssh
RUN chmod 600 /root/.ssh/authorized_keys

RUN chown -R www:www /app

WORKDIR /app
RUN npm install

EXPOSE 22 3000

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
