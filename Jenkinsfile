// Jenkins pipeline for automation_framework (Windows agent).
// Setup guide: JENKINS_SETUP.md
//
// Desktop tests (Calculator / Notepad / Excel) need a logged-in interactive Windows desktop, so the
// agent that runs this job must be started by a user session - not as a Windows service.
pipeline {
    agent { label params.AGENT_LABEL ?: 'windows' }

    parameters {
        string(name: 'AGENT_LABEL', defaultValue: 'windows', description: 'Label of the Windows agent / node')
        choice(name: 'TEST_ENV', choices: ['qa', 'dev'], description: 'Environment from config/config.yaml')
        choice(name: 'TEST_APP', choices: ['cli', 'calculator', 'notepad', 'excel', 'all'],
               description: 'Application under test (cli needs no desktop)')
        string(name: 'MARKER', defaultValue: '', description: 'Optional pytest marker, e.g. smoke or regression (empty = all tests)')
    }

    triggers {
        pollSCM('H/5 * * * *')   // build when new commits land
        cron('H 2 * * *')        // nightly regression
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()    // only one run at a time: desktop tests share one screen
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        PYTHONUTF8 = '1'
        CI = 'true'                  // run_tests.py never prompts for the application when CI is set
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                bat '''
                    if not exist .venv\\Scripts\\python.exe python -m venv .venv
                    .venv\\Scripts\\python -m pip install --quiet --upgrade pip
                    .venv\\Scripts\\python -m pip install --quiet -r requirements.txt
                    call npm ci
                '''
            }
        }

        stage('Run tests') {
            steps {
                script {
                    def marker = params.MARKER?.trim() ? "-m ${params.MARKER.trim()}" : ''
                    int rc = bat(returnStatus: true, script: """
                        cd automation_framework
                        ..\\.venv\\Scripts\\python run_tests.py --no-prompt --app ${params.TEST_APP} --env ${params.TEST_ENV} ${marker} --junitxml=reports/junit.xml
                    """)
                    if (rc != 0) {
                        // failing tests -> yellow (unstable) build, reports are still published
                        unstable("Tests finished with exit code ${rc}")
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'automation_framework/reports/junit.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: '''
                automation_framework/reports/**,
                automation_framework/allure-report/**,
                automation_framework/logs/**,
                automation_framework/screenshots/**
            '''
        }
        cleanup {
            // leave no stray test applications on the shared desktop
            bat(returnStatus: true, script: 'taskkill /F /IM CalculatorApp.exe /IM Calculator.exe /IM notepad.exe /IM EXCEL.EXE 2>nul')
        }
    }
}
