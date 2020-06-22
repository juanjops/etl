FROM node:10

RUN apt-get update && apt-get -y install cron

WORKDIR /home/node/app

COPY src/nodejs/package*.json ./

RUN npm install

COPY cron-jobs /etc/cron.d/cron-jobs

RUN chmod 0644 /etc/cron.d/cron-jobs

RUN crontab /etc/cron.d/cron-jobs

RUN touch /var/log/cron.log

COPY src/nodejs .

EXPOSE 3000

CMD cron && tail -f /var/log/cron.log
