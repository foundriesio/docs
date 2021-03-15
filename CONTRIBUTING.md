# Contributing

When contributing, consider the following properties and whether the submitted
documentation has them:

- Expanded acronyms

  If an acronym is used, it should be expanded, at least during its first
  occurrence on a page. 
  
  ###### Example
  
  ```diff
  < we chose to integrate the NXP middleware with our ROT by bringing it under the
  < umbrella of our Trusted Execution Environment: OP-TEE.
  ---
  > we chose to integrate the NXP middleware with our ROT (root of trust) by bringing
  > it under the umbrella of our Trusted Execution Environment: OP-TEE.
  ```

- Export variables instead of using `<placeholders>` 

  If telling the user to run a command which requires modification by the user,
  tell them to export variables instead of using a `<placeholder>`.

  ###### Example

  ```diff
  < git config --global http.https://source.foundries.io.extraheader "Authorization: basic $(echo -n <GIT_TOKEN> | openssl base64)"
  ---
  > set the ``GIT_TOKEN`` variable. Replace ``<token>`` with your application/oauth token.
  >
  > ``export GIT_TOKEN=<token>``
  >
  > git config --global http.https://source.foundries.io.extraheader "Authorization: basic $(echo -n $GIT_TOKEN | openssl base64)"
  ```
