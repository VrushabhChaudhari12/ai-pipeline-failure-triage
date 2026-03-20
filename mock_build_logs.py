"""
Mock AWS CodeBuild failure logs for testing triage functionality
"""

SCENARIOS = {
    "unit_test_failure": """[Container] 2024-03-15 14:23:01 Starting phase INSTALL
[Container] 2024-03-15 14:23:05 Phase INSTALL completed
[Container] 2024-03-15 14:23:06 Starting phase PRE_BUILD
[Container] 2024-03-15 14:23:10 Phase PRE_BUILD completed
[Container] 2024-03-15 14:23:11 Starting phase BUILD
[Container] 2024-03-15 14:23:15 Executing npm run build
[Container] 2024-03-15 14:23:45 Phase BUILD completed
[Container] 2024-03-15 14:23:46 Starting phase POST_BUILD
[Container] 2024-03-15 14:23:50 Running tests with npm test
[Container] 2024-03-15 14:24:15 FAILURE: Test "UserService.createUser" failed: Expected status 201 but got 400
[Container] 2024-03-15 14:24:15 FAILURE: Test "AuthService.validateToken" failed: Token validation returned false for valid token
[Container] 2024-03-15 14:24:16 FAILURE: 2 tests failed, 45 passed
[Container] 2024-03-15 14:24:16 Command "npm test" exited with code 1""",

    "dependency_error": """[Container] 2024-03-15 15:30:01 Starting phase INSTALL
[Container] 2024-03-15 15:30:05 Running npm install
[Container] 2024-03-15 15:30:25 WARN notice Looking for https://registry.npmjs.org/react-scripts@5.0.0 - not found
[Container] 2024-03-15 15:30:26 ERR! 404 Not found: @myorg/custom-logger@2.1.0
[Container] 2024-03-15 15:30:26 ERR! code E404
[Container] 2024-03-15 15:30:26 ERR! Unable to install dependency @myorg/custom-logger
[Container] 2024-03-15 15:30:27 ERR! npm ERR! Maximum call stack size exceeded
[Container] 2024-03-15 15:30:27 Command "npm install" exited with code 1
[Container] 2024-03-15 15:30:27 Phase INSTALL failed""",

    "docker_build_failure": """[Container] 2024-03-15 16:45:01 Starting phase INSTALL
[Container] 2024-03-15 16:45:10 Phase INSTALL completed
[Container] 2024-03-15 16:45:11 Starting phase PRE_BUILD
[Container] 2024-03-15 16:45:15 Running docker login -u AWS -p *** https://123456789012.dkr.ecr.us-east-1.amazonaws.com
[Container] 2024-03-15 16:45:16 Error response from daemon: Get https://123456789012.dkr.ecr.us-east-1.amazonaws.com/v2/: unauthorized: authentication required
[Container] 2024-03-15 16:45:17 BUILD_CONTAINER_UNABLE_TO_PULL_IMAGE: Unable to pull Docker image
[Container] 2024-03-15 16:45:17 Error: Cannot pull Docker image - ECR authentication failed
[Container] 2024-03-15 16:45:18 Command "docker build" exited with code 1
[Container] 2024-03-15 16:45:18 Phase BUILD failed""",

    "iam_permission_error": """[Container] 2024-03-15 17:20:01 Starting phase INSTALL
[Container] 2024-03-15 17:20:05 Phase INSTALL completed
[Container] 2024-03-15 17:20:06 Starting phase PRE_BUILD
[Container] 2024-03-15 17:20:10 Phase PRE_BUILD completed
[Container] 2024-03-15 17:20:11 Starting phase BUILD
[Container] 2024-03-15 17:20:20 Executing build script
[Container] 2024-03-15 17:20:35 Upload failed: AccessDenied: Access Denied
[Container] 2024-03-15 17:20:35 ERROR: s3:PutObject permission denied on bucket myapp-build-artifacts
[Container] 2024-03-15 17:20:36 Upload failed: AccessDenied: User: arn:aws:sts::123456789012:assumed-role/codebuild-build-role is not authorized
[Container] 2024-03-15 17:20:36 ERROR: sts:AssumeRole failed for role arn:aws:iam::123456789012:role/DeploymentRole
[Container] 2024-03-15 17:20:37 Command "./deploy.sh" exited with code 1
[Container] 2024-03-15 17:20:37 Phase POST_BUILD failed"""
}


def get_build_log(scenario):
    """
    Get CodeBuild log for a given scenario.

    Args:
        scenario: One of 'unit_test_failure', 'dependency_error', 'docker_build_failure', 'iam_permission_error'

    Returns:
        String containing the build log
    """
    return SCENARIOS.get(scenario, SCENARIOS["unit_test_failure"])