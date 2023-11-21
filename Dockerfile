from node:lts
COPY ./src/ui /ui
WORKDIR /ui
RUN npm run build


from python:3.11

COPY ./src /app
COPY --from=0 /ui/dist /app/ui/dist

# Important: 
#   Add "/" to python path so that the "app.*" namespace works.
#   Without it, the tests can't import from server.py and models
#   Example: from app.models import Task
ENV PYTHONPATH=/ 

WORKDIR /app
RUN pip install poetry
RUN poetry install
CMD ["poetry", "run", "uvicorn", "server:app", "--host", "0.0.0.0"]