FROM node:18-bookworm as base
RUN npm install -g @usebruno/cli
WORKDIR /app

FROM base as deps
COPY ./bruno/catalogue/package.json .
RUN npm install

FROM base
ADD --chmod=755 https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for /usr/local/bin/wait-for
COPY --from=deps /app/node_modules node_modules
COPY ./bruno/catalogue .
ENTRYPOINT [ "./entrypoint.sh" ]
