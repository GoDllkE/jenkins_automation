FROM registry.ng.bluemix.net/livelo/stretch_python3:latest

LABEL 'company'='Livelo' \
	  'creator'='Gustavo Toledo' \
	  'maintainer'='Unknow'

COPY dist/automation /bin/jenkins_automation
COPY automation/resources/config.yaml /etc/jenkins_automations/config.yaml

# Set tools and file R/X permissions
RUN chmod a+x /bin/jenkins_automation &&\
    chmod a+r /etc/jenkins_automations/config.yaml

# Define a entrypoint as app
ENTRYPOINT ["jenkins_automation"]

# End of file
