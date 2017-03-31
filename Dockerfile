FROM drewantech/flask_sqlalchemy_psycopg2:1.0.1
MAINTAINER Benton Drew <benton.s.drew@drewantech.com>
USER root
RUN rm test_psycopg2.py
ADD source/ /usr/lib/python3.5/site-packages/drewantech_common
ADD service/test_common.py .
ENV FLASK_APP test_common.py
USER python_user
ENTRYPOINT ["python3", "-m", "flask", "run"]
CMD ["--host=127.0.0.2", "--port=5001"]
