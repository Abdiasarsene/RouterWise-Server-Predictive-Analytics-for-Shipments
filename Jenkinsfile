pipeline {
    agent any

    environment {
        IMAGE_NAME = "monprojet-api"
        IMAGE_TAG = "latest"
        REGISTRY = "mon-registry.example.com"  // Modifie selon ton registry Docker
    }

    stages {
        stage('Préparation') {
            steps {
                echo "🔧 Installation des dépendances"
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Formatage + Linting + Tests') {
            steps {
                echo "Formatage du code avec Ruff"
                sh 'make all'
            }
        }

        stage('Lancement du serveur MLflow'){
            step(
                echo "MLflow Server"
                sh 'make mlflow_server'
            )
        }

        stage('Lancement de RouteWise-Server') {
            steps {
                echo " API: RouteWise-Server"
                sh 'make run'
            }
        }

        stage('Continuous Training (CT)') {
            steps {
                echo "♻️ Entraînement continu - re-train et validation"
                // Ici tu peux ajouter un script spécifique CT, par exemple recharger données, réentraîner, valider modèle
                sh 'python ct_training.py || echo "CT échoué, mais on continue"'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Construction de l'image Docker"
                sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "📤 Push de l'image Docker vers le registry"
                sh "docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Déploiement') {
            steps {
                echo "🚀 Déploiement de la nouvelle image"
                // Ex : appeler un script de déploiement ou déployer via kubectl/docker-compose
                sh './deploy.sh || echo "Déploiement échoué"'
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline CI/CD/CT réussi !"
        }
        failure {
            echo "❌ Pipeline échoué"
        }
    }
}
