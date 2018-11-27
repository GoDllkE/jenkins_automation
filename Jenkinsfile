pipeline {
    agent {
        kubernetes {
            cloud 'kubernetes'
            label 'python3-app-builder'
            serviceAccount 'jenkins'
            defaultContainer 'builder'
            yamlFile 'KubernetesPod.yaml'
        }
    }
    environment {
        ON_STAGE = "Inicializando CI"
        PYTHON_VERSION = '3.7.1'
        SLACK_CHANNEL = '#devops-notifications'

        // Structural environments
        PROJECT = sh(script: "echo $JOB_NAME | cut -d '/' -f2", returnStdout: true).trim()
        COMPONENT = sh(script: "echo $JOB_NAME | cut -d '/' -f4", returnStdout: true).trim()

        //
        NAME = sh(script: "py-parser setup.py | grep name | cut -d ' ' -f2", returnStdout: true).trim()
        VERSION = sh(script: "py-parser setup.py | grep version | cut -d ' ' -f2", returnStdout: true).trim()
    }
    stages {
        stage ('Instalando dependencias do modulo') {
            steps {
                script { ON_STAGE = "${ON_STAGE}" }
                sh(script: "pip install -r requirements.txt", returnStdout: true)
            }
        }
        stage('Realizando build do modulo') {
            steps {
                script { ON_STAGE = "${ON_STAGE}" }
                sh(script: "python setup.py develop && python setup.py sdist", returnStdout: true)
                sh(script: "pyinstaller --onefile --path automation/ --console bin/jenkins_automation", returnStdout: true)
            }
        }
        stage('Subindo modulo para o Nexus') {
            steps {
                script { ON_STAGE = "${ON_STAGE}" }
                nexusArtifactUploader (
                    nexusVersion: 'nexus2',
                    protocol: 'http',
                    nexusUrl: 'nexus.pontoslivelo.com.br/nexus',
                    groupId: "br.com.pontoslivelo.$PROJECT.$COMPONENT",
                    version: "${VERSION}",
                    repository: 'site-automations',
                    credentialsId: 'jenkins-nexus',
                    artifacts: [[
                        artifactId: "${NAME}",
                        classifier: 'python37',
                        file: "dist/jenkins_automation",
                        type: 'bin'
                    ]]
                )
                //
            }
        }
        stage('Criando TAG referente ao build') {
            steps {
                script {
                    ON_STAGE = "${ON_STAGE}"

                    withCredentials([usernamePassword(credentialsId: 'jenkins-stash', usernameVariable:'user', passwordVariable:'passwd')]) {
                        sh(script: "git remote add cotag https:${user}:${passwd}@stash.pontoslivelo.com.br/scm/jnk/automation_role-strategy.git")
                        sh(script: "git fetch cotag --tags")
                        sh(script: "git tag -f -a $VERSION -m 'Tag from CI/CD'")
                        sh(script: "git push cotag --tags")
                    }
                }
            }
        }
        // Need to create this other job/image first
        //stage('Atualizando imagem da automacao') {
        //   when { branch 'master' }
        //   steps {
        //      script {
        //          IMG_JOB = ''
        //          build job: $IMG_JOB, parameters: [String(name: 'version', value: $VERSION)]
        //      }
        //  }
        //}
    }
    post {
		failure {
			slackSend channel: env.SLACK_CHANNEL, color: 'danger',
			message: "Construção falhou no estágio de: ${ON_STAGE} - '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
		}
		success {
			slackSend channel: env.SLACK_CHANNEL, color: 'good',
			message: "Construido com sucesso! '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
		}
	}
}