pipeline {
    agent any

    environment {
        // Python version for virtual environment
        PYTHON_VERSION = 'python3'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from the repository
                checkout scm
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                // Create a virtual environment and activate it
                script {
                    sh """
                    ${PYTHON_VERSION} -m venv venv
                    source venv/bin/activate
                    """
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install required dependencies from requirements.txt
                script {
                    sh """
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Run tests (Optional, add your test commands here)
                script {
                    sh """
                    source venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                    """
                }
            }
        }

        stage('Build') {
            steps {
                // Optional build stage if you have a build process (e.g., building assets)
                echo 'Building the application (if needed)'
            }
        }

        stage('Deploy') {
            steps {
                // Deploy the application (add your deployment script here)
                // For example, use SCP, FTP, or any deployment tool to push your app to the server.
                echo 'Deploying Flask app to production'
            }
        }
    }

    post {
        always {
            // Clean up actions after the pipeline execution
            echo 'Cleaning up resources...'
            sh 'rm -rf venv' // Remove virtual environment
        }
    }
}
