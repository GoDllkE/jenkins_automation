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
        stage ('Instalando das dependencias do modulo') {
            steps {
                script { ON_STAGE = "${ON_STAGE}" }
                sh(script: "pip install -r requirements.txt", returnStdout: true)
            }
        }
        stage('Realizando build do modulo') {
            steps {
                script { ON_STAGE = "${ON_STAGE}" }
                sh(script: "python setup.py develop && python setup.py sdist", returnStdout: true)
                sh(script: "pyinstaller --onefile --path automation/ --console bin/automation", returnStdout: true)
            }
        }
        stage('Realizando testes basicos do modulo') {
            steps {
                script { ON_STAGE = "${ON_STAGE}" }
                sh(script: "chmod a+x dist/automation", returnStdout: true)
                sh(script: "./dist/automation -h", returnStdout: true)
            }
        }
        stage('Realizando testes avançados no modulo') {
            parallel {
                stage('Teste de execução unica') {
                    steps {
                        script {
                            script { ON_STAGE = "${ON_STAGE}" }
                            sh(script: "./dist/automation --create=role --type=projectRoles --name=teste_unit_automacao --pattern=.*", returnStdout: true)
                            sh(script: "./dist/automation --delete=role --type=projectRoles --name=teste_unit_automacao", returnStdout: true)
                        }
                    }
                }
                stage('Teste de execução composta') {
                    steps {
                        script {
                            script { ON_STAGE = "${ON_STAGE}" }
                            sh(script: "./dist/automation --create=project --name=teste_prj_automacao", returnStdout: true)
                            sh(script: "./dist/automation --delete=project --name=teste_prj_automacao", returnStdout: true)
                        }
                    }
                }
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
                    credentialsId: 'jenkins-user',
                    artifacts: [[
                        artifactId: "jenkins_${NAME}",
                        classifier: 'python37',
                        file: "dist/automation",
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

                    withCredentials([usernamePassword(credentialsId: 'jenkins-user', usernameVariable:'user', passwordVariable:'passwd')]) {
                        sh(script: "git remote add cotag https://${user}:${passwd}@stash.pontoslivelo.com.br/scm/jnk/automation_role-strategy.git")
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
			message: "Falha na construção do modulo 'Jenkins_${NAME}', no estágio: ${ON_STAGE}'. <${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
		}
		success {
			slackSend channel: env.SLACK_CHANNEL, color: 'good',
			message: "Modulo 'Jenkins_${NAME}' construido com sucesso! '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
		}
	}
}