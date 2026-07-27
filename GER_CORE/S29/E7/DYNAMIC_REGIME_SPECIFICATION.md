# DynamicRegime Specification

Version: 1.0

Status: Experimental (S29/E7)

---

# 1. Purpose

This document defines the canonical representation of the `DynamicRegime`
object used by the GER framework.

Its purpose is to establish:

- the identity of the object;
- the mandatory components;
- the derived components;
- the metadata components;
- the structural invariants.

This specification applies exclusively to the S29 experimental series.

---

# 2. Canonical Structure

```
DynamicRegime
│
├── Core
│   ├── Configuration
│   └── Signature
│
├── Derived
│   └── Classification
│
└── Metadata
    └── Audit
```

---

# 3. Core

The Core defines the identity of the object.

Removing any Core component changes the object itself.

## 3.1 Configuration

The Configuration stores the physical parameters used to generate the regime.

Examples include:

- β
- σ
- potential
- timestep
- integration step

Configuration is mandatory.

---

## 3.2 Signature

The Signature stores the intrinsic geometric representation produced by GER.

Typical observables include:

- Diameter
- Convergence
- Recurrence
- Drift

Signature is mandatory.

The Signature represents the geometric identity of the DynamicRegime.

---

# 4. Derived Components

Derived components are computed from the Core.

They describe the object but do not define it.

## Classification

Classification represents the interpretation of the regime according to the
current classification rules.

Examples:

- Persistent
- Oscillatory
- Transitional
- Unstable

Classification may change if the classification methodology evolves.

Therefore it is not part of the canonical identity.

---

# 5. Metadata

Metadata records information about the execution process.

Metadata never defines the object.

## Audit

Audit may contain:

- provenance
- statistics
- persistence history
- diagnostics
- validation information

Removing Audit does not modify the DynamicRegime.

---

# 6. Structural Invariants

A valid DynamicRegime satisfies:

- Configuration exists.
- Signature exists.
- Classification is optional.
- Audit is optional.
- Classification shall be derivable from the Core.
- Metadata shall never modify the identity of the object.

---

# 7. Canonical Identity

The canonical identity of a DynamicRegime is defined exclusively by:

```
(Configuration, Signature)
```

Neither Classification nor Audit belong to the canonical identity.

---

# 8. Equality

Two DynamicRegime objects are considered structurally equivalent if their
canonical identities are equivalent.

Metadata shall not participate in equality.

Derived properties shall not participate in equality.

---

# 9. Extension Rules

Future fields incorporated into DynamicRegime shall be classified as exactly
one of the following categories:

- CORE
- DERIVED
- METADATA

before being integrated into the object.

---

# 10. Scope

This specification is experimental.

Promotion to the GER Core shall occur only after successful reuse by multiple
independent experimental series.
