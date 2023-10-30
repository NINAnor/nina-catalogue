FROM registry.opensuse.org/opensuse/bci/python:3.11 as base
RUN --mount=type=cache,target=/var/cache/zypper \
    zypper install --no-recommends -y gdal proj
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
    zypper install --no-recommends -y python311-pdm
COPY ./pyproject.toml ./pdm.lock .

FROM pdm as production
RUN --mount=type=cache,target=/var/cache/zypper \
    zypper install --no-recommends -y gdal-devel gcc gcc-c++
RUN pdm add gdal==$(rpm -q --queryformat='%{VERSION}' gdal)
RUN --mount=type=cache,target=/root/.cache/pdm \
    pdm install -G production

FROM pdm as translation
RUN --mount=type=cache,target=/var/cache/zypper \
    zypper install --no-recommends -y gettext-tools
COPY --from=production /app/.venv .venv
COPY --from=source /app .
COPY locale locale
RUN DATABASE_URL="" \
  DJANGO_SETTINGS_MODULE="config.settings.test" \
  pdm run ./manage.py compilemessages

FROM pdm as docs
RUN --mount=type=cache,target=/var/cache/zypper \
    zypper install --no-recommends -y make
RUN --mount=type=cache,target=/root/.cache/pdm \
    pdm install -G docs
COPY --from=source /app .
COPY docs docs
WORKDIR /app/docs
CMD [ "make", "livehtml" ]

FROM base as django
COPY --from=production /app .
COPY --from=translation /app/locale locale
COPY --from=source /app .
COPY entrypoint.sh .
ENV DJANGO_ENV=production
ENTRYPOINT ["./entrypoint.sh"]

FROM pdm as dev
COPY --from=django /app/.venv .venv
RUN --mount=type=cache,target=/root/.cache/pdm \
    pdm install --dev
COPY --from=django /app/locale locale
COPY --from=django /app/manage.py .
COPY --from=django /app/entrypoint.sh .
ENV DJANGO_ENV=dev
ENTRYPOINT ["./entrypoint.sh"]
