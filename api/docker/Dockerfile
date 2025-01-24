FROM python:3.10 AS build

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -Ur ./requirements.txt

############################################################
FROM python:3.10-slim

# Copy venv from builder
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /api
COPY ./src ./src

#COPY ./docker/entrypoint.sh ./entrypoint.sh
#RUN chmod +x ./entrypoint.sh

#entrypoint ["./entrypoint.sh"]