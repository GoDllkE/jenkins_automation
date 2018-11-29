FROM python:3.7-stretch

# Required arguments
#ARG version
#ARG n_user
#ARG n_pass

LABEL 	'company'='Livelo' \
		'creator'='Gustavo Toledo' \
		'maintainer'='Unknow'

# Update repo and packages
RUN apt update && \
	apt upgrade -y

# Install packages
RUN apt install git curl bash vim zip jq -y

# Create etc directory for app
RUN mkdir /etc/jenkins_automations

# Add tool-scripts into image
COPY build-scripts/data_collector.sh /bin/data_collector
COPY build-scripts/py-parser.sh /bin/py-parser
COPY ../dist/automation /bin/jenkins_automation
COPY ../automation/resources/config.yaml /etc/jenkins_automations/config.yaml

# Default python packages
RUN pip install pip setuptools pyinstaller pyyaml requests --upgrade

# Set tools and file R/X permissions
RUN chmod a+x /bin/data_collector && \
    chmod a+x /bin/py-parser && \
    chmod a+x /bin/jenkins_automation &&\
    chmod a+r /etc/jenkins_automations/config.yaml

# Define a entrypoint as app
ENTRYPOINT ["jenkins_automation"]

# End of file
