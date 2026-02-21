# Branch Protection and Workflow Security

This directory contains configuration files that protect the Kairos bot workflows and restrict unauthorized access.

## Files

### CODEOWNERS
Defines code ownership for specific paths in the repository. Changes to protected paths require approval from designated owners.

**Protected Paths:**
- `/.github/workflows/` - Bot workflows (requires @Kushmanmb approval)
- `/.github/settings.yml` - Repository settings (requires @Kushmanmb approval)
- `/.github/branch-protection.yml` - Branch protection config (requires @Kushmanmb approval)
- `/.github/CODEOWNERS` - This file itself (requires @Kushmanmb approval)

### branch-protection.yml
Documents recommended branch protection rules for the repository.

## Setting Up Branch Protection

### Option 1: GitHub Web UI

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Branches**
3. Click **Add rule** or edit existing rule
4. Configure the following settings for the `main` branch:

   ✅ **Require pull request reviews before merging**
   - Required approving reviews: 1
   - Dismiss stale pull request approvals when new commits are pushed
   - ✅ **Require review from Code Owners** (Critical for workflow protection)
   
   ✅ **Require status checks to pass before merging**
   
   ✅ **Require conversation resolution before merging**
   
   ✅ **Require linear history** (optional)
   
   ✅ **Do not allow bypassing the above settings**
   
   ✅ **Restrict who can push to matching branches**
   - Add: Kushmanmb (or other trusted maintainers)
   
   ❌ **Allow force pushes** (Keep disabled)
   
   ❌ **Allow deletions** (Keep disabled)

5. Click **Create** or **Save changes**

### Option 2: GitHub CLI

```bash
# Install GitHub CLI if not already installed
# https://cli.github.com/

# Enable branch protection for main branch
gh api repos/Kushmanmb/Kairos/branches/main/protection \
  -X PUT \
  -f required_status_checks[strict]=true \
  -f required_pull_request_reviews[required_approving_review_count]=1 \
  -f required_pull_request_reviews[require_code_owner_reviews]=true \
  -f required_pull_request_reviews[dismiss_stale_reviews]=true \
  -f enforce_admins=true \
  -f required_conversation_resolution=true \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```

### Option 3: GitHub Settings App

Install the [Settings GitHub App](https://github.com/apps/settings) which automatically syncs repository settings from `.github/settings.yml`.

## How This Protects Bot Workflows

1. **CODEOWNERS Enforcement**: 
   - Any changes to files in `/.github/workflows/` require approval from @Kushmanmb
   - Pull requests modifying workflows will automatically request review from the code owner
   
2. **Branch Protection**: 
   - Direct pushes to `main` are restricted
   - All changes must go through pull requests
   - Pull requests require approval before merging
   
3. **Code Owner Review Requirement**: 
   - When "Require review from Code Owners" is enabled, PRs touching protected paths cannot be merged without code owner approval
   - This prevents other users from modifying bot workflows without explicit permission

## Testing Protection

To verify the protection is working:

1. Have another user attempt to create a PR that modifies a file in `.github/workflows/`
2. The PR should automatically request review from @Kushmanmb
3. The PR should not be mergeable until @Kushmanmb approves it

## Additional Security Recommendations

1. **Enable 2FA**: Require two-factor authentication for all contributors
2. **Audit Logs**: Regularly review audit logs for unauthorized access attempts
3. **Workflow Permissions**: Set minimal necessary permissions in workflow files:
   ```yaml
   permissions:
     contents: read
     pull-requests: write
   ```
4. **Secret Management**: Use GitHub Secrets for sensitive data, never commit credentials
5. **Dependabot**: Enable Dependabot alerts for security vulnerabilities

## Maintenance

- Review and update CODEOWNERS as team structure changes
- Periodically audit branch protection rules
- Document any exceptions or changes to protection rules

## Questions or Issues

If you have questions about these protection rules, please contact the repository owner @Kushmanmb.
