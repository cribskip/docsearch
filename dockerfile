# docsearch
#
FROM debian:latest

LABEL maintainer="Sascha Kloß"

EXPOSE 8080/tcp
VOLUME /docs

RUN apt-get update && apt-get install -y --no-install-recommends \
htop \
figlet \
libexempi3 \
ocrmypdf \
pngquant \
python3-pip \
python3-venv \
rename \
tesseract-ocr \
tesseract-ocr-eng \
tesseract-ocr-deu \
tesseract-ocr-fra \
tesseract-ocr-spa \
tesseract-ocr-por \
unpaper \
unzip \
wget \
imagemagick \
file \
poppler-utils

RUN apt-get install python3-setuptools
RUN python3 -m venv --system-site-packages /appenv

RUN . /appenv/bin/activate; \
pip3 install --upgrade flask \
&& pip3 install --upgrade flask-autoindex

# Cleanup
RUN rm -rf /tmp/* /var/tmp/* /root/* /application/ocrmypdf \
&& apt-get autoremove -y \
&& apt-get autoclean -y

RUN useradd docsearch \
&& mkdir /home/docsearch \
&& chown docsearch:docsearch /home/docsearch \
&& chown docsearch:docsearch /docs \
&& chmod 775 /docs \
&& chmod ug+s /docs

WORKDIR /appenv
RUN wget https://github.com/cribskip/docsearch/archive/master.zip \
&& unzip master.zip && mv docsearch-master docsearch

ADD docker-entrypoint.sh /sbin
ENTRYPOINT ["/sbin/docker-entrypoint.sh"]
