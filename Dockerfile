FROM registry.opensuse.org/opensuse/leap:latest as base
RUN --mount=type=cache,target=/var/cache/zypper \
    zypper install --no-recommends -y python311 gdal proj
WORKDIR /app
ENV PYTHONPATH=/app/.venv/lib
ENV PATH=$PATH:/app/.venv/bin

FROM scratch as source
WORKDIR /app
COPY config config
COPY metadata_catalogue metadata_catalogue
COPY manage.py .

FROM base as pdm
RUN --mount=type=cache,target=/var/cache/zypper \
    zypper install --no-recommends -y python311-pip git
RUN python3.11 -m pip install pdm
COPY ./pyproject.toml ./pdm.lock .

FROM pdm as production
RUN --mount=type=cache,target=/var/cache/zypper \
    zypper install --no-recommends -y gdal-devel gcc gcc-c++ python311-devel
RUN pdm add gdal==$(rpm -q --queryformat='%{VERSION}' gdal)
RUN --mount=type=cache,target=/root/.cache/pdm \
    pdm install -G production

FROM pdm as translation
RUN --mount=type=cache,target=/var/cache/zypper \
    zypper install --no-recommends -y gettext-tools
COPY --from=production /app/.venv .venv
COPY --from=source /app .
COPY locale locale
RUN DATABASE_URL="" DJANGO_BASE_SCHEMA_URL="" \
  DJANGO_SETTINGS_MODULE="config.settings.test" \
  pdm run ./manage.py compilemessages

FROM base as django
COPY --from=production /app .
COPY --from=translation /app/locale locale
COPY --from=source /app .
RUN mkdir media
COPY entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]

FROM pdm as dev
COPY --from=django /app/.venv .venv
RUN --mount=type=cache,target=/root/.cache/pdm \
    pdm install --dev
COPY --from=django /app/locale locale
COPY --from=django /app/manage.py .
COPY --from=django /app/entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]
