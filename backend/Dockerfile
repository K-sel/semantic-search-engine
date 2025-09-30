FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "semantic-search", "/bin/bash", "-c"]

COPY . .

EXPOSE 5000

CMD ["conda", "run", "--no-capture-output", "-n", "semantic-search", "python", "app.py"]
