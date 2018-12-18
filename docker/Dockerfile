FROM python3:latest

LABEL 'creator'='Gustavo Toledo' \
	  'maintainer'='Unknow'

# Instala dependencias
RUN python -m pip install -r requirements.txt

# Copia arquivos para imagem
COPY dist/automation /bin/jenkins_automation
COPY automation/resources/config.yaml /etc/jenkins_automations/config.yaml
COPY automation/resources/job_config.xml /etc/jenkins_automations/job_config.xml

# Set tools and file R/X permissions
RUN chmod a+x /bin/jenkins_automation &&\
    chmod a+r /etc/jenkins_automations/config.yaml && \
    chmod a+r /etc/jenkins_automations/job_config.xml

# Define a entrypoint as app
ENTRYPOINT ["/bin/jenkins_automation"]

# End of file
