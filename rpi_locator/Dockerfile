FROM python:3.11-buster AS setup
COPY /rpi_locator/requirements.txt requirements.txt

RUN pip install -r requirements.txt --root-user-action=ignore
RUN apt-get update
RUN apt-get install -y libpcap-dev

FROM scratch
COPY --from=setup / /
WORKDIR /rpi_locator
CMD ["/rpi_locator/rpi_locator.py"] 
