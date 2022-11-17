pipeline {
  agent any
  stages {
    stage('Checkout SCM') {
			steps {
				git 'https://github.com/2000859YangXiao/flask-login.git'
			}
		}
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            sh 'echo "building the repo"'
          }
        }
      }
    }
  
    stage('Deploy')
    {
      steps {
        echo "deploying the application"
        sh "flask run --port 8000"
      }
    }
  }
  stage('OWASP DependencyCheck') {
			steps {
				dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
			}
		}
  
  stage('Code Quality Check via SonarQube') {
      steps {
        script {
          def scannerHome = tool 'SonarQube';
          withSonarQubeEnv('SonarQube') {
            sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=OWASP -Dsonar.sources=."
          }
        }
      }
    }
  }
  post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
            recordIssues enabledForFailure: true, tool: SonarQube()
        }
        success {                   
            echo "Flask Application Up and running!!"
            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}
