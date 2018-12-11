pipeline {
    agent {
        kubernetes {
            cloud 'kubernetes'
            label 'python3-app-builder'
            serviceAccount 'jenkins'
            defaultContainer 'python-build'
            yamlFile 'KubernetesPod.yaml'
        }
    }
    environment {
        // Controle de build
        PYTHON_VERSION = '3.7.1'
        SLACK_CHANNEL = '#devops-notifications'

        // Controle da imagem
        IMAGEM_DOCKER = 'livelo/jenkins_automation'

        // Controle do nexus
        PROJECT = sh(script: "echo $JOB_NAME | cut -d '/' -f2", returnStdout: true).trim()
        COMPONENT = sh(script: "echo $JOB_NAME | cut -d '/' -f4", returnStdout: true).trim()
        NAME = sh(script: "py-parser setup.py | grep name | cut -d ' ' -f2", returnStdout: true).trim()
        VERSION = sh(script: "py-parser setup.py | grep version | cut -d ' ' -f2", returnStdout: true).trim()
    }
    stages {
        stage ('Instalando das dependencias do modulo') {
            steps {
                sh(script: "pip install -r requirements.txt", returnStdout: true)
            }
        }
        stage('Realizando build do modulo') {
            steps {
                sh(script: "python setup.py develop && python setup.py sdist", returnStdout: true)
                sh(script: "pyinstaller --onefile --path automation/ --console bin/automation", returnStdout: true)
            }
        }
        stage('Realizando testes no modulo') {
            parallel {
                stage('Teste de compilação') {
                    steps {
                        sh "chmod a+x dist/automation"
                        sh "./dist/automation -h"
                    }
                }
                stage('Teste simples') {
                    steps {
                        script {
                            sh "./dist/automation --create=role --type=projectRoles --name=teste_unit_automacao --pattern=.* --debug"
                            sh "./dist/automation --delete=role --type=projectRoles --name=teste_unit_automacao --debug"
                        }
                    }
                }
                stage('Teste composto') {
                    steps {
                        script {
                            sh "./dist/automation --create=project --name=teste_prj_automacao --id=PUP --debug"
                            sh "./dist/automation --create=deploy_job --name=teste_prj_automacao --repo=https://stash.pontoslivelo.com.br/scm/pup/puppet-enc-livelocmdb.git --debug"
                            sh "./dist/automation --check=deploy_job --name=teste_prj_automacao --repo=https://stash.pontoslivelo.com.br/scm/pup/puppet-enc-livelocmdb.git --debug"

                            sh "./dist/automation --delete=deploy_job --name=teste_prj_automacao --repo=https://stash.pontoslivelo.com.br/scm/pup/puppet-enc-livelocmdb.git --debug"
                            sh "./dist/automation --check=deploy_job --name=teste_prj_automacao --repo=https://stash.pontoslivelo.com.br/scm/pup/puppet-enc-livelocmdb.git --debug"
                            sh "./dist/automation --delete=deploy_job --name=teste_prj_automacao --repo=https://stash.pontoslivelo.com.br/scm/pup/puppet-enc-livelocmdb.git --debug"

                            sh "./dist/automation --delete=project --name=teste_prj_automacao --debug"
                        }
                    }
                }
            }
        }
        stage('Subindo modulo para o Nexus') {
            steps {
                nexusArtifactUploader (
                    nexusVersion: 'nexus2',
                    protocol: 'http',
                    nexusUrl: 'nexus.pontoslivelo.com.br/nexus',
                    groupId: "br.com.pontoslivelo.$PROJECT.$COMPONENT",
                    version: "${VERSION}",
                    repository: 'site-automations',
                    credentialsId: 'jenkins-user',
                    artifacts: [[
                        artifactId: "jenkins_${NAME}",
                        classifier: 'python37',
                        file:       "dist/automation",
                        type:       'bin'
                    ]]
                )
            }
        }
        stage('Criando imagem da automacao') {
            parallel {
                stage('Construindo latest') {
                    when { branch 'master' }
                    steps {
                        container('docker-build') {
                            script {
                                docker.withRegistry('https://registry.ng.bluemix.net', 'ibmcloud-container_registry-token') {
                                    docker_img = docker.build("$IMAGEM_DOCKER:latest", '-f docker/Dockerfile .')
                                    docker_img.push()
                                }
                            }
                        }
                    }
                }
                stage('Construindo branch latest') {
                    steps {
                        container('docker-build') {
                            script {
                                docker.withRegistry('https://registry.ng.bluemix.net', 'ibmcloud-container_registry-token') {
                                    DOCKER_TAG = env.BRANCH_NAME.replaceAll("[^0-9a-zA-Z-._]","_") + ".latest"
                                    docker_img = docker.build("$IMAGEM_DOCKER:$DOCKER_TAG", '-f docker/Dockerfile .')
                                    docker_img.push()
                                }
                            }
                        }
                    }
                }
                stage('Construindo branch com tag do build') {
                    steps {
                        container('docker-build') {
                            script {
                                docker.withRegistry('https://registry.ng.bluemix.net', 'ibmcloud-container_registry-token') {
                                    DOCKER_TAG = env.BRANCH_NAME.replaceAll("[^0-9a-zA-Z-._]","_") + "." + env.BUILD_ID
                                    docker_img = docker.build("$IMAGEM_DOCKER:$DOCKER_TAG", '-f docker/Dockerfile .')
                                    docker_img.push()
                                }
                            }
                        }
                    }
                }
            }
        }
        stage('Criando TAG referente ao build') {
            when { branch 'master' }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'jenkins-user', usernameVariable:'user', passwordVariable:'passwd')]) {
                        sh(script: "git remote add cotag https://${user}:${passwd}@stash.pontoslivelo.com.br/scm/jnk/automation_role-strategy.git")
                        sh(script: "git fetch cotag --tags")
                        sh(script: "git tag -f -a $VERSION -m 'Tag from CI/CD'")
                        sh(script: "git push cotag --tags")
                    }
                }
            }
        }
    }
    post {
		failure {
			slackSend channel: env.SLACK_CHANNEL, color: 'danger',
			message: "Falha na construção do modulo 'Jenkins_${NAME}'. <${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
		}
		success {
			slackSend channel: env.SLACK_CHANNEL, color: 'good',
			message: "Modulo 'Jenkins_${NAME}' construido com sucesso! (Tag: $VERSION).'<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
		}
	}
}