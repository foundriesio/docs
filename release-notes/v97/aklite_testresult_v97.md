# Test Results for Aktualizr-lite in LmP v97 Release

The following tables summarize the results of the unit and end-to-end tests conducted for aktualizr-lite in https://github.com/user-attachments/files/27636568/logs_58655807117.zip.
## Unit Tests

| Test # | Test Name                    | Result |
|--------|------------------------------|--------|
| 104    | test_aktualizr-lite          | Passed |
| 105    | test_yaml2json               | Passed |
| 106    | test_compose-apps            | Passed |
| 107    | test_lite-helpers            | Passed |
| 108    | test_ostree                  | Passed |
| 109    | test_liteclient              | Passed |
| 110    | test_liteclientHSM           | Passed |
| 111    | test_composeappengine        | Passed |
| 112    | test_restorableappengine     | Passed |
| 113    | test_aklite                  | Passed |
| 114    | test_aklite_rollback         | Passed |
| 115    | test_aklite_rollback_ext     | Passed |
| 116    | test_apiclient               | Passed |
| 117    | test_exec                    | Passed |
| 118    | test_docker                  | Passed |
| 119    | test_aklite_offline          | Passed |
| 120    | test_boot_flag_mgmt          | Passed |
| 121    | test_cli                     | Passed |
| 122    | test_nospace                 | Passed |
| 123    | test_daemon                  | Passed |

## End-to-End Tests

| Test Name                                     | Result |
|-----------------------------------------------|--------|
| test_incremental_updates[False-True-True]     | Passed |
| test_incremental_updates[False-True-False]    | Passed |
| test_incremental_updates[False-False-True]    | Passed |
| test_incremental_updates[False-False-False]   | Passed |
| test_update_to_latest[False-True]             | Passed |
| test_update_to_latest[False-False]            | Passed |
