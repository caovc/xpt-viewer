FROM caov2021/base-plotly-dash
ENV DEBUG=False
RUN mkdir app
WORKDIR app
EXPOSE 80
CMD [ "gunicorn", "--workers=5", "--threads=1", "--timeout=120", "-b 0.0.0.0:80", "app:server"]
