FROM registry.ng.bluemix.net/livelo/stretch_python3:latest

LABEL 'company'='Livelo' \
	  'creator'='Gustavo Toledo' \
	  'maintainer'='Unknow'

COPY dist/automation /bin/jenkins_automation
COPY automation/resources/config.yaml /etc/jenkins_automations/config.yaml
COPY automation/resources/job_config.xml /etc/jenkins_automations/job_config.xml

# Set tools and file R/X permissions
RUN chmod a+x /bin/jenkins_automation &&\
    chmod a+r /etc/jenkins_automations/config.yaml && \
    chmod a+r /etc/jenkins_automations/job_config.xml

# Define a entrypoint as app
ENTRYPOINT ["bash"]

# End of file
