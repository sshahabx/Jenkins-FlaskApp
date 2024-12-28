pipeline {
    agent any

    environment {
        // Set environment variables if needed
        FLASK_ENV = 'production'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository from GitHub
                git 'https://github.com/yourusername/your-flask-app.git'
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                // Set up virtual environment and install dependencies
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Run tests (if any)
                sh 'source venv/bin/activate && pytest'
            }
        }

        stage('Build') {
            steps {
                // Build the application (optional)
                echo 'Building the Flask application...'
            }
        }

        stage('Deploy') {
            steps {
                // Deploy the application (this could be SSH, Docker, etc.)
                // Example: SSH to a server and restart the Flask app
                sh 'ssh user@your-server "cd /path/to/app && git pull origin master && sudo systemctl restart flask-app"'
            }
        }
    }

    post {
        always {
            // Clean up actions (if needed)
            cleanWs()
        }

        success {
            // Notify on success (optional)
            echo 'Pipeline executed successfully!'
        }

        failure {
            // Notify on failure (optional)
            echo 'Pipeline failed!'
        }
    }
}
