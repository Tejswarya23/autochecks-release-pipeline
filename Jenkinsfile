pipeline {
    agent any

    environment {
        PIPELINE_NAME = "auto-release-pipeline"
        VERSION       = "1.0.0"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out monorepo..."
                checkout scm
            }
        }

        stage('Detect Changed Modules') {
            steps {
                echo "Detecting changed packages via Bazel query..."
                sh '''
                    bazel query "//..." --output label 2>/dev/null || echo "All modules queued for build"
                '''
            }
        }

        stage('Build All Modules') {
            steps {
                echo "Building with Bazel..."
                sh 'bazel build //...'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running all Bazel tests..."
                sh 'bazel test //... --test_output=short'
            }
        }

        stage('Generate Release Manifest') {
            steps {
                echo "Evaluating release gates and generating manifest..."
                sh 'python3 release_tool/release.py'
                archiveArtifacts artifacts: 'release_manifest.json'
            }
        }

        stage('Release Gate Check') {
            steps {
                script {
                    def manifest = readJSON file: 'release_manifest.json'
                    if (!manifest.release_approved) {
                        error("RELEASE BLOCKED: ${manifest.summary}")
                    }
                    echo "Release approved: ${manifest.summary}"
                }
            }
        }
    }

    post {
        success { echo "Pipeline complete - release manifest published." }
        failure { echo "Pipeline failed - release blocked by gate check." }
    }
}
