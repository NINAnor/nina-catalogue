FROM node:18-bookworm as base
RUN npm install -g @usebruno/cli
WORKDIR /app

FROM base as deps
RUN wget https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for
RUN chmod +x wait-for
COPY ./bruno/catalogue/package.json .
RUN npm install

FROM base
COPY --from=deps /app/node_modules node_modules
COPY --from=deps /app/wait-for .
COPY ./bruno/catalogue .
ENTRYPOINT [ "./entrypoint.sh" ]
