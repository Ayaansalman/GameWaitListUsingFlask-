pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Fetching code from GitHub...'
                git branch: 'main', url: 'https://github.com/Ayaansalman/GameWaitListUsingFlask-.git'
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building containerized application...'
                sh 'docker-compose -f docker-compose-jenkins.yml down || true'
                sh 'docker-compose -f docker-compose-jenkins.yml up -d --build'
            }
        }
        
        stage('Verify') {
            steps {
                echo 'Verifying deployment...'
                sh 'docker ps'
                sh 'sleep 10'
                sh 'curl -f http://localhost:5001 || exit 1'
            }
        }
    }
    
    post {
        success {
            echo '✅ Build successful! Application running on port 5001'
        }
        failure {
            echo '❌ Build failed!'
            sh 'docker-compose -f docker-compose-jenkins.yml logs'
        }
    }
}
