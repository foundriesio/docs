# fiotest

The Factory includes a simple, but effective way to manage automated
testing. It's managed by a feature called the Device Gateway Testing
API. This API allows registered devices to report the results of tests.
The Factory makes the raw results of these tests available through
api.foundries.io. Fioctl also includes the ability to summarize test
results.

## The Model

The API is built around a generic model for recording test results:

    Test:
      Name: string - "ltp"
      Target: string - "raspberrypi3-64-lmp-8"
      Device: string - device uuid
      Status: string - PASS/FAIL/RUNNING
      CreatedOn: timestamp - when the test was started
      CompletedOn: timestamp - when the test was finished
      Details: raw text - could be a summary or test failure details

      # An optional listing of Test Results for when granular details are needed.
      Results: [
        {
          Name: string - "statx"
          Status: PASS/FAIL/SKIPPED
          Metrics: dict[str, float] optional int - if there’s a meaningful measurement for the test
          Details: raw text - could be the text to the failure
        }...
      ]

## The API

### POST /tests/

> Create a new test (`status=RUNNING`):
>
>     # Content-type: application/json
>     {
>       "name": "test-name",
>       "target": "raspberrypi3-64-lmp-8"
>     }
>     # The CreatedOn value will be auto-populated by the server.
>
> **RETURNS**: A location to the new Test object:
>
>     HTTP 201
>     LOCATION: /tests/12345

### PUT /tests/&lt;test id&gt;

> Complete a test with data:
>
>     # Content-type: application/json
>     {
>       "status": PASS/FAIL
>     }
>
>     or
>
>     {
>       "results": [
>         {"name": "test-1", "status": "PASS"},
>         {"name": "test-2", "status": "SKIPPED"}
>       ]
>     }
>     # The CompletedOn value will be auto-populated by the server. If results
>     # are provided PASS/FAIL will be based on their values.
>
> **RETURNS**: `HTTP 200`

## Creating Custom Tests

The [fiotest](https://github.com/foundriesio/fiotest) project provides a
good starting point and example of how to do device testing.
