from node:18-bookworm
RUN npm install -g @usebruno/cli

WORKDIR /app
RUN wget https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for
RUN chmod +x wait-for
COPY ./catalogue .
COPY ./entrypoint.sh .
ENTRYPOINT [ "./entrypoint.sh" ]
