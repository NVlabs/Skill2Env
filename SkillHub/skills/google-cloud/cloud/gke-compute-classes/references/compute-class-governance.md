# Restricting ComputeClass Access (Governance)

Two **independent** layers — each protects something the other can't. Use both
for full governance.

Layer           | Protects                                 | Mechanism                   | Asset
--------------- | ---------------------------------------- | --------------------------- | -----
**CRUD**        | who can create/modify the CC **object**  | RBAC `ClusterRole`          | `computeclass-rbac-editor.yaml`
**Consumption** | who can **request** a CC from a workload | `ValidatingAdmissionPolicy` | `restrict-computeclass-usage-vap.yaml`

**Key point:** RBAC cannot restrict consumption. Referencing a CC from a Pod
isn't a CRUD verb on the CC object — it's a field in the Pod/Deployment spec.
RBAC governs the object; admission validation governs the spec. Recommending
RBAC alone for "stop team X using this CC" is wrong.

**No native consumption field — don't hallucinate one.** The ComputeClass spec
has **no** `namespacePolicy`/`allowedNamespaces`/`allowedNamespacesPolicy` field
(or any field) that restricts which namespaces may *consume* the class.
Consumption control is **admission-only** (the VAP below). If asked "can't I
just allow-list namespaces on the ComputeClass itself?", say no such field
exists and redirect to the VAP.

## CRUD safeguard — RBAC

-   ComputeClass is a **cluster-scoped CRD** → use `ClusterRole` +
    `ClusterRoleBinding`, **not** a namespaced `Role`.
-   `apiGroups: ["cloud.google.com"]`, `resources: ["computeclasses"]`.
-   Tutorial verbs: `create`, `update`. **For a full lockdown also grant `patch`
    and `delete`** — otherwise a non-creator can still patch/delete an existing
    CC.
-   Bind to a **Google Group** (`kind: Group`, `name: ...@<GROUP_DOMAIN>`) for
    centralized membership over per-user bindings.
-   Verify: `kubectl auth can-i create computeclasses.cloud.google.com
    --as=<USER>` (run for a member and a non-member).

## Consumption safeguard — ValidatingAdmissionPolicy (VAP)

Native K8s admission (in-process CEL, **no webhook**). Policy = the CEL rules;
Binding = scope + actions.

**Three access paths — the CEL must close ALL of them, or it leaks:**

1.  `nodeSelector` → `cloud.google.com/compute-class: <NAME>`.
2.  `nodeAffinity` → `matchExpressions` key `cloud.google.com/compute-class`,
    `In [<NAME>]`.
3.  `tolerations` → tolerating the CC's `NoSchedule` taint, **including the
    wildcard** (`operator: Exists` with **no key**) which tolerates *every*
    taint and thus the restricted CC. A nodeSelector-only policy is the classic
    bypass.

**Match every workload kind, not just Pods+Deployments.** The tutorial's
`matchConstraints` lists only `pods` (core/v1) and `deployments` (apps/v1) —
leaving `statefulsets`/`daemonsets`/`replicasets` (apps), `jobs`/`cronjobs`
(batch) as bypasses. Controllers carry the spec at `spec.template.spec`
(CronJob: `spec.jobTemplate.spec.template.spec`); bare Pods at `spec`.

**Binding:**

-   `validationActions: ["Deny","Audit"]` — Deny rejects; Audit logs to the K8s
    audit log. Run **Audit-only first** to find existing violators, then add
    Deny.
-   `failurePolicy: Fail` — fail closed.
-   Scope with `namespaceSelector.matchLabels` (e.g.
    `kubernetes.io/metadata.name: <NS>`).
-   Apply: `kubectl apply -f restrict-computeclass-usage-vap.yaml`.

Denial surfaces as: `admission webhook ... denied the request: This namespace
cannot request ComputeClass <NAME> ...`.

Source: GKE docs — *restrict-computeclass-usage-admission* tutorial.
