FROM rabbitmq:4-management-alpine

ENV RABBITMQ_DEFAULT_USER=rabbit
ENV RABBITMQ_DEFAULT_PASS=rabbit

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD rabbitmq-diagnostics check_port_connectivity || exit 1

EXPOSE 5672 15672
