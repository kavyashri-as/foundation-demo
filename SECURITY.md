# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it by:

1. **Do not** create a public GitHub issue for security vulnerabilities
2. Send an email to the repository maintainers with details of the vulnerability
3. Include steps to reproduce the issue if possible
4. Allow reasonable time for the issue to be addressed before public disclosure

## Security Best Practices

This repository follows these security practices:

- Regular dependency updates (when applicable)
- Minimal permissions in GitHub Actions workflows
- No sensitive data stored in version control
- Proper file permissions and access controls

## Recent Security Assessment

**Last Updated:** September 2024

### Assessment Results:
- ✅ No sensitive data (passwords, keys, tokens) found in repository
- ✅ No code injection vulnerabilities detected
- ✅ File permissions are appropriate
- ✅ No large files that might contain sensitive data
- ✅ GitHub Actions workflow uses specific action versions
- ⚠️  Missing `.gitignore` file to prevent accidental commits
- ⚠️  GitHub Actions workflow lacks explicit minimal permissions
- ⚠️  No automated security scanning enabled

### Recommendations:
1. Add `.gitignore` file to prevent accidental commits of sensitive files
2. Configure minimal permissions in GitHub Actions workflows
3. Consider enabling GitHub's security features like Dependabot and CodeQL
4. Regular security reviews for any future code additions