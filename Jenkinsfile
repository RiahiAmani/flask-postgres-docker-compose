pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: ci-deployer
  containers:
  - name: gitleaks
    image: zricethezav/gitleaks:latest
    command: [sleep]
    args: [infinity]
  - name: python
    image: python:3.10-slim
    command: [sleep]
    args: [infinity]
  - name: sonar-scanner
    image: sonarsource/sonar-scanner-cli:latest
    command: [sleep]
    args: [infinity]
  - name: checkov
    image: bridgecrew/checkov:latest
    command: [sleep]
    args: [infinity]
  - name: trivy
    image: aquasec/trivy:latest
    command: [sleep]
    args: [infinity]
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command: [sleep]
    args: [infinity]
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  - name: kubectl
    image: apline/k8s:1.30.1
    command: [sleep]
    args: [infinity]
  volumes:
  - name: docker-config
    secret:
      secretName: docker-hub-creds
      items:
      - key: .dockerconfigjson
        path: config.json
"""
    }
  }
  environment {
    IMAGE_NAME = "riahiamani/taskmanager-flask"
    IMAGE_TAG  = "${BUILD_NUMBER}"
  }
  stages {

    stage('Analyse des secrets (Gitleaks)') {
      steps {
        container('gitleaks') {
          sh '''
          gitleaks detect --source=${WORKSPACE} --report-format=json --report-path=${WORKSPACE}/gitleaks-report.json --exit-code=0
          '''
        }
        archiveArtifacts artifacts: 'gitleaks-report.json', allowEmptyArchive: true
      }
    }

    stage('Analyse infrastructure (Checkov)') {
      steps {
        container('checkov') {
          sh '''
          checkov --directory ${WORKSPACE} \
            --framework dockerfile \
            --output json \
            --output-file-path ${WORKSPACE} \
            --soft-fail
          '''
        }
        archiveArtifacts artifacts: 'results_json.json', allowEmptyArchive: true
      }
    }

    stage('Tests unitaires et couverture') {
      steps {
        container('python') {
          sh '''
          if [ -d tests ]; then
            pip install -r requirements.txt pytest pytest-cov --quiet --break-system-packages
            pytest --cov=. --cov-report=xml:coverage.xml || true
          else
            echo "Aucun dossier tests/ trouve - stage ignore."
          fi
          '''
        }
      }
    }

    stage('Analyse statique du code (SonarCloud)') {
      steps {
        container('sonar-scanner') {
          withCredentials([string(credentialsId: 'sonarcloud-token', variable: 'SONAR_TOKEN')]) {
            sh '''
            if [ -f coverage.xml ]; then
              COVERAGE_ARG="-Dsonar.python.coverage.reportPaths=coverage.xml"
            else
              COVERAGE_ARG=""
            fi
            sonar-scanner \
              -Dsonar.host.url=https://sonarcloud.io \
              -Dsonar.token=${SONAR_TOKEN} \
              ${COVERAGE_ARG} \
              -Dsonar.qualitygate.wait=true \
              -Dsonar.qualitygate.timeout=300
            '''
          }
        }
      }
    }

    stage('Build et push avec Kaniko') {
      steps {
        container('kaniko') {
          sh '''
          /kaniko/executor \
            --context=dir://${WORKSPACE} \
            --dockerfile=${WORKSPACE}/Dockerfile \
            --destination=${IMAGE_NAME}:${IMAGE_TAG} \
            --destination=${IMAGE_NAME}:latest
          '''
        }
      }
    }

    stage('Scan de vulnerabilites (Trivy)') {
      steps {
        container('trivy') {
          sh '''
          trivy image \
            --scanners vuln \
            --timeout 15m \
            --severity HIGH,CRITICAL \
            --format json \
            --output trivy-report.json \
            --exit-code 0 \
            ${IMAGE_NAME}:${IMAGE_TAG}
          '''
        }
        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
      }
    }

    stage('Deploiement Kubernetes') {
      steps {
        container('kubectl') {
          sh '''
          kubectl apply -f k8s-manifests/taskmanager/app-deployment.yaml
          kubectl set image deployment/taskmanager-app \
            taskmanager-app=${IMAGE_NAME}:${IMAGE_TAG} \
            -n devsecops
          kubectl rollout status deployment/taskmanager-app -n devsecops --timeout=120s
          '''
        }
      }
    }
  }
}
