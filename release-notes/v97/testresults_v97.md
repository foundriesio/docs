- [Test Results for LmP v97 Release](#test-results-for-lmp-v97-release)
  - [Unit Tests](#unit-tests)
  - [Component-Specific Tests](#component-specific-tests)
    - [aktualizr-lite Test Results](#aktualizr-lite-test-results)
  - [Integration Tests](#integration-tests)
    - [Compatibility Tests](#compatibility-tests)
  - [System Testing](#system-testing)

# Test Results for LmP v97 Release
This document provides a summary of the test results for the LmP v97 release.

## Unit Tests

_No unit tests were conducted for this release._

## Component-Specific Tests

### aktualizr-lite Test Results
Aktualizr-lite underwent comprehensive testing as part of the LmP v97 release process as described in the [Aktualizr-lite Testing Plan](aklite_testresult_v97.md).


## Integration Tests

Manual tests were conducted to verify the integration of various components in the LmP v97 release. The results of these tests were satisfactory, and no major issues were identified

| Test                  | qemuarm64-secureboot | qemuarm64-secureboot | intel-corei7-64 | intel-corei7-64 |
|-----------------------|----------------------|----------------------|-----------------|-----------------|
| Builder               | factory              | CI pre-built         | factory         | CI pre-built    |
| Build                 | PASS                 | PASS                 | PASS            | PASS            |
| Boot                  | PASS                 | PASS                 | PASS            | PASS            |
| XTest                 | PASS                 | PASS                 | PASS            | N/A             |
| Registration          | PASS                 | PASS                 | PASS            | PASS            |
| Update (prev release) | PASS                 | PASS                 | PASS            | PASS            |
| OTA Rollback          | PASS                 | N/A                  | PASS            | N/A             |
| Compose-app           | PASS                 | N/A                  | PASS            | N/A             |


### Compatibility Tests

Compatibility tests are being developed and will be executed in the next phase of testing.

## System Testing

System testing is performed automatically and the results can be viewed at [QA Reports](https://qa-reports.foundries.io/lmp/lmp-ci-stable/build/542654a850c2984675515a8816110c2911d2df64/tests/). The scope of the automated system testing is being expanded and more tests will be added for the next release.