FROM --platform=linux/amd64 solace/solace-agent-mesh:latest
WORKDIR /app

# Install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /app/requirements.txt

# Copy project files
COPY . /app

# Build Solace Agent Mesh
RUN solace-agent-mesh build
#CMD ["run", "--use-system-env"]

#CMD ["run", "-b", "--use-system-env"]
ENTRYPOINT ["bash", "/app/start-sam.sh"]