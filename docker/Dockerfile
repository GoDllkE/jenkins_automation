FROM registry.ng.bluemix.net/livelo/stretch_python3:latest

LABEL 'company'='Livelo' \
	  'creator'='Gustavo Toledo' \
	  'maintainer'='Unknow'

## Update repo and packages
#RUN apt update && \
#	apt upgrade -y
#
## Install packages
#RUN apt install git curl bash vim zip jq -y
#
## Create etc directory for app
#RUN mkdir /etc/jenkins_automations
#
## Add tool-scripts into image
#COPY docker/build_scripts/data_collector.sh /bin/data_collector
#COPY docker/build_scripts/py-parser.sh /bin/py-parser
COPY dist/automation /bin/jenkins_automation
COPY automation/resources/config.yaml /etc/jenkins_automations/config.yaml

# Default python packages
#RUN pip install pip setuptools pyinstaller pyyaml requests --upgrade

# Set tools and file R/X permissions
RUN chmod a+x /bin/jenkins_automation &&\
    chmod a+r /etc/jenkins_automations/config.yaml

# Define a entrypoint as app
ENTRYPOINT ["jenkins_automation"]

# End of file
