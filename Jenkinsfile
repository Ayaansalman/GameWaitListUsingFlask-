pipeline {
    agent any
    
    stages {
        stage('Fetch Code') {
            steps {
                echo 'Fetching code from GitHub...'
                git branch: 'master', url: 'https://github.com/Ayaansalman/GameWaitListUsingFlask-.git'
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building containerized application...'
                sh 'docker-compose -f docker-compose-jenkins.yml down || true'
                sh 'docker-compose -f docker-compose-jenkins.yml up -d --build'
                sh 'nohup bash -c "sleep 200 && docker-compose -f docker-compose-jenkins.yml down" >/dev/null 2>&1 &'
            }
        }
        
        stage('Verify') {
            steps {
                echo 'Verifying deployment...'
                sh 'sleep 20'
                echo 'Verifying deployment by checking container status...'
                sh 'docker ps | grep jenkins_waitlist_web'
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
