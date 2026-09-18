# OWASP Security Best Practices 2025-2026

A comprehensive guide to the latest OWASP security standards for developers building secure applications.

---

## Table of Contents

1. [OWASP Top 10:2025](#owasp-top-102025)
2. [OWASP ASVS 5.0.0](#owasp-asvs-500)
3. [OWASP Top 10 for Agentic Applications 2026](#owasp-top-10-for-agentic-applications-2026)
4. [Key Security Principles](#key-security-principles)
5. [Sources and References](#sources-and-references)

---

## OWASP Top 10:2025

Released at OWASP Global AppSec EU Barcelona 2025, based on analysis of 175,000+ CVEs and 2.8 million applications tested.

### Summary Table

| Rank | Category | Change from 2021 |
|------|----------|------------------|
| A01 | Broken Access Control | Unchanged #1 |
| A02 | Security Misconfiguration | Up from #5 |
| A03 | Software Supply Chain Failures | **NEW** (expanded from A06:2021) |
| A04 | Cryptographic Failures | Down from #2 |
| A05 | Injection | Down from #3 |
| A06 | Insecure Design | Down from #4 |
| A07 | Identification and Authentication Failures | Unchanged #7 |
| A08 | Software and Data Integrity Failures | Unchanged #8 |
| A09 | Security Logging and Monitoring Failures | Unchanged #9 |
| A10 | Mishandling of Exceptional Conditions | **NEW** |

---

### A01:2025 – Broken Access Control

**Description:** Access control enforces policies that prevent users from acting outside their intended permissions. Failures lead to unauthorized data disclosure, modification, or destruction.

**Common Vulnerabilities:**
- Bypassing access control by modifying URLs, application state, or HTML pages
- Allowing primary key changes to access others' records (IDOR)
- Privilege escalation (acting as admin while logged in as user)
- Missing access control for POST, PUT, DELETE APIs
- CORS misconfiguration allowing unauthorized API access

**Prevention:**
```python
# BAD: No authorization check
@app.route('/api/user/<user_id>')
def get_user(user_id):
    return db.get_user(user_id)

# GOOD: Authorization enforced
@app.route('/api/user/<user_id>')
@login_required
def get_user(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)
    return db.get_user(user_id)
```

**Mitigation Strategies:**
1. Deny access by default (allowlist approach)
2. Implement access control once, reuse throughout application
3. Enforce record ownership instead of accepting user-supplied IDs
4. Disable directory listing and remove sensitive files from web roots
5. Log access control failures and alert on repeated attempts
6. Rate limit API access to minimize automated attack damage

---

### A02:2025 – Security Misconfiguration

**Description:** Applications are vulnerable when security hardening is missing, cloud permissions are improperly configured, unnecessary features are enabled, or default accounts remain active.

**Common Vulnerabilities:**
- Missing security hardening across the application stack
- Unnecessary features enabled (ports, services, pages, accounts)
- Default credentials unchanged
- Error handling revealing stack traces
- Outdated or vulnerable software components
- Insecure cloud storage permissions (S3 buckets public)

**Prevention:**
```yaml
# BAD: Debug mode in production
DEBUG=True
SECRET_KEY="development-key"

# GOOD: Production hardened
DEBUG=False
SECRET_KEY="${RANDOM_SECRET_FROM_VAULT}"
ALLOWED_HOSTS=["app.example.com"]
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**Mitigation Strategies:**
1. Automated, repeatable hardening process across environments
2. Minimal platform without unnecessary features or frameworks
3. Regularly review and update configurations (cloud permissions, patches)
4. Segmented application architecture with secure separation
5. Send security directives (CSP, HSTS, X-Frame-Options)
6. Automated verification of configurations in all environments

---

### A03:2025 – Software Supply Chain Failures

**Description:** NEW category highlighting risks from third-party dependencies, compromised build pipelines, and insecure package management. Expanded from 2021's component vulnerabilities focus.

**Common Vulnerabilities:**
- Using components with known vulnerabilities
- Dependency confusion attacks
- Typosquatting in package registries
- Compromised CI/CD pipelines
- Unsigned or unverified packages
- Lack of software bill of materials (SBOM)

**Prevention:**
```bash
# BAD: Installing without verification
npm install some-package

# GOOD: Lock versions, verify integrity, audit
npm install some-package@1.2.3 --save-exact
npm audit
npm audit signatures
```

```json
// package-lock.json with integrity hashes
{
  "dependencies": {
    "lodash": {
      "version": "4.17.21",
      "integrity": "sha512-v2kDEe57lecT..."
    }
  }
}
```

**Mitigation Strategies:**
1. Maintain inventory of all components (SBOM)
2. Remove unused dependencies and features
3. Continuously monitor for vulnerabilities (Dependabot, Snyk)
4. Obtain components from official sources over secure links
5. Sign packages and verify signatures
6. Ensure CI/CD pipelines have proper access controls and audit logs
7. Use lock files and verify integrity hashes

---

### A04:2025 – Cryptographic Failures

**Description:** Failures related to cryptography that lead to exposure of sensitive data. Includes weak algorithms, improper key management, and missing encryption.

**Common Vulnerabilities:**
- Transmitting data in clear text (HTTP, SMTP, FTP)
- Using deprecated algorithms (MD5, SHA1, DES)
- Weak or default cryptographic keys
- Missing certificate validation
- Using encryption without authenticated modes
- Insufficient entropy for random number generation

**Prevention:**
```python
# BAD: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# GOOD: Modern password hashing
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)

# BAD: ECB mode
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_ECB)

# GOOD: Authenticated encryption
from cryptography.fernet import Fernet
cipher = Fernet(key)
```

**Mitigation Strategies:**
1. Classify data by sensitivity; apply controls accordingly
2. Don't store sensitive data unnecessarily
3. Encrypt all data in transit (TLS 1.2+) and at rest
4. Use strong, current algorithms (AES-256-GCM, Argon2, bcrypt)
5. Encrypt with authenticated modes (GCM, CCM)
6. Generate keys randomly; store securely (HSM, vault)
7. Disable caching for sensitive responses

---

### A05:2025 – Injection

**Description:** Injection occurs when untrusted data is sent to an interpreter as part of a command or query. Includes SQL, NoSQL, OS, LDAP, and expression language injection.

**Common Vulnerabilities:**
- User input not validated, filtered, or sanitized
- Dynamic queries without parameterization
- Hostile data used in ORM search parameters
- Direct concatenation of user input in commands

**Prevention:**
```python
# BAD: SQL Injection vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# BAD: Command injection
os.system(f"convert {filename} output.png")

# GOOD: Use safe APIs, avoid shell
subprocess.run(["convert", filename, "output.png"], shell=False)
```

```javascript
// BAD: NoSQL injection
db.users.find({ username: req.body.username })

// GOOD: Validate type
if (typeof req.body.username !== 'string') throw new Error();
db.users.find({ username: req.body.username })
```

**Mitigation Strategies:**
1. Use safe APIs with parameterized interfaces
2. Validate all input using allowlists
3. Escape special characters for specific interpreters
4. Use LIMIT and pagination to prevent mass disclosure
5. Implement positive server-side input validation

---

### A06:2025 – Insecure Design

**Description:** Flaws in design and architecture that cannot be fixed by perfect implementation. Represents missing or ineffective security controls at the design phase.

**Common Vulnerabilities:**
- Missing rate limiting on sensitive operations
- No account lockout for failed authentication
- Lack of tenant isolation in multi-tenant systems
- Missing fraud detection controls
- Insufficient trust boundaries

**Prevention:**
```python
# BAD: No rate limiting on password reset
@app.route('/password-reset', methods=['POST'])
def password_reset():
    send_reset_email(request.form['email'])
    return "Email sent"

# GOOD: Rate limiting and verification
from flask_limiter import Limiter
limiter = Limiter(app)

@app.route('/password-reset', methods=['POST'])
@limiter.limit("3 per hour")
def password_reset():
    email = request.form['email']
    if not is_valid_email_format(email):
        abort(400)
    # Use consistent timing to prevent enumeration
    send_reset_email_async(email)
    return "If account exists, email was sent"
```

**Mitigation Strategies:**
1. Establish secure development lifecycle with security experts
2. Create and use secure design patterns library
3. Threat modeling for authentication, access control, business logic
4. Integrate security language in user stories
5. Implement tenant isolation and resource limits
6. Limit resource consumption per user/service

---

### A07:2025 – Identification and Authentication Failures

**Description:** Confirmation of user identity, authentication, and session management is critical. Weaknesses allow attackers to compromise passwords, keys, or session tokens.

**Common Vulnerabilities:**
- Permitting weak or well-known passwords
- Using weak credential recovery (knowledge-based answers)
- Plain text or weakly hashed passwords
- Missing or ineffective MFA
- Exposing session IDs in URLs
- Not properly invalidating sessions on logout

**Prevention:**
```python
# Password strength requirements
import re
def validate_password(password):
    if len(password) < 12:
        return False
    if password in COMMON_PASSWORDS:  # Check against breach lists
        return False
    return True

# Session management
@app.route('/logout')
@login_required
def logout():
    session.clear()  # Clear server-side session
    response = redirect('/')
    response.delete_cookie('session')
    return response
```

**Mitigation Strategies:**
1. Implement MFA to prevent automated attacks
2. Avoid shipping with default credentials
3. Check passwords against known breached password lists
4. Align password policies with NIST 800-63b
5. Harden against enumeration attacks (consistent responses)
6. Limit failed login attempts with exponential backoff
7. Use server-side, secure session manager; regenerate IDs after login

---

### A08:2025 – Software and Data Integrity Failures

**Description:** Code and infrastructure that doesn't protect against integrity violations. Includes insecure deserialization, trusting unsigned updates, and CI/CD without verification.

**Common Vulnerabilities:**
- Applications relying on untrusted CDNs or repositories
- Auto-update without integrity verification
- Insecure deserialization of untrusted data
- CI/CD pipelines without proper access controls
- Unsigned or unverified code deployments

**Prevention:**
```html
<!-- BAD: CDN without integrity -->
<script src="https://cdn.example.com/lib.js"></script>

<!-- GOOD: Subresource Integrity -->
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>
```

```python
# BAD: Unsafe deserialization
import pickle
data = pickle.loads(user_input)

# GOOD: Safe serialization with validation
import json
data = json.loads(user_input)
validate_schema(data)
```

**Mitigation Strategies:**
1. Use digital signatures to verify software/data from expected source
2. Ensure dependencies are from trusted repositories
3. Use software supply chain security tools (OWASP Dependency-Check)
4. Review code and configuration changes
5. Ensure CI/CD has proper segregation, configuration, and access control
6. Don't send unsigned/unencrypted serialized data to untrusted clients

---

### A09:2025 – Security Logging and Monitoring Failures

**Description:** Without logging and monitoring, breaches cannot be detected. Insufficient logging, detection, monitoring, and response allows attackers to persist.

**Common Vulnerabilities:**
- Auditable events not logged (logins, failed logins, transactions)
- Warnings and errors generate unclear log messages
- Logs only stored locally
- Alerting thresholds not set or ineffective
- Penetration tests don't trigger alerts
- Application can't detect active attacks in real-time

**Prevention:**
```python
import logging
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('security')

@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        logger.info(f"LOGIN_SUCCESS user={user.id} ip={request.remote_addr}")
        return redirect('/dashboard')
    else:
        logger.warning(f"LOGIN_FAILURE username={request.form['username']} ip={request.remote_addr}")
        return "Invalid credentials", 401
```

**Mitigation Strategies:**
1. Log all login, access control, and server-side validation failures
2. Generate logs in format consumable by log management solutions
3. Encode log data correctly to prevent injection attacks
4. Ensure high-value transactions have audit trail with integrity controls
5. Establish effective monitoring and alerting
6. Create incident response and recovery plan (NIST 800-61r2)

---

### A10:2025 – Mishandling of Exceptional Conditions

**Description:** NEW category addressing failures in handling errors, edge cases, and unexpected states. Poor exception handling can leak information or cause security failures.

**Common Vulnerabilities:**
- Exposing stack traces to users
- Inconsistent error handling between components
- Fail-open behavior (allowing access on error)
- Resource exhaustion without graceful degradation
- Race conditions in error paths
- Incomplete transaction rollbacks

**Prevention:**
```python
# BAD: Leaking information
@app.errorhandler(Exception)
def handle_error(e):
    return str(e), 500  # Exposes internal details

# GOOD: Secure error handling
@app.errorhandler(Exception)
def handle_error(e):
    error_id = uuid.uuid4()
    logger.exception(f"Error {error_id}: {e}")
    return {"error": "An error occurred", "id": str(error_id)}, 500
```

```python
# BAD: Fail-open
def check_permission(user, resource):
    try:
        return authorization_service.check(user, resource)
    except Exception:
        return True  # Fail-open!

# GOOD: Fail-closed
def check_permission(user, resource):
    try:
        return authorization_service.check(user, resource)
    except Exception as e:
        logger.error(f"Auth check failed: {e}")
        return False  # Fail-closed
```

**Mitigation Strategies:**
1. Design for failure: expect and handle all error conditions
2. Implement fail-closed (deny by default) on errors
3. Use structured exception handling with appropriate granularity
4. Never expose internal errors to end users
5. Log all exceptions with context for debugging
6. Test error handling paths as thoroughly as happy paths
7. Implement circuit breakers for external dependencies

---

## OWASP ASVS 5.0.0

The Application Security Verification Standard (ASVS) 5.0.0 was released May 30, 2025. It provides approximately 350 security requirements across 17 categories (the exact total varies by verification level) with three verification levels.

### Verification Levels

| Level | Use Case | Description |
|-------|----------|-------------|
| L1 | All applications | Basic security controls for low-risk applications |
| L2 | Most applications | Standard security for applications handling sensitive data |
| L3 | High-value targets | Advanced security for critical infrastructure, healthcare, finance |

### ASVS Categories

1. **V1: Architecture, Design & Threat Modeling**
2. **V2: Authentication**
3. **V3: Session Management**
4. **V4: Access Control**
5. **V5: Input Validation**
6. **V6: Stored Cryptography**
7. **V7: Error Handling & Logging**
8. **V8: Data Protection**
9. **V9: Communication**
10. **V10: Malicious Code**
11. **V11: Business Logic**
12. **V12: Files and Resources**
13. **V13: API and Web Services**
14. **V14: Configuration**
15. **V15: OAuth and OIDC** (New in 5.0)
16. **V16: Self-Contained Tokens** (New in 5.0)
17. **V17: WebSockets** (New in 5.0)

### Key Requirements Examples

**Authentication (V2):**
- V2.1.1: User passwords SHALL be at least 12 characters
- V2.1.6: Passwords SHALL be checked against breached password lists
- V2.2.1: Anti-automation controls SHALL prevent credential stuffing
- V2.5.2: Password recovery SHALL NOT reveal if account exists

**Session Management (V3):**
- V3.2.1: Session tokens SHALL have at least 128 bits of entropy
- V3.3.1: Sessions SHALL be invalidated on logout
- V3.4.1: Cookie-based tokens SHALL have Secure attribute set

**Access Control (V4):**
- V4.1.1: Access control SHALL be enforced server-side
- V4.2.1: Sensitive data SHALL only be accessible to authorized users
- V4.3.1: Directory browsing SHALL be disabled

**Cryptography (V6):**
- V6.2.1: All cryptographic modules SHALL fail securely
- V6.4.1: Keys SHALL be generated using approved random generators
- V6.4.2: Keys SHALL be stored securely (HSM, vault)

---

## OWASP Top 10 for Agentic Applications 2026

Released December 2025, this framework addresses security risks specific to AI agents, multi-agent systems, and autonomous applications.

### Summary Table

| ID | Risk | Description |
|----|------|-------------|
| ASI01 | Agent Goal Hijacking | Prompt injection alters agent's core objectives |
| ASI02 | Tool Misuse | Legitimate tools used in unintended/unsafe ways |
| ASI03 | Identity & Privilege Abuse | Credential escalation across agent interactions |
| ASI04 | Agentic Supply Chain Vulnerabilities | Compromised plugins, MCP servers, or dependencies |
| ASI05 | Unexpected Code Execution | Unsafe code generation or execution by agents |
| ASI06 | Memory & Context Poisoning | Manipulation of RAG systems or agent memory |
| ASI07 | Insecure Inter-Agent Communication | Spoofing or tampering between agent systems |
| ASI08 | Cascading Failures | Error propagation across interconnected systems |
| ASI09 | Human-Agent Trust Exploitation | Social engineering through AI-generated content |
| ASI10 | Rogue Agents | Compromised or malicious agents within systems |

---

### ASI01: Agent Goal Hijacking

**Description:** Attackers use prompt injection to alter an agent's intended goals, making it serve malicious purposes while appearing to function normally.

**Attack Vectors:**
- Direct prompt injection in user inputs
- Indirect injection via compromised data sources
- Hidden instructions in documents, websites, or emails
- Multi-turn conversation manipulation

**Prevention:**
- Implement strict input sanitization and filtering
- Use structured output formats to limit agent responses
- Establish clear goal boundaries with system prompts
- Monitor for goal deviation through behavioral analysis
- Implement human-in-the-loop for sensitive operations

---

### ASI02: Tool Misuse

**Description:** Agents with access to tools (APIs, databases, file systems) may use them in unintended ways due to malicious instructions or flawed reasoning.

**Attack Vectors:**
- Tricking agents into executing harmful commands
- Using tools with elevated privileges
- Chaining tool calls to achieve unauthorized outcomes
- Exploiting ambiguous tool descriptions

**Prevention:**
- Apply principle of least privilege to all tool access
- Implement fine-grained permissions per tool
- Validate all tool inputs and outputs
- Create tool usage policies and enforce them
- Log all tool invocations for audit

---

### ASI03: Identity & Privilege Abuse

**Description:** Agents may inherit, accumulate, or escalate privileges beyond what's appropriate, especially in multi-agent or long-running contexts.

**Attack Vectors:**
- Credential theft through prompt injection
- Session token exposure
- Privilege escalation through tool chaining
- Identity confusion in multi-agent systems

**Prevention:**
- Use short-lived, scoped credentials
- Implement identity verification between agents
- Don't pass raw credentials through agent context
- Audit privilege usage patterns
- Implement credential rotation

---

### ASI04: Agentic Supply Chain Vulnerabilities

**Description:** Compromised plugins, MCP servers, or third-party integrations introduce vulnerabilities into agent systems.

**Attack Vectors:**
- Malicious MCP server implementations
- Typosquatting in plugin registries
- Compromised update mechanisms
- Backdoored agent frameworks

**Prevention:**
- Verify plugin/server authenticity and signatures
- Maintain inventory of all integrations
- Sandbox third-party components
- Monitor for anomalous behavior from integrations
- Use allowlists for permitted plugins

---

### ASI05: Unexpected Code Execution

**Description:** Agents that generate or execute code may be tricked into running malicious code.

**Attack Vectors:**
- Code injection through prompts
- Malicious code in retrieved context
- Unsafe code execution environments
- Bypassing code review through obfuscation

**Prevention:**
- Execute generated code in sandboxed environments
- Implement static analysis before execution
- Limit code execution capabilities
- Require human approval for sensitive operations
- Use allowlists for permitted operations

---

### ASI06: Memory & Context Poisoning

**Description:** Attackers corrupt agent memory, RAG databases, or context to influence future behavior.

**Attack Vectors:**
- Injecting malicious content into vector databases
- Manipulating conversation history
- Poisoning knowledge bases
- Exploiting context window limitations

**Prevention:**
- Validate and sanitize all stored content
- Implement content integrity verification
- Segment memory by trust level
- Regular audits of stored knowledge
- Implement memory decay/expiration

---

### ASI07: Insecure Inter-Agent Communication

**Description:** Communication between agents may be vulnerable to interception, spoofing, or tampering.

**Attack Vectors:**
- Man-in-the-middle attacks on agent communication
- Agent identity spoofing
- Message tampering
- Replay attacks

**Prevention:**
- Authenticate all agent communications
- Encrypt inter-agent messages
- Implement message integrity verification
- Use secure channels for agent orchestration
- Validate agent identities cryptographically

---

### ASI08: Cascading Failures

**Description:** Errors in one agent or component propagate through interconnected systems, causing widespread failures.

**Attack Vectors:**
- Triggering errors that cascade through agent chains
- Resource exhaustion in one agent affecting others
- Error handling that exposes sensitive information
- Retry storms from failed operations

**Prevention:**
- Implement circuit breakers between agents
- Design for graceful degradation
- Isolate agent failures
- Rate limit inter-agent calls
- Monitor for cascade patterns

---

### ASI09: Human-Agent Trust Exploitation

**Description:** Attackers leverage the trust humans place in AI agents to conduct social engineering attacks.

**Attack Vectors:**
- AI-generated phishing content
- Impersonation through agent responses
- Trust exploitation via helpful-seeming agents
- Deceptive multi-turn conversations

**Prevention:**
- Clear labeling of AI-generated content
- User education on AI limitations
- Verification steps for sensitive actions
- Maintain human oversight for critical decisions
- Implement suspicious behavior detection

---

### ASI10: Rogue Agents

**Description:** Agents that have been compromised or are acting maliciously, either through external attack or flawed design.

**Attack Vectors:**
- Agent compromise through injection attacks
- Malicious agent deployment
- Agent behavior modification
- Insider threats via agent systems

**Prevention:**
- Monitor agent behavior for anomalies
- Implement agent authentication and authorization
- Regular security audits of agent systems
- Kill switches for agent operations
- Behavioral baselines and deviation detection

---

## Key Security Principles

### Defense in Depth
Layer multiple security controls so that if one fails, others provide protection.

### Least Privilege
Grant minimum permissions necessary for functionality. Regularly review and revoke unnecessary access.

### Fail Secure
When errors occur, default to a secure state. Deny access rather than allow it when uncertain.

### Zero Trust
Never trust, always verify. Authenticate and authorize every request regardless of source.

### Secure by Default
Ship products with secure defaults. Require explicit action to reduce security.

### Input Validation
Validate all input on the server side. Use allowlists over denylists.

### Output Encoding
Encode output based on context (HTML, JavaScript, SQL, etc.) to prevent injection.

### Keep Security Simple
Complex security is often bypassed. Prefer simple, understandable controls.

---

## Sources and References

### Official OWASP Resources
- [OWASP Top 10:2025](https://owasp.org/Top10/)
- [OWASP ASVS 5.0](https://github.com/OWASP/ASVS)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)

### Industry Analysis
- [GitLab: OWASP Top 10 2025 - What's Changed and Why It Matters](https://about.gitlab.com/blog/)
- [Aikido: OWASP Top 10 for Agentic Applications Guide](https://www.aikido.dev/blog/)
- [Security Boulevard: OWASP 2025 Analysis](https://securityboulevard.com/)

### Standards and Guidelines
- [NIST SP 800-63b: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)
- [NIST SP 800-61r2: Incident Handling Guide](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [CWE/SANS Top 25 Software Errors](https://cwe.mitre.org/top25/)

---

*Last updated: January 2026*
